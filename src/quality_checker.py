"""
quality_checker.py
ZX Cloud Security — Guide Quality Checker

Validates humanised guide drafts from drafts/guides/ against a suite of
structural, SEO, and content checks. Produces a quality score (0–100) per
guide and a final quality_report.json consumed by publisher.py / the SES
email digest.

Scoring:
    Frontmatter completeness   20 pts
    Word count                 20 pts
    Heading structure          15 pts
    Keyword presence           20 pts
    Code examples              10 pts
    Duplicate content          15 pts
    ─────────────────────────  ────
    Total                     100 pts

Outcomes:
    score >= 60  → pass (included in email digest)
    score 40–59  → flagged (included in email digest with prominent warning)
    score < 40   → auto-reject (removed from queue; generator retries once)
"""

import json
import logging
import re
from collections import Counter
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORD_COUNT_MINIMUMS = {
    "pillar":     3000,
    "supporting": 1200,
}

REQUIRED_FRONTMATTER_FIELDS = [
    "title", "date", "description", "tags", "slug", "author", "word_count",
]

# Score thresholds
PASS_THRESHOLD   = 60
REJECT_THRESHOLD = 40

# Duplicate content: max allowed Jaccard similarity vs any existing guide
MAX_DUPLICATE_SIMILARITY = 0.20

# N-gram size for duplicate detection
NGRAM_SIZE = 4

# Max description length for SEO
META_DESC_MIN = 100
META_DESC_MAX = 160

# ---------------------------------------------------------------------------
# Scoring weights (must sum to 100)
# ---------------------------------------------------------------------------

WEIGHTS = {
    "frontmatter":  20,
    "word_count":   20,
    "headings":     15,
    "keyword":      20,
    "code":         10,
    "duplicate":    15,
}

assert sum(WEIGHTS.values()) == 100, "Scoring weights must sum to 100"

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    name: str
    passed: bool
    score: int          # Points earned for this check
    max_score: int      # Maximum possible points for this check
    detail: str = ""    # Human-readable detail for email digest


@dataclass
class QualityReport:
    slug: str
    topic_label: str
    tier: str
    draft_path: str
    total_score: int
    outcome: str        # "pass" | "flag" | "reject"
    checks: list = field(default_factory=list)
    flags: list = field(default_factory=list)
    word_count: int = 0
    title: str = ""
    description: str = ""
    checked_at: str = ""
    most_similar_guide: str = ""
    similarity_score: float = 0.0


# ---------------------------------------------------------------------------
# Markdown parsing helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter into a dict. Returns {} on failure."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    fm: dict = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip().strip("\"'")
    return fm


def _strip_frontmatter(content: str) -> str:
    return re.sub(r"^---\n.*?\n---\n?", "", content, flags=re.DOTALL)


def _strip_code_blocks(content: str) -> str:
    return re.sub(r"```.*?```", "", content, flags=re.DOTALL)


def _strip_comments(content: str) -> str:
    return re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)


def _prose_only(content: str) -> str:
    """Return just the prose: no frontmatter, code blocks, or comments."""
    text = _strip_frontmatter(content)
    text = _strip_code_blocks(text)
    text = _strip_comments(text)
    return text


def _count_words(content: str) -> int:
    return len(_prose_only(content).split())


def _get_headings(content: str) -> list:
    """Return list of (level, text) tuples for all ATX headings."""
    body = _strip_frontmatter(content)
    body = _strip_code_blocks(body)
    return [
        (len(m.group(1)), m.group(2).strip())
        for m in re.finditer(r"^(#{1,6})\s+(.+)$", body, re.MULTILINE)
    ]


def _get_first_n_words(content: str, n: int = 200) -> str:
    prose = _prose_only(content)
    return " ".join(prose.split()[:n]).lower()


def _count_code_blocks(content: str) -> int:
    return len(re.findall(r"```", _strip_frontmatter(content))) // 2


def _ngrams(text: str, n: int = NGRAM_SIZE) -> set:
    words = re.sub(r"[^\w\s]", "", text.lower()).split()
    return set(zip(*[words[i:] for i in range(n)]))


