"""
generate.py
ZX Cloud Security — Hugo Content Generator

Reads enriched_feed.json produced by enricher.py.
Creates one Hugo-formatted markdown file per article in the site/content/posts/ directory.
- Add-only by default: skips slugs that already exist (deduplication)
- Removes posts older than MAX_AGE_DAYS to keep archive manageable
- Writes stats.json based on ALL posts in archive for accurate homepage counts
"""

import json
import logging
import re
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

INPUT_FILE = "enriched_feed.json"
SITE_CONTENT_DIR = Path("site/content/posts")
SITE_DATA_DIR = Path("site/data")
MAX_AGE_DAYS = 180  # 6 months

SEVERITY_EMOJI = {
    "Critical": "🔴",
    "High":     "🟠",
    "Medium":   "🟡",
    "Low":      "🟢",
}

SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
WEIGHT_MAP = {"Critical": 10, "High": 20, "Medium": 30, "Low": 40}

# Severity year encoding — Critical gets highest year so Hugo sorts it first
SEVERITY_YEAR = {"Critical": 2026, "High": 2025, "Medium": 2024, "Low": 2023}


def safe_slug(item: dict) -> str:
    slug = (item.get("ai_slug") or "").strip()
    if slug:
        return slug
    title = item.get("title", "untitled")
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug[:80]


