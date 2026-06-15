"""
handler.py
ZX Cloud Security — Guide Approval Lambda

Handles approve and reject flows triggered by links in the SES email digest.
Secured by single-use UUID tokens stored in DynamoDB.

Routes:
  GET  /approve?id=<guide_id>&token=<token>   → confirmation page
  POST /approve?id=<guide_id>&token=<token>   → trigger publish workflow
  GET  /reject?id=<guide_id>&token=<token>    → confirmation page
  POST /reject?id=<guide_id>&token=<token>    → delete draft from branch

Environment variables (set on the Lambda function):
  DYNAMODB_TABLE      e.g. guide-approval-tokens
  GITHUB_PAT_SECRET   Secrets Manager secret name for GitHub PAT
                      (default: zxcloudsecurity/github-pat)
  GITHUB_REPO         e.g. ZX-Cloud/zxcloudsecurity  (not sensitive, plain env var)
  SES_FROM_ADDRESS    Verified SES sender
  SES_TO_ADDRESS      Steve's email
  AWS_REGION          e.g. eu-west-2 (set automatically by Lambda runtime)
"""

import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from functools import lru_cache

import boto3

log = logging.getLogger()
log.setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

DYNAMODB_TABLE     = os.environ["DYNAMODB_TABLE"]
GITHUB_REPO        = os.environ["GITHUB_REPO"]
SES_FROM_ADDRESS   = os.environ["SES_FROM_ADDRESS"]
SES_TO_ADDRESS     = os.environ["SES_TO_ADDRESS"]
GITHUB_PAT_SECRET  = os.environ.get("GITHUB_PAT_SECRET", "zxcloudsecurity/github-pat")
DRAFTS_BRANCH      = "drafts"
PUBLISH_WORKFLOW   = "publish-guide.yml"

# ---------------------------------------------------------------------------
# Secrets Manager — fetch PAT at runtime, cache for Lambda lifetime
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _get_github_pat() -> str:
    """
    Fetch the GitHub PAT from Secrets Manager.
    Result is cached so subsequent invocations in the same Lambda instance
    don't make repeated API calls.
    """
    log.info(f"Fetching GitHub PAT from Secrets Manager: {GITHUB_PAT_SECRET}")
    client = boto3.client("secretsmanager")
    resp = client.get_secret_value(SecretId=GITHUB_PAT_SECRET)
    secret = resp.get("SecretString", "")
    # Support both plain string and JSON {"token": "ghp_..."} formats
    try:
        parsed = json.loads(secret)
        return parsed.get("token", parsed.get("GITHUB_PAT", secret))
    except (json.JSONDecodeError, AttributeError):
        return secret.strip()


# ---------------------------------------------------------------------------
# Colours (matches publisher.py palette for visual consistency)
# ---------------------------------------------------------------------------

_C = {
    "bg":      "#0f1117",
    "card":    "#1a1f2e",
    "border":  "#2d3348",
    "text":    "#e2e8f0",
    "muted":   "#94a3b8",
    "accent":  "#3b82f6",
    "green":   "#22c55e",
    "red":     "#ef4444",
    "btn_yes": "#15803d",
    "btn_no":  "#374151",
}

# ---------------------------------------------------------------------------
# DynamoDB helpers
# ---------------------------------------------------------------------------

def _get_token_record(token: str) -> dict | None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE)
    resp = table.get_item(Key={"token": token})
    return resp.get("Item")


def _validate_token(token: str, guide_id: str) -> tuple:
    """
    Validate token exists, matches guide_id, is not expired, and is not used.
    Returns (record, error_message). error_message is "" on success.
    """
    if not token or not guide_id:
        return None, "Missing token or guide ID."

    record = _get_token_record(token)
    if not record:
        return None, "Token not found. It may have already been used or expired."

    if record.get("used"):
        return None, "This link has already been used."

    if record.get("guide_id") != guide_id:
        return None, "Token does not match guide ID."

    expires_at = record.get("expires_at", "")
    if expires_at:
        try:
            exp = datetime.fromisoformat(expires_at)
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > exp:
                return None, "This approval link has expired (7-day limit)."
        except Exception:
            pass

    return record, ""