def _jaccard_similarity(set_a: set, set_b: set) -> float:
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_frontmatter(content: str, fm: dict) -> CheckResult:
    """20 pts: all required fields present and non-empty."""
    missing = [f for f in REQUIRED_FRONTMATTER_FIELDS if not fm.get(f)]
    extra_checks = []

    # Description length
    desc = fm.get("description", "")
    if desc and not (META_DESC_MIN <= len(desc) <= META_DESC_MAX):
        extra_checks.append(
            f"description is {len(desc)} chars (target {META_DESC_MIN}–{META_DESC_MAX})"
        )

    # Tags present and is a list-like value
    tags_raw = fm.get("tags", "")
    if tags_raw and not (tags_raw.startswith("[") or "\n-" in tags_raw):
        extra_checks.append("tags field may not be a list")

    if missing:
        detail = f"Missing fields: {', '.join(missing)}"
        if extra_checks:
            detail += f". Also: {'; '.join(extra_checks)}"
        return CheckResult("frontmatter", False, 0, WEIGHTS["frontmatter"], detail)

    if extra_checks:
        # Partial credit — fields present but some issues
        partial = WEIGHTS["frontmatter"] // 2
        return CheckResult(
            "frontmatter", False, partial, WEIGHTS["frontmatter"],
            "; ".join(extra_checks),
        )

    return CheckResult("frontmatter", True, WEIGHTS["frontmatter"], WEIGHTS["frontmatter"], "All fields present")


def check_word_count(content: str, tier: str) -> tuple:
    """20 pts: meets tier minimum word count."""
    minimum = WORD_COUNT_MINIMUMS.get(tier, 1200)
    actual = _count_words(content)
    if actual >= minimum:
        score = WEIGHTS["word_count"]
        detail = f"{actual} words (minimum {minimum})"
        passed = True
    elif actual >= minimum * 0.85:
        # Within 15% of minimum — partial credit
        score = WEIGHTS["word_count"] // 2
        detail = f"{actual} words — below minimum {minimum} (within 15%)"
        passed = False
    else:
        score = 0
        detail = f"{actual} words — below minimum {minimum}"
        passed = False
    return CheckResult("word_count", passed, score, WEIGHTS["word_count"], detail), actual


def check_headings(content: str) -> CheckResult:
    """15 pts: H1 present + at least 3 H2s."""
    headings = _get_headings(content)
    h1s = [h for h in headings if h[0] == 1]
    h2s = [h for h in headings if h[0] == 2]

    issues = []
    score = WEIGHTS["headings"]

    if not h1s:
        issues.append("No H1 found")
        score -= 8
    elif len(h1s) > 1:
        issues.append(f"{len(h1s)} H1s found (should be exactly 1)")
        score -= 4

    if len(h2s) < 3:
        issues.append(f"Only {len(h2s)} H2(s) found (minimum 3)")
        score -= 7

    score = max(0, score)
    passed = score == WEIGHTS["headings"]
    detail = "H1 present, {} H2s".format(len(h2s)) if passed else "; ".join(issues)
    return CheckResult("headings", passed, score, WEIGHTS["headings"], detail)


def check_keyword(content: str, fm: dict) -> CheckResult:
    """
    20 pts: target keyword present in title and first 200 words of prose.
    Keyword is derived from the frontmatter title (lowercased, stripped of
    stop words) — same logic as guide_generator.py's _derive_target_keyword.
    """
    title = fm.get("title", "").lower()
    description = fm.get("description", "").lower()

    # Derive keyword: longest 2–4 word phrase from title that isn't all stop words
    STOP = {"a", "an", "the", "and", "or", "for", "to", "in", "on", "of",
            "with", "best", "guide", "how", "your", "using", "complete"}
    title_words = [w for w in re.sub(r"[^\w\s]", "", title).split() if w not in STOP]
    # Use first 3 content words as keyword
    keyword = " ".join(title_words[:3]) if title_words else title[:30]

    first_200 = _get_first_n_words(content, 200)
    score = 0
    issues = []

    # Keyword in title
    if keyword and keyword in title:
        score += 8
    else:
        issues.append(f"Keyword '{keyword}' not in title")

    # Keyword in first 200 words
    if keyword and keyword in first_200:
        score += 8
    else:
        issues.append(f"Keyword '{keyword}' not in first 200 words")

    # Keyword in meta description
    if keyword and keyword in description:
        score += 4
    else:
        issues.append(f"Keyword '{keyword}' not in meta description")

    score = min(score, WEIGHTS["keyword"])
    passed = score == WEIGHTS["keyword"]
    detail = f"Keyword: '{keyword}'" if passed else f"Keyword: '{keyword}' — {'; '.join(issues)}"
    return CheckResult("keyword", passed, score, WEIGHTS["keyword"], detail)


def check_code_examples(content: str, tier: str) -> CheckResult:
    """10 pts: pillar guides need ≥ 1 code block; supporting guides get full marks regardless."""
    count = _count_code_blocks(content)
    if tier == "supporting":
        return CheckResult(
            "code", True, WEIGHTS["code"], WEIGHTS["code"],
            f"{count} code block(s) (not required for supporting guides)",
        )
    # Pillar guide
    if count >= 3:
        score = WEIGHTS["code"]
        detail = f"{count} code blocks"
        passed = True
    elif count >= 1:
        score = WEIGHTS["code"] // 2
        detail = f"{count} code block(s) — pillar guides should have ≥ 3"
        passed = False
    else:
        score = 0
        detail = "No code blocks found (pillar guides require ≥ 1)"
        passed = False
    return CheckResult("code", passed, score, WEIGHTS["code"], detail)


