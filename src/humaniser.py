"""
humaniser.py
ZX Cloud Security — Guide Humanisation Pipeline

Takes generated guide drafts from drafts/guides/, runs each through the
Claude API using the Humanizer v2.8.0 prompt (github.com/blader/humanizer)
to strip AI writing patterns, and overwrites the draft in place.

Must be run after guide_generator.py and before quality_checker.py.

Updates generation_report.json with humanisation results.
"""

import json
import logging
import os
import re
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

import anthropic

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 8000
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 5

# Steve's writing voice sample — used for voice calibration in the humaniser.
# Update this with real examples from Steve's own writing over time for
# progressively better voice matching.
VOICE_SAMPLE = """
Here's how I typically write about cloud security:

When AWS released IAM Identity Centre (previously SSO), most teams I spoke to
missed the real change: it's not just a portal, it's a shift in how you think
about access across accounts. The old way was to federate into each account
separately and manage permission sets per account. That works until you've got
fifty accounts and six teams and nobody's quite sure who approved what.

The truth is most GuardDuty deployments I review are running on defaults.
That's not necessarily wrong — the defaults catch a lot — but you're leaving
signal on the table. DNS exfiltration detection, for example, is off by default
in some regions. So is runtime monitoring for ECS. If you haven't reviewed your
threat intelligence feeds since you turned it on, you probably should.

SCP design is where I see the most cargo-culting. Teams copy an example from
the AWS docs, tweak a few ARNs, and call it done. The problem is those examples
are illustrative, not production-ready. They don't account for service-linked
roles, they don't handle the inevitable exception for your legacy workload in
us-east-1, and they'll definitely break your next Control Tower update.
"""


# ---------------------------------------------------------------------------
# Humanizer system prompt — based on blader/humanizer SKILL.md v2.8.0
# ---------------------------------------------------------------------------

