"""
publisher.py
ZX Cloud Security — Draft Commit & SES Email Digest

Reads quality_report.json, commits passing/flagged guides to the `drafts`
branch, generates approval tokens in DynamoDB, and sends a mobile-optimised
SES email digest to Steve for review.

Auto-rejects guides that scored below threshold (removes from drafts/).
Sends a catch-up email if > 3 drafts have been pending for > 24 hours.

Environment variables required:
    ANTHROPIC_API_KEY       (not used here — for other scripts)
    GITHUB_TOKEN            GitHub Actions auto-provided token
    GITHUB_REPO             e.g. "steveharrison/zxcloudsecurity"
    SES_FROM_ADDRESS        Verified SES sending identity
    SES_TO_ADDRESS          Steve's email address
    APPROVAL_LAMBDA_URL     Lambda Function URL base (no trailing slash)
    DYNAMODB_TABLE          DynamoDB table name (default: guide-approval-tokens)
    AWS_REGION              AWS region (default: eu-west-2)
"""

import json
import logging
import os
import re
import subprocess
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import boto3
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DRAFTS_BRANCH        = "drafts"
DRAFTS_DIR           = Path("drafts/guides")
TOKEN_TTL_DAYS       = 7
CATCH_UP_THRESHOLD   = 3          # drafts pending before catch-up email fires
CATCH_UP_AGE_HOURS   = 24         # hours before catch-up email fires
DYNAMODB_TABLE       = os.environ.get("DYNAMODB_TABLE", "guide-approval-tokens")
AWS_REGION           = os.environ.get("AWS_REGION", "eu-west-2")

# Email send window: only send immediately if UTC hour falls within this range.
# Outside this window the email is stored in DynamoDB and drained at next window open.
# Defaults to the full day — GitHub Actions' scheduled cron fires at an unpredictable
# offset from the configured time, so a narrow window was routinely missed entirely.
EMAIL_SEND_HOUR_UTC  = int(os.environ.get("EMAIL_SEND_HOUR_UTC", "0"))   # 00:00 UTC
EMAIL_SEND_WINDOW_H  = int(os.environ.get("EMAIL_SEND_WINDOW_H",  "24")) # open all day

# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PublishRecord:
    slug: str
    title: str
    tier: str
    total_score: int
    outcome: str          # "pass" | "flag" | "reject"
    word_count: int
    description: str
    draft_path: str
    guide_id: str = ""    # UUID, set after token generation
    token: str = ""
    committed: bool = False
    email_sent: bool = False
    error: str = ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _expires_at() -> str:
    return (_now_utc() + timedelta(days=TOKEN_TTL_DAYS)).isoformat()


def _env(key: str, required: bool = True) -> str:
    val = os.environ.get(key, "")
    if required and not val:
        raise EnvironmentError(f"Required environment variable not set: {key}")
    return val


def _derive_keyword(title: str) -> str:
    STOP = {"a", "an", "the", "and", "or", "for", "to", "in", "on", "of",
            "with", "best", "guide", "how", "your", "using", "complete"}
    words = [w for w in re.sub(r"[^\w\s]", "", title.lower()).split() if w not in STOP]
    return " ".join(words[:3])


def _short_summary(description: str, max_chars: int = 200) -> str:
    """Return description truncated to max_chars, ending cleanly at a word boundary."""
    if len(description) <= max_chars:
        return description
    truncated = description[:max_chars].rsplit(" ", 1)[0]
    return truncated + "…"


# ---------------------------------------------------------------------------
# Git: commit drafts to drafts branch
# ---------------------------------------------------------------------------

def _git(args: list, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        check=check,
        capture_output=True,
        text=True,
    )