def _mark_token_used(token: str) -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE)
    table.update_item(
        Key={"token": token},
        UpdateExpression="SET #u = :t, used_at = :ts",
        ExpressionAttributeNames={"#u": "used"},
        ExpressionAttributeValues={
            ":t": True,
            ":ts": datetime.now(timezone.utc).isoformat(),
        },
    )


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def _github_request(method: str, path: str, body: dict = None) -> tuple:
    """
    Make a GitHub API request. Returns (status_code, response_dict).
    path should start with / e.g. /repos/owner/repo/actions/workflows/...
    """
    url = f"https://api.github.com{path}"
    headers = {
        "Authorization": f"Bearer {_get_github_pat()}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "ZXCloudSecurity-ApprovalLambda/1.0",
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body_bytes = resp.read()
            return resp.status, json.loads(body_bytes) if body_bytes else {}
    except urllib.error.HTTPError as e:
        body_bytes = e.read()
        log.error(f"GitHub API {method} {path} → {e.code}: {body_bytes[:500]}")
        return e.code, {}
    except Exception as e:
        log.error(f"GitHub API error: {e}")
        return 0, {}


def _trigger_publish_workflow(filename: str, token_value: str) -> bool:
    """Trigger the publish-guide.yml GitHub Actions workflow."""
    path = f"/repos/{GITHUB_REPO}/actions/workflows/{PUBLISH_WORKFLOW}/dispatches"
    status, _ = _github_request("POST", path, {
        "ref": "main",
        "inputs": {
            "guide_filename": filename,
            "token": token_value,
        },
    })
    success = status in (204, 200)
    if success:
        log.info(f"Triggered {PUBLISH_WORKFLOW} for {filename}")
    else:
        log.error(f"Failed to trigger workflow: status {status}")
    return success


def _delete_draft_from_branch(filename: str) -> bool:
    """Delete the draft file from the drafts branch via GitHub API."""
    path = f"/repos/{GITHUB_REPO}/contents/drafts/guides/{filename}"

    # Get current file SHA (required for deletion)
    status, resp = _github_request("GET", f"{path}?ref={DRAFTS_BRANCH}")
    if status != 200:
        log.error(f"Could not get file SHA for {filename}: {status}")
        return False

    sha = resp.get("sha", "")
    if not sha:
        log.error(f"No SHA in response for {filename}")
        return False

    status, _ = _github_request("DELETE", path, {
        "message": f"chore: reject draft {filename} [guide-agent]",
        "sha": sha,
        "branch": DRAFTS_BRANCH,
    })
    success = status in (200, 204)
    if success:
        log.info(f"Deleted draft {filename} from {DRAFTS_BRANCH}")
    else:
        log.error(f"Failed to delete {filename}: status {status}")
    return success


# ---------------------------------------------------------------------------
# SES confirmation email
# ---------------------------------------------------------------------------

def _send_confirmation_email(title: str, action: str, site_url: str = "") -> None:
    """Send a brief confirmation email after approve or reject."""
    if action == "approve":
        subject = f"Published: {title}"
        body_html = f"""<html><body style="font-family:sans-serif;color:#e2e8f0;background:#0f1117;padding:32px;">
<h2 style="color:#22c55e;">Guide published</h2>
<p style="font-size:16px;"><b>{title}</b> is now live on zxcloudsecurity.co.uk.</p>
{f'<p><a href="{site_url}" style="color:#3b82f6;">{site_url}</a></p>' if site_url else ''}
<p style="color:#94a3b8;font-size:13px;">GitHub Actions is building and deploying now - allow 2-3 minutes.</p>
</body></html>"""
        body_text = f"Published: {title}\nLive on zxcloudsecurity.co.uk\nGitHub Actions is deploying now."
    else:
        subject = f"Rejected: {title}"
        body_html = f"""<html><body style="font-family:sans-serif;color:#e2e8f0;background:#0f1117;padding:32px;">
<h2 style="color:#ef4444;">Draft rejected</h2>
<p style="font-size:16px;"><b>{title}</b> has been removed from the drafts branch.</p>
<p style="color:#94a3b8;font-size:13px;">The guide agent will regenerate a replacement on the next run.</p>
</body></html>"""
        body_text = f"Rejected: {title}\nDraft removed from drafts branch."

    try:
        ses = boto3.client("ses")
        ses.send_email(
            Source=SES_FROM_ADDRESS,
            Destination={"ToAddresses": [SES_TO_ADDRESS]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": {
                    "Html": {"Data": body_html, "Charset": "UTF-8"},
                    "Text": {"Data": body_text, "Charset": "UTF-8"},
                },
            },
        )
        log.info(f"Confirmation email sent: {subject}")
    except Exception as e:
        log.error(f"SES confirmation email failed: {e}")


