"""
send_digest.py
ZX Cloud Security — Daily Email Digest

Reads enriched_feed.json and sends a daily digest to Buttondown subscribers
via the Buttondown API. Always sends — even on quiet days — to maintain
subscriber trust and consistent delivery expectations.

Usage:
    set ANTHROPIC_API_KEY=...  (not needed for this script)
    set BUTTONDOWN_API_KEY=your-key
    python send_digest.py
"""

import json
import logging
import os
import re
import requests
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

BUTTONDOWN_API_URL = "https://api.buttondown.email/v1/emails"
INPUT_FILE = "enriched_feed.json"
MAX_ITEMS_IN_EMAIL = 15

SEVERITY_EMOJI = {
    "Critical": "🔴",
    "High":     "🟠",
    "Medium":   "🟡",
    "Low":      "🟢",
}

SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

# ---------------------------------------------------------------------------
# Subject line
# ---------------------------------------------------------------------------

def build_subject(items: list, date_str: str) -> str:
    counts = Counter(i.get("ai_severity", "Medium") for i in items)
    critical = counts.get("Critical", 0)
    high = counts.get("High", 0)

    if not items:
        return f"ZX Cloud Security | Security Digest — {date_str}"
    elif critical == 0 and high == 0:
        return f"ZX Cloud Security | Security Digest — {date_str}"
    elif critical > 0:
        parts = []
        if critical:
            parts.append(f"{critical} Critical")
        if high:
            parts.append(f"{high} High")
        return f"ZX Cloud Security | {', '.join(parts)} {'advisory' if critical + high == 1 else 'advisories'} — {date_str}"
    else:
        return f"ZX Cloud Security | {high} High {'advisory' if high == 1 else 'advisories'} — {date_str}"


# ---------------------------------------------------------------------------
# Email body
# ---------------------------------------------------------------------------

QUIET_DAY_HTML = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 640px; margin: 0 auto; color: #1a1a1a;">

  <div style="background: #f8f9fa; border-left: 4px solid #0066cc; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; border-radius: 0 8px 8px 0;">
    <p style="margin: 0; font-size: 15px; line-height: 1.6;">
      Today is a relatively quiet day in the cloud security world — no Critical or High severity advisories have been published in the last 24 hours across AWS, Azure or GCP. This is worth noting in itself: sustained quiet periods occasionally precede coordinated disclosure events, so it is worth keeping monitoring tools active.
    </p>
  </div>

  <p style="font-size: 14px; color: #555; line-height: 1.6;">
    We will be back tomorrow with your full daily digest. In the meantime, if you are looking to deepen your cloud security knowledge, our <a href="https://zxcloudsecurity.co.uk/guides/" style="color: #0066cc;">in-depth guides</a> cover Zero Trust architecture, CSPM, AWS IAM best practices, Kubernetes security, and our cross-cloud security service comparison.
  </p>

  <p style="font-size: 14px; color: #555; line-height: 1.6;">
    You can also browse the full advisory archive at <a href="https://zxcloudsecurity.co.uk" style="color: #0066cc;">zxcloudsecurity.co.uk</a>.
  </p>

  <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;">
  <p style="font-size: 12px; color: #999; text-align: center; margin: 0;">
    ZX Cloud Security · Daily cloud security intelligence for architects and engineers<br>
    <a href="https://zxcloudsecurity.co.uk" style="color: #999;">zxcloudsecurity.co.uk</a>
  </p>
</div>
"""


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


def build_item_html(item: dict, index: int) -> str:
    severity = item.get("ai_severity", "Medium")
    emoji = SEVERITY_EMOJI.get(severity, "⚪")
    title = item.get("ai_seo_title") or item.get("title", "Untitled")
    summary = strip_html(item.get("ai_summary") or item.get("summary", ""))[:280]
    architects_take = strip_html(item.get("ai_architects_take", ""))
    source = item.get("source_name", "")
    link = item.get("link", "https://zxcloudsecurity.co.uk")
    slug = (item.get("ai_slug") or "").strip()
    article_url = f"https://zxcloudsecurity.co.uk/posts/{slug}/" if slug else link

    severity_colours = {
        "Critical": "#dc2626",
        "High":     "#d97706",
        "Medium":   "#2563eb",
        "Low":      "#16a34a",
    }
    colour = severity_colours.get(severity, "#6b7280")
    bg_colours = {
        "Critical": "#fef2f2",
        "High":     "#fffbeb",
        "Medium":   "#eff6ff",
        "Low":      "#f0fdf4",
    }
    bg = bg_colours.get(severity, "#f9fafb")

    return f"""
<div style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem; background: #fff;">
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
    <span style="font-size: 13px; font-weight: 600; color: {colour}; background: {bg}; padding: 2px 10px; border-radius: 20px;">{emoji} {severity}</span>
    <span style="font-size: 12px; color: #9ca3af;">{source}</span>
  </div>
  <h3 style="margin: 0 0 0.5rem; font-size: 15px; font-weight: 600;">
    <a href="{article_url}" style="color: #1a1a1a; text-decoration: none;">{title}</a>
  </h3>
  <p style="margin: 0 0 0.75rem; font-size: 13px; color: #4b5563; line-height: 1.5;">{summary}{"..." if len(summary) >= 280 else ""}</p>
  {"<div style='font-size: 12px; padding: 0.6rem 0.75rem; background: " + bg + "; border-radius: 6px; color: " + colour + ";'><strong>Security Architect's Take:</strong> " + architects_take + "</div>" if architects_take else ""}