def commit_drafts_to_branch(records: list) -> list:
    """
    Stage and commit all passing/flagged draft files to the drafts branch.
    Returns updated records with committed=True on success.
    """
    files_to_commit = [r.draft_path for r in records if Path(r.draft_path).exists()]
    if not files_to_commit:
        log.warning("No draft files to commit")
        return records

    try:
        # Configure git identity for Actions runner
        _git(["config", "user.email", "actions@github.com"])
        _git(["config", "user.name", "ZX Guide Agent"])

        # Ensure we're on the drafts branch
        current = _git(["branch", "--show-current"], check=False).stdout.strip()
        if current != DRAFTS_BRANCH:
            _git(["checkout", "-B", DRAFTS_BRANCH])

        # Stage draft files and quality report
        for path in files_to_commit:
            _git(["add", path])
        
        # Build commit message
        titles = [r.title or r.slug for r in records if r.outcome != "reject"]
        commit_msg = f"chore: add {len(titles)} guide draft(s) for review\n\n"
        for t in titles:
            commit_msg += f"- {t}\n"
        commit_msg += f"\n[guide-agent] {_now_utc().strftime('%Y-%m-%dT%H:%M:%SZ')}"

        _git(["commit", "-m", commit_msg])
        _git(["push", "origin", DRAFTS_BRANCH, "--force-with-lease"])

        log.info(f"  ✓ Committed {len(files_to_commit)} draft(s) to branch '{DRAFTS_BRANCH}'")
        for r in records:
            if r.outcome != "reject":
                r.committed = True

    except subprocess.CalledProcessError as e:
        log.error(f"  Git error: {e.stderr}")
        for r in records:
            r.error = f"Git commit failed: {e.stderr[:200]}"

    return records


# ---------------------------------------------------------------------------
# DynamoDB: store approval tokens
# ---------------------------------------------------------------------------

def store_approval_token(record: PublishRecord) -> tuple:
    """
    Generate a UUID token and store it in DynamoDB.
    Returns (guide_id, token) on success, ("", "") on failure.
    """
    guide_id = str(uuid.uuid4())
    token = str(uuid.uuid4())
    expires_at = _expires_at()
    filename = Path(record.draft_path).name

    try:
        dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
        table = dynamodb.Table(DYNAMODB_TABLE)
        table.put_item(Item={
            "token":       token,
            "guide_id":    guide_id,
            "guide_title": record.title,
            "filename":    filename,
            "slug":        record.slug,
            "expires_at":  expires_at,
            "used":        False,
            "created_at":  _now_utc().isoformat(),
        })
        log.info(f"  ✓ Token stored for '{record.title}' (expires {expires_at[:10]})")
        return guide_id, token

    except Exception as e:
        log.error(f"  DynamoDB error for '{record.slug}': {e}")
        return "", ""


# ---------------------------------------------------------------------------
# HTML email generation
# ---------------------------------------------------------------------------

# Colour palette
_C = {
    "bg":          "#0f1117",
    "card":        "#1a1f2e",
    "card_flag":   "#2a1f0e",
    "card_reject": "#1f0e0e",
    "border":      "#2d3348",
    "border_flag": "#c97a20",
    "border_rej":  "#8b1a1a",
    "text":        "#e2e8f0",
    "muted":       "#94a3b8",
    "accent":      "#3b82f6",
    "green":       "#22c55e",
    "amber":       "#f59e0b",
    "red":         "#ef4444",
    "btn_edit":    "#1d4ed8",
    "btn_approve": "#15803d",
    "btn_reject":  "#991b1b",
}


def _score_colour(score: int) -> str:
    if score >= 75:
        return _C["green"]
    elif score >= 60:
        return _C["accent"]
    elif score >= 40:
        return _C["amber"]
    return _C["red"]


def _outcome_label(outcome: str) -> str:
    return {"pass": "✓ Pass", "flag": "⚠ Flagged", "reject": "✗ Rejected"}.get(outcome, outcome)