HUMANIZER_SYSTEM_PROMPT = """You are a senior writing editor specialising in technical cloud security content.
Your task is to remove signs of AI-generated writing from text, making it sound natural and human.
You are working on guides written for zxcloudsecurity.co.uk, authored by Steve Harrison,
a Principal Security Architect with 15 years of AWS and cloud security experience.

CRITICAL CONSTRAINT: The input is a Hugo markdown file. You must:
- Preserve the YAML frontmatter block exactly (between --- delimiters) — do not modify it
- Preserve all code blocks exactly (between ``` fences) — do not rewrite code
- Preserve all HTML comments (<!-- INTERNAL_LINK: ... -->) exactly
- Preserve all Hugo shortcodes exactly
- Only rewrite prose content

OUTPUT: Return only the complete rewritten markdown file. No preamble, no explanation,
no commentary about what you changed. Start with --- and end with the last line of content.


## VOICE CALIBRATION

Match Steve Harrison's writing voice. He writes:
- Direct and opinionated — he has views based on real production experience
- UK English (organisation, authorisation, colour, centre, recognised)
- Short punchy sentences mixed with longer technical ones
- Occasional first-person when sharing a real-world observation
- Honest about trade-offs — no pretending everything has a clean answer
- References specific AWS service behaviour, not vague generalisations
- Doesn't use exclamation marks. Ever.


## 33 PATTERNS TO FIX

### Content patterns
1. SIGNIFICANCE INFLATION — remove "marking a pivotal moment", "serves as a testament",
   "underscores its importance", "reflects broader trends", "setting the stage for"
2. NOTABILITY NAME-DROPPING — remove lists of media outlets; cite specific articles instead
3. SUPERFICIAL -ING ANALYSES — remove trailing "-ing" phrases that add fake depth:
   "highlighting...", "showcasing...", "reflecting...", "fostering...", "ensuring..."
4. PROMOTIONAL LANGUAGE — remove "nestled", "breathtaking", "vibrant", "groundbreaking",
   "renowned", "boasts", "stunning", "must-visit"
5. VAGUE ATTRIBUTIONS — remove "experts believe", "industry observers note", "some argue";
   replace with specific sources or remove
6. FORMULAIC CHALLENGES SECTIONS — replace generic "Despite challenges... continues to thrive"
   with specific facts

### Language patterns
7. AI VOCABULARY — remove or replace: "actually", "additionally", "align with", "crucial",
   "delve", "emphasizing", "enduring", "enhance", "fostering", "garner", "highlight" (verb),
   "interplay", "intricate/intricacies", "key" (adjective), "landscape" (abstract),
   "pivotal", "showcase", "tapestry", "testament", "underscore" (verb), "valuable", "vibrant"
8. COPULA AVOIDANCE — replace "serves as", "stands as", "features", "boasts" with "is"/"has"
9. NEGATIVE PARALLELISMS — remove "It's not just X, it's Y" constructions and tailing
   negations like "no guessing", "no wasted motion" tacked onto sentence ends
10. RULE OF THREE — break forced triads; use natural number of items
11. SYNONYM CYCLING — stop switching between synonyms for the same concept; pick one and repeat
12. FALSE RANGES — remove "from X to Y" where X and Y aren't on a meaningful scale
13. PASSIVE VOICE / SUBJECTLESS FRAGMENTS — name the actor; avoid "No configuration needed"

### Style patterns
14. EM DASHES — HARD RULE: zero em dashes (—) or en dashes (–) or spaced versions ( — )
    or double hyphens ( -- ) in the final output. Replace with: period, comma, colon,
    or parentheses. Scan the output before finishing — any hit means the draft isn't done.
15. BOLDFACE OVERUSE — remove bold from inline terms; keep bold only in table headers
    and genuine UI element names
16. INLINE-HEADER LISTS — convert "**Label:** description" bullet lists to prose
17. TITLE CASE HEADINGS — use sentence case: "AWS SCP best practices" not
    "AWS SCP Best Practices" (proper nouns and acronyms remain capitalised)
18. EMOJIS — remove all emojis from headings and bullet points
19. CURLY QUOTES — replace "smart quotes" with straight "quotes"

### Communication patterns
20. CHATBOT ARTIFACTS — remove "I hope this helps", "Let me know if", "Want me to",
    "Here is a...", "Of course!", "Certainly!"
21. KNOWLEDGE-CUTOFF DISCLAIMERS — remove "as of my last update", "while details are limited",
    "based on available information"; find the fact or cut the sentence
22. SYCOPHANTIC TONE — remove "Great question!", "You're absolutely right!", excessive positivity

### Filler and hedging
23. FILLER PHRASES — replace: "In order to" → "To", "Due to the fact that" → "Because",
    "At this point in time" → "Now", "has the ability to" → "can",
    "It is important to note that" → remove entirely
24. EXCESSIVE HEDGING — replace "could potentially possibly" with "may"; one qualifier maximum
25. GENERIC POSITIVE CONCLUSIONS — replace "The future looks bright" with a specific fact
    or concrete next step
26. HYPHENATED WORD PAIRS — drop hyphens in predicate position:
    "the team is cross functional", "the report is high quality"
    Keep them in attributive position: "a cross-functional team", "a high-quality report"
27. PERSUASIVE AUTHORITY TROPES — remove "at its core", "the real question is",
    "what really matters", "fundamentally", "the heart of the matter"
28. SIGNPOSTING — remove "Let's dive in", "let's explore", "here's what you need to know",
    "without further ado"; just start the content
29. FRAGMENTED HEADERS — remove generic warm-up sentences after headings that just
    restate the heading before the real content begins
30. DIFF-ANCHORED WRITING — describe things as they are, not as what changed:
    replace "This was added to replace..." with "This does X because..."
31. MANUFACTURED STACCATO DRAMA — break up runs of short emphatic fragments that
    feel engineered; one short sentence for emphasis is fine, three in a row is AI
32. APHORISM FORMULAS — replace "X is the Y of Z" and "X becomes a trap" with the
    concrete claim they're gesturing at
33. CONVERSATIONAL RHETORICAL OPENERS — remove standalone "Honestly?", "Look,",
    "Here's the thing," as theatrical openers; just say the thing


## PROCESS

1. Read the markdown, identifying the frontmatter, code blocks, and comments to preserve
2. Write a draft rewrite of the prose content only
3. Check: "What still makes this obviously AI-generated?" — note any remaining tells
4. Produce a final rewrite that addresses them, with zero em dashes
5. Return the complete markdown file (frontmatter + prose + code blocks, all in place)"""