def check_duplicate(
    content: str,
    slug: str,
    existing_guides_dir: Path,
) -> tuple:
    """
    15 pts: < 20% n-gram overlap with any existing published guide.
    Returns (CheckResult, most_similar_slug, similarity_score).
    """
    prose = _prose_only(content)
    candidate_ngrams = _ngrams(prose)

    if not candidate_ngrams:
        return (
            CheckResult("duplicate", True, WEIGHTS["duplicate"], WEIGHTS["duplicate"], "No existing guides to compare"),
            "", 0.0,
        )

    if not existing_guides_dir.exists():
        return (
            CheckResult("duplicate", True, WEIGHTS["duplicate"], WEIGHTS["duplicate"], "No existing guides directory"),
            "", 0.0,
        )

    worst_similarity = 0.0
    worst_slug = ""

    for guide_file in existing_guides_dir.glob("**/*.md"):
        if guide_file.stem == slug:
            continue  # Don't compare against itself
        try:
            existing_prose = _prose_only(guide_file.read_text(encoding="utf-8", errors="ignore"))
            existing_ngrams = _ngrams(existing_prose)
            sim = _jaccard_similarity(candidate_ngrams, existing_ngrams)
            if sim > worst_similarity:
                worst_similarity = sim
                worst_slug = guide_file.stem
        except Exception:
            continue

    passed = worst_similarity < MAX_DUPLICATE_SIMILARITY
    if passed:
        score = WEIGHTS["duplicate"]
        detail = f"Max similarity {worst_similarity:.1%} vs '{worst_slug}'" if worst_slug else "No overlap detected"
    elif worst_similarity < MAX_DUPLICATE_SIMILARITY * 1.5:
        # Borderline — partial credit
        score = WEIGHTS["duplicate"] // 2
        detail = f"Similarity {worst_similarity:.1%} vs '{worst_slug}' — borderline (threshold {MAX_DUPLICATE_SIMILARITY:.0%})"
    else:
        score = 0
        detail = f"Similarity {worst_similarity:.1%} vs '{worst_slug}' — exceeds {MAX_DUPLICATE_SIMILARITY:.0%} threshold"

    return (
        CheckResult("duplicate", passed, score, WEIGHTS["duplicate"], detail),
        worst_slug,
        worst_similarity,
    )


# ---------------------------------------------------------------------------
# Main quality check for a single guide
# ---------------------------------------------------------------------------

def check_guide(
    draft_path: Path,
    topic_label: str,
    tier: str,
    existing_guides_dir: Path = Path("content/guides"),
) -> QualityReport:
    """Run all checks on a single draft guide and return a QualityReport."""
    slug = draft_path.stem

    try:
        content = draft_path.read_text(encoding="utf-8")
    except Exception as e:
        log.error(f"  Cannot read {draft_path}: {e}")
        return QualityReport(
            slug=slug,
            topic_label=topic_label,
            tier=tier,
            draft_path=str(draft_path),
            total_score=0,
            outcome="reject",
            flags=[f"Cannot read file: {e}"],
            checked_at=datetime.now(timezone.utc).isoformat(),
        )

    fm = _parse_frontmatter(content)

    # Run all checks
    fm_check = check_frontmatter(content, fm)
    wc_check, actual_wc = check_word_count(content, tier)
    h_check = check_headings(content)
    kw_check = check_keyword(content, fm)
    code_check = check_code_examples(content, tier)
    dup_check, most_similar, similarity = check_duplicate(content, slug, existing_guides_dir)

    checks = [fm_check, wc_check, h_check, kw_check, code_check, dup_check]
    total_score = sum(c.score for c in checks)

    # Collect flags (failed checks)
    flags = [f"{c.name}: {c.detail}" for c in checks if not c.passed]

    # Determine outcome
    # Auto-reject overrides: missing frontmatter or duplicate content
    if not fm_check.passed and fm_check.score == 0:
        outcome = "reject"
        flags.insert(0, "AUTO-REJECT: frontmatter incomplete — will retry generation")
    elif not dup_check.passed and dup_check.score == 0:
        outcome = "reject"
        flags.insert(0, f"AUTO-REJECT: duplicate content ({similarity:.1%} overlap with '{most_similar}')")
    elif total_score < REJECT_THRESHOLD:
        outcome = "reject"
        flags.insert(0, f"AUTO-REJECT: score {total_score}/100 below threshold {REJECT_THRESHOLD}")
    elif total_score < PASS_THRESHOLD:
        outcome = "flag"
    else:
        outcome = "pass"

    report = QualityReport(
        slug=slug,
        topic_label=topic_label,
        tier=tier,
        draft_path=str(draft_path),
        total_score=total_score,
        outcome=outcome,
        checks=[asdict(c) for c in checks],
        flags=flags,
        word_count=actual_wc,
        title=fm.get("title", ""),
        description=fm.get("description", ""),
        checked_at=datetime.now(timezone.utc).isoformat(),
        most_similar_guide=most_similar,
        similarity_score=round(similarity, 4),
    )

    _log_result(report)
    return report


