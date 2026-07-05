"""
topic_scorer.py
ZX Cloud Security — Guide Topic Research & Scoring Agent

Consumes raw_feed.json from feed_scraper.py, pulls additional signals from
Reddit, Hacker News, and NVD CVE, clusters items into named topics, scores
each topic across four dimensions, and outputs a ranked topic queue for
guide_generator.py.

Scoring dimensions (out of 100):
  score_trending     0–30  velocity of new mentions: last 12h vs 12–48h ratio
  score_keyword_api  0–30  DataForSEO search volume + competition (UK, English)
  score_volume       0–20  cross-source signal count + engagement scores
  score_coverage_gap 0–20  how uncovered this topic is on the existing site

Secrets required (GitHub Actions secrets / env vars):
  DATAFORSEO_LOGIN     DataForSEO account email
  DATAFORSEO_PASSWORD  DataForSEO account password

Output: topic_queue.json
"""

import json
import hashlib
import logging
import os
import re
import subprocess
import time
from collections import defaultdict
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

HEADERS = {
    "User-Agent": "ZXCloudSecurity/1.0 (+https://zxcloudsecurity.co.uk)",
    "Accept": "application/json",
}

HN_ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"
HN_QUERY_TERMS = [
    "AWS security", "cloud security", "IAM", "GuardDuty", "S3 breach",
    "CloudTrail", "SCP", "Landing Zone", "zero trust AWS", "CVE cloud",
]
HN_MAX_AGE_HOURS = 48

NVD_CVE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_MAX_RESULTS = 50
NVD_MAX_AGE_HOURS = 48
NVD_API_KEY = os.environ.get("NVD_API_KEY", "")

# DataForSEO Keywords Data API
DATAFORSEO_API_URL = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
DATAFORSEO_LOCATION = "United Kingdom"
DATAFORSEO_LANGUAGE = "English"

# Trending velocity window: signals within this many hours are "recent"
TRENDING_WINDOW_HOURS = 12

# Minimum score (out of 100) for a topic to be included in the output queue
MIN_SCORE_THRESHOLD = 35

# Number of top topics to select
TOP_N = 3

# Content directory to scan for existing guides (coverage gap check)
GUIDES_DIR = Path("content/guides")

# Topics scoring >= this get pillar treatment
PILLAR_SCORE_THRESHOLD = 65

# ---------------------------------------------------------------------------
# Tier 1 seed keywords (from requirements §3.2 + common AWS security terms)
# ---------------------------------------------------------------------------

TIER1_KEYWORDS = [
    # Explicit seed list from requirements
    "cloud security architect", "day rate", "career pathway",
    "aws scp", "service control policy",
    "guardduty", "guard duty",
    "landing zone", "control tower",
    "iam identity centre", "iam identity center", "aws sso",
    "security hub",
    "post-quantum", "post quantum", "pqc",
    "cyberark", "pam", "privileged access",
    "ncsc", "ncsc cloud",
    "kms", "key management",
    # Broader high-value AWS security terms
    "iam", "least privilege",
    "cloudtrail", "cloud trail",
    "vpc", "network firewall",
    "macie",
    "inspector",
    "waf",
    "shield",
    "secrets manager",
    "config rules",
    "s3 bucket policy", "s3 security",
    "eks security", "kubernetes security",
    "lambda security",
    "zero trust",
    "ransomware aws",
    "data exfiltration",
    "compliance", "pci", "hipaa", "iso 27001", "soc 2",
    "cve", "vulnerability",
    "penetration testing aws", "pen test",
    "incident response aws",
    "forensics aws",
    "threat detection",
]

# Seeds that qualify for partial-credit fallback when DataForSEO data is absent
_TIER1_SEEDS = {
    "cloud security architect", "day rate", "aws scp", "service control policy",
    "guardduty", "landing zone", "control tower", "iam identity centre",
    "iam identity center", "security hub", "post-quantum", "cyberark", "pam",
    "ncsc", "kms", "key management",
}

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class RawSignal:
    """A single data point from any source (feed item, Reddit post, HN story, CVE)."""
    id: str
    source: str           # e.g. "feed_scraper", "reddit_aws", "hn", "nvd"
    title: str
    url: str
    published: str        # ISO 8601
    score: int = 0        # Source-native engagement score (upvotes, HN points)
    text: str = ""        # Summary / selftext snippet