</div>
"""


def build_full_email_html(items: list, date_str: str) -> str:
    counts = Counter(i.get("ai_severity", "Medium") for i in items)
    critical = counts.get("Critical", 0)
    high = counts.get("High", 0)
    medium = counts.get("Medium", 0)
    total = len(items)

    top_items = items[:MAX_ITEMS_IN_EMAIL]
    remaining = total - len(top_items)

    items_html = "".join(build_item_html(item, i) for i, item in enumerate(top_items, 1))

    remaining_html = f"""
<div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; margin-top: 1rem;">
  <p style="margin: 0; font-size: 13px; color: #6b7280;">
    + {remaining} more {'advisory' if remaining == 1 else 'advisories'} on the site today.
    <a href="https://zxcloudsecurity.co.uk" style="color: #0066cc;">View all at zxcloudsecurity.co.uk →</a>
  </p>
</div>
""" if remaining > 0 else ""

    return f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 640px; margin: 0 auto; color: #1a1a1a;">

  <p style="font-size: 14px; color: #4b5563; margin-bottom: 1.5rem; line-height: 1.6;">
    Your daily cloud security digest for <strong>{date_str}</strong>. {total} {'advisory' if total == 1 else 'advisories'} published today across AWS, Azure, GCP and general security sources.
  </p>

 <table width="100%" cellpadding="0" cellspacing="8" style="margin-bottom: 1.5rem;">
    <tr>
      <td width="25%" style="background: #fef2f2; border-radius: 8px; padding: 0.75rem; text-align: center;">
        <div style="font-size: 10px; color: #dc2626; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Critical</div>
        <div style="font-size: 22px; font-weight: 600; color: #dc2626;">{critical}</div>
      </td>
      <td width="25%" style="background: #fffbeb; border-radius: 8px; padding: 0.75rem; text-align: center;">
        <div style="font-size: 10px; color: #d97706; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">High</div>
        <div style="font-size: 22px; font-weight: 600; color: #d97706;">{high}</div>
      </td>
      <td width="25%" style="background: #eff6ff; border-radius: 8px; padding: 0.75rem; text-align: center;">
        <div style="font-size: 10px; color: #2563eb; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Medium</div>
        <div style="font-size: 22px; font-weight: 600; color: #2563eb;">{medium}</div>
      </td>
      <td width="25%" style="background: #f8f9fa; border-radius: 8px; padding: 0.75rem; text-align: center;">
        <div style="font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px;">Total</div>
        <div style="font-size: 22px; font-weight: 600; color: #1a1a1a;">{total}</div>
      </td>
    </tr>
  </table>

  {items_html}
  {remaining_html}

  <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;">
  <p style="font-size: 12px; color: #9ca3af; text-align: center; margin: 0;">
    ZX Cloud Security · Daily cloud security intelligence for architects and engineers<br>
    <a href="https://zxcloudsecurity.co.uk" style="color: #9ca3af;">zxcloudsecurity.co.uk</a> ·
    <a href="https://zxcloudsecurity.co.uk/guides/" style="color: #9ca3af;">Guides</a>
  </p>
</div>
"""


# ---------------------------------------------------------------------------
# Buttondown API
# ---------------------------------------------------------------------------

def send_email(subject: str, body_html: str, api_key: str) -> bool:
    try:
        resp = requests.post(
            BUTTONDOWN_API_URL,
            headers={
                "Authorization": f"Token {api_key}",
                "Content-Type": "application/json",
                "X-Buttondown-Live-Dangerously": "true",
            },
            json={
                "subject": subject,
                "body": body_html,
                "status": "about_to_send",  # sends immediately to all subscribers
            },
            timeout=30,
        )
        resp.raise_for_status()
        log.info(f"Email sent successfully — subject: {subject}")
        return True
    except requests.RequestException as e:
        log.error(f"Failed to send email: {e}")
        if hasattr(e, "response") and e.response is not None:
            log.error(f"Response body: {e.response.text[:500]}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def send_digest(
    input_path: str = INPUT_FILE,
    api_key: str | None = None,
) -> bool:
    if api_key is None:
        api_key = os.environ.get("BUTTONDOWN_API_KEY")
    if not api_key:
        raise ValueError("BUTTONDOWN_API_KEY not set")

    date_str = datetime.now(timezone.utc).strftime("%d %b %Y")

    # Load enriched items
    path = Path(input_path)
    if not path.exists():
        log.warning(f"Input file not found: {input_path} — sending quiet day email")
        items = []
    else:
        with open(path) as f:
            items = json.load(f)

    # Sort by severity
    items.sort(key=lambda x: SEVERITY_ORDER.get(x.get("ai_severity", ""), 4))

    counts = Counter(i.get("ai_severity", "Medium") for i in items)
    critical = counts.get("Critical", 0)
    high = counts.get("High", 0)

    log.info(f"Loaded {len(items)} items — Critical: {critical}, High: {high}")

    # Decide which email to send
    is_quiet = (critical == 0 and high == 0) or len(items) == 0

    subject = build_subject(items, date_str)
    body_html = QUIET_DAY_HTML if is_quiet else build_full_email_html(items, date_str)

    log.info(f"Sending {'quiet day' if is_quiet else 'full digest'} email")
    log.info(f"Subject: {subject}")

    return send_email(subject, body_html, api_key)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    success = send_digest()
    if success:
        print("\n✅ Digest sent successfully")
    else:
        print("\n❌ Failed to send digest — check logs above")
        exit(1)