def _log_result(r: QualityReport) -> None:
    icon = {"pass": "✓", "flag": "⚠", "reject": "✗"}.get(r.outcome, "?")
    log.info(f"  {icon} [{r.outcome.upper():6s}] {r.total_score:3d}/100  {r.topic_label}")
    for flag in r.flags:
        log.warning(f"      ↳ {flag}")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(
    generation_report_path: str = "generation_report.json",
    existing_guides_dir: Path = Path("content/guides"),
    output_report_path: str = "quality_report.json",
) -> list:
    """
    Quality-check all humanised guides listed in the generation report.
    Returns list of QualityReport. Writes quality_report.json.
    """
    log.info("─" * 60)
    log.info("quality_checker.py — ZX Cloud Security")
    log.info("─" * 60)

    # Load generation report
    p = Path(generation_report_path)
    if not p.exists():
        log.error(f"Generation report not found: {generation_report_path}")
        return []

    with open(p) as f:
        report = json.load(f)

    guides = [g for g in report.get("guides", []) if g.get("success")]
    if not guides:
        log.warning("No successful guides in generation report — nothing to check")
        return []

    log.info(f"[1/2] Checking {len(guides)} guide(s) ...")
    results: list = []
    for i, guide in enumerate(guides, 1):
        draft_path = Path(guide.get("output_path", ""))
        topic_label = guide.get("topic_label", draft_path.stem)
        tier = guide.get("tier", "supporting")

        log.info(f"\n  Guide {i}/{len(guides)}: {topic_label}")

        if not draft_path.exists():
            log.warning(f"    Draft not found: {draft_path} — skipping")
            results.append(QualityReport(
                slug=draft_path.stem,
                topic_label=topic_label,
                tier=tier,
                draft_path=str(draft_path),
                total_score=0,
                outcome="reject",
                flags=["Draft file not found"],
                checked_at=datetime.now(timezone.utc).isoformat(),
            ))
            continue

        result = check_guide(
            draft_path=draft_path,
            topic_label=topic_label,
            tier=tier,
            existing_guides_dir=existing_guides_dir,
        )
        results.append(result)

    # Save quality report
    log.info(f"\n[2/2] Saving quality report ...")
    _save_report(results, output_report_path)

    # Summary
    passed  = sum(1 for r in results if r.outcome == "pass")
    flagged = sum(1 for r in results if r.outcome == "flag")
    rejected = sum(1 for r in results if r.outcome == "reject")
    log.info(f"\n{'─'*60}")
    log.info(f"  Pass:    {passed}")
    log.info(f"  Flag:    {flagged}")
    log.info(f"  Reject:  {rejected}")
    log.info(f"  Report:  {output_report_path}")
    log.info(f"{'─'*60}")

    return results


def _save_report(results: list, path: str) -> None:
    output = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "passed": sum(1 for r in results if r.outcome == "pass"),
        "flagged": sum(1 for r in results if r.outcome == "flag"),
        "rejected": sum(1 for r in results if r.outcome == "reject"),
        "guides": [asdict(r) for r in results],
    }
    with open(path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info(f"  Saved → {path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ZX Cloud Security — Quality Checker")
    parser.add_argument("--report",      default="generation_report.json", help="Path to generation_report.json")
    parser.add_argument("--guides-dir",  default="content/guides",         help="Existing published guides directory")
    parser.add_argument("--output",      default="quality_report.json",    help="Output quality report path")
    args = parser.parse_args()

    results = run(
        generation_report_path=args.report,
        existing_guides_dir=Path(args.guides_dir),
        output_report_path=args.output,
    )

    print(f"\n{'─'*60}")
    for r in results:
        icon = {"pass": "✓", "flag": "⚠", "reject": "✗"}.get(r.outcome, "?")
        print(f"  {icon} [{r.outcome.upper():6s}] {r.total_score:3d}/100  {r.topic_label}")
        for flag in r.flags:
            print(f"      ↳ {flag}")
    print(f"{'─'*60}\n")
