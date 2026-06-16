"""
guide_generator.py
ZX Cloud Security — AI Guide Generation Pipeline

Consumes topic_queue.json from topic_scorer.py, calls the Claude API with
web search enabled to generate full Hugo-compatible markdown guides, and
writes drafts to drafts/guides/.

Output: drafts/guides/<slug>.md  (one file per topic)
        generation_report.json   (metadata for quality_checker.py)
"""

import json
import logging
import os
import re
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import anthropic

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 8000
AUTHOR = "Steve Harrison - Principal Security Architect"

WORD_COUNT_TARGETS = {
    "pillar":     {"min": 3000, "target": 4500, "max": 6000},
    "supporting": {"min": 1200, "target": 1600, "max": 2000},
}

DRAFTS_DIR = Path("drafts/guides")

# Retry config: regenerate once on API error or quality failure
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 5

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class GenerationResult:
    """Outcome of a single guide generation attempt."""
    topic_label: str
    slug: str
    tier: str
    success: bool
    output_path: str = ""
    word_count: int = 0
    error: str = ""
    attempts: int = 0
    generated_at: str = ""
    source_urls: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def _build_system_prompt() -> str:
    return """You are Steve Harrison, a Principal Security Architect with 15 years of experience \
designing and securing AWS cloud environments for UK financial services, government, and enterprise clients. \
You write practical, authoritative guides for your peers — other cloud security architects, \
senior engineers, and CTOs evaluating cloud security posture.

Your writing style:
- Direct and opinionated — you have a point of view based on real production experience
- Technical depth without padding — every paragraph earns its place
- UK English spelling throughout (e.g. "organisation", "authorisation", "colour")
- You reference real AWS services, IAM policy syntax, SCP JSON, and CloudFormation/CDK snippets where they add value
- You acknowledge trade-offs honestly rather than pretending everything has a clean answer
- You occasionally reference UK-specific context: NCSC guidance, FCA compliance, GDPR, IR35

SEO requirements (follow these precisely):
- The target keyword must appear in the H1, in the first paragraph (within the first 100 words), \
and at least twice more naturally throughout the guide
- Use proper heading hierarchy: one H1, multiple H2s, H3s under H2s where needed
- Meta description must be 140–160 characters and include the target keyword
- Include practical takeaways in a concluding section

Output format — you must respond with ONLY valid Hugo markdown, starting with the frontmatter \
block and ending with the last line of content. No preamble, no explanation, no code fences \
around the entire document. The output must be ready to save directly as a .md file.

Hugo frontmatter format (YAML, between --- delimiters):
---
title: "Exact guide title here"
date: YYYY-MM-DD
description: "140–160 char meta description including target keyword"
tags: ["tag1", "tag2", "tag3", "tag4"]
slug: "kebab-case-slug"
author: "Steve Harrison - Principal Security Architect"
word_count: NNNN
draft: false
---

Internal linking: where you would naturally reference another guide on the site, \
include a commented-out Hugo link in this format:
<!-- INTERNAL_LINK: suggested anchor text | suggested-target-slug -->
These will be reviewed and activated by the editor."""


def _build_user_prompt(
    topic_label: str,
    target_keyword: str,
    tier: str,
    word_count_target: int,
    source_urls: list,
    existing_guide_slugs: list,
) -> str:
    wc = WORD_COUNT_TARGETS[tier]
    source_block = "\n".join(f"- {url}" for url in source_urls[:5]) if source_urls else "- (use web search to find current authoritative sources)"
    existing_block = "\n".join(f"- {slug}" for slug in existing_guide_slugs[:20]) if existing_guide_slugs else "- (none yet)"

    return f"""Write a {tier} guide on the following topic for zxcloudsecurity.co.uk.

TOPIC: {topic_label}
TARGET KEYWORD: {target_keyword}
TIER: {tier}
WORD COUNT TARGET: {word_count_target} words (minimum {wc['min']}, maximum {wc['max']})

REFERENCE SOURCES (use web search to retrieve current content from these and find additional authoritative sources):
{source_block}

EXISTING GUIDES ON THE SITE (for internal linking suggestions only — do not duplicate their content):
{existing_block}

GUIDE REQUIREMENTS:
1. Open with a strong paragraph establishing why this topic matters right now — include the target keyword within the first 100 words
2. Structure with clear H2 sections covering the main aspects a practitioner needs to know
3. Include at least {"3 code blocks (JSON policy, CLI command, or CloudFormation/CDK snippet)" if tier == "pillar" else "1 code block"} with real, working examples
4. Where relevant, reference AWS documentation, NCSC guidance, or CIS benchmarks
5. Include a "Common Mistakes" or "Pitfalls" section — this performs well in search and adds genuine value
6. End with a "Key Takeaways" section (bullet list, 4–6 points)
7. Add <!-- INTERNAL_LINK: ... --> comments wherever you'd naturally cross-reference another guide

Write the complete guide now. Start immediately with the --- frontmatter block."""