def _guide_card_html(record: PublishRecord, lambda_url: str, github_repo: str) -> str:
    """Render one guide card for the email digest."""
    filename = Path(record.draft_path).name
    edit_url = (
        f"https://github.com/{github_repo}/edit/{DRAFTS_BRANCH}"
        f"/drafts/guides/{filename}"
    )
    approve_url = f"{lambda_url}/approve?id={record.guide_id}&token={record.token}"
    reject_url  = f"{lambda_url}/reject?id={record.guide_id}&token={record.token}"

    score_col  = _score_colour(record.total_score)
    tier_label = record.tier.capitalize() + " guide"
    keyword    = _derive_keyword(record.title)
    summary    = _short_summary(record.description)

    outcome_col = {
        "pass":   _C["green"],
        "flag":   _C["amber"],
        "reject": _C["red"],
    }.get(record.outcome, _C["muted"])

    card_bg     = {"flag": _C["card_flag"], "reject": _C["card_reject"]}.get(record.outcome, _C["card"])
    card_border = {"flag": _C["border_flag"], "reject": _C["border_rej"]}.get(record.outcome, _C["border"])

    # Flag reasons (shown for flagged guides)
    flags_html = ""

    # Action buttons — only for non-rejected guides
    buttons_html = ""
    if record.outcome != "reject":
        buttons_html = f"""
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;">
          <tr>
            <td style="padding:4px;">
              <a href="{edit_url}"
                 style="display:block;background:{_C['btn_edit']};color:#ffffff;text-decoration:none;
                        text-align:center;padding:14px 8px;border-radius:8px;font-size:16px;
                        font-weight:600;letter-spacing:0.3px;">
                ✏️ Edit in GitHub
              </a>
            </td>
            <td style="padding:4px;">
              <a href="{approve_url}"
                 style="display:block;background:{_C['btn_approve']};color:#ffffff;text-decoration:none;
                        text-align:center;padding:14px 8px;border-radius:8px;font-size:16px;
                        font-weight:600;letter-spacing:0.3px;">
                ✅ Approve
              </a>
            </td>
            <td style="padding:4px;">
              <a href="{reject_url}"
                 style="display:block;background:{_C['btn_reject']};color:#ffffff;text-decoration:none;
                        text-align:center;padding:14px 8px;border-radius:8px;font-size:16px;
                        font-weight:600;letter-spacing:0.3px;">
                ❌ Reject
              </a>
            </td>
          </tr>
        </table>"""

    return f"""
    <div style="background:{card_bg};border:1.5px solid {card_border};border-radius:12px;
                padding:20px;margin-bottom:20px;">

      <!-- Title row -->
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td>
            <div style="font-size:19px;font-weight:700;color:{_C['text']};
                        line-height:1.3;margin-bottom:6px;">
              {record.title}
            </div>
          </td>
          <td style="text-align:right;white-space:nowrap;padding-left:12px;vertical-align:top;">
            <span style="font-size:22px;font-weight:800;color:{score_col};">
              {record.total_score}
            </span>
            <span style="font-size:13px;color:{_C['muted']};">/100</span>
          </td>
        </tr>
      </table>

      <!-- Meta row -->
      <table role="presentation" width="100%" cellpadding="0" cellspacing="6"
             style="margin-bottom:14px;">
        <tr>
          <td style="font-size:13px;color:{_C['muted']};padding-right:16px;">
            <b style="color:{_C['text']};">Type</b>&nbsp;&nbsp;{tier_label}
          </td>
          <td style="font-size:13px;color:{_C['muted']};padding-right:16px;">
            <b style="color:{_C['text']};">Words</b>&nbsp;&nbsp;{record.word_count:,}
          </td>
          <td style="font-size:13px;color:{outcome_col};font-weight:600;">
            {_outcome_label(record.outcome)}
          </td>
        </tr>
        <tr>
          <td colspan="3" style="font-size:13px;color:{_C['muted']};padding-top:4px;">
            <b style="color:{_C['text']};">Keyword</b>&nbsp;&nbsp;{keyword}
          </td>
        </tr>
      </table>

      <!-- Summary -->
      <div style="font-size:15px;color:{_C['muted']};line-height:1.6;
                  border-left:3px solid {card_border};padding-left:12px;
                  margin-bottom:4px;">
        {summary}
      </div>

      {flags_html}
      {buttons_html}
    </div>"""


