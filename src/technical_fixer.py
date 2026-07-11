"""
technical_fixer.py
ZX Cloud Security — Technical Accuracy Auto-Fix

Takes guides flagged with technical inaccuracies by technical_reviewer.py and
asks Claude to correct them in the draft file itself, then re-reviews (reusing
technical_reviewer.review_guide) to confirm the fix actually worked before
moving on. Guides that still have unresolved findings after MAX_FIX_ATTEMPTS
are left with those findings intact in quality_report.json, so the digest
email still surfaces them — this only removes the manual work Claude can do
reliably; it never hides a problem it couldn't fix.

Must run after technical_reviewer.py and before publisher.py.

Reads/writes: quality_report.json (updates "technical_review" and "word_count"
per guide)
"""

import json
import logging
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import anthropic

from technical_reviewer import review_guide

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

MODEL = "claude-fable-5"
FALLBACK_MODEL = "claude-opus-4-8"
MAX_TOKENS = 16000
MAX_FIX_ATTEMPTS = 2
RETRY_DELAY_SECONDS = 5

FIXER_SYSTEM_PROMPT = """You are a senior cloud security editor fixing factual errors in a \
security guide for zxcloudsecurity.co.uk, published under Steve Harrison's byline.

You will be given the full guide (Hugo markdown) and a list of specific technical findings \
from an independent accuracy review. Fix ONLY the issues described in those findings. Do \
not rewrite, restructure, or "improve" anything else — the prose voice, tone, and structure \
have already been finalised and must survive untouched.

CRITICAL CONSTRAINTS:
- Preserve the YAML frontmatter block exactly (between --- delimiters), except correcting a \
field if a finding specifically concerns it
- Preserve all code blocks exactly (between ``` fences) unless a finding specifically \
concerns the code inside one
- Preserve all HTML comments (<!-- INTERNAL_LINK: ... -->) and Hugo shortcodes exactly
- Do not touch any sentence, paragraph, or section that isn't implicated by a finding
- Use web search to verify the correct fact before writing a replacement — never swap one \
unverified claim for another. If you cannot verify a correction with confidence, remove or \
soften the unverifiable claim rather than inventing a replacement fact.
- Do not add a note, disclaimer, or comment about what you changed — the fix must read as \
though it was correct from the start

OUTPUT: Return only the complete corrected markdown file. No preamble, no explanation, no \
commentary. Start with --- and end with the last line of content."""