def _derive_target_keyword(topic_label: str, slug: str) -> str:
    """
    Derive the primary SEO target keyword from the topic label.
    Prefers lowercase, natural phrasing suitable for search.
    """
    # Strip common filler words from the label for a tighter keyword
    label_lower = topic_label.lower()
    # Remove trailing "best practices", "guide", "overview" for cleaner keyword
    keyword = re.sub(r"\s+(guide|overview|tutorial|introduction|complete guide)$", "", label_lower).strip()
    return keyword


# ---------------------------------------------------------------------------
# Existing guide index (for internal linking hints)
# ---------------------------------------------------------------------------

def _load_existing_slugs(guides_dir: Path = Path("content/guides")) -> list:
    """Return list of existing guide slugs from content/guides/."""
    slugs = []
    if not guides_dir.exists():
        return slugs
    for md_file in guides_dir.glob("**/*.md"):
        slugs.append(md_file.stem)
        # Also try to extract slug from frontmatter
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"^slug:\s*['\"]?(.+?)['\"]?\s*$", content, re.MULTILINE)
            if match:
                slugs.append(match.group(1).strip())
        except Exception:
            pass
    return list(dict.fromkeys(slugs))  # deduplicate, preserve order


# ---------------------------------------------------------------------------
# Markdown validation helpers
# ---------------------------------------------------------------------------

def _count_words(text: str) -> int:
    """Word count excluding frontmatter and code blocks."""
    # Strip YAML frontmatter
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    # Strip code blocks
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    return len(body.split())


def _extract_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter into a dict. Returns empty dict on failure."""
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fm: dict = {}
    for line in match.group(1).splitlines():
        kv = line.split(":", 1)
        if len(kv) == 2:
            fm[kv[0].strip()] = kv[1].strip().strip('"\'')
    return fm


def _patch_word_count(text: str, actual_count: int) -> str:
    """Update the word_count frontmatter field to match actual count."""
    return re.sub(
        r"(^word_count:\s*)\d+",
        f"\\g<1>{actual_count}",
        text,
        flags=re.MULTILINE,
    )


def _looks_like_valid_markdown(text: str) -> tuple:
    """
    Basic sanity checks before saving. Returns (is_valid, reason).
    Detailed validation is handled by quality_checker.py.
    """
    if not text.strip().startswith("---"):
        return False, "Missing frontmatter — response did not start with ---"
    fm = _extract_frontmatter(text)
    if not fm.get("title"):
        return False, "Frontmatter missing 'title' field"
    if not fm.get("slug"):
        return False, "Frontmatter missing 'slug' field"
    if "# " not in text:
        return False, "No headings found in generated content"
    return True, ""


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def _call_claude_api(
    client: anthropic.Anthropic,
    system_prompt: str,
    user_prompt: str,
) -> tuple:
    """
    Call Claude API with web search tool enabled.
    Returns (content_text, raw_response).
    Raises anthropic.APIError on failure.
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": user_prompt}],
    )

    # Concatenate all text blocks from the response
    # (web search tool may interleave tool_use/tool_result blocks)
    text_parts = [
        block.text
        for block in response.content
        if hasattr(block, "text") and block.text
    ]
    content_text = "\n".join(text_parts).strip()
    return content_text, response


# ---------------------------------------------------------------------------
# Single guide generation
# ---------------------------------------------------------------------------

