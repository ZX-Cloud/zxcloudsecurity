"""
send_digest/lambda_function.py
ZX Cloud Security — Daily Email Digest Sender

Reads confirmed subscribers from DynamoDB.
Filters advisories by each subscriber's category preferences.
Sends personalised HTML digest via SES.

Triggered by GitHub Actions after the site is built and deployed.
"""

import json
import os
import boto3
from collections import Counter
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
ses = boto3.client('ses', region_name='eu-west-1')

TABLE_NAME = 'zxcloudsecurity-subscribers'
FROM_EMAIL = 'advisories@zxcloudsecurity.co.uk'
SITE_URL = 'https://zxcloudsecurity.co.uk'
API_URL = 'https://3525nbuoej.execute-api.eu-west-1.amazonaws.com/prod'
ENRICHED_FEED_BUCKET = os.environ.get('ENRICHED_FEED_BUCKET', 'zxcloudsecurity-site')
MAX_ITEMS_IN_EMAIL = 15

SEVERITY_EMOJI = {
    "Critical": "🔴",
    "High":     "🟠",
    "Medium":   "🟡",
    "Low":      "🟢",
}

SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

QUIET_DAY_HTML = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 640px; margin: 0 auto; color: #1a1a1a;">
  <div style="background: #f8f9fa; border-left: 4px solid #0066cc; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; border-radius: 0 8px 8px 0;">
    <p style="margin: 0; font-size: 15px; line-height: 1.6;">
      Today is a relatively quiet day in the cloud security world — no Critical or High severity advisories have been published in the last 24 hours across AWS, Azure or GCP. Sustained quiet periods occasionally precede coordinated disclosure events, so keep monitoring tools active.
    </p>
  </div>
  <p style="font-size: 14px; color: #555; line-height: 1.6;">
    Back tomorrow with your full digest. In the meantime, explore our <a href="{site_url}/guides/" style="color: #0066cc;">in-depth cloud security guides</a> covering Zero Trust, CSPM, AWS IAM, Kubernetes security, and our cross-cloud service comparison.
  </p>
  <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;">
  <p style="font-size: 12px; color: #9ca3af; text-align: center; margin: 0;">
    ZX Cloud Security · <a href="{site_url}" style="color: #9ca3af;">{site_url}</a> ·
    <a href="{unsubscribe_url}" style="color: #9ca3af;">Unsubscribe</a>
  </p>
</div>
""".replace("{site_url}", SITE_URL)


def get_confirmed_subscribers():
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('confirmed').eq(True)
    )
    return response.get('Items', [])


def filter_items_for_subscriber(items: list, categories: list) -> list:
    if 'all' in categories:
        return items
    return [i for i in items if i.get('category', 'general') in categories]


def build_subject(items: list, date_str: str) -> str:
    counts = Counter(i.get("ai_severity", "Medium") for i in items)
    critical = counts.get("Critical", 0)
    high = counts.get("High", 0)
    if critical > 0:
        parts = []
        if critical: parts.append(f"{critical} Critical")
        if high: parts.append(f"{high} High")
        return f"ZX Cloud Security | {', '.join(parts)} {'advisory' if critical + high == 1 else 'advisories'} — {date_str}"
    elif high > 0:
        return f"ZX Cloud Security | {high} High {'advisory' if high == 1 else 'advisories'} — {date_str}"
    return f"ZX Cloud Security | Security Digest — {date_str}"


def build_item_html(item: dict) -> str:
    severity = item.get("ai_severity", "Medium")
    emoji = SEVERITY_EMOJI.get(severity, "⚪")
    title = item.get("ai_seo_title") or item.get("title", "Untitled")
    summary = (item.get("ai_summary") or item.get("summary", ""))[:280]
    architects_take = item.get("ai_architects_take", "")
    source = item.get("source_name", "")
    slug = (item.get("ai_slug") or "").strip()
    article_url = f"{SITE_URL}/posts/{slug}/" if slug else item.get("link", SITE_URL)

    colours = {"Critical": "#dc2626", "High": "#d97706", "Medium": "#2563eb", "Low": "#16a34a"}
    bgs = {"Critical": "#fef2f2", "High": "#fffbeb", "Medium": "#eff6ff", "Low": "#f0fdf4"}
    colour = colours.get(severity, "#6b7280")
    bg = bgs.get(severity, "#f9fafb")

    take_html = f"<div style='font-size:12px;padding:0.6rem 0.75rem;background:{bg};border-radius:6px;color:{colour};margin-top:0.5rem;'><strong>Security Architect's Take:</strong> {architects_take}</div>" if architects_take else ""

    return f"""
<div style="border:1px solid #e5e7eb;border-radius:8px;padding:1.25rem;margin-bottom:1rem;background:#fff;">
  <div style="margin-bottom:0.5rem;">
    <span style="font-size:13px;font-weight:600;color:{colour};background:{bg};padding:2px 10px;border-radius:20px;">{emoji} {severity}</span>
    <span style="font-size:12px;color:#9ca3af;margin-left:8px;">{source}</span>
  </div>
  <h3 style="margin:0 0 0.5rem;font-size:15px;font-weight:600;">
    <a href="{article_url}" style="color:#1a1a1a;text-decoration:none;">{title}</a>
  </h3>
  <p style="margin:0;font-size:13px;color:#4b5563;line-height:1.5;">{summary}{"..." if len(summary) >= 280 else ""}</p>
  {take_html}