@dataclass
class ScoredTopic:
    """A clustered topic with its four-dimension score."""
    label: str                          # Human-readable topic label
    slug: str                           # kebab-case, used as filename hint
    tier: str                           # "pillar" | "supporting"
    total_score: int                    # 0–100
    score_trending: int                 # 0–30  velocity of mentions in last 12h
    score_keyword_api: int              # 0–30  DataForSEO search volume + competition
    score_volume: int                   # 0–20  signal count + source diversity
    score_coverage_gap: int             # 0–20  gap in existing site coverage
    signal_count: int                   # Number of raw signals in cluster
    recent_signal_count: int            # Signals within last TRENDING_WINDOW_HOURS
    keyword_search_volume: int          # Raw DataForSEO search_volume (0 = no data)
    keyword_competition: float          # Raw DataForSEO competition (0.0–1.0)
    source_urls: list = field(default_factory=list)   # Up to 5 representative URLs
    matched_keywords: list = field(default_factory=list)
    newest_signal: str = ""             # ISO 8601 of most recent signal


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_id(source: str, url: str) -> str:
    return hashlib.sha256(f"{source}:{url}".encode()).hexdigest()[:16]


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _parse_iso(ts: str) -> Optional[datetime]:
    try:
        dt = datetime.fromisoformat(ts)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _is_recent(published_iso: str, max_age_hours: int = 48) -> bool:
    dt = _parse_iso(published_iso)
    if dt is None:
        return True
    return _now_utc() - dt < timedelta(hours=max_age_hours)


def _hours_ago(published_iso: str) -> float:
    dt = _parse_iso(published_iso)
    if dt is None:
        return 48.0
    delta = _now_utc() - dt
    return max(0.0, delta.total_seconds() / 3600)


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:80]


def _extract_keywords(text: str) -> list:
    """Return which TIER1_KEYWORDS appear in the given text (lowercase)."""
    text_lower = text.lower()
    return [kw for kw in TIER1_KEYWORDS if kw in text_lower]


# ---------------------------------------------------------------------------
# Source fetchers
# ---------------------------------------------------------------------------

def load_feed_scraper_signals(path: str = "raw_feed.json") -> list:
    """Load existing feed_scraper.py output as RawSignals."""
    signals = []
    p = Path(path)
    if not p.exists():
        log.warning(f"  {path} not found — skipping feed_scraper signals")
        return signals
    try:
        with open(p) as f:
            items = json.load(f)
        for item in items:
            if not _is_recent(item.get("published", ""), max_age_hours=48):
                continue
            signals.append(RawSignal(
                id=_make_id("feed_scraper", item.get("link", item.get("id", ""))),
                source=f"feed_{item.get('source_id', 'unknown')}",
                title=item.get("title", ""),
                url=item.get("link", ""),
                published=item.get("published", _now_utc().isoformat()),
                score=0,
                text=item.get("summary", ""),
            ))
        log.info(f"  → {len(signals)} signals from feed_scraper ({path})")
    except Exception as e:
        log.error(f"  Error loading {path}: {e}")
    return signals


