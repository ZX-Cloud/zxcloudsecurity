"""
enricher.py
ZX Cloud Security — Claude API Enrichment Pipeline

Reads raw_feed.json produced by feed_scraper.py.
Skips items whose IDs already exist in site/content/posts/ (deduplication).
Calls Claude API only for genuinely new items.
Writes enriched_feed.json ready for the Hugo static site generator.
"""

import json
import logging
import os
import re
import time
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024
MAX_RETRIES = 3
RETRY_DELAY = 5
REQUEST_DELAY = 0.5

INPUT_FILE = "raw_feed.json"
OUTPUT_FILE = "enriched_feed.json"
FAILED_FILE = "enrichment_failures.json"
SEEN_IDS_FILE = "site/data/seen_ids.json"

SYSTEM_PROMPT = """You are a senior cloud security architect writing for zxcloudsecurity.co.uk,
a UK-based security news site aimed at cloud security architects and engineers.

Your job is to enrich raw security advisory and news items with structured metadata.
Write in clear, professional UK English. Be concise and practical — your readers
are experienced practitioners, not beginners.

Always respond with valid JSON only. No preamble, no markdown, no explanation."""


def build_user_prompt(item: dict) -> str:
    return f"""Enrich this security news item with structured metadata.

Source: {item['source_name']}
Category: {item['category']}
Priority: {item['priority']}
Title: {item['title']}
Summary: {item['summary'][:1500]}
URL: {item['link']}

Return a JSON object with exactly these fields:

{{
  "ai_summary": "2-3 sentence plain-English summary of what this is and why it matters. No jargon where possible.",
  "ai_architects_take": "1-2 sentences of practical advice for a cloud security architect — what action should they consider, if any? Be specific.",
  "ai_severity": "One of: Critical | High | Medium | Low — based on exploitability and blast radius.",
  "ai_seo_title": "SEO-optimised page title, maximum 60 characters, include the cloud provider or CVE ID if relevant.",
  "ai_seo_description": "Meta description for search engines, maximum 155 characters, should summarise the security impact clearly.",
  "ai_slug": "URL slug: lowercase, hyphens only, no special characters, include CVE ID or key terms e.g. aws-iam-privilege-escalation-cve-2026-1234",
  "ai_tags": ["tag1", "tag2", "tag3"]
}}

For ai_tags: include the cloud provider (aws/gcp/azure), affected service names, CVE IDs if present,
and 2-3 relevant security concepts (e.g. iam, privilege-escalation, ransomware, supply-chain).
Maximum 8 tags."""


def load_seen_ids(seen_ids_path: str = SEEN_IDS_FILE) -> set:
    """Load the set of already-published item IDs."""
    path = Path(seen_ids_path)
    if not path.exists():
        return set()
    try:
        with open(path) as f:
            data = json.load(f)
        return set(data.get("ids", []))
    except Exception as e:
        log.warning(f"Could not load seen_ids: {e}")
        return set()


