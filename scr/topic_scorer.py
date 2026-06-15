"""
topic_scorer.py
ZX Cloud Security — Guide Topic Research & Scoring Agent

Consumes raw_feed.json from feed_scraper.py, pulls additional signals from
Reddit, Hacker News, and NVD CVE, clusters items into named topics, scores
each topic across four dimensions, and outputs a ranked topic queue for
guide_generator.py.

Output: topic_queue.json
"""

import json
import hashlib
import logging
import os
import re
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

# Reddit public JSON API — no auth, ~1 req/sec courtesy limit
REDDIT_SOURCES = [
    {"subreddit": "aws",    "sort": "hot", "limit": 25},
    {"subreddit": "netsec", "sort": "hot", "limit": 25},
]

HN_ALGOLIA_URL = "https://hn.algolia.com/api/v1/search"
HN_QUERY_TERMS = [
    "AWS security", "cloud security", "IAM", "GuardDuty", "S3 breach",
    "CloudTrail", "SCP", "Landing Zone", "zero trust AWS", "CVE cloud",
]
HN_MAX_AGE_HOURS = 48

NVD_CVE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_MAX_RESULTS = 50
NVD_MAX_AGE_HOURS = 48

# Minimum score (out of 100) for a topic to be included in the output queue
MIN_SCORE_THRESHOLD = 35

# Number of top topics to select
TOP_N = 3

# Content directory to scan for existing guides (coverage gap check)
GUIDES_DIR = Path("content/guides")

# Tier word-count thresholds (determines guide tier assignment)
PILLAR_SCORE_THRESHOLD = 65  # topics scoring >= this get pillar treatment

# ---------------------------------------------------------------------------
# Tier 1 seed keywords (from requirements §3.2 + common AWS security terms)
# Matched against topic label for keyword_potential scoring.
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
    score_recency: int                  # 0–25
    score_volume: int                   # 0–25
    score_coverage_gap: int             # 0–25
    score_keyword_potential: int        # 0–25
    signal_count: int                   # Number of raw signals in cluster
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


def fetch_reddit_signals(max_age_hours: int = 48) -> list:
    """Fetch hot posts from r/aws and r/netsec via public JSON API."""
    signals = []
    for source in REDDIT_SOURCES:
        subreddit = source["subreddit"]
        url = f"https://www.reddit.com/r/{subreddit}/{source['sort']}.json?limit={source['limit']}"
        try:
            log.info(f"  Fetching r/{subreddit} ...")
            resp = requests.get(url, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            posts = data.get("data", {}).get("children", [])
            count = 0
            for post in posts:
                p = post.get("data", {})
                created_utc = p.get("created_utc", 0)
                published = datetime.fromtimestamp(created_utc, tz=timezone.utc).isoformat()
                if not _is_recent(published, max_age_hours):
                    continue
                # Filter out non-security posts from r/aws
                title = p.get("title", "")
                selftext = p.get("selftext", "")[:500]
                keywords = _extract_keywords(title + " " + selftext)
                if subreddit == "aws" and not keywords:
                    continue
                link = p.get("url", "")
                permalink = f"https://reddit.com{p.get('permalink', '')}"
                signals.append(RawSignal(
                    id=_make_id(f"reddit_{subreddit}", p.get("id", link)),
                    source=f"reddit_{subreddit}",
                    title=title,
                    url=link if link.startswith("http") else permalink,
                    published=published,
                    score=p.get("score", 0),
                    text=selftext,
                ))
                count += 1
            log.info(f"    → {count} relevant posts from r/{subreddit}")
            time.sleep(1)  # Reddit public API courtesy rate limit
        except Exception as e:
            log.error(f"  Error fetching r/{subreddit}: {e}")
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


def fetch_nvd_signals(max_age_hours: int = NVD_MAX_AGE_HOURS) -> list:
    """
    Fetch recent CVEs from NVD 2.0 API, filtered to cloud/AWS-relevant products.
    NVD API allows ~5 req/30s unauthenticated; we make one request.
    """
    signals = []
    CLOUD_KEYWORDS = [
        "aws", "amazon", "azure", "google cloud", "kubernetes", "docker",
        "openssl", "log4j", "spring", "nginx", "apache", "linux kernel",
        "terraform", "ansible", "jenkins", "gitlab", "github",
    ]
    try:
        log.info("  Fetching NVD CVE feed ...")
        pub_start = (_now_utc() - timedelta(hours=max_age_hours)).strftime("%Y-%m-%dT%H:%M:%S.000")
        pub_end = _now_utc().strftime("%Y-%m-%dT%H:%M:%S.000")
        params = {
            "pubStartDate": pub_start,
            "pubEndDate": pub_end,
            "resultsPerPage": NVD_MAX_RESULTS,
            "startIndex": 0,
        }
        resp = requests.get(NVD_CVE_URL, params=params, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        count = 0
        for vuln in data.get("vulnerabilities", []):
            cve = vuln.get("cve", {})
            cve_id = cve.get("id", "")
            descriptions = cve.get("descriptions", [])
            desc = next((d["value"] for d in descriptions if d.get("lang") == "en"), "")
            published = cve.get("published", _now_utc().isoformat())
            # Filter to cloud-relevant CVEs only
            if not any(kw in desc.lower() for kw in CLOUD_KEYWORDS):
                continue
            # CVSS score for native scoring
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
                score=int(cvss_score * 10),  # 0–100 proxy
                text=desc[:1000],
            ))
            count += 1
        log.info(f"  → {count} cloud-relevant CVEs from NVD")
    except Exception as e:
        log.error(f"  Error fetching NVD: {e}")
    return signals


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
        # Use filename stem as slug signal
        terms.append(md_file.stem.lower().replace("-", " "))
        # Also extract title from frontmatter if present
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", content, re.MULTILINE | re.IGNORECASE)
            if match:
                terms.append(match.group(1).lower())
        except Exception:
            pass
    log.info(f"  → {len(terms)} existing guide terms loaded from {guides_dir}")
    return terms