def format_date(iso_date: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def severity_badge(severity: str) -> str:
    emoji = SEVERITY_EMOJI.get(severity, "⚪")
    return f"{emoji} **{severity}**"


def build_frontmatter(item: dict) -> str:
    slug = safe_slug(item)
    severity = item.get("ai_severity", "Medium")

    # Encode severity into year so Hugo sorts Critical first
    try:
        raw_dt = datetime.fromisoformat(item.get("published", ""))
        year = SEVERITY_YEAR.get(severity, 2023)
        dt = raw_dt.replace(year=year)
        date = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        date = format_date(item.get("published", ""))

    real_date = format_date(item.get("published", ""))
    title = item.get("ai_seo_title") or item.get("title", "Untitled")
    title = title.replace('"', '\\"')
    description = (item.get("ai_seo_description") or "").replace('"', '\\"')
    category = item.get("category", "general")
    source_name = item.get("source_name", "")
    link = item.get("link", "")

    tags = item.get("ai_tags", []) or item.get("tags", [])
    tags_toml = ", ".join(f'"{t}"' for t in tags[:8])
    weight = WEIGHT_MAP.get(severity, 50)

    return f"""+++
title = "{title}"
date = "{date}"
publishDate = "{real_date}"
slug = "{slug}"
description = "{description}"
categories = ["{category}"]
tags = [{tags_toml}]
severity = "{severity}"
source = "{source_name}"
source_url = "{link}"
weight = {weight}
draft = false
+++
"""


def build_body(item: dict) -> str:
    severity = item.get("ai_severity", "Medium")
    source_name = item.get("source_name", "")
    link = item.get("link", "#")
    summary = item.get("ai_summary") or item.get("summary", "")
    architects_take = item.get("ai_architects_take", "")
    original_title = item.get("title", "")

    if not item.get("ai_summary"):
        summary = re.sub(r"<[^>]+>", "", summary)

    lines = []
    lines.append(f"{severity_badge(severity)} &nbsp;|&nbsp; **Source:** [{source_name}]({link})\n")
    lines.append("---\n")
    if summary:
        lines.append(f"{summary}\n")
    if architects_take:
        lines.append(f"\n> **Security Architect's Take:** {architects_take}\n")
    lines.append(f"\n**Original advisory:** [{original_title}]({link})\n")

    return "\n".join(lines)


def read_archive_stats(output_dir: Path) -> list:
    """Read severity and category from all existing archive posts."""
    archive_items = []
    for filepath in output_dir.glob("*.md"):
        try:
            content = filepath.read_text(encoding="utf-8")
            severity_match = re.search(r'severity = "([^"]+)"', content)
            category_match = re.search(r'categories = \["([^"]+)"\]', content)
            title_match = re.search(r'title = "([^"]+)"', content)
            slug_match = re.search(r'slug = "([^"]+)"', content)
            summary_match = re.search(r'\n\n(.+?)(?:\n|$)', content[content.find('+++\n', 3)+4:])
            if severity_match and category_match:
                archive_items.append({
                    "ai_severity": severity_match.group(1),
                    "category": category_match.group(1),
                    "ai_seo_title": title_match.group(1) if title_match else "",
                    "ai_slug": slug_match.group(1) if slug_match else filepath.stem,
                    "ai_summary": "",
                    "ai_architects_take": "",
                })
        except Exception as e:
            log.warning(f"Could not read stats from {filepath.name}: {e}")
    return archive_items


def write_stats(items: list, top_item_full: dict = None) -> None:
    """Write stats.json for the Hugo homepage dashboard."""
    severity_counts = Counter(i.get("ai_severity", "Medium") for i in items)
    category_counts = Counter(i.get("category", "general") for i in items)

    top_item = None
    if top_item_full:
        top_item = {
            "title": top_item_full.get("ai_seo_title") or top_item_full.get("title", ""),
            "summary": top_item_full.get("ai_summary", "")[:200],
            "architects_take": top_item_full.get("ai_architects_take", ""),
            "slug": safe_slug(top_item_full),
            "source": top_item_full.get("source_name", ""),
            "category": top_item_full.get("category", "general"),
        }

    stats = {
        "updated": datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC"),
        "total": len(items),
        "severity": {
            "critical": severity_counts.get("Critical", 0),
            "high": severity_counts.get("High", 0),
            "medium": severity_counts.get("Medium", 0),
        },
        "categories": {
            "aws": category_counts.get("aws", 0),
            "azure": category_counts.get("azure", 0),
            "gcp": category_counts.get("gcp", 0),
            "general": category_counts.get("general", 0),
        },
        "top_critical": top_item,
    }

    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SITE_DATA_DIR / "stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    log.info(f"Wrote stats.json — {len(items)} total posts, {severity_counts.get('Critical',0)} critical")


def prune_old_posts(output_dir: Path, max_age_days: int = MAX_AGE_DAYS) -> int:
    """Remove posts older than max_age_days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    removed = 0
    for filepath in output_dir.glob("*.md"):
        try:
            content = filepath.read_text(encoding="utf-8")
            match = re.search(r'publishDate = "([^"]+)"', content)
            if match:
                pub_date = datetime.fromisoformat(match.group(1))
                if pub_date.tzinfo is None:
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                if pub_date < cutoff:
                    filepath.unlink()
                    removed += 1
                    log.info(f"  Pruned old post: {filepath.name}")
        except Exception as e:
            log.warning(f"  Could not check age of {filepath.name}: {e}")
    return removed


def generate(
    input_path: str = INPUT_FILE,
    output_dir: Path = SITE_CONTENT_DIR,
) -> int:
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path) as f:
        items = json.load(f)

    log.info(f"Loaded {len(items)} items from {input_path}")

    # Sort today's new items by severity
    items.sort(key=lambda x: (
        SEVERITY_ORDER.get(x.get("ai_severity", ""), 4),
        x.get("published", "")
    ))

    output_dir.mkdir(parents=True, exist_ok=True)

    # Prune posts older than 6 months
    pruned = prune_old_posts(output_dir)
    if pruned:
        log.info(f"Pruned {pruned} posts older than {MAX_AGE_DAYS} days")

    # Get existing slugs to avoid duplicates
    existing_slugs = {f.stem for f in output_dir.glob("*.md")}
    log.info(f"Existing posts in archive: {len(existing_slugs)}")

    written = 0
    skipped = 0
    slugs_seen = set()
    top_critical = None

    for item in items:
        slug = safe_slug(item)
        if slug in slugs_seen:
            slug = f"{slug}-{item['id'][:6]}"
        slugs_seen.add(slug)

        # Track top critical for homepage featured item
        if top_critical is None and item.get("ai_severity") == "Critical":
            top_critical = item

        # Skip if already in archive
        if slug in existing_slugs:
            skipped += 1
            continue

        frontmatter = build_frontmatter(item)
        body = build_body(item)
        content = frontmatter + "\n" + body

        filepath = output_dir / f"{slug}.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        log.info(f"  Wrote: {filepath.name}")
        written += 1

    log.info(f"Written: {written} new, Skipped: {skipped} duplicates")

    # Write stats based on ALL posts in archive (not just today's new ones)
    all_archive = read_archive_stats(output_dir)
    log.info(f"Archive total for stats: {len(all_archive)} posts")
    write_stats(all_archive, top_critical)

    return written


if __name__ == "__main__":
    count = generate()
    print(f"\n{'─'*50}")
    print(f"  New posts written  : {count}")
    print(f"  Output directory   : {SITE_CONTENT_DIR}")
    print(f"{'─'*50}\n")
    print("Next step: cd site && hugo server")