def generate_guide(
    client: anthropic.Anthropic,
    topic: dict,
    existing_slugs: list,
    drafts_dir: Path = DRAFTS_DIR,
) -> GenerationResult:
    """
    Generate a single guide for the given topic dict (from topic_queue.json).
    Retries up to MAX_RETRIES times on failure.
    """
    label = topic["label"]
    slug = topic["slug"]
    tier = topic["tier"]
    source_urls = topic.get("source_urls", [])
    target_keyword = _derive_target_keyword(label, slug)
    word_count_target = WORD_COUNT_TARGETS[tier]["target"]

    log.info(f"  Generating [{tier}] guide: {label}")
    log.info(f"    Keyword: {target_keyword} | Target words: {word_count_target}")

    system_prompt = _build_system_prompt()
    user_prompt = _build_user_prompt(
        topic_label=label,
        target_keyword=target_keyword,
        tier=tier,
        word_count_target=word_count_target,
        source_urls=source_urls,
        existing_guide_slugs=existing_slugs,
    )

    result = GenerationResult(
        topic_label=label,
        slug=slug,
        tier=tier,
        success=False,
        source_urls=source_urls,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    for attempt in range(1, MAX_RETRIES + 1):
        result.attempts = attempt
        try:
            log.info(f"    API call attempt {attempt}/{MAX_RETRIES} ...")
            content, response = _call_claude_api(client, system_prompt, user_prompt)

            if not content:
                log.warning(f"    Attempt {attempt}: empty response from API")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_SECONDS)
                continue

            # Basic validation before saving
            is_valid, reason = _looks_like_valid_markdown(content)
            if not is_valid:
                log.warning(f"    Attempt {attempt}: {reason}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_SECONDS)
                continue

            # Patch word count in frontmatter to match actual
            actual_wc = _count_words(content)
            content = _patch_word_count(content, actual_wc)

            # Save to drafts directory
            drafts_dir.mkdir(parents=True, exist_ok=True)
            output_path = drafts_dir / f"{slug}.md"
            output_path.write_text(content, encoding="utf-8")

            result.success = True
            result.output_path = str(output_path)
            result.word_count = actual_wc
            log.info(f"    ✓ Saved: {output_path} ({actual_wc} words)")
            break

        except anthropic.RateLimitError as e:
            log.warning(f"    Attempt {attempt}: rate limited — waiting 30s: {e}")
            time.sleep(30)
        except anthropic.APIStatusError as e:
            log.error(f"    Attempt {attempt}: API error {e.status_code}: {e.message}")
            result.error = f"API error {e.status_code}: {e.message}"
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)
        except Exception as e:
            log.error(f"    Attempt {attempt}: unexpected error: {e}")
            result.error = str(e)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SECONDS)

    if not result.success and not result.error:
        result.error = "Max retries reached without valid output"

    return result


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(
    topic_queue_path: str = "topic_queue.json",
    guides_dir: Path = Path("content/guides"),
    drafts_dir: Path = DRAFTS_DIR,
    output_report_path: str = "generation_report.json",
) -> list:
    """
    Full guide generation pipeline. Returns list of GenerationResult dicts.
    """
    log.info("─" * 60)
    log.info("guide_generator.py — ZX Cloud Security")
    log.info("─" * 60)

    # 1. Load topic queue
    p = Path(topic_queue_path)
    if not p.exists():
        log.error(f"Topic queue not found: {topic_queue_path} — run topic_scorer.py first")
        return []

    with open(p) as f:
        queue_data = json.load(f)

    topics = queue_data.get("topics", [])
    if not topics:
        log.warning("Topic queue is empty — nothing to generate")
        return []

    log.info(f"[1/3] Loaded {len(topics)} topic(s) from {topic_queue_path}")

    # 2. Load existing guide slugs for internal linking hints
    log.info("[2/3] Loading existing guide index ...")
    existing_slugs = _load_existing_slugs(guides_dir)
    log.info(f"  → {len(existing_slugs)} existing guide slugs loaded")

    # 3. Initialise API client (reads ANTHROPIC_API_KEY from environment)
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY environment variable not set")
        return []

    client = anthropic.Anthropic(api_key=api_key)

    # 4. Generate each guide
    log.info(f"[3/3] Generating {len(topics)} guide(s) ...")
    results: list = []
    for i, topic in enumerate(topics, 1):
        log.info(f"\n  Topic {i}/{len(topics)}: {topic['label']}")
        result = generate_guide(
            client=client,
            topic=topic,
            existing_slugs=existing_slugs,
            drafts_dir=drafts_dir,
        )
        results.append(result)
        # Courtesy pause between guides to avoid burst rate limiting
        if i < len(topics):
            time.sleep(3)

    # 5. Save generation report
    _save_report(results, output_report_path)

    # Summary
    successes = sum(1 for r in results if r.success)
    failures = len(results) - successes
    log.info(f"\n{'─'*60}")
    log.info(f"  Generated: {successes}/{len(results)} guides")
    if failures:
        log.warning(f"  Failed:    {failures} guide(s) — see {output_report_path}")
    log.info(f"  Report:    {output_report_path}")
    log.info(f"{'─'*60}")

    return results


def _save_report(results: list, path: str) -> None:
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "succeeded": sum(1 for r in results if r.success),
        "failed": sum(1 for r in results if not r.success),
        "guides": [asdict(r) for r in results],
    }
    with open(path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    log.info(f"  Saved generation report → {path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ZX Cloud Security — Guide Generator")
    parser.add_argument("--topic-queue",   default="topic_queue.json",   help="Path to topic_scorer.py output")
    parser.add_argument("--guides-dir",    default="content/guides",     help="Path to existing Hugo guides (for internal link hints)")
    parser.add_argument("--drafts-dir",    default="drafts/guides",      help="Output directory for generated drafts")
    parser.add_argument("--report",        default="generation_report.json", help="Output path for generation report")
    args = parser.parse_args()

    results = run(
        topic_queue_path=args.topic_queue,
        guides_dir=Path(args.guides_dir),
        drafts_dir=Path(args.drafts_dir),
        output_report_path=args.report,
    )

    print(f"\n{'─'*60}")
    for r in results:
        status = "✓" if r.success else "✗"
        print(f"  {status} [{r.tier}] {r.topic_label}")
        if r.success:
            print(f"      {r.output_path} ({r.word_count} words, {r.attempts} attempt(s))")
        else:
            print(f"      FAILED: {r.error}")
    print(f"{'─'*60}\n")