def _build_email_html(
    records: list,
    lambda_url: str,
    github_repo: str,
    is_catchup: bool = False,
    pending_count: int = 0,
    oldest_hours: float = 0,
) -> tuple:
    """Build the full HTML email and plain text fallback. Returns (html, text)."""

    date_str   = _now_utc().strftime("%A %-d %B %Y")
    passcount  = sum(1 for r in records if r.outcome == "pass")
    flagcount  = sum(1 for r in records if r.outcome == "flag")
    rejcount   = sum(1 for r in records if r.outcome == "reject")
    actionable = passcount + flagcount

    if is_catchup:
        subject_prefix = f"⏰ {pending_count} guides waiting"
        header_text    = f"{pending_count} guides are waiting for your review"
        subheader      = f"Oldest draft: {int(oldest_hours)} hours ago"
    else:
        subject_prefix = f"📋 {actionable} guide(s) ready for review"
        header_text    = "Your daily guide digest"
        subheader      = date_str

    subject = f"{subject_prefix} — zxcloudsecurity.co.uk"

    # Cards for actionable guides first, then rejected
    actionable_cards = "".join(
        _guide_card_html(r, lambda_url, github_repo)
        for r in records if r.outcome in ("pass", "flag")
    )
    rejected_cards = ""
    if rejcount:
        rejected_items = "".join(
            f"<li style='margin-bottom:6px;color:{_C['muted']};font-size:14px;'>"
            f"<span style='color:{_C['red']};'>✗</span> {r.title} "
            f"<span style='color:{_C['muted']};'>({r.total_score}/100)</span></li>"
            for r in records if r.outcome == "reject"
        )
        rejected_cards = f"""
        <div style="margin-top:24px;">
          <div style="font-size:13px;font-weight:600;color:{_C['muted']};
                      text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">
            Auto-rejected ({rejcount}) — will be regenerated
          </div>
          <ul style="margin:0;padding-left:18px;">{rejected_items}</ul>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="dark">
  <title>{subject}</title>
</head>
<body style="margin:0;padding:0;background:{_C['bg']};font-family:-apple-system,BlinkMacSystemFont,
             'Segoe UI',Roboto,Helvetica,Arial,sans-serif;-webkit-text-size-adjust:100%;">

  <!-- Wrapper -->
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
         style="background:{_C['bg']};min-height:100vh;">
    <tr>
      <td align="center" style="padding:24px 16px;">

        <!-- Content column (max 600px) -->
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
               style="max-width:600px;">

          <!-- Header -->
          <tr>
            <td style="padding-bottom:24px;">
              <div style="font-size:13px;font-weight:600;color:{_C['accent']};
                          text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;">
                zxcloudsecurity.co.uk
              </div>
              <div style="font-size:26px;font-weight:800;color:{_C['text']};
                          line-height:1.2;margin-bottom:6px;">
                {header_text}
              </div>
              <div style="font-size:14px;color:{_C['muted']};">{subheader}</div>
            </td>
          </tr>

          <!-- Stats bar -->
          <tr>
            <td style="padding-bottom:24px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                     style="background:{_C['card']};border-radius:10px;padding:14px 16px;">
                <tr>
                  <td style="text-align:center;padding:0 12px;">
                    <div style="font-size:28px;font-weight:800;color:{_C['green']};">{passcount}</div>
                    <div style="font-size:12px;color:{_C['muted']};">Ready</div>
                  </td>
                  <td style="text-align:center;padding:0 12px;border-left:1px solid {_C['border']};">
                    <div style="font-size:28px;font-weight:800;color:{_C['amber']};">{flagcount}</div>
                    <div style="font-size:12px;color:{_C['muted']};">Flagged</div>
                  </td>
                  <td style="text-align:center;padding:0 12px;border-left:1px solid {_C['border']};">
                    <div style="font-size:28px;font-weight:800;color:{_C['red']};">{rejcount}</div>
                    <div style="font-size:12px;color:{_C['muted']};">Rejected</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Guide cards -->
          <tr>
            <td>
              {actionable_cards}
              {rejected_cards}
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding-top:32px;border-top:1px solid {_C['border']};margin-top:8px;">
              <div style="font-size:12px;color:{_C['muted']};text-align:center;line-height:1.6;">
                Generated by the ZX Cloud Security guide agent.<br>
                Approve links expire in {TOKEN_TTL_DAYS} days.
                Drafts are on the <code style="color:{_C['accent']};">{DRAFTS_BRANCH}</code> branch.
              </div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    # Plain text fallback
    lines = [f"ZX Cloud Security — {header_text}", f"{subheader}", ""]
    lines.append(f"Ready: {passcount}  |  Flagged: {flagcount}  |  Rejected: {rejcount}")
    lines.append("")
    for r in records:
        if r.outcome == "reject":
            continue
        lines.append(f"{'='*50}")
        lines.append(f"{r.title}")
        lines.append(f"Type: {r.tier.capitalize()} guide  |  Words: {r.word_count:,}  |  Score: {r.total_score}/100")
        lines.append(f"Outcome: {_outcome_label(r.outcome)}")
        lines.append(f"Keyword: {_derive_keyword(r.title)}")
        lines.append("")
        lines.append(_short_summary(r.description))
        lines.append("")
        if r.guide_id and r.token:
            filename = Path(r.draft_path).name
            lines.append(f"Edit:    https://github.com/{github_repo}/edit/{DRAFTS_BRANCH}/drafts/guides/{filename}")
            lines.append(f"Approve: {lambda_url}/approve?id={r.guide_id}&token={r.token}")
            lines.append(f"Reject:  {lambda_url}/reject?id={r.guide_id}&token={r.token}")
        lines.append("")

    text = "\n".join(lines)
    return html, text, subject


# ---------------------------------------------------------------------------
# Email send-window gating and deferred delivery via DynamoDB
# ---------------------------------------------------------------------------

def _is_send_window() -> bool:
    """Return True if the current UTC hour falls within the permitted send window."""
    hour = _now_utc().hour
    return EMAIL_SEND_HOUR_UTC <= hour < EMAIL_SEND_HOUR_UTC + EMAIL_SEND_WINDOW_H


def _next_send_at() -> datetime:
    """Return the next 07:00 UTC datetime (today if still ahead, tomorrow otherwise)."""
    now = _now_utc()
    candidate = now.replace(hour=EMAIL_SEND_HOUR_UTC, minute=0, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(days=1)
    return candidate


def _store_pending_email(
    html: str,
    text: str,
    subject: str,
    from_addr: str,
    to_addr: str,
) -> bool:
    """
    Persist a deferred email to DynamoDB.
    Uses token = 'pending_email_<uuid>' so it shares the approval table
    without colliding with guide approval tokens.
    """
    send_at = _next_send_at()
    item_id = str(uuid.uuid4())
    try:
        dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
        table = dynamodb.Table(DYNAMODB_TABLE)
        table.put_item(Item={
            "token":      f"pending_email_{item_id}",
            "type":       "pending_email",
            "send_at":    send_at.isoformat(),
            "subject":    subject,
            "html":       html,
            "text":       text,
            "from_addr":  from_addr,
            "to_addr":    to_addr,
            "sent":       False,
            "created_at": _now_utc().isoformat(),
        })
        log.info(f"  Email deferred — will send at {send_at.strftime('%Y-%m-%dT%H:%M UTC')}")
        return True
    except Exception as e:
        log.error(f"  DynamoDB error storing pending email: {e}")
        return False


def drain_pending_emails(from_addr: str, to_addr: str) -> int:
    """
    Scan DynamoDB for pending_email items whose send_at has passed and send them.
    Marks each as sent after delivery. Returns count of emails sent.
    """
    now = _now_utc()
    sent_count = 0
    try:
        dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
        table = dynamodb.Table(DYNAMODB_TABLE)
        # FilterExpression: type = pending_email AND sent = false AND send_at <= now
        result = table.scan(
            FilterExpression=(
                "attribute_exists(#t) AND #t = :ptype"
                " AND #sent = :false"
                " AND send_at <= :now"
            ),
            ExpressionAttributeNames={
                "#t":    "type",
                "#sent": "sent",
            },
            ExpressionAttributeValues={
                ":ptype": "pending_email",
                ":false": False,
                ":now":   now.isoformat(),
            },
        )
        items = result.get("Items", [])
        if not items:
            return 0

        log.info(f"  Draining {len(items)} pending email(s) ...")
        for item in items:
            ok = send_ses_email(
                item["html"],
                item["text"],
                item["subject"],
                item.get("from_addr", from_addr),
                item.get("to_addr", to_addr),
            )
            if ok:
                table.update_item(
                    Key={"token": item["token"]},
                    UpdateExpression="SET #sent = :true, sent_at = :ts",
                    ExpressionAttributeNames={"#sent": "sent"},
                    ExpressionAttributeValues={":true": True, ":ts": now.isoformat()},
                )
                sent_count += 1
    except Exception as e:
        log.error(f"  Error draining pending emails: {e}")
    return sent_count


# ---------------------------------------------------------------------------
# SES: send email
# ---------------------------------------------------------------------------

def send_ses_email(
    html: str,
    text: str,
    subject: str,
    from_addr: str,
    to_addr: str,
) -> bool:
    """Send email via AWS SES. Returns True on success."""
    try:
        ses = boto3.client("ses", region_name=AWS_REGION)
        ses.send_email(
            Source=from_addr,
            Destination={"ToAddresses": [to_addr]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {
                    "Html": {"Data": html, "Charset": "UTF-8"},
                    "Text": {"Data": text, "Charset": "UTF-8"},
                },
            },
        )
        log.info(f"  ✓ Email sent to {to_addr}: {subject}")
        return True
    except Exception as e:
        log.error(f"  SES error: {e}")
        return False


# ---------------------------------------------------------------------------
# Catch-up email: pending drafts > threshold
# ---------------------------------------------------------------------------

def check_and_send_catchup_email(
    drafts_dir: Path,
    lambda_url: str,
    github_repo: str,
    from_addr: str,
    to_addr: str,
) -> None:
    """
    If more than CATCH_UP_THRESHOLD drafts are pending for > CATCH_UP_AGE_HOURS,
    send a catch-up digest email covering all pending drafts.
    """
    if not drafts_dir.exists():
        return

    pending = list(drafts_dir.glob("*.md"))
    if len(pending) <= CATCH_UP_THRESHOLD:
        return

    # Find oldest file by mtime
    oldest_mtime = min(f.stat().st_mtime for f in pending)
    oldest_dt = datetime.fromtimestamp(oldest_mtime, tz=timezone.utc)
    oldest_hours = (_now_utc() - oldest_dt).total_seconds() / 3600

    if oldest_hours < CATCH_UP_AGE_HOURS:
        return

    log.info(f"  Catch-up threshold met: {len(pending)} drafts, oldest {oldest_hours:.0f}h ago")

    # Build lightweight records from pending draft filenames (no tokens — just link to branch)
    records = []
    for draft_path in sorted(pending, key=lambda f: f.stat().st_mtime):
        try:
            content = draft_path.read_text(encoding="utf-8", errors="ignore")
            fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            fm: dict = {}
            if fm_match:
                for line in fm_match.group(1).splitlines():
                    if ":" in line:
                        k, _, v = line.partition(":")
                        fm[k.strip()] = v.strip().strip("\"'")
            records.append(PublishRecord(
                slug=draft_path.stem,
                title=fm.get("title", draft_path.stem),
                tier=fm.get("tier", "supporting"),
                total_score=int(fm.get("quality_score", 0)),
                outcome="pass",
                word_count=int(fm.get("word_count", 0)),
                description=fm.get("description", ""),
                draft_path=str(draft_path),
            ))
        except Exception:
            pass

    if not records:
        return

    html, text, subject = _build_email_html(
        records,
        lambda_url,
        github_repo,
        is_catchup=True,
        pending_count=len(pending),
        oldest_hours=oldest_hours,
    )
    send_ses_email(html, text, subject, from_addr, to_addr)


# ---------------------------------------------------------------------------
# Handle auto-rejected guides: delete draft files
# ---------------------------------------------------------------------------

def cleanup_rejected_drafts(records: list) -> None:
    """Remove draft files for auto-rejected guides."""
    for r in records:
        if r.outcome == "reject":
            p = Path(r.draft_path)
            if p.exists():
                p.unlink()
                log.info(f"  Deleted rejected draft: {p.name}")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(
    quality_report_path: str = "quality_report.json",
    drafts_dir: Path = DRAFTS_DIR,
    output_report_path: str = "publish_report.json",
) -> list:
    """
    Full publisher pipeline:
      1. Load quality report
      2. Delete rejected drafts
      3. Commit passing/flagged drafts to drafts branch
      4. Generate DynamoDB tokens per guide
      5. Send SES email digest
      6. Check for catch-up email condition
    """
    log.info("─" * 60)
    log.info("publisher.py — ZX Cloud Security")
    log.info("─" * 60)

    # Read environment
    try:
        github_repo   = _env("GITHUB_REPO")
        from_addr     = _env("SES_FROM_ADDRESS")
        to_addr       = _env("SES_TO_ADDRESS")
        lambda_url    = _env("APPROVAL_LAMBDA_URL").rstrip("/")
    except EnvironmentError as e:
        log.error(str(e))
        return []

    # Drain any previously deferred emails whose send_at window has now arrived
    drained = drain_pending_emails(from_addr, to_addr)
    if drained:
        log.info(f"  Drained {drained} deferred email(s)")

    # Load quality report
    p = Path(quality_report_path)
    if not p.exists():
        log.error(f"Quality report not found: {quality_report_path} — run quality_checker.py first")
        return []

    with open(p) as f:
        quality_data = json.load(f)

    guides = quality_data.get("guides", [])
    if not guides:
        log.warning("No guides in quality report")
        return []

    log.info(f"[1/5] Loaded {len(guides)} guide(s) from quality report")

    # Build PublishRecord list
    records = [
        PublishRecord(
            slug        = g["slug"],
            title       = g.get("title", g["slug"]),
            tier        = g.get("tier", "supporting"),
            total_score = g.get("total_score", 0),
            outcome     = g.get("outcome", "reject"),
            word_count  = g.get("word_count", 0),
            description = g.get("description", ""),
            draft_path  = g.get("draft_path", ""),
        )
        for g in guides
    ]

    # Step 1: Clean up rejected drafts
    log.info("[2/5] Cleaning up rejected drafts ...")
    cleanup_rejected_drafts(records)

    # Step 2: Commit passing/flagged drafts to drafts branch
    log.info("[3/5] Committing drafts to branch ...")
    records = commit_drafts_to_branch(records)

    # Step 3: Generate DynamoDB approval tokens for actionable guides
    log.info("[4/5] Generating approval tokens ...")
    for r in records:
        if r.outcome in ("pass", "flag") and r.committed:
            guide_id, token = store_approval_token(r)
            r.guide_id = guide_id
            r.token    = token

    # Step 4: Build and send (or defer) email digest
    log.info("[5/5] Building SES email digest ...")
    actionable = [r for r in records if r.outcome in ("pass", "flag")]
    if actionable:
        html, text, subject = _build_email_html(records, lambda_url, github_repo)
        if _is_send_window():
            log.info("  Within send window — sending now ...")
            sent = send_ses_email(html, text, subject, from_addr, to_addr)
            for r in actionable:
                r.email_sent = sent
        else:
            send_at = _next_send_at()
            log.info(
                f"  Outside send window (current UTC hour: {_now_utc().hour:02d}:xx, "
                f"window: {EMAIL_SEND_HOUR_UTC:02d}:00-{EMAIL_SEND_HOUR_UTC + EMAIL_SEND_WINDOW_H:02d}:00). "
                f"Deferring to {send_at.strftime('%Y-%m-%dT%H:%M UTC')} ..."
            )
            _store_pending_email(html, text, subject, from_addr, to_addr)
    else:
        log.warning("  No actionable guides — skipping email")

    # Step 5: Check catch-up email condition
    check_and_send_catchup_email(drafts_dir, lambda_url, github_repo, from_addr, to_addr)

    # Save publish report
    _save_report(records, output_report_path)

    # Summary
    committed = sum(1 for r in records if r.committed)
    emailed   = sum(1 for r in records if r.email_sent)
    rejected  = sum(1 for r in records if r.outcome == "reject")
    log.info(f"\n{'─'*60}")
    log.info(f"  Committed: {committed}  |  Emailed: {emailed}  |  Rejected & cleaned: {rejected}")
    log.info(f"  Report:    {output_report_path}")
    log.info(f"{'─'*60}")

    return records


def _save_report(records: list, path: str) -> None:
    output = {
        "published_at": _now_utc().isoformat(),
        "total": len(records),
        "committed": sum(1 for r in records if r.committed),
        "emailed": sum(1 for r in records if r.email_sent),
        "rejected": sum(1 for r in records if r.outcome == "reject"),
        "guides": [asdict(r) for r in records],
    }
    with open(path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    log.info(f"  Saved → {path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ZX Cloud Security — Publisher")
    parser.add_argument("--quality-report", default="quality_report.json",
                        help="Path to quality_report.json from quality_checker.py")
    parser.add_argument("--drafts-dir",     default="drafts/guides",
                        help="Drafts directory")
    parser.add_argument("--output",         default="publish_report.json",
                        help="Output publish report path")
    args = parser.parse_args()

    records = run(
        quality_report_path=args.quality_report,
        drafts_dir=Path(args.drafts_dir),
        output_report_path=args.output,
    )

    print(f"\n{'─'*60}")
    for r in records:
        icon = {"pass": "✓", "flag": "⚠", "reject": "✗"}.get(r.outcome, "?")
        committed = "committed" if r.committed else "not committed"
        print(f"  {icon} {r.title} — {committed}, score {r.total_score}/100")
    print(f"{'─'*60}\n")
