"""
feed_scraper.py
ZX Cloud Security — Daily Feed Ingestion Pipeline
"""

import feedparser
import requests
import json
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict, field
from typing import Optional
from email.utils import parsedate_to_datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

FEEDS = [
    {"id": "aws_bulletins", "category": "aws", "name": "AWS Security Bulletins", "url": "https://aws.amazon.com/security/security-bulletins/feed/", "type": "rss", "priority": "high"},
    {"id": "aws_blog", "category": "aws", "name": "AWS Security Blog", "url": "http://feeds.feedburner.com/AWSSecurity", "type": "rss", "priority": "medium"},
    {"id": "aws_whats_new", "category": "aws", "name": "AWS What's New", "url": "https://aws.amazon.com/about-aws/whats-new/recent/feed/", "type": "rss", "priority": "low", "keyword_filter": ["security", "iam", "waf", "guardduty", "inspector", "security hub", "macie", "kms", "cloudtrail", "config", "shield", "firewall", "scp"]},
    {"id": "gcp_compute_bulletins", "category": "gcp", "name": "GCP Compute Engine Security Bulletins", "url": "https://cloud.google.com/feeds/compute-engine-security-bulletins.xml", "type": "rss", "priority": "high"},
    {"id": "gcp_gke_bulletins", "category": "gcp", "name": "GCP GKE Security Bulletins", "url": "https://cloud.google.com/feeds/kubernetes-engine-security-bulletins.xml", "type": "rss", "priority": "high"},
    {"id": "google_project_zero", "category": "gcp", "name": "Google Project Zero", "url": "https://googleprojectzero.blogspot.com/feeds/posts/default", "type": "atom", "priority": "medium"},
    {"id": "msrc", "category": "azure", "name": "Microsoft Security Response Center", "url": "https://api.msrc.microsoft.com/update-guide/rss", "type": "rss", "priority": "high", "max_items": 20},
    {"id": "azure_updates", "category": "azure", "name": "Azure Updates", "url": "https://azure.microsoft.com/en-gb/updates/feed/", "type": "rss", "priority": "low", "keyword_filter": ["security", "defender", "sentinel", "entra", "firewall", "key vault", "policy", "rbac", "zero trust", "identity"]},
    {"id": "cisa_kev", "category": "general", "name": "CISA Known Exploited Vulnerabilities", "url": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json", "type": "json_cisa", "priority": "critical", "fallback_url": "https://raw.githubusercontent.com/cisagov/known-exploited-vulnerabilities/main/json/known_exploited_vulnerabilities.json"},
    {"id": "thehackernews", "category": "general", "name": "The Hacker News", "url": "http://thehackernews.com/feeds/posts/default", "type": "rss", "priority": "medium"},
    {"id": "krebs", "category": "general", "name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/", "type": "rss", "priority": "medium"},
    {"id": "theregister_security", "category": "general", "name": "The Register — Security", "url": "https://www.theregister.co.uk/security/headlines.atom", "type": "atom", "priority": "medium"},
    {"id": "schneier", "category": "general", "name": "Schneier on Security", "url": "https://www.schneier.com/blog/atom.xml", "type": "atom", "priority": "medium"},
]

@dataclass
class FeedItem:
    id: str
    source_id: str
    source_name: str
    category: str
    title: str
    link: str
    summary: str
    published: str
    priority: str
    keyword_matched: bool = False
    tags: list = field(default_factory=list)
    ai_summary: Optional[str] = None
    ai_architects_take: Optional[str] = None
    ai_severity: Optional[str] = None
    ai_seo_title: Optional[str] = None
    ai_seo_description: Optional[str] = None
    ai_slug: Optional[str] = None
    ai_tags: list = field(default_factory=list)


def make_id(source_id: str, link: str) -> str:
    return hashlib.sha256(f"{source_id}:{link}".encode()).hexdigest()[:16]


def _parse_date(entry) -> str:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc).isoformat()
    if hasattr(entry, "published") and entry.published:
        try:
            return parsedate_to_datetime(entry.published).isoformat()
        except Exception:
            pass
    return datetime.now(timezone.utc).isoformat()


def _keyword_match(text: str, keywords: list) -> bool:
    return any(kw in text.lower() for kw in keywords)


def _is_recent(published_iso: str, max_age_hours: int = 48) -> bool:
    try:
        dt = datetime.fromisoformat(published_iso)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) - dt < timedelta(hours=max_age_hours)
    except Exception:
        return True


