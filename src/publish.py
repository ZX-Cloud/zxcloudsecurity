"""
publish.py
ZX Cloud Security — Guide Publisher (final publish step)

Triggered by the publish-guide.yml GitHub Actions workflow after Steve
approves a guide via the approval Lambda. Moves a single guide from
drafts/guides/ to content/guides/, updates its frontmatter, and commits
to main. The existing Hugo build workflow fires automatically on push.

Usage:
    python publish.py --filename aws-scp-best-practices.md

The token argument is accepted for audit logging but validation has
already happened in the approval Lambda before this runs.
"""

import argparse
import logging
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

DRAFTS_DIR  = Path("drafts/guides")
CONTENT_DIR = Path("site/content/guides")
DRAFTS_BRANCH = "drafts"
MAIN_BRANCH   = "main"


def _git(args: list, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, check=check, capture_output=True, text=True)


def _update_frontmatter(content: str) -> str:
    """Set draft: false and update date to today in the frontmatter."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Set draft: false (handles draft: true or any existing value)
    if re.search(r"^draft:\s*.+$", content, re.MULTILINE):
        content = re.sub(r"^draft:\s*.+$", "draft: false", content, count=1, flags=re.MULTILINE)
    else:
        # Insert draft: false after the opening --- if not present
        content = re.sub(r"^(---\n)", r"\1draft: false\n", content, count=1)

    # Update date to today
    if re.search(r"^date:\s*.+$", content, re.MULTILINE):
        content = re.sub(r"^date:\s*.+$", f"date: {today}", content, count=1, flags=re.MULTILINE)
    else:
        content = re.sub(r"^(---\n)", rf"\1date: {today}\n", content, count=1)

    return content


def publish_guide(filename: str, token: str = "") -> bool:
    """
    Move a guide from drafts/guides/ to content/guides/, update frontmatter,
    commit and push to main. Returns True on success.
    """
    log.info("─" * 60)
    log.info(f"publish.py — publishing: {filename}")
    if token:
        log.info(f"  Approval token (audit): {token[:8]}...")
    log.info("─" * 60)

    # Sanitise filename — prevent path traversal
    safe_name = Path(filename).name
    if safe_name != filename:
        log.error(f"Invalid filename (path components not allowed): {filename}")
        return False
    if not safe_name.endswith(".md"):
        log.error(f"Filename must end in .md: {filename}")
        return False

    draft_path   = DRAFTS_DIR / safe_name
    content_path = CONTENT_DIR / safe_name

    # The draft lives on the drafts branch — fetch and check it out
    try:
        _git(["fetch", "origin", DRAFTS_BRANCH])
    except subprocess.CalledProcessError as e:
        log.error(f"Could not fetch drafts branch: {e.stderr}")
        return False

    # Read the draft file from the drafts branch
    try:
        result = _git(["show", f"origin/{DRAFTS_BRANCH}:drafts/guides/{safe_name}"])
        draft_content = result.stdout
    except subprocess.CalledProcessError as e:
        log.error(f"Draft not found on {DRAFTS_BRANCH} branch: {safe_name}")
        log.error(f"  {e.stderr}")
        return False

    if not draft_content.strip():
        log.error(f"Draft file is empty: {safe_name}")
        return False

    # Update frontmatter
    published_content = _update_frontmatter(draft_content)

    # Configure git identity for the Actions runner
    _git(["config", "user.email", "actions@github.com"])
    _git(["config", "user.name", "ZX Guide Agent"])

    # Ensure we're on main and up to date
    try:
        _git(["checkout", MAIN_BRANCH])
        _git(["pull", "origin", MAIN_BRANCH])
    except subprocess.CalledProcessError as e:
        log.error(f"Could not switch to main: {e.stderr}")
        return False

    # Write the published guide to content/guides/
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    content_path.write_text(published_content, encoding="utf-8")
    log.info(f"  ✓ Written: {content_path}")

    # Extract title for commit message
    title_match = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", published_content, re.MULTILINE)
    title = title_match.group(1) if title_match else safe_name

    # Commit and push to main
    try:
        _git(["add", str(content_path)])
        _git(["commit", "-m", f"feat: publish guide '{title}'\n\n[guide-agent] approved and published"])
        _git(["push", "origin", MAIN_BRANCH])
        log.info(f"  ✓ Committed and pushed to {MAIN_BRANCH}")
    except subprocess.CalledProcessError as e:
        log.error(f"Could not commit/push to main: {e.stderr}")
        return False

    # Remove the draft from the drafts branch
    try:
        _git(["checkout", DRAFTS_BRANCH])
        _git(["pull", "origin", DRAFTS_BRANCH])
        if draft_path.exists():
            _git(["rm", str(draft_path)])
            _git(["commit", "-m", f"chore: remove published draft '{title}' [guide-agent]"])
            _git(["push", "origin", DRAFTS_BRANCH])
            log.info(f"  ✓ Removed draft from {DRAFTS_BRANCH}")
    except subprocess.CalledProcessError as e:
        # Non-fatal — the guide is published; the draft cleanup can be done manually
        log.warning(f"  Could not remove draft (non-fatal): {e.stderr}")

    log.info("─" * 60)
    log.info(f"  ✓ Published: {title}")
    log.info(f"  Hugo build will trigger automatically on the push to {MAIN_BRANCH}")
    log.info("─" * 60)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ZX Cloud Security — Publish approved guide")
    parser.add_argument("--filename", required=True, help="Guide filename, e.g. aws-scp-best-practices.md")
    parser.add_argument("--token", default="", help="Approval token (for audit logging)")
    args = parser.parse_args()

    success = publish_guide(args.filename, args.token)
    sys.exit(0 if success else 1)