def save_seen_ids(seen_ids: set, seen_ids_path: str = SEEN_IDS_FILE) -> None:
    """Save the updated set of published item IDs."""
    path = Path(seen_ids_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w") as f:
            json.dump({"ids": sorted(seen_ids)}, f, indent=2)
        log.info(f"Saved {len(seen_ids)} seen IDs to {seen_ids_path}")
    except Exception as e:
        log.warning(f"Could not save seen_ids: {e}")


def call_claude(item: dict, api_key: str) -> dict | None:
    prompt = build_user_prompt(item)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                ANTHROPIC_API_URL,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30,
            )

            if resp.status_code == 429:
                wait = RETRY_DELAY * attempt
                log.warning(f"  Rate limited — waiting {wait}s (attempt {attempt}/{MAX_RETRIES})")
                time.sleep(wait)
                continue

            if resp.status_code == 529:
                wait = RETRY_DELAY * attempt
                log.warning(f"  API overloaded — waiting {wait}s (attempt {attempt}/{MAX_RETRIES})")
                time.sleep(wait)
                continue

            resp.raise_for_status()
            data = resp.json()

            text = ""
            for block in data.get("content", []):
                if block.get("type") == "text":
                    text += block.get("text", "")

            text = re.sub(r"^```(?:json)?\s*", "", text.strip())
            text = re.sub(r"\s*```$", "", text)

            return json.loads(text)

        except json.JSONDecodeError as e:
            log.error(f"  JSON parse error for '{item['title'][:50]}': {e}")
            return None

        except requests.RequestException as e:
            log.error(f"  API request error (attempt {attempt}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                return None

    return None


def apply_enrichment(item: dict, enrichment: dict) -> dict:
    item["ai_summary"] = enrichment.get("ai_summary", "")
    item["ai_architects_take"] = enrichment.get("ai_architects_take", "")
    item["ai_severity"] = enrichment.get("ai_severity", item["priority"].capitalize())
    item["ai_seo_title"] = enrichment.get("ai_seo_title", item["title"])[:60]
    item["ai_seo_description"] = enrichment.get("ai_seo_description", "")[:155]
    item["ai_slug"] = enrichment.get("ai_slug", "").lower().strip()
    item["ai_tags"] = enrichment.get("ai_tags", [])[:8]
    return item


def enrich_all(
    input_path: str = INPUT_FILE,
    output_path: str = OUTPUT_FILE,
    failed_path: str = FAILED_FILE,
    api_key: str | None = None,
) -> tuple[int, int]:
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    raw_path = Path(input_path)
    if not raw_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(raw_path) as f:
        items = json.load(f)

    log.info(f"Loaded {len(items)} items from {input_path}")

    # Load already-seen IDs to skip items already in the archive
    seen_ids = load_seen_ids()
    log.info(f"Already seen IDs in archive: {len(seen_ids)}")

    # Filter to only new items
    new_items = [i for i in items if i.get("id") not in seen_ids]
    skipped_count = len(items) - len(new_items)
    log.info(f"New items to enrich: {len(new_items)} (skipped {skipped_count} already archived)")

    enriched = []
    failed = []

    for i, item in enumerate(new_items, 1):
        log.info(f"[{i}/{len(new_items)}] Enriching: {item['title'][:70]}")

        enrichment = call_claude(item, api_key)

        if enrichment:
            enriched_item = apply_enrichment(item, enrichment)
            enriched.append(enriched_item)
            log.info(f"  ✓ severity={enriched_item['ai_severity']}  slug={enriched_item['ai_slug'][:50]}")
        else:
            log.warning(f"  ✗ Enrichment failed — keeping raw item")
            failed.append(item)
            enriched.append(item)

        if i < len(new_items):
            time.sleep(REQUEST_DELAY)

    # Filter out Low severity and cap at 50
    before_filter = len(enriched)
    enriched = [i for i in enriched if i.get("ai_severity", "Medium") != "Low"]
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    enriched.sort(key=lambda x: severity_order.get(x.get("ai_severity", ""), 4))
    enriched = enriched[:50]
    log.info(f"After filter: {before_filter} → {len(enriched)} items (Lows removed, capped at 50)")

    # Update seen_ids with newly enriched items
    for item in enriched:
        seen_ids.add(item.get("id", ""))
    save_seen_ids(seen_ids)

    with open(output_path, "w") as f:
        json.dump(enriched, f, indent=2, default=str)
    log.info(f"Wrote {len(enriched)} enriched items to {output_path}")

    if failed:
        with open(failed_path, "w") as f:
            json.dump(failed, f, indent=2, default=str)
        log.warning(f"Wrote {len(failed)} failed items to {failed_path}")

    return len(enriched) - len(failed), len(failed)


if __name__ == "__main__":
    success, failures = enrich_all()

    print(f"\n{'─'*50}")
    print(f"  Enriched successfully : {success}")
    print(f"  Failed (raw fallback) : {failures}")
    print(f"  Output               : {OUTPUT_FILE}")
    if failures:
        print(f"  Failures logged      : {FAILED_FILE}")
    print(f"{'─'*50}\n")
