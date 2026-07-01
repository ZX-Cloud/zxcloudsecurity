"""
email-agent/lambda_function.py
ZX Cloud Security — Email Agent

Polls the advisories@zxcloudsecurity.co.uk shared mailbox for unread emails,
drafts a reply using Claude, and saves it as a Draft in the mailbox.
Steve reviews and sends manually — nothing goes out automatically.

Triggered by EventBridge Scheduler every 15 minutes.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import logging
import os
from functools import lru_cache
from datetime import datetime, timezone

import boto3

log = logging.getLogger()
log.setLevel(logging.INFO)

MAILBOX        = 'advisories@zxcloudsecurity.co.uk'
SECRET_NAME    = 'zxcloudsecurity/email-agent'
CLAUDE_MODEL   = 'claude-haiku-4-5-20251001'
MAX_EMAILS     = 10   # max to process per run
REGION         = 'eu-west-1'

SYSTEM_PROMPT = """You are the email assistant for ZX Cloud Security (zxcloudsecurity.co.uk).

ZX Cloud Security is a UK-focused cloud security advisory site run by Steve Harrison, a security architect. The site publishes:
- Daily cloud security advisories covering AWS, Azure, and GCP threats
- In-depth practitioner guides on topics like AWS IAM, Zero Trust, CSPM, KMS, CloudTrail, WAF
- A free daily email digest for security professionals

You draft professional, helpful replies to emails received at advisories@zxcloudsecurity.co.uk. Common email types:

1. CORRECTIONS / ERRORS: Acknowledge the correction graciously, thank them, confirm it will be reviewed and published promptly if valid.
2. SUBSCRIPTION SUPPORT (can't unsubscribe etc): Apologise for the trouble, confirm you will manually remove them within 24 hours, ask them to confirm their email address if not clear.
3. FEEDBACK / COMPLIMENTS: Thank them warmly and briefly, keep it short.
4. GUEST CONTRIBUTION / PARTNERSHIP: Acknowledge interest, explain the site is editorially independent and currently not accepting guest posts, but thank them for reaching out.
5. PRESS / MEDIA: Acknowledge and say Steve will respond personally shortly.
6. SPAM / IRRELEVANT: Draft a polite one-liner declining.

Tone: professional, concise, warm but not effusive. Sign off as:

Steve Harrison
ZX Cloud Security
zxcloudsecurity.co.uk

Write ONLY the email body — no subject line, no metadata. Plain text."""


@lru_cache(maxsize=1)
def _get_secrets() -> dict:
    client = boto3.client('secretsmanager', region_name=REGION)
    resp = client.get_secret_value(SecretId=SECRET_NAME)
    return json.loads(resp['SecretString'])


def _graph_token(secrets: dict) -> str:
    """Get Microsoft Graph access token via client credentials flow."""
    tenant_id     = secrets['azure_tenant_id']
    client_id     = secrets['azure_client_id']
    client_secret = secrets['azure_client_secret']

    url  = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = urllib.parse.urlencode({
        'grant_type':    'client_credentials',
        'client_id':     client_id,
        'client_secret': client_secret,
        'scope':         'https://graph.microsoft.com/.default',
    }).encode()

    req = urllib.request.Request(url, data=data, method='POST')
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())['access_token']


def _graph(method: str, path: str, token: str, body: dict = None) -> dict:
    """Make a Microsoft Graph API call."""
    url     = f'https://graph.microsoft.com/v1.0{path}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type':  'application/json',
    }
    data = json.dumps(body).encode() if body else None
    req  = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        log.error(f'Graph {method} {path} → {e.code}: {e.read()[:300]}')
        raise


def _get_unread_emails(token: str) -> list:
    """Fetch unread emails from the advisories mailbox."""
    params = urllib.parse.urlencode({
        '$filter':  'isRead eq false',
        '$select':  'id,subject,from,body,receivedDateTime',
        '$top':     MAX_EMAILS,
        '$orderby': 'receivedDateTime asc',
    })
    path = f'/users/{urllib.parse.quote(MAILBOX)}/messages?{params}'
    resp = _graph('GET', path, token)
    return resp.get('value', [])


def _draft_reply_with_claude(email: dict, secrets: dict) -> str:
    """Call Claude to draft a reply to the email."""
    sender  = email.get('from', {}).get('emailAddress', {})
    name    = sender.get('name', 'there')
    subject = email.get('subject', '(no subject)')
    body    = email.get('body', {}).get('content', '')

    # Strip basic HTML if content type is HTML
    if email.get('body', {}).get('contentType') == 'html':
        import re
        body = re.sub(r'<[^>]+>', ' ', body)
        body = re.sub(r'\s+', ' ', body).strip()

    user_message = f"""Please draft a reply to this email.

Sender: {name}
Subject: {subject}
Message:
{body[:3000]}"""

    payload = json.dumps({
        'model':      CLAUDE_MODEL,
        'max_tokens': 500,
        'system':     SYSTEM_PROMPT,
        'messages':   [{'role': 'user', 'content': user_message}],
    }).encode()

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'x-api-key':         secrets['anthropic_api_key'],
            'anthropic-version': '2023-06-01',
            'content-type':      'application/json',
        },
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())
        return result['content'][0]['text']


def _save_draft(token: str, original: dict, reply_body: str) -> None:
    """Save Claude's reply as a Draft in the mailbox."""
    sender = original.get('from', {}).get('emailAddress', {})
    subject = original.get('subject', '')
    if not subject.lower().startswith('re:'):
        subject = f"Re: {subject}"

    draft = {
        'subject': subject,
        'from': {
            'emailAddress': {
                'address': MAILBOX,
                'name':    'ZX Cloud Security',
            }
        },
        'body': {
            'contentType': 'Text',
            'content': reply_body,
        },
        'toRecipients': [{
            'emailAddress': {
                'address': sender.get('address', ''),
                'name':    sender.get('name', ''),
            }
        }],
    }
    mb = urllib.parse.quote(MAILBOX)
    _graph('POST', f'/users/{mb}/messages', token, draft)
    log.info(f"Draft saved: {subject} → {sender.get('address')}")


def _mark_read(token: str, email_id: str) -> None:
    """Mark email as read so it isn't processed again."""
    mb = urllib.parse.quote(MAILBOX)
    _graph('PATCH', f'/users/{mb}/messages/{email_id}', token, {'isRead': True})


def handler(event, context):
    log.info(f"Email agent starting at {datetime.now(timezone.utc).isoformat()}")

    secrets = _get_secrets()
    token   = _graph_token(secrets)

    emails = _get_unread_emails(token)
    log.info(f"Found {len(emails)} unread email(s)")

    drafted = 0
    skipped = 0

    for email in emails:
        email_id = email['id']
        subject  = email.get('subject', '(no subject)')
        sender   = email.get('from', {}).get('emailAddress', {}).get('address', '')

        log.info(f"Processing: '{subject}' from {sender}")

        try:
            reply = _draft_reply_with_claude(email, secrets)
            _save_draft(token, email, reply)
            _mark_read(token, email_id)
            drafted += 1
            log.info(f"  ✓ Draft saved for: {subject}")
        except Exception as e:
            log.error(f"  ✗ Failed to process '{subject}': {e}")
            skipped += 1

    summary = {'processed': len(emails), 'drafted': drafted, 'skipped': skipped}
    log.info(f"Done: {summary}")
    return {'statusCode': 200, 'body': json.dumps(summary)}