def fetch_rss_feed(feed_def: dict, max_age_hours: int = 48) -> list:
    items = []
    items = []
    try:
        log.info(f"Fetching {feed_def['name']} ...")
        parsed = feedparser.parse(
            feed_def["url"],
            request_headers={"User-Agent": "ZXCloudSecurity/1.0 (+https://zxcloudsecurity.co.uk)"},
        )
        if parsed.bozo:
            log.warning(f"  Minor parse warning ({feed_def['id']}): {parsed.bozo_exception}")
            if not parsed.entries:
                log.error(f"  No entries returned for {feed_def['id']} — skipping")
                return items

        keywords = feed_def.get("keyword_filter", [])
        for entry in parsed.entries:
            title = getattr(entry, "title", "") or ""
            link = getattr(entry, "link", "") or ""
            summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
            published = _parse_date(entry)

            if not _is_recent(published, max_age_hours):
                continue
            if keywords and not _keyword_match(title + " " + summary, keywords):
                continue

            items.append(FeedItem(
                id=make_id(feed_def["id"], link),
                source_id=feed_def["id"],
                source_name=feed_def["name"],
                category=feed_def["category"],
                title=title,
                link=link,
                summary=summary[:2000],
                published=published,
                priority=feed_def["priority"],
                keyword_matched=bool(keywords),
            ))
        # Cap items if max_items is set
        max_items = feed_def.get("max_items")
        if max_items:
            items = items[:max_items]
        log.info(f"  → {len(items)} items from {feed_def['name']}")
    except Exception as e:
        log.error(f"  Error fetching {feed_def['id']}: {e}")
    return items


def fetch_cisa_kev(feed_def: dict, max_age_hours: int = 48) -> list:
    items = []
    # CISA blocks non-browser user-agents; use a fallback GitHub mirror if primary fails
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ZXCloudSecurity/1.0; +https://zxcloudsecurity.co.uk)",
        "Accept": "application/json",
    }
    try:
        log.info("Fetching CISA KEV ...")
        url = feed_def["url"]
        resp = requests.get(url, timeout=30, headers=headers)
        if resp.status_code != 200:
            fallback = feed_def.get("fallback_url")
            if fallback:
                log.warning(f"  CISA primary returned {resp.status_code}, trying GitHub mirror ...")
                resp = requests.get(fallback, timeout=30, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        for v in data.get("vulnerabilities", []):
            date_added = v.get("dateAdded", "")
            if date_added:
                try:
                    published = datetime.strptime(date_added, "%Y-%m-%d").replace(
                        tzinfo=timezone.utc
                    ).isoformat()
                    if not _is_recent(published, max_age_hours):
                        continue
                except ValueError:
                    published = datetime.now(timezone.utc).isoformat()
            else:
                published = datetime.now(timezone.utc).isoformat()

            cve_id = v.get("cveID", "")
            product = v.get("product", "")
            vendor = v.get("vendorProject", "")
            description = v.get("shortDescription", "")
            due_date = v.get("dueDate", "")

            items.append(FeedItem(
                id=make_id(feed_def["id"], cve_id),
                source_id=feed_def["id"],
                source_name=feed_def["name"],
                category=feed_def["category"],
                title=f"{cve_id}: {vendor} {product}",
                link="https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                summary=f"{description} (Remediation due: {due_date})",
                published=published,
                priority="critical",
                tags=[cve_id, vendor, product],
            ))
        log.info(f"  → {len(items)} new KEV entries")
    except Exception as e:
        log.error(f"  Error fetching CISA KEV: {e}")
    return items


def ingest_all(max_age_hours: int = 48) -> list:
    all_items = []
    seen_ids = set()
    for feed_def in FEEDS:
        if feed_def["type"] == "json_cisa":
            items = fetch_cisa_kev(feed_def, max_age_hours)
        else:
            items = fetch_rss_feed(feed_def, max_age_hours)
        for item in items:
            if item.id not in seen_ids:
                seen_ids.add(item.id)
                all_items.append(item)
    all_items.sort(key=lambda x: x.published, reverse=True)
    all_items = all_items[:50]
    log.info(f"Total unique items ingested: {len(all_items)}")
    return all_items


def save_raw(items: list, path: str = "raw_feed.json") -> None:
    with open(path, "w") as f:
        json.dump([asdict(i) for i in items], f, indent=2, default=str)
    log.info(f"Saved {len(items)} items to {path}")


if __name__ == "__main__":
    items = ingest_all(max_age_hours=48)
    save_raw(items, "raw_feed.json")
    from collections import Counter
    cats = Counter(i.category for i in items)
    priorities = Counter(i.priority for i in items)
    print(f"\n{'-'*50}")
    print(f"  Items by category: {dict(cats)}")
    print(f"  Items by priority: {dict(priorities)}")
    print(f"  Output: raw_feed.json")
    print(f"{'-'*50}\n")