def _build_fixer_user_prompt(content: str, findings: list) -> str:
    findings_text = "\n".join(
        f"- [{f.get('severity', 'minor').upper()}] {f.get('description', '')}"
        for f in findings
    )
    return f"""Fix the following technical findings in this guide. Do not change anything else.

FINDINGS:
{findings_text}

GUIDE:
{content}"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _count_words(text: str) -> int:
    """Word count excluding frontmatter and code blocks."""
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    return len(body.split())


def _patch_word_count(text: str, actual_count: int) -> str:
    """Update the word_count frontmatter field to match actual count."""
    return re.sub(
        r"(^word_count:\s*)\d+",
        f"\\g<1>{actual_count}",
        text,
        flags=re.MULTILINE,
    )


def _strip_preamble(text: str) -> str:
    """Web search can cause stray preamble text despite the system prompt — drop
    anything before the frontmatter delimiter, mirroring guide_generator.py."""
    fm_start = text.find("---")
    if fm_start > 0:
        return text[fm_start:]
    return text


def _validate_fixed_output(original: str, fixed: str) -> tuple:
    """
    Check the fixed output looks sane before saving. Returns (is_valid, reason).
    """
    if not fixed.strip():
        return False, "Empty response from API"

    if not fixed.strip().startswith("---"):
        return False, "Frontmatter missing from fixed output"

    for field in ("title:", "slug:", "author:", "date:"):
        if field not in fixed:
            return False, f"Frontmatter field '{field}' missing from fixed output"

    original_words = len(original.split())
    fixed_words = len(fixed.split())
    if fixed_words < original_words * 0.70:
        return False, (
            f"Fixed output is too short ({fixed_words} words vs "
            f"{original_words} original) — possible content loss"
        )

    return True, ""


# ---------------------------------------------------------------------------
# Single guide fix
# ---------------------------------------------------------------------------

@dataclass
class FixResult:
    slug: str
    title: str
    attempted: bool = False
    auto_fix_applied: bool = False
    fully_resolved: bool = False
    attempts: int = 0
    findings_before: int = 0
    findings_after: int = 0
    fixed_count: int = 0
    word_count: int = 0
    error: str = ""
    fixed_at: str = ""


def _call_fixer(client: anthropic.Anthropic, content: str, findings: list) -> str:
    """One fixer API call. Returns extracted, preamble-stripped text (may be empty)."""
    user_prompt = _build_fixer_user_prompt(content, findings)
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=FIXER_SYSTEM_PROMPT,
        betas=["server-side-fallback-2026-06-01"],
        fallbacks=[{"model": FALLBACK_MODEL}],
        tools=[{"type": "web_search_20260209", "name": "web_search"}],
        messages=[{"role": "user", "content": user_prompt}],
    )

    if response.stop_reason == "refusal":
        log.warning("    Fix declined by safety classifiers")
        return ""

    text_parts = [
        block.text for block in response.content
        if hasattr(block, "text") and block.text
    ]
    fixed = "\n".join(text_parts).strip()
    return _strip_preamble(fixed)


def fix_guide(
    client: anthropic.Anthropic,
    draft_path: Path,
    title: str,
    technical_review: dict,
) -> tuple:
    """
    Attempt to fix the findings in technical_review against draft_path, re-verifying
    after each attempt. Overwrites draft_path in place on any successful fix.
    Returns (FixResult, updated_technical_review_dict).
    """
    slug = draft_path.stem
    result = FixResult(slug=slug, title=title, fixed_at=_now_utc())

    result.findings_before = len(technical_review.get("findings", []))

    try:
        content = draft_path.read_text(encoding="utf-8")
    except Exception as e:
        result.error = f"Could not read draft file: {e}"
        log.error(f"  {slug}: {result.error}")
        return result, technical_review

    result.attempted = True
    current_review = technical_review
    fixed_any = False

    for attempt in range(1, MAX_FIX_ATTEMPTS + 1):
        result.attempts = attempt
        current_findings = current_review.get("findings", [])
        if not current_findings:
            break

        log.info(
            f"    Fix attempt {attempt}/{MAX_FIX_ATTEMPTS} — "
            f"{len(current_findings)} finding(s) ..."
        )

        try:
            fixed = _call_fixer(client, content, current_findings)
        except anthropic.RateLimitError as e:
            log.warning(f"    Attempt {attempt}: rate limited — waiting 30s: {e}")
            time.sleep(30)
            continue
        except anthropic.APIStatusError as e:
            log.error(f"    Attempt {attempt}: API error {e.status_code}: {e.message}")
            result.error = f"API error {e.status_code}: {e.message}"
            break
        except Exception as e:
            log.error(f"    Attempt {attempt}: unexpected error: {e}")
            result.error = str(e)
            break

        is_valid, reason = _validate_fixed_output(content, fixed)
        if not is_valid:
            log.warning(f"    Attempt {attempt}: {reason}")
            result.error = reason
            if attempt < MAX_FIX_ATTEMPTS:
                time.sleep(RETRY_DELAY_SECONDS)
            continue

        actual_wc = _count_words(fixed)
        fixed = _patch_word_count(fixed, actual_wc)

        # Verify the fix actually worked before trusting it
        log.info("    Re-reviewing to verify fix ...")
        verify_review = review_guide(client, fixed)

        # Save regardless — even a partial fix is progress, and the re-review
        # tells us exactly what (if anything) still needs attention
        draft_path.write_text(fixed, encoding="utf-8")
        content = fixed
        result.word_count = actual_wc
        fixed_any = True

        resolved_this_round = len(current_findings) - len(verify_review.get("findings", []))
        result.fixed_count += max(resolved_this_round, 0)
        current_review = verify_review

        if not verify_review.get("issues_found"):
            log.info(f"    ✓ All findings resolved after {attempt} attempt(s)")
            break

        log.warning(
            f"    {len(verify_review.get('findings', []))} finding(s) remain after "
            f"attempt {attempt}"
        )

    result.auto_fix_applied = fixed_any
    result.findings_after = len(current_review.get("findings", []))
    result.fully_resolved = fixed_any and not current_review.get("issues_found", True)

    current_review = dict(current_review)
    current_review["auto_fix_attempted"] = result.attempted
    current_review["auto_fix_applied"] = result.auto_fix_applied
    current_review["fixed_count"] = result.fixed_count

    return result, current_review


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(quality_report_path: str = "quality_report.json") -> list:
    log.info("─" * 60)
    log.info("technical_fixer.py — ZX Cloud Security")
    log.info("─" * 60)

    p = Path(quality_report_path)
    if not p.exists():
        log.error(f"Quality report not found: {quality_report_path} — run technical_reviewer.py first")
        return []

    with open(p) as f:
        data = json.load(f)

    guides = data.get("guides", [])
    candidates = [
        g for g in guides
        if g.get("outcome") in ("pass", "flag")
        and g.get("technical_review", {}).get("issues_found")
    ]

    if not candidates:
        log.info("No guides with flagged technical issues — nothing to fix")
        return []

    log.info(f"[1/1] Fixing {len(candidates)} guide(s) with flagged findings ...")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY environment variable not set")
        return []

    client = anthropic.Anthropic(api_key=api_key)

    results: list = []
    for i, guide in enumerate(candidates, 1):
        title = guide.get("title", guide.get("slug", ""))
        draft_path = Path(guide.get("draft_path", ""))
        log.info(f"\n  Guide {i}/{len(candidates)}: {title}")

        if not draft_path.exists():
            log.warning(f"    Draft file not found: {draft_path} — skipping")
            results.append(FixResult(
                slug=draft_path.stem,
                title=title,
                error="Draft file not found",
            ))
            continue

        result, updated_review = fix_guide(
            client, draft_path, title, guide.get("technical_review", {})
        )
        results.append(result)

        guide["technical_review"] = updated_review
        if result.auto_fix_applied:
            guide["word_count"] = result.word_count

        if i < len(candidates):
            time.sleep(3)

    with open(p, "w") as f:
        json.dump(data, f, indent=2, default=str)
    log.info(f"\n  Saved → {quality_report_path}")

    resolved = sum(1 for r in results if r.fully_resolved)
    partial = sum(1 for r in results if r.auto_fix_applied and not r.fully_resolved)
    failed = sum(1 for r in results if not r.auto_fix_applied)
    log.info(f"{'─'*60}")
    log.info(f"  Fully resolved: {resolved}  |  Partially fixed: {partial}  |  Unfixed: {failed}")
    log.info(f"{'─'*60}")

    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ZX Cloud Security — Technical Fixer")
    parser.add_argument(
        "--quality-report",
        default="quality_report.json",
        help="Path to quality_report.json from technical_reviewer.py",
    )
    args = parser.parse_args()

    results = run(quality_report_path=args.quality_report)

    print(f"\n{'-'*60}")
    for r in results:
        if r.fully_resolved:
            status = "OK"
        elif r.auto_fix_applied:
            status = "PARTIAL"
        else:
            status = "FAILED"
        print(f"  [{status}] {r.title}")
        if r.attempted:
            print(
                f"      {r.findings_before} -> {r.findings_after} finding(s) "
                f"({r.fixed_count} fixed, {r.attempts} attempt(s))"
            )
        if r.error:
            print(f"      {r.error}")
    print(f"{'-'*60}\n")
