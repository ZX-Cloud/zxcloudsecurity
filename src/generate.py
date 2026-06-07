"""
generate.py
ZX Cloud Security — Hugo Content Generator

Reads enriched_feed.json produced by enricher.py.
Creates one Hugo-formatted markdown file per article in the site/content/posts/ directory.
Also writes site/data/stats.json for the homepage dashboard.
"""

import json
import logging
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

INPUT_FILE = "enriched_feed.json"
SITE_CONTENT_DIR = Path("site/content/posts")
SITE_DATA_DIR = Path("site/data")

SEVERITY_EMOJI = {
    "Critical": "🔴",
    "High":     "🟠",
    "Medium":   "🟡",
    "Low":      "🟢",
}

SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
WEIGHT_MAP = {"Critical": 10, "High": 20, "Medium": 30, "Low": 40}


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

    severity_year = {"Critical": 2026, "High": 2025, "Medium": 2024, "Low": 2023}
    try:
        raw_dt = datetime.fromisoformat(item.get("published", ""))
        year = severity_year.get(severity, 2023)
        dt = raw_dt.replace(year=year)
        date = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        date = format_date(item.get("published", ""))

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


def write_stats(items: list) -> None:
    """Write stats.json for the Hugo homepage dashboard."""
    severity_counts = Counter(i.get("ai_severity", "Medium") for i in items)
    category_counts = Counter(i.get("category", "general") for i in items)

    # Find top critical item
    top_item = None
    for item in items:
        if item.get("ai_severity") == "Critical":
            top_item = {
                "title": item.get("ai_seo_title") or item.get("title", ""),
                "summary": item.get("ai_summary", "")[:200],
                "architects_take": item.get("ai_architects_take", ""),
                "slug": safe_slug(item),
                "source": item.get("source_name", ""),
                "category": item.get("category", "general"),
            }
            break

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
    stats_path = SITE_DATA_DIR / "stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    log.info(f"Wrote stats to {stats_path}")


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

    items.sort(key=lambda x: (
        SEVERITY_ORDER.get(x.get("ai_severity", ""), 4),
        x.get("published", "")
    ))

    # Write stats for homepage
    write_stats(items)

    output_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    slugs_seen = set()

    for item in items:
        slug = safe_slug(item)
        if slug in slugs_seen:
            slug = f"{slug}-{item['id'][:6]}"
        slugs_seen.add(slug)

        frontmatter = build_frontmatter(item)
        body = build_body(item)
        content = frontmatter + "\n" + body

        filepath = output_dir / f"{slug}.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        log.info(f"  Wrote: {filepath.name}")
        written += 1

    log.info(f"Generated {written} content files in {output_dir}")
    return written


if __name__ == "__main__":
    count = generate()
    print(f"\n{'─'*50}")
    print(f"  Content files generated : {count}")
    print(f"  Output directory        : {SITE_CONTENT_DIR}")
    print(f"{'─'*50}\n")
    print("Next step: cd ../site && hugo server")