# ---------------------------------------------------------------------------
# Clustering: group signals into topics by keyword overlap
# ---------------------------------------------------------------------------

def _topic_key_for_signal(signal: RawSignal) -> Optional[str]:
    """
    Map a signal to its primary topic key based on TIER1_KEYWORDS.
    Returns the first matched keyword cluster key, or None if no match.
    """
    text = (signal.title + " " + signal.text).lower()
    # Check keyword matches; return the most specific (longest) match
    matched = [kw for kw in TIER1_KEYWORDS if kw in text]
    if not matched:
        return None
    # Use longest match as cluster anchor (avoids "iam" swallowing everything)
    return max(matched, key=len)


def _derive_topic_label(cluster_key: str, signals: list) -> str:
    """
    Produce a human-readable topic label from the cluster key.
    Prefer the most common title words that match the cluster key.
    """
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

def _score_recency(signals: list) -> tuple:
    """
    0–25 based on the most recent signal in the cluster.
    < 6h  → 25 | < 12h → 22 | < 24h → 18 | < 36h → 12 | < 48h → 6 | older → 0
    Returns (score, newest_iso)
    """
    if not signals:
        return 0, ""
    newest_dt = max(
        (_parse_iso(s.published) or _now_utc()) for s in signals
    )
    newest_iso = newest_dt.isoformat()
    age_h = (_now_utc() - newest_dt).total_seconds() / 3600
    if age_h < 6:
        return 25, newest_iso
    elif age_h < 12:
        return 22, newest_iso
    elif age_h < 24:
        return 18, newest_iso
    elif age_h < 36:
        return 12, newest_iso
    elif age_h < 48:
        return 6, newest_iso
    return 0, newest_iso


