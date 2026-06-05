"""
generate.py
ZX Cloud Security — Hugo Content Generator

Reads enriched_feed.json produced by enricher.py.
Creates one Hugo-formatted markdown file per article in the site/content/posts/ directory.
Also generates a _index.md for each category.
"""

import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

INPUT_FILE = "enriched_feed.json"
SITE_CONTENT_DIR = Path("../site/content/posts")
CATEGORIES = ["aws", "gcp", "azure", "general"]

SEVERITY_EMOJI = {
    "Critical": "🔴",
    "High":     "🟠",
    "Medium":   "🟡",
    "Low":      "🟢",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_slug(item: dict) -> str:
    """Return a clean URL slug — prefer AI-generated, fall back to title-based."""
    slug = (item.get("ai_slug") or "").strip()
    if slug:
        return slug
    # Fallback: slugify the title
    title = item.get("title", "untitled")
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug[:80]


def format_date(iso_date: str) -> str:
    """Return Hugo-compatible date string."""
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def severity_badge(severity: str) -> str:
    emoji = SEVERITY_EMOJI.get(severity, "⚪")
    return f"{emoji} **{severity}**"


def build_frontmatter(item: dict) -> str:
    """Build Hugo TOML front matter for an article."""
    slug = safe_slug(item)
    date = format_date(item.get("published", ""))
    title = item.get("ai_seo_title") or item.get("title", "Untitled")
    title = title.replace('"', '\\"')  # escape quotes
    description = item.get("ai_seo_description", "")
    description = description.replace('"', '\\"')
    severity = item.get("ai_severity", "Medium")
    category = item.get("category", "general")
    source_name = item.get("source_name", "")
    link = item.get("link", "")

    # Build tags list
    tags = item.get("ai_tags", [])
    if not tags:
        tags = item.get("tags", [])
    tags_toml = ", ".join(f'"{t}"' for t in tags[:8])

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
draft = false
+++
"""


def build_body(item: dict) -> str:
    """Build the markdown body for an article."""
    severity = item.get("ai_severity", "Medium")
    source_name = item.get("source_name", "")
    link = item.get("link", "#")
    summary = item.get("ai_summary") or item.get("summary", "")
    architects_take = item.get("ai_architects_take", "")
    original_title = item.get("title", "")

    # Strip HTML tags from raw summary if ai_summary not available
    if not item.get("ai_summary"):
        summary = re.sub(r"<[^>]+>", "", summary)

    lines = []

    # Severity + source line
    lines.append(f"{severity_badge(severity)} &nbsp;|&nbsp; **Source:** [{source_name}]({link})\n")
    lines.append("---\n")

    # Summary
    if summary:
        lines.append(f"{summary}\n")

    # Architect's take
    if architects_take:
        lines.append(f"\n> **Architect's Take:** {architects_take}\n")

    # Original title + link
    lines.append(f"\n**Original advisory:** [{original_title}]({link})\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate(
    input_path: str = INPUT_FILE,
    output_dir: Path = SITE_CONTENT_DIR,
) -> int:
    """
    Generate Hugo markdown files from enriched_feed.json.
    Returns the number of files written.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path) as f:
        items = json.load(f)

    log.info(f"Loaded {len(items)} items from {input_path}")

    # Sort by severity: Critical → High → Medium → Low → unknown
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    items.sort(key=lambda x: severity_order.get(x.get("ai_severity", ""), 4))
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    slugs_seen = set()

    for item in items:
        slug = safe_slug(item)

        # Deduplicate slugs
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


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    count = generate()
    print(f"\n{'─'*50}")
    print(f"  Content files generated : {count}")
    print(f"  Output directory        : {SITE_CONTENT_DIR}")
    print(f"{'─'*50}\n")
    print("Next step: cd ../site && hugo server")