</div>"""


def build_digest_html(items: list, date_str: str, unsubscribe_url: str) -> str:
    counts = Counter(i.get("ai_severity", "Medium") for i in items)
    critical = counts.get("Critical", 0)
    high = counts.get("High", 0)
    medium = counts.get("Medium", 0)
    total = len(items)

    top_items = items[:MAX_ITEMS_IN_EMAIL]
    remaining = total - len(top_items)

    items_html = "".join(build_item_html(i) for i in top_items)
    remaining_html = f'<div style="text-align:center;padding:1rem;background:#f8f9fa;border-radius:8px;margin-top:1rem;"><p style="margin:0;font-size:13px;color:#6b7280;">+ {remaining} more on the site. <a href="{SITE_URL}" style="color:#0066cc;">View all →</a></p></div>' if remaining > 0 else ""

    return f"""
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:640px;margin:0 auto;color:#1a1a1a;">
  <p style="font-size:14px;color:#4b5563;margin-bottom:1.5rem;line-height:1.6;">
    Your daily cloud security digest for <strong>{date_str}</strong>. {total} {'advisory' if total == 1 else 'advisories'} today.
  </p>
  <table width="100%" cellpadding="0" cellspacing="8" style="margin-bottom:1.5rem;">
    <tr>
      <td width="25%" style="background:#fef2f2;border-radius:8px;padding:0.75rem;text-align:center;">
        <div style="font-size:10px;color:#dc2626;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:2px;">Critical</div>
        <div style="font-size:22px;font-weight:600;color:#dc2626;">{critical}</div>
      </td>
      <td width="25%" style="background:#fffbeb;border-radius:8px;padding:0.75rem;text-align:center;">
        <div style="font-size:10px;color:#d97706;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:2px;">High</div>
        <div style="font-size:22px;font-weight:600;color:#d97706;">{high}</div>
      </td>
      <td width="25%" style="background:#eff6ff;border-radius:8px;padding:0.75rem;text-align:center;">
        <div style="font-size:10px;color:#2563eb;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:2px;">Medium</div>
        <div style="font-size:22px;font-weight:600;color:#2563eb;">{medium}</div>
      </td>
      <td width="25%" style="background:#f8f9fa;border-radius:8px;padding:0.75rem;text-align:center;">
        <div style="font-size:10px;color:#6b7280;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:2px;">Total</div>
        <div style="font-size:22px;font-weight:600;color:#1a1a1a;">{total}</div>
      </td>
    </tr>
  </table>
  {items_html}
  {remaining_html}
  <hr style="border:none;border-top:1px solid #e5e7eb;margin:2rem 0;">
  <p style="font-size:12px;color:#9ca3af;text-align:center;margin:0;">
    ZX Cloud Security · <a href="{SITE_URL}" style="color:#9ca3af;">{SITE_URL}</a> ·
    <a href="{SITE_URL}/guides/" style="color:#9ca3af;">Guides</a> ·
    <a href="{unsubscribe_url}" style="color:#9ca3af;">Unsubscribe</a>
  </p>
</div>"""


def send_email(to_email: str, subject: str, html: str) -> bool:
    try:
        ses.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Html': {'Data': html}}
            }
        )
        return True
    except Exception as e:
        print(f"Failed to send to {to_email}: {e}")
        return False


def handler(event, context):
    # Load enriched feed from S3
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=ENRICHED_FEED_BUCKET, Key='enriched_feed.json')
        all_items = json.loads(obj['Body'].read())
    except Exception as e:
        print(f"Could not load enriched_feed.json from S3: {e}")
        all_items = []

    # Sort by severity
    all_items.sort(key=lambda x: SEVERITY_ORDER.get(x.get("ai_severity", ""), 4))

    date_str = datetime.now(timezone.utc).strftime("%d %b %Y")

    # Get confirmed subscribers
    subscribers = get_confirmed_subscribers()
    print(f"Sending digest to {len(subscribers)} confirmed subscribers")

    sent = 0
    failed = 0

    for subscriber in subscribers:
        email = subscriber.get('email', '')
        categories = subscriber.get('categories', ['all'])
        unsubscribe_url = f"{API_URL}/unsubscribe?email={email}"

        # Filter items for this subscriber's preferences
        items = filter_items_for_subscriber(all_items, categories)
        counts = Counter(i.get("ai_severity", "Medium") for i in items)
        is_quiet = counts.get("Critical", 0) == 0 and counts.get("High", 0) == 0

        subject = build_subject(items, date_str)

        if is_quiet or not items:
            html = QUIET_DAY_HTML.replace("{unsubscribe_url}", unsubscribe_url)
            subject = f"ZX Cloud Security | Security Digest — {date_str}"
        else:
            html = build_digest_html(items, date_str, unsubscribe_url)

        if send_email(email, subject, html):
            sent += 1
            print(f"  ✓ Sent to {email}")
        else:
            failed += 1

    return {
        'statusCode': 200,
        'body': json.dumps({
            'subscribers': len(subscribers),
            'sent': sent,
            'failed': failed
        })
    }