# ---------------------------------------------------------------------------
# HTML page builders (< 10KB, no external dependencies)
# ---------------------------------------------------------------------------

def _page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} - ZX Cloud Security</title>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:{_C['bg']};color:{_C['text']};font-family:-apple-system,BlinkMacSystemFont,
         'Segoe UI',Roboto,Helvetica,Arial,sans-serif;min-height:100vh;
         display:flex;align-items:center;justify-content:center;padding:24px}}
    .card{{background:{_C['card']};border:1.5px solid {_C['border']};border-radius:16px;
           padding:32px 28px;max-width:480px;width:100%}}
    .label{{font-size:12px;font-weight:600;color:{_C['accent']};text-transform:uppercase;
            letter-spacing:1.5px;margin-bottom:12px}}
    h1{{font-size:22px;font-weight:700;line-height:1.3;margin-bottom:8px}}
    .meta{{font-size:14px;color:{_C['muted']};margin-bottom:24px;line-height:1.5}}
    .btn{{display:block;width:100%;padding:16px;border:none;border-radius:10px;
          font-size:17px;font-weight:600;cursor:pointer;text-align:center;
          margin-bottom:12px;text-decoration:none;letter-spacing:0.2px}}
    .btn-yes{{background:{_C['btn_yes']};color:#fff}}
    .btn-no{{background:{_C['btn_no']};color:{_C['text']}}}
    .btn:active{{opacity:0.85}}
    .msg{{text-align:center;font-size:15px;line-height:1.6;padding:8px 0}}
    .msg-icon{{font-size:40px;margin-bottom:12px}}
    .err{{color:{_C['red']}}}
    .ok{{color:{_C['green']}}}
    form{{margin:0}}
  </style>
</head>
<body>
  <div class="card">
    <div class="label">zxcloudsecurity.co.uk</div>
    {body}
  </div>
</body>
</html>"""


def _confirmation_page(action: str, guide_title: str, guide_id: str, token: str) -> str:
    if action == "approve":
        heading   = "Publish this guide?"
        btn_label = "Yes, publish it"
        meta      = "This will trigger a GitHub Actions build and deploy. Allow 2-3 minutes to go live."
    else:
        heading   = "Remove this draft?"
        btn_label = "Yes, remove it"
        meta      = "The draft will be deleted from the drafts branch. The agent will regenerate a replacement."

    body = f"""
    <h1>{heading}</h1>
    <div class="meta">
      <b style="color:{_C['text']}">{guide_title}</b><br>{meta}
    </div>
    <form method="POST">
      <input type="hidden" name="confirmed" value="1">
      <button type="submit" class="btn btn-yes">{btn_label}</button>
    </form>
    <a href="javascript:history.back()" class="btn btn-no">Cancel</a>"""
    return _page(heading, body)


def _success_page(action: str, guide_title: str) -> str:
    if action == "approve":
        icon = "Done"
        msg  = f"<b>{guide_title}</b> has been queued for publishing.<br>GitHub Actions is building now - allow 2-3 minutes."
    else:
        icon = "Done"
        msg  = f"<b>{guide_title}</b> has been removed from the drafts branch."

    body = f"""
    <div class="msg">
      <div class="msg-icon">{icon}</div>
      <p class="ok">{msg}</p>
    </div>"""
    return _page("Done", body)


def _error_page(message: str) -> str:
    body = f"""
    <div class="msg">
      <div class="msg-icon">Error</div>
      <p class="err">{message}</p>
    </div>"""
    return _page("Error", body)


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------

def _html_response(body: str, status: int = 200) -> dict:
    return {
        "statusCode": status,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": body,
    }


def _parse_query(event: dict) -> dict:
    return event.get("queryStringParameters") or {}


def _parse_body(event: dict) -> dict:
    raw = event.get("body", "") or ""
    if event.get("isBase64Encoded"):
        import base64
        raw = base64.b64decode(raw).decode("utf-8", errors="ignore")
    params: dict = {}
    for part in raw.split("&"):
        if "=" in part:
            k, _, v = part.partition("=")
            params[urllib.parse.unquote_plus(k)] = urllib.parse.unquote_plus(v)
    return params


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------

def handle_approve_get(qs: dict) -> dict:
    token    = qs.get("token", "")
    guide_id = qs.get("id", "")
    record, err = _validate_token(token, guide_id)
    if err:
        return _html_response(_error_page(err), 400)
    return _html_response(_confirmation_page("approve", record["guide_title"], guide_id, token))


def handle_approve_post(qs: dict, body: dict) -> dict:
    if not body.get("confirmed"):
        return _html_response(_error_page("Confirmation not received."), 400)

    token    = qs.get("token", "")
    guide_id = qs.get("id", "")
    record, err = _validate_token(token, guide_id)
    if err:
        return _html_response(_error_page(err), 400)

    filename    = record["filename"]
    guide_title = record["guide_title"]

    ok = _trigger_publish_workflow(filename, token)
    if not ok:
        return _html_response(_error_page(
            "Failed to trigger the publish workflow. Please check GitHub Actions and try again."
        ), 500)

    _mark_token_used(token)
    _send_confirmation_email(guide_title, "approve")

    log.info(f"APPROVED: {guide_title} ({filename})")
    return _html_response(_success_page("approve", guide_title))


def handle_reject_get(qs: dict) -> dict:
    token    = qs.get("token", "")
    guide_id = qs.get("id", "")
    record, err = _validate_token(token, guide_id)
    if err:
        return _html_response(_error_page(err), 400)
    return _html_response(_confirmation_page("reject", record["guide_title"], guide_id, token))


def handle_reject_post(qs: dict, body: dict) -> dict:
    if not body.get("confirmed"):
        return _html_response(_error_page("Confirmation not received."), 400)

    token    = qs.get("token", "")
    guide_id = qs.get("id", "")
    record, err = _validate_token(token, guide_id)
    if err:
        return _html_response(_error_page(err), 400)

    filename    = record["filename"]
    guide_title = record["guide_title"]

    ok = _delete_draft_from_branch(filename)
    if not ok:
        return _html_response(_error_page(
            "Failed to delete the draft from GitHub. Please remove it manually from the drafts branch."
        ), 500)

    _mark_token_used(token)
    _send_confirmation_email(guide_title, "reject")

    log.info(f"REJECTED: {guide_title} ({filename})")
    return _html_response(_success_page("reject", guide_title))


# ---------------------------------------------------------------------------
# Main handler
# ---------------------------------------------------------------------------

def lambda_handler(event: dict, context) -> dict:
    log.info(f"Event: method={event.get('requestContext', {}).get('http', {}).get('method')} "
             f"path={event.get('rawPath')}")

    method = event.get("requestContext", {}).get("http", {}).get("method", "GET").upper()
    path   = event.get("rawPath", "/").rstrip("/") or "/"
    qs     = _parse_query(event)
    body   = _parse_body(event) if method == "POST" else {}

    try:
        if path == "/approve" and method == "GET":
            return handle_approve_get(qs)
        elif path == "/approve" and method == "POST":
            return handle_approve_post(qs, body)
        elif path == "/reject" and method == "GET":
            return handle_reject_get(qs)
        elif path == "/reject" and method == "POST":
            return handle_reject_post(qs, body)
        else:
            return _html_response(_error_page("Page not found."), 404)

    except Exception as e:
        log.exception(f"Unhandled error: {e}")
        return _html_response(_error_page(
            "An unexpected error occurred. Please try again or approve via GitHub Actions directly."
        ), 500)