def fetch_hn_signals(max_age_hours: int = HN_MAX_AGE_HOURS) -> list:
    """Fetch relevant HN stories via Algolia search API."""
    signals = []
    cutoff = int((_now_utc() - timedelta(hours=max_age_hours)).timestamp())
    seen_ids: set = set()
    for term in HN_QUERY_TERMS:
        try:
            params = {
                "query": term,
                "tags": "story",
                "numericFilters": f"created_at_i>{cutoff}",
                "hitsPerPage": 10,
            }
            resp = requests.get(HN_ALGOLIA_URL, params=params, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            hits = resp.json().get("hits", [])
            for hit in hits:
                hn_id = str(hit.get("objectID", ""))
                if hn_id in seen_ids:
                    continue
                seen_ids.add(hn_id)
                created = hit.get("created_at", _now_utc().isoformat())
                url = hit.get("url") or f"https://news.ycombinator.com/item?id={hn_id}"
                signals.append(RawSignal(
                    id=_make_id("hn", hn_id),
                    source="hn",
                    title=hit.get("title", ""),
                    url=url,
                    published=created,
                    score=hit.get("points", 0),
                    text=hit.get("story_text", "") or "",
                ))
        except Exception as e:
            log.error(f"  HN search error for '{term}': {e}")
        time.sleep(0.3)
    log.info(f"  → {len(signals)} unique stories from Hacker News")
    return signals


def fetch_nvd_signals(max_age_hours: int = NVD_MAX_AGE_HOURS, max_retries: int = 3) -> list:
    """
    Fetch recent CVEs from NVD 2.0 API, filtered to cloud/AWS-relevant products.
    Uses NVD_API_KEY if set (50 req/30s) else falls back to unauthenticated (5 req/30s).
    Retries on transient errors (503, timeouts) with exponential backoff.
    """
    signals = []
    CLOUD_KEYWORDS = [
        "aws", "amazon", "azure", "google cloud", "kubernetes", "docker",
        "openssl", "log4j", "spring", "nginx", "apache", "linux kernel",
        "terraform", "ansible", "jenkins", "gitlab", "github",
    ]

    headers = dict(HEADERS)
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY
    else:
        log.warning("  NVD_API_KEY not set — using unauthenticated NVD rate limit (5 req/30s)")

    pub_start = (_now_utc() - timedelta(hours=max_age_hours)).strftime("%Y-%m-%dT%H:%M:%S.000")
    pub_end = _now_utc().strftime("%Y-%m-%dT%H:%M:%S.000")
    params = {
        "pubStartDate": pub_start,
        "pubEndDate": pub_end,
        "resultsPerPage": NVD_MAX_RESULTS,
        "startIndex": 0,
    }

    data = None
    for attempt in range(1, max_retries + 1):
        try:
            log.info(f"  Fetching NVD CVE feed (attempt {attempt}/{max_retries}) ...")
            resp = requests.get(NVD_CVE_URL, params=params, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            break
        except requests.RequestException as e:
            log.warning(f"  NVD fetch attempt {attempt} failed: {e}")
            if attempt < max_retries:
                backoff = 2 ** attempt  # 2s, 4s, 8s
                log.info(f"  Retrying in {backoff}s ...")
                time.sleep(backoff)
            else:
                log.error(f"  NVD fetch failed after {max_retries} attempts — skipping NVD signals")
                return signals

    if data is None:
        return signals

    try:
        count = 0
        for vuln in data.get("vulnerabilities", []):
            cve = vuln.get("cve", {})
            cve_id = cve.get("id", "")
            descriptions = cve.get("descriptions", [])
            desc = next((d["value"] for d in descriptions if d.get("lang") == "en"), "")
            published = cve.get("published", _now_utc().isoformat())
            if not any(kw in desc.lower() for kw in CLOUD_KEYWORDS):
                continue
            metrics = cve.get("metrics", {})
            cvss_score = 0.0
            for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
                metric_list = metrics.get(key, [])
                if metric_list:
                    cvss_score = metric_list[0].get("cvssData", {}).get("baseScore", 0.0)
                    break
            signals.append(RawSignal(
                id=_make_id("nvd", cve_id),
                source="nvd",
                title=f"{cve_id}: {desc[:120]}",
                url=f"https://nvd.nist.gov/vuln/detail/{cve_id}",
                published=published,
                score=int(cvss_score * 10),
                text=desc[:1000],
            ))
            count += 1
        log.info(f"  → {count} cloud-relevant CVEs from NVD")
    except Exception as e:
        log.error(f"  Error parsing NVD response: {e}")

    return signals

# New section added 20-06-26

def _competition_to_float(val) -> float:
    """
    DataForSEO's google_ads/search_volume/live endpoint returns competition as
    a string label (LOW/MEDIUM/HIGH), not a numeric score. Map it to a 0.0–1.0
    float for consistency with how score_keyword_api() expects to use it.
    """
    mapping = {"LOW": 0.15, "MEDIUM": 0.5, "HIGH": 0.85}
    return mapping.get((val or "").upper(), 0.0)


# ---------------------------------------------------------------------------
# DataForSEO keyword research
# ---------------------------------------------------------------------------

def fetch_keyword_data(
    phrases: list,
    login: str,
    password: str,
) -> dict:
    """
    Fetch monthly search volume and competition for a batch of keyword phrases
    from the DataForSEO Google Ads Keywords Data API (live endpoint).

    Returns dict: phrase_lower -> {"search_volume": int, "competition": float, "cpc": float}
    All phrases are batched into a single API call to minimise cost.
    Phrases that return no data are absent from the result dict.
    """
    results: dict = {}
    if not phrases:
        return results

    # DataForSEO allows up to 700 keywords per task; our cluster count is well below that
    payload = [{
        "keywords": phrases,
        "location_name": DATAFORSEO_LOCATION,
        "language_name": DATAFORSEO_LANGUAGE,
    }]

    try:
        log.info(f"  Querying DataForSEO for {len(phrases)} keyword(s) ...")
        resp = requests.post(
            DATAFORSEO_API_URL,
            auth=(login, password),
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        tasks = data.get("tasks", [])
        if not tasks:
            log.warning("  DataForSEO returned no tasks")
            return results

        task = tasks[0]
        status_code = task.get("status_code")
        log.info(f"  DataForSEO task status: {status_code} — {task.get('status_message', '')}")
        if status_code != 20000:
            log.warning(f"  DataForSEO task error: {task.get('status_message', 'unknown')}")
            return results

        # NOTE: the google_ads/search_volume/live endpoint returns `result` as a
        # FLAT LIST of per-keyword objects — unlike DataForSEO's Labs/SERP-style
        # endpoints, there is no wrapping {"items": [...]} object here. Each
        # element of `result` IS a keyword result directly.
        items = task.get("result") or []
        log.info(f"  DataForSEO raw item count: {len(items)}")

        for item in items:
            kw = (item.get("keyword") or "").lower().strip()
            if not kw:
                continue
            results[kw] = {
                "search_volume": int(item.get("search_volume") or 0),
                "competition": _competition_to_float(item.get("competition")),
                "cpc": float(item.get("cpc") or 0.0),
            }

        log.info(f"  → DataForSEO returned data for {len(results)}/{len(phrases)} phrase(s)")

    except requests.RequestException as e:
        log.error(f"  DataForSEO request error: {e}")
    except Exception as e:
        log.error(f"  DataForSEO unexpected error: {e}")

    return results


# ---------------------------------------------------------------------------
# Coverage gap: scan content/guides/ for existing guide slugs/titles
# ---------------------------------------------------------------------------

def load_existing_guide_index(guides_dir: Path = GUIDES_DIR) -> list:
    """
    Scan content/guides/ for existing .md files and extract title + slug.
    Returns list of lowercase strings to match against candidate topics.
    """
    terms = []
    if not guides_dir.exists():
        log.warning(f"  {guides_dir} not found — coverage gap check will score all topics as uncovered")
        return terms
    for md_file in guides_dir.glob("**/*.md"):
        terms.append(md_file.stem.lower().replace("-", " "))
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", content, re.MULTILINE | re.IGNORECASE)
            if match:
                terms.append(match.group(1).lower())
        except Exception:
            pass
    log.info(f"  → {len(terms)} existing guide terms loaded from {guides_dir}")
    return terms


def load_drafts_branch_guide_index(branch: str = "drafts", guides_prefix: str = "drafts/guides/") -> list:
    """
    Scan the `drafts` branch (via git, without checking it out) for guides
    already generated and awaiting approval, so a topic isn't regenerated
    and re-billed on every run until Steve approves or rejects it.
    Returns list of lowercase strings to match against candidate topics.
    """
    terms: list = []
    try:
        subprocess.run(
            ["git", "fetch", "origin", branch],
            check=False, capture_output=True, text=True,
        )
        listing = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", f"origin/{branch}", "--", guides_prefix],
            check=False, capture_output=True, text=True,
        )
        if listing.returncode != 0:
            log.warning(f"  Could not read '{branch}' branch — skipping pending-drafts coverage check")
            return terms

        filenames = [f for f in listing.stdout.splitlines() if f.strip()]
        for filename in filenames:
            terms.append(Path(filename).stem.lower().replace("-", " "))
            show = subprocess.run(
                ["git", "show", f"origin/{branch}:{filename}"],
                check=False, capture_output=True, text=True,
            )
            if show.returncode == 0:
                match = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", show.stdout, re.MULTILINE | re.IGNORECASE)
                if match:
                    terms.append(match.group(1).lower())
        log.info(f"  → {len(filenames)} pending draft(s) loaded from '{branch}' branch")
    except Exception as e:
        log.warning(f"  Error loading '{branch}' branch index: {e}")
    return terms


# ---------------------------------------------------------------------------
# Clustering: group signals into topics by keyword overlap
# ---------------------------------------------------------------------------

def _topic_key_for_signal(signal: RawSignal) -> Optional[str]:
    """
    Map a signal to its primary topic key based on TIER1_KEYWORDS.
    Returns the longest (most specific) matched keyword, or None.
    """
    text = (signal.title + " " + signal.text).lower()
    matched = [kw for kw in TIER1_KEYWORDS if kw in text]
    if not matched:
        return None
    return max(matched, key=len)


def _derive_topic_label(cluster_key: str, signals: list) -> str:
    """Produce a human-readable topic label from the cluster key."""
    label_map = {
        "aws scp": "AWS SCP Best Practices",
        "service control policy": "AWS Service Control Policies",
        "guardduty": "AWS GuardDuty Configuration and Tuning",
        "guard duty": "AWS GuardDuty Configuration and Tuning",
        "landing zone": "AWS Landing Zone and Control Tower",
        "control tower": "AWS Control Tower Setup",
        "iam identity centre": "AWS IAM Identity Centre",
        "iam identity center": "AWS IAM Identity Centre",
        "aws sso": "AWS IAM Identity Centre",
        "security hub": "AWS Security Hub Configuration",
        "post-quantum": "Post-Quantum Cryptography and AWS Migration",
        "post quantum": "Post-Quantum Cryptography and AWS Migration",
        "pqc": "Post-Quantum Cryptography and AWS Migration",
        "cyberark": "CyberArk PAM Integration with AWS",
        "pam": "Privileged Access Management in AWS",
        "privileged access": "Privileged Access Management in AWS",
        "ncsc": "NCSC Guidance for Cloud Workloads",
        "ncsc cloud": "NCSC Guidance for Cloud Workloads",
        "kms": "AWS KMS Key Management Best Practices",
        "key management": "AWS KMS Key Management Best Practices",
        "cloud security architect": "UK Cloud Security Architect Day Rates and Career Pathway",
        "day rate": "UK Cloud Security Architect Day Rates",
        "career pathway": "Cloud Security Career Pathway",
        "iam": "AWS IAM Best Practices",
        "least privilege": "AWS Least Privilege IAM Design",
        "cloudtrail": "AWS CloudTrail Configuration Best Practices",
        "cloud trail": "AWS CloudTrail Configuration Best Practices",
        "macie": "AWS Macie Data Security",
        "inspector": "AWS Inspector Vulnerability Management",
        "waf": "AWS WAF Configuration",
        "shield": "AWS Shield DDoS Protection",
        "secrets manager": "AWS Secrets Manager Best Practices",
        "config rules": "AWS Config Rules and Compliance",
        "s3 bucket policy": "AWS S3 Bucket Security",
        "s3 security": "AWS S3 Security Best Practices",
        "eks security": "Amazon EKS Security Best Practices",
        "kubernetes security": "Kubernetes Security on AWS",
        "lambda security": "AWS Lambda Security Best Practices",
        "zero trust": "Zero Trust Architecture on AWS",
        "ransomware aws": "Ransomware Protection on AWS",
        "data exfiltration": "Preventing Data Exfiltration on AWS",
        "compliance": "AWS Compliance and Governance",
        "cve": "Recent Cloud Security CVEs",
        "vulnerability": "Cloud Security Vulnerability Management",
        "incident response aws": "AWS Incident Response Playbook",
        "forensics aws": "AWS Digital Forensics",
        "threat detection": "Cloud Threat Detection Strategies",
        "vpc": "AWS VPC Security Design",
        "network firewall": "AWS Network Firewall Configuration",
    }
    return label_map.get(cluster_key, cluster_key.replace("-", " ").title())


def cluster_signals(signals: list) -> dict:
    """
    Group signals into topic clusters keyed by their primary keyword match.
    Signals with no keyword match are discarded (not guide-worthy).
    Returns dict: cluster_key -> list of RawSignal
    """
    clusters: dict = defaultdict(list)
    for signal in signals:
        key = _topic_key_for_signal(signal)
        if key:
            clusters[key].append(signal)
    log.info(f"  → {len(clusters)} topic clusters from {len(signals)} signals")
    return dict(clusters)


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _score_trending(signals: list) -> tuple:
    """
    0–30 based on velocity: signals appearing in the last TRENDING_WINDOW_HOURS
    vs. signals in the prior window (TRENDING_WINDOW_HOURS–48h).

    Returns (score, newest_iso, recent_count).
    """
    if not signals:
        return 0, "", 0

    now = _now_utc()
    recent = [s for s in signals if _hours_ago(s.published) < TRENDING_WINDOW_HOURS]
    older  = [s for s in signals if TRENDING_WINDOW_HOURS <= _hours_ago(s.published) < 48]

    newest_dt = max((_parse_iso(s.published) or now) for s in signals)
    newest_iso = newest_dt.isoformat()

    recent_count = len(recent)
    older_count  = len(older)
    ratio = recent_count / max(older_count, 1)

    if recent_count >= 3 and ratio >= 2.0:
        score = 30   # Strong surge: many recent, accelerating
    elif recent_count >= 2 and ratio >= 1.5:
        score = 25   # Clear acceleration
    elif recent_count >= 2:
        score = 20   # Multiple recent signals, flat trend
    elif recent_count >= 1 and ratio >= 1.0:
        score = 18   # Single recent signal, holding pace
    elif recent_count >= 1:
        score = 14   # Single recent signal, slowing
    elif older_count >= 3:
        score = 8    # No recent activity but solid older base
    elif older_count >= 1:
        score = 4    # Only older signals
    else:
        score = 0

    return score, newest_iso, recent_count


def _score_volume(signals: list) -> int:
    """
    0–20 based on total signal count and source diversity.
    Also weights native engagement scores (Reddit upvotes, HN points).
    """
    n = len(signals)
    source_types = len({s.source.split("_")[0] for s in signals})  # feed/reddit/hn/nvd
    engagement_bonus = min(4, sum(min(s.score, 100) for s in signals) // 200)

    if n >= 8:
        base = 12
    elif n >= 5:
        base = 10
    elif n >= 3:
        base = 7
    elif n == 2:
        base = 4
    else:
        base = 2

    diversity_bonus = min(4, (source_types - 1) * 2)
    return min(20, base + diversity_bonus + engagement_bonus)


def _score_coverage_gap(cluster_key: str, label: str, existing_terms: list) -> int:
    """
    0–20: how uncovered this topic is on the existing site.
    Full 20 if no existing guide matches; 0 if well-covered; partial otherwise.
    """
    if not existing_terms:
        return 20

    label_lower = label.lower()
    key_lower   = cluster_key.lower()
    key_words   = set(key_lower.split())

    for term in existing_terms:
        if key_lower in term or term in key_lower:
            return 0
        term_words = set(term.split())
        overlap = len(key_words & term_words)
        if overlap >= 2:
            return 6
        if overlap >= 1 and len(key_words) <= 2:
            return 10

    return 20


def _score_keyword_api(
    cluster_key: str,
    label: str,
    keyword_data: dict,
) -> tuple:
    """
    0–30 based on DataForSEO search volume and competition.
    High volume + low competition = maximum score.

    Falls back to static TIER1_KEYWORDS match (capped at 15) when API data
    is unavailable (DataForSEO not configured or keyword returned no result).

    Returns (score, search_volume, competition).
    """
    data = keyword_data.get(cluster_key.lower()) or keyword_data.get(label.lower())

    if not data:
        # Graceful fallback: static keyword match gives partial credit
        matched = _extract_keywords(cluster_key + " " + label)
        if not matched:
            return 0, 0, 0.0
        is_tier1 = any(seed in cluster_key for seed in _TIER1_SEEDS)
        return (15 if is_tier1 else 8), 0, 0.0

    search_volume = data["search_volume"]
    competition   = data["competition"]   # 0.0 (none) → 1.0 (high)

    # Volume component: 0–20
    if search_volume >= 10_000:
        vol_score = 20
    elif search_volume >= 5_000:
        vol_score = 17
    elif search_volume >= 1_000:
        vol_score = 14
    elif search_volume >= 500:
        vol_score = 10
    elif search_volume >= 100:
        vol_score = 6
    elif search_volume > 0:
        vol_score = 3
    else:
        vol_score = 0

    # Competition ease component: 0–10 (lower competition = higher score)
    ease_score = int((1.0 - competition) * 10)

    return min(30, vol_score + ease_score), search_volume, competition


# ---------------------------------------------------------------------------
# Topic scoring
# ---------------------------------------------------------------------------

def score_topic(
    cluster_key: str,
    signals: list,
    existing_terms: list,
    keyword_data: dict,
) -> ScoredTopic:
    label = _derive_topic_label(cluster_key, signals)
    slug  = _slugify(label)

    score_trending, newest_iso, recent_count = _score_trending(signals)
    score_volume    = _score_volume(signals)
    score_gap       = _score_coverage_gap(cluster_key, label, existing_terms)
    score_kw, search_volume, competition = _score_keyword_api(cluster_key, label, keyword_data)

    total = score_trending + score_volume + score_gap + score_kw

    sorted_signals = sorted(signals, key=lambda s: s.score, reverse=True)
    source_urls    = [s.url for s in sorted_signals[:5] if s.url]

    all_text         = " ".join(s.title + " " + s.text for s in signals)
    matched_keywords = list(set(_extract_keywords(all_text)))

    tier = "pillar" if total >= PILLAR_SCORE_THRESHOLD else "supporting"

    return ScoredTopic(
        label=label,
        slug=slug,
        tier=tier,
        total_score=total,
        score_trending=score_trending,
        score_keyword_api=score_kw,
        score_volume=score_volume,
        score_coverage_gap=score_gap,
        signal_count=len(signals),
        recent_signal_count=recent_count,
        keyword_search_volume=search_volume,
        keyword_competition=competition,
        source_urls=source_urls,
        matched_keywords=matched_keywords,
        newest_signal=newest_iso,
    )


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(
    raw_feed_path: str = "raw_feed.json",
    guides_dir: Path = GUIDES_DIR,
    output_path: str = "topic_queue.json",
    top_n: int = TOP_N,
    min_score: int = MIN_SCORE_THRESHOLD,
    dataforseo_login: Optional[str] = None,
    dataforseo_password: Optional[str] = None,
) -> list:
    """Full topic scoring pipeline. Returns list of ScoredTopic dicts."""
    log.info("─" * 60)
    log.info("topic_scorer.py — ZX Cloud Security")
    log.info("─" * 60)

    # Resolve DataForSEO credentials
    dfs_login    = dataforseo_login    or os.environ.get("DATAFORSEO_LOGIN", "")
    dfs_password = dataforseo_password or os.environ.get("DATAFORSEO_PASSWORD", "")
    if not (dfs_login and dfs_password):
        log.warning("  DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD not set — keyword API scores will use static fallback")

    # 1. Gather signals from all sources
    log.info("[1/5] Gathering signals ...")
    all_signals: list = []
    seen_ids: set = set()

    def _add_signals(new_signals: list) -> None:
        for s in new_signals:
            if s.id not in seen_ids:
                seen_ids.add(s.id)
                all_signals.append(s)

    _add_signals(load_feed_scraper_signals(raw_feed_path))
    _add_signals(fetch_hn_signals())
    _add_signals(fetch_nvd_signals())

    log.info(f"  Total unique signals: {len(all_signals)}")

    if not all_signals:
        log.warning("No signals collected — exiting with empty queue")
        _save_queue([], output_path)
        return []

    # 2. Load existing guide index for coverage gap scoring — published guides
    #    plus anything already drafted and awaiting approval on the drafts branch
    log.info("[2/5] Loading existing guide index ...")
    existing_terms = load_existing_guide_index(guides_dir)
    existing_terms += load_drafts_branch_guide_index()

    # 3. Cluster signals into topics
    log.info("[3/5] Clustering signals into topics ...")
    clusters = cluster_signals(all_signals)

    # 4. Fetch keyword data for all cluster labels in one API call
    # Send both labels and cluster keys — labels are descriptive, keys are short.
    # Google Ads has data for neither "iam" alone nor 6-word titles, but mid-length
    # phrases like "aws iam best practices" or "privileged access management" hit well.
    log.info("[4/5] Fetching keyword research data ...")
    cluster_labels = {
        key: _derive_topic_label(key, signals)
        for key, signals in clusters.items()
    }
    # Deduplicated union of labels + keys, all lowercased
    dfs_phrases = list(dict.fromkeys(
        p.lower() for p in list(cluster_labels.values()) + list(cluster_labels.keys())
    ))
    keyword_data: dict = {}
    if dfs_login and dfs_password:
        log.info(f"  Phrases sent to DataForSEO: {dfs_phrases}")
        keyword_data = fetch_keyword_data(
            phrases=dfs_phrases,
            login=dfs_login,
            password=dfs_password,
        )
    else:
        log.info("  Skipping DataForSEO — no credentials")

    # 5. Score each cluster and rank
    log.info("[5/5] Scoring and ranking topics ...")
    scored: list = []
    for cluster_key, signals in clusters.items():
        topic = score_topic(cluster_key, signals, existing_terms, keyword_data)
        scored.append(topic)
        log.info(
            f"  {topic.total_score:3d}/100  [{topic.tier:10s}]  {topic.label}"
            f"  (trending={topic.score_trending}, kw={topic.score_keyword_api},"
            f" vol={topic.score_volume}, gap={topic.score_coverage_gap},"
            f" recent={topic.recent_signal_count}/{topic.signal_count},"
            f" sv={topic.keyword_search_volume})"
        )

    qualified = [t for t in scored if t.total_score >= min_score]
    qualified.sort(key=lambda t: t.total_score, reverse=True)
    selected = qualified[:top_n]

    if not selected:
        log.warning(
            f"  No topics above minimum score threshold ({min_score}) — "
            f"top scorer was {scored[0].total_score if scored else 'N/A'}"
        )
    else:
        log.info(f"  Selected {len(selected)} topic(s) for guide generation:")
        for i, t in enumerate(selected, 1):
            log.info(f"    {i}. [{t.total_score}/100] {t.label} ({t.tier})")

    _save_queue(selected, output_path)
    return selected


def _save_queue(topics: list, path: str) -> None:
    output = {
        "generated_at": _now_utc().isoformat(),
        "topic_count": len(topics),
        "topics": [asdict(t) for t in topics],
    }
    with open(path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info(f"  Saved topic queue → {path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ZX Cloud Security — Topic Scorer")
    parser.add_argument("--raw-feed",    default="raw_feed.json",   help="Path to feed_scraper.py output")
    parser.add_argument("--guides-dir",  default="content/guides",  help="Path to existing Hugo guides directory")
    parser.add_argument("--output",      default="topic_queue.json", help="Output JSON path")
    parser.add_argument("--top-n",       type=int, default=TOP_N,    help="Number of topics to select")
    parser.add_argument("--min-score",   type=int, default=MIN_SCORE_THRESHOLD, help="Minimum score threshold (0–100)")
    args = parser.parse_args()

    topics = run(
        raw_feed_path=args.raw_feed,
        guides_dir=Path(args.guides_dir),
        output_path=args.output,
        top_n=args.top_n,
        min_score=args.min_score,
    )

    print(f"\n{'-'*60}")
    print(f"  Topics selected: {len(topics)}")
    for i, t in enumerate(topics, 1):
        print(f"  {i}. [{t.total_score}/100] [{t.tier}] {t.label}")
        print(f"     Slug      : {t.slug}")
        print(f"     Trending  : {t.score_trending}/30  (recent {t.recent_signal_count}/{t.signal_count} signals)")
        print(f"     Keyword   : {t.score_keyword_api}/30  (sv={t.keyword_search_volume}, comp={t.keyword_competition:.2f})")
        print(f"     Volume    : {t.score_volume}/20")
        print(f"     Gap       : {t.score_coverage_gap}/20")
        print(f"     Sources   : {len(t.source_urls)} URL(s)")
    print(f"  Output: topic_queue.json")
    print(f"{'-'*60}\n")