def _score_volume(signals: list) -> int:
    """
    0–25 based on number of signals in the cluster and source diversity.
    Also weights native engagement scores (Reddit upvotes, HN points).
    """
    n = len(signals)
    source_types = len({s.source.split("_")[0] for s in signals})  # feed/reddit/hn/nvd
    engagement_bonus = min(5, sum(min(s.score, 100) for s in signals) // 200)

    if n >= 8:
        base = 20
    elif n >= 5:
        base = 16
    elif n >= 3:
        base = 12
    elif n == 2:
        base = 8
    else:
        base = 4

    diversity_bonus = min(5, (source_types - 1) * 2)
    return min(25, base + diversity_bonus + engagement_bonus)


def _score_coverage_gap(cluster_key: str, label: str, existing_terms: list) -> int:
    """
    0–25: how uncovered this topic is on the existing site.
    Full 25 if no existing guide matches; 0 if well-covered; partial otherwise.
    """
    if not existing_terms:
        return 25  # No guides exist yet → always a gap

    label_lower = label.lower()
    key_lower = cluster_key.lower()
    key_words = set(key_lower.split())

    for term in existing_terms:
        # Exact or near-exact match: topic already covered
        if key_lower in term or term in key_lower:
            return 0
        # Partial word overlap: partially covered
        term_words = set(term.split())
        overlap = len(key_words & term_words)
        if overlap >= 2:
            return 8
        if overlap >= 1 and len(key_words) <= 2:
            return 12

    return 25  # No meaningful overlap found → full gap score


def _score_keyword_potential(cluster_key: str, matched_keywords: list) -> int:
    """
    0–25 based on match against TIER1_KEYWORDS and keyword specificity.
    Longer, more specific matches score higher (e.g. 'guardduty tuning' > 'security').
    """
    if not matched_keywords:
        return 0

    # Score by longest match (most specific keyword wins)
    best = max(matched_keywords, key=len)
    specificity = len(best.split())  # word count of the keyword phrase

    # Check if it directly matches a Tier 1 seed topic from the requirements
    TIER1_SEEDS = [
        "cloud security architect", "day rate", "aws scp", "service control policy",
        "guardduty", "landing zone", "control tower", "iam identity centre",
        "iam identity center", "security hub", "post-quantum", "cyberark", "pam",
        "ncsc", "kms", "key management",
    ]
    is_tier1 = any(seed in cluster_key for seed in TIER1_SEEDS)

    if is_tier1:
        base = 20
    elif specificity >= 3:
        base = 16
    elif specificity == 2:
        base = 12
    else:
        base = 8

    # Bonus for multiple keyword matches within the cluster
    bonus = min(5, len(matched_keywords) - 1)
    return min(25, base + bonus)


def score_topic(
    cluster_key: str,
    signals: list,
    existing_terms: list,
) -> ScoredTopic:
    label = _derive_topic_label(cluster_key, signals)
    slug = _slugify(label)

    score_recency, newest_iso = _score_recency(signals)
    score_volume = _score_volume(signals)
    score_coverage_gap = _score_coverage_gap(cluster_key, label, existing_terms)

    all_text = " ".join(s.title + " " + s.text for s in signals)
    matched_keywords = list(set(_extract_keywords(all_text)))
    score_kw = _score_keyword_potential(cluster_key, matched_keywords)

    total = score_recency + score_volume + score_coverage_gap + score_kw

    # Collect up to 5 source URLs, preferring higher-engagement signals
    sorted_signals = sorted(signals, key=lambda s: s.score, reverse=True)
    source_urls = [s.url for s in sorted_signals[:5] if s.url]

    tier = "pillar" if total >= PILLAR_SCORE_THRESHOLD else "supporting"

    return ScoredTopic(
        label=label,
        slug=slug,
        tier=tier,
        total_score=total,
        score_recency=score_recency,
        score_volume=score_volume,
        score_coverage_gap=score_coverage_gap,
        score_keyword_potential=score_kw,
        signal_count=len(signals),
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
) -> list:
    """
    Full topic scoring pipeline. Returns list of ScoredTopic dicts.
    """
    log.info("─" * 60)
    log.info("topic_scorer.py — ZX Cloud Security")
    log.info("─" * 60)

    # 1. Gather signals from all sources
    log.info("[1/4] Gathering signals ...")
    all_signals: list = []
    seen_ids: set = set()

    def _add_signals(new_signals: list) -> None:
        for s in new_signals:
            if s.id not in seen_ids:
                seen_ids.add(s.id)
                all_signals.append(s)

    _add_signals(load_feed_scraper_signals(raw_feed_path))
    _add_signals(fetch_reddit_signals())
    _add_signals(fetch_hn_signals())
    _add_signals(fetch_nvd_signals())

    log.info(f"  Total unique signals: {len(all_signals)}")

    if not all_signals:
        log.warning("No signals collected — exiting with empty queue")
        _save_queue([], output_path)
        return []

    # 2. Load existing guide index for coverage gap scoring
    log.info("[2/4] Loading existing guide index ...")
    existing_terms = load_existing_guide_index(guides_dir)

    # 3. Cluster signals into topics and score each
    log.info("[3/4] Clustering and scoring topics ...")
    clusters = cluster_signals(all_signals)

    scored: list = []
    for cluster_key, signals in clusters.items():
        topic = score_topic(cluster_key, signals, existing_terms)
        scored.append(topic)
        log.info(
            f"  {topic.total_score:3d}/100  [{topic.tier:10s}]  {topic.label}"
            f"  (n={topic.signal_count}, recency={topic.score_recency},"
            f" volume={topic.score_volume}, gap={topic.score_coverage_gap},"
            f" kw={topic.score_keyword_potential})"
        )

    # 4. Filter and rank
    log.info("[4/4] Ranking and selecting top topics ...")
    qualified = [t for t in scored if t.total_score >= min_score]
    qualified.sort(key=lambda t: t.total_score, reverse=True)
    selected = qualified[:top_n]

    if not selected:
        log.warning(f"  No topics above minimum score threshold ({min_score}) — "
                    f"top scorer was {scored[0].total_score if scored else 'N/A'}")
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
    parser.add_argument("--raw-feed",   default="raw_feed.json",   help="Path to feed_scraper.py output")
    parser.add_argument("--guides-dir", default="content/guides",  help="Path to existing Hugo guides directory")
    parser.add_argument("--output",     default="topic_queue.json", help="Output JSON path")
    parser.add_argument("--top-n",      type=int, default=TOP_N,    help="Number of topics to select")
    parser.add_argument("--min-score",  type=int, default=MIN_SCORE_THRESHOLD, help="Minimum score threshold (0–100)")
    args = parser.parse_args()

    topics = run(
        raw_feed_path=args.raw_feed,
        guides_dir=Path(args.guides_dir),
        output_path=args.output,
        top_n=args.top_n,
        min_score=args.min_score,
    )

    print(f"\n{'─'*60}")
    print(f"  Topics selected: {len(topics)}")
    for i, t in enumerate(topics, 1):
        print(f"  {i}. [{t.total_score}/100] [{t.tier}] {t.label}")
        print(f"     Slug:    {t.slug}")
        print(f"     Sources: {len(t.source_urls)} URL(s)")
    print(f"  Output: topic_queue.json")
    print(f"{'─'*60}\n")