def _build_humaniser_user_prompt(content: str, topic_label: str) -> str:
    return f"""Humanise the following cloud security guide for zxcloudsecurity.co.uk.
Topic: {topic_label}

Voice calibration sample (Steve Harrison's writing style):
{VOICE_SAMPLE}

Now humanise this guide. Return only the complete rewritten markdown file:

{content}"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _extract_frontmatter_raw(content: str) -> tuple:
    """
    Split content into (frontmatter_block, body).
    frontmatter_block includes the --- delimiters.
    Returns ("", content) if no frontmatter found.
    """
    match = re.match(r"^(---\n.*?\n---\n?)", content, re.DOTALL)
    if match:
        fm = match.group(1)
        body = content[len(fm):]
        return fm, body
    return "", content


def _validate_humanised_output(original: str, humanised: str) -> tuple:
    """
    Check the humanised output looks sane before saving.
    Returns (is_valid, reason).
    """
    if not humanised.strip():
        return False, "Empty response from API"

    if not humanised.strip().startswith("---"):
        return False, "Frontmatter missing from humanised output"

    # Check frontmatter fields survived
    for field in ("title:", "slug:", "author:", "date:"):
        if field not in humanised:
            return False, f"Frontmatter field '{field}' missing from humanised output"

    # Check we haven't lost too much content (allow up to 30% word count reduction)
    original_words = len(original.split())
    humanised_words = len(humanised.split())
    if humanised_words < original_words * 0.70:
        return False, (
            f"Humanised output is too short ({humanised_words} words vs "
            f"{original_words} original) — possible content loss"
        )

    return True, ""


def _count_remaining_ai_tells(text: str) -> list:
    """Quick scan for obvious remaining AI patterns — logged as a warning."""
    tells = []
    body = re.sub(r"^---\n.*?\n---\n?", "", text, flags=re.DOTALL)
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)

    EM_DASH_RE = re.compile(r"[—–]| -- | --- ")
    if EM_DASH_RE.search(body):
        tells.append("em/en dash still present")

    AI_WORDS = [
        "delve", "tapestry", "testament", "pivotal", "underscore",
        "showcase", "fostering", "intricate", "garnered", "vibrant",
        "Let's dive in", "Here's what you need to know",
    ]
    for word in AI_WORDS:
        if word.lower() in body.lower():
            tells.append(f"AI vocabulary: '{word}'")

    return tells


# ---------------------------------------------------------------------------
# Single guide humanisation
# ---------------------------------------------------------------------------

@dataclass
class HumanisationResult:
    slug: str
    topic_label: str
    success: bool
    input_path: str
    output_path: str = ""
    original_word_count: int = 0
    humanised_word_count: int = 0
    remaining_tells: list = None
    error: str = ""
    attempts: int = 0
    humanised_at: str = ""

    def __post_init__(self):
        if self.remaining_tells is None:
            self.remaining_tells = []


def humanise_guide(
    client: anthropic.Anthropic,
    draft_path: Path,
    topic_label: str,
) -> HumanisationResult:
    """
    Humanise a single draft guide. Overwrites the file in place on success.
    """
    slug = draft_path.stem
    result = HumanisationResult(
        slug=slug,
        topic_label=topic_label,
        success=False,
        input_path=str(draft_path),
        humanised_at=_now_utc(),
    )

    try:
        original_content = draft_path.read_text(encoding="utf-8")
    except Exception as e:
        result.error = f"Could not read draft file: {e}"
        log.error(f"  {slug}: {result.error}")
        return result

    result.original_word_count = len(original_content.split())
    log.info(f"  Humanising: {topic_label} ({result.original_word_count} words)")

    user_prompt = _build_humaniser_user_prompt(original_content, topic_label)

    for attempt in range(1, MAX_RETRIES + 1):
        result.attempts = attempt
        try:
            log.info(f"    API call attempt {attempt}/{MAX_RETRIES} ...")
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=HUMANIZER_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_prompt}],
            )

            # Collect all text blocks
            text_parts = [
                block.text
                for block in response.content
                if hasattr(block, "text") and block.text
            ]
            humanised = "\n".join(text_parts).strip()

            is_valid, reason = _validate_humanised_output(original_content, humanised)
            if not is_valid:
                log.warning(f"    Attempt {attempt}: {reason}")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY_SECONDS)
                continue

            # Scan for remaining tells — log but don't fail
            tells = _count_remaining_ai_tells(humanised)
            if tells:
                log.warning(f"    Remaining AI tells ({len(tells)}): {', '.join(tells)}")

            # Overwrite draft in place
            draft_path.write_text(humanised, encoding="utf-8")

            result.success = True
            result.output_path = str(draft_path)
            result.humanised_word_count = len(humanised.split())
            result.remaining_tells = tells
            log.info(
                f"    ✓ Humanised: {draft_path.name} "
                f"({result.original_word_count} → {result.humanised_word_count} words)"
            )
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
    generation_report_path: str = "generation_report.json",
    drafts_dir: Path = Path("drafts/guides"),
    output_report_path: str = "generation_report.json",
) -> list:
    """
    Humanise all successfully generated guides listed in the generation report.
    Updates generation_report.json with humanisation results in place.
    Returns list of HumanisationResult.
    """
    log.info("─" * 60)
    log.info("humaniser.py — ZX Cloud Security")
    log.info("─" * 60)

    # Load generation report to know which drafts to process
    p = Path(generation_report_path)
    if not p.exists():
        log.error(f"Generation report not found: {generation_report_path} — run guide_generator.py first")
        return []

    with open(p) as f:
        report = json.load(f)

    guides = [g for g in report.get("guides", []) if g.get("success")]
    if not guides:
        log.warning("No successfully generated guides in report — nothing to humanise")
        return []

    log.info(f"[1/3] Found {len(guides)} guide(s) to humanise")

    # Initialise API client
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY environment variable not set")
        return []

    client = anthropic.Anthropic(api_key=api_key)

    # Humanise each guide
    log.info("[2/3] Humanising guides ...")
    results: list = []
    for i, guide in enumerate(guides, 1):
        draft_path = Path(guide.get("output_path", ""))
        topic_label = guide.get("topic_label", draft_path.stem)

        log.info(f"\n  Guide {i}/{len(guides)}: {topic_label}")

        if not draft_path.exists():
            log.warning(f"    Draft file not found: {draft_path} — skipping")
            results.append(HumanisationResult(
                slug=draft_path.stem,
                topic_label=topic_label,
                success=False,
                input_path=str(draft_path),
                error="Draft file not found",
            ))
            continue

        result = humanise_guide(client, draft_path, topic_label)
        results.append(result)

        # Courtesy pause between guides
        if i < len(guides):
            time.sleep(3)

    # Update generation report with humanisation results
    log.info("\n[3/3] Updating generation report ...")
    _update_report(report, results, output_report_path)

    # Summary
    successes = sum(1 for r in results if r.success)
    failures = len(results) - successes
    log.info(f"\n{'─'*60}")
    log.info(f"  Humanised: {successes}/{len(results)} guides")
    if failures:
        log.warning(f"  Failed:    {failures} guide(s)")
    log.info(f"  Report:    {output_report_path}")
    log.info(f"{'─'*60}")

    return results


def _update_report(original_report: dict, results: list, path: str) -> None:
    """Merge humanisation results back into the generation report."""
    results_by_slug = {r.slug: asdict(r) for r in results}

    for guide in original_report.get("guides", []):
        slug = guide.get("slug", "")
        if slug in results_by_slug:
            guide["humanisation"] = results_by_slug[slug]

    original_report["humanised_at"] = datetime.now(timezone.utc).isoformat()
    original_report["humanisation_succeeded"] = sum(1 for r in results if r.success)
    original_report["humanisation_failed"] = sum(1 for r in results if not r.success)

    with open(path, "w") as f:
        json.dump(original_report, f, indent=2, default=str)
    log.info(f"  Saved updated report → {path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ZX Cloud Security — Guide Humaniser")
    parser.add_argument(
        "--report",
        default="generation_report.json",
        help="Path to generation_report.json from guide_generator.py",
    )
    parser.add_argument(
        "--drafts-dir",
        default="drafts/guides",
        help="Directory containing generated draft guides",
    )
    args = parser.parse_args()

    results = run(
        generation_report_path=args.report,
        drafts_dir=Path(args.drafts_dir),
        output_report_path=args.report,
    )

    print(f"\n{'─'*60}")
    for r in results:
        status = "✓" if r.success else "✗"
        print(f"  {status} {r.topic_label}")
        if r.success:
            wc_delta = r.humanised_word_count - r.original_word_count
            delta_str = f"{wc_delta:+d}" if wc_delta else "±0"
            print(f"      {r.original_word_count} → {r.humanised_word_count} words ({delta_str})")
            if r.remaining_tells:
                print(f"      ⚠ Remaining tells: {', '.join(r.remaining_tells)}")
        else:
            print(f"      FAILED: {r.error}")
    print(f"{'─'*60}\n")
