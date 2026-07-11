"""
technical_reviewer.py
ZX Cloud Security — Technical Accuracy Review

Runs a second, independent Claude review over guides that passed
quality_checker.py's structural checks, looking specifically for technical
inaccuracies quality_checker.py cannot catch: wrong AWS/Azure/GCP service
names or API calls, malformed IAM policy JSON, fabricated or outdated CVE
references, and factually incorrect security claims.

Uses Claude Sonnet 5 at medium effort rather than Haiku — accuracy matters
more than cost here, and guide volume is low enough (a handful per day) that
the extra spend is immaterial in absolute terms.

Reads/writes: quality_report.json (adds a "technical_review" field per guide)
"""

import json
import logging
from pathlib import Path

import anthropic

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

MODEL = "claude-sonnet-5"
# Sonnet 5 runs adaptive thinking by default (thinking tokens count against
# max_tokens), so keep the same generous budget the Fable 5 version needed.
MAX_TOKENS = 16000

SYSTEM_PROMPT = """You are a senior cloud security engineer performing a technical accuracy \
review of a security guide before it is published under a named author's byline.

Check specifically for:
- Incorrect AWS, Azure, or GCP service names, API operations, or CLI commands
- Malformed or logically wrong IAM policy / SCP JSON (e.g. wrong effect, invalid \
resource ARN patterns, contradictory Allow/Deny statements)
- CVE references that don't match the CVE ID's actual vulnerability, or that appear fabricated
- Security claims that are outdated, misleading, or factually wrong

Do not comment on writing style, structure, or SEO — a separate check already covers those. \
Only report genuine technical problems a knowledgeable practitioner would flag before \
publication. If the guide is technically sound, say so."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "issues_found": {"type": "boolean"},
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "severity": {"type": "string", "enum": ["minor", "major"]},
                    "description": {"type": "string"},
                },
                "required": ["severity", "description"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["issues_found", "findings"],
    "additionalProperties": False,
}


def review_guide(client: anthropic.Anthropic, content: str) -> dict:
    """Run the technical review for a single guide. Returns the parsed findings dict."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        output_config={
            "effort": "medium",
            "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA},
        },
        messages=[{"role": "user", "content": f"Review this guide:\n\n{content}"}],
    )

    if response.stop_reason == "refusal":
        log.warning("    Review declined by safety classifiers — skipping technical review for this guide")
        return {"issues_found": False, "findings": [], "review_error": "refused"}

    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        log.warning(
            f"    Could not parse review response (stop_reason={response.stop_reason}): {text[:200]}"
        )
        return {"issues_found": False, "findings": [], "review_error": "parse_failed"}


def run(quality_report_path: str = "quality_report.json") -> None:
    log.info("─" * 60)
    log.info("technical_reviewer.py — ZX Cloud Security")
    log.info("─" * 60)

    p = Path(quality_report_path)
    if not p.exists():
        log.error(f"Quality report not found: {quality_report_path} — run quality_checker.py first")
        return

    with open(p) as f:
        data = json.load(f)

    guides = data.get("guides", [])
    reviewable = [g for g in guides if g.get("outcome") in ("pass", "flag")]
    if not reviewable:
        log.warning("No pass/flag guides to review")
        return

    log.info(f"[1/1] Reviewing {len(reviewable)} guide(s) for technical accuracy ...")
    client = anthropic.Anthropic()

    for guide in reviewable:
        draft_path = Path(guide["draft_path"])
        if not draft_path.exists():
            log.warning(f"  Draft not found on disk, skipping: {draft_path}")
            continue
        log.info(f"  Reviewing: {guide.get('title', guide['slug'])}")
        content = draft_path.read_text(encoding="utf-8")
        result = review_guide(client, content)
        guide["technical_review"] = result
        if result.get("issues_found"):
            severities = [f["severity"] for f in result.get("findings", [])]
            log.warning(f"    ⚠ {len(result['findings'])} finding(s): {severities}")
        elif result.get("review_error"):
            log.warning(f"    ⚠ Review incomplete: {result['review_error']}")
        else:
            log.info("    ✓ No technical issues found")

    with open(p, "w") as f:
        json.dump(data, f, indent=2, default=str)
    log.info(f"  Saved → {quality_report_path}")
    log.info("─" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ZX Cloud Security — Technical Reviewer")
    parser.add_argument("--quality-report", default="quality_report.json",
                        help="Path to quality_report.json from quality_checker.py")
    args = parser.parse_args()

    run(quality_report_path=args.quality_report)
