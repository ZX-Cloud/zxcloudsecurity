"""
seo_dashboard.py
ZX Cloud Security — Weekly SEO Snapshot (email-only)

Pulls rank tracking, domain visibility, and backlink data from DataForSEO,
snapshots it to data/seo_history/ (repo-only, NOT under site/ — never
published, never synced to S3/CloudFront), and emails a summary via SES.

Data sources (all DataForSEO — same account as topic_scorer.py):
  - SERP Live Advanced       per-keyword rank for zxcloudsecurity.co.uk
  - DataForSEO Labs          domain_rank_overview (organic ETV, keyword count)
  - Backlinks API            summary (backlinks, referring domains, domain rank)

NOTE: Backlinks and Labs are separate DataForSEO product lines from the
Keywords Data API used elsewhere in this pipeline. If your account doesn't
have them enabled, those sections degrade gracefully (logged + skipped) —
verify via a manual workflow_dispatch run before trusting the schedule.
Response shapes are logged on every run rather than assumed — see the
"raw keys" log lines — after the items/result parsing bug found 20 June 2026.

Secrets required (all reused from elsewhere in the pipeline):
  DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD
  SES_FROM_ADDRESS, SES_TO_ADDRESS
  AWS_REGION (+ AWS credentials via boto3 default chain)

Output:
  data/seo_history/YYYY-MM-DD.json   dated snapshot (repo-only, not public)
  data/seo_history/index.json        list of all snapshot dates
  Weekly SES email digest — this is the only place results are visible
"""

import json
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

import boto3
import requests
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

DOMAIN = "zxcloudsecurity.co.uk"
LOCATION = "United Kingdom"
LANGUAGE = "English"

SERP_URL = "https://api.dataforseo.com/v3/serp/google/organic/live/advanced"
DOMAIN_RANK_OVERVIEW_URL = "https://api.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live"
BACKLINKS_SUMMARY_URL = "https://api.dataforseo.com/v3/backlinks/summary/live"

# Deliberately OUTSIDE site/ — this directory is never built by Hugo, never
# synced to S3, and never reachable on the public site. Email is the only
# delivery channel for this data (see §1.4-style decision log if/when this
# gets added to the LLD).
HISTORY_DIR = Path("data/seo_history")

# Curated keyword list — keep roughly aligned with published guide topics.
# Kept deliberately short: each keyword is a billed SERP lookup, run weekly.
TRACKED_KEYWORDS = [
    "aws scp best practices",
    "aws guardduty configuration",
    "aws landing zone control tower",
    "aws iam identity centre",
    "aws security hub",
    "cyberark pam aws",
    "ncsc cloud guidance",
    "aws kms key management",
    "cloud security architect day rate uk",
    "aws cloudtrail configuration best practices",
    "aws compliance and governance",
    "cloud security vulnerability management",
    "recent cloud security cves",
    "aws least privilege iam",
    "post quantum cryptography aws",
]


def _auth():
    login = os.environ.get("DATAFORSEO_LOGIN", "")
    password = os.environ.get("DATAFORSEO_PASSWORD", "")
    if not (login and password):
        raise RuntimeError("DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD not set")
    return login, password


def fetch_keyword_rank(keyword: str, login: str, password: str) -> dict:
    """Look up zxcloudsecurity.co.uk's organic rank for a single keyword."""
    payload = [{
        "keyword": keyword,
        "location_name": LOCATION,
        "language_name": LANGUAGE,
        "device": "desktop",
        "depth": 30,
    }]
    try:
        resp = requests.post(SERP_URL, auth=(login, password), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        tasks = data.get("tasks", [])
        if not tasks or tasks[0].get("status_code") != 20000:
            msg = tasks[0].get("status_message") if tasks else "no tasks"
            log.warning(f"  SERP lookup failed for '{keyword}': {msg}")
            return {"keyword": keyword, "found": False, "rank_absolute": None}

        result = tasks[0].get("result") or []
        # SERP live/advanced DOES wrap items under result[0]["items"] — confirmed
        # against this endpoint's actual shape, unlike Keywords Data's
        # google_ads/search_volume/live endpoint (see topic_scorer.py history).
        items = (result[0].get("items") if result else []) or []
        for item in items:
            if item.get("type") != "organic":
                continue
            url = (item.get("url") or "").lower()
            dom = (item.get("domain") or "").lower()
            if DOMAIN in url or DOMAIN in dom:
                return {
                    "keyword": keyword,
                    "found": True,
                    "rank_absolute": item.get("rank_absolute"),
                    "rank_group": item.get("rank_group"),
                    "url": item.get("url"),
                }
        return {"keyword": keyword, "found": False, "rank_absolute": None}

    except requests.RequestException as e:
        log.error(f"  SERP request error for '{keyword}': {e}")
        return {"keyword": keyword, "found": False, "rank_absolute": None, "error": str(e)}


def fetch_domain_overview(login: str, password: str) -> dict:
    """Organic ETV (estimated traffic value) and ranking keyword count."""
    payload = [{"target": DOMAIN, "location_name": LOCATION, "language_name": LANGUAGE}]
    try:
        resp = requests.post(DOMAIN_RANK_OVERVIEW_URL, auth=(login, password), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        tasks = data.get("tasks", [])
        if not tasks or tasks[0].get("status_code") != 20000:
            msg = tasks[0].get("status_message") if tasks else "no tasks"
            log.warning(f"  Domain rank overview failed: {msg} — Labs API may not be enabled")
            return {}
        result = tasks[0].get("result") or []
        if not result:
            return {}
        items = result[0].get("items") or []
        if not items:
            log.warning("  Domain rank overview returned no items — Labs API may not be enabled")
            return {}
        metrics = items[0].get("metrics", {}).get("organic", {})
        log.info(f"  Domain overview raw keys: {list(metrics.keys())}")  # verify shape, don't assume
        return {
            "organic_etv": metrics.get("etv"),
            "organic_count": metrics.get("count"),
            "pos_1": metrics.get("pos_1"),
            "pos_2_3": metrics.get("pos_2_3"),
            "pos_4_10": metrics.get("pos_4_10"),
            "pos_11_20": metrics.get("pos_11_20"),
            "pos_21_30": metrics.get("pos_21_30"),
        }
    except requests.RequestException as e:
        log.error(f"  Domain rank overview request error: {e}")
        return {"error": str(e)}


def fetch_backlinks_summary(login: str, password: str) -> dict:
    """Backlink and referring-domain counts for the domain."""
    payload = [{"target": DOMAIN}]
    try:
        resp = requests.post(BACKLINKS_SUMMARY_URL, auth=(login, password), json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        tasks = data.get("tasks", [])
        if not tasks or tasks[0].get("status_code") != 20000:
            msg = tasks[0].get("status_message") if tasks else "no tasks"
            log.warning(f"  Backlinks summary failed: {msg} — Backlinks API may not be enabled")
            return {}
        result = tasks[0].get("result") or []
        if not result:
            return {}
        item = result[0]
        log.info(f"  Backlinks raw keys: {list(item.keys())}")  # verify shape, don't assume
        return {
            "backlinks": item.get("backlinks"),
            "referring_domains": item.get("referring_domains"),
            "referring_main_domains": item.get("referring_main_domains"),
            "rank": item.get("rank"),
            "broken_backlinks": item.get("broken_backlinks"),
        }
    except requests.RequestException as e:
        log.error(f"  Backlinks summary request error: {e}")
        return {"error": str(e)}


def load_previous_snapshot() -> dict:
    """Load the most recent prior snapshot for week-over-week deltas."""
    index_path = HISTORY_DIR / "index.json"
    if not index_path.exists():
        return {}
    try:
        dates = json.loads(index_path.read_text())
        if not dates:
            return {}
        prev_path = HISTORY_DIR / f"{dates[-1]}.json"
        if prev_path.exists():
            return json.loads(prev_path.read_text())
    except Exception as e:
        log.warning(f"  Could not load previous snapshot: {e}")
    return {}


def save_snapshot(snapshot: dict) -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    date_str = snapshot["date"]
    (HISTORY_DIR / f"{date_str}.json").write_text(json.dumps(snapshot, indent=2))

    index_path = HISTORY_DIR / "index.json"
    dates = []
    if index_path.exists():
        try:
            dates = json.loads(index_path.read_text())
        except Exception:
            dates = []
    if date_str not in dates:
        dates.append(date_str)
    dates.sort()
    index_path.write_text(json.dumps(dates, indent=2))
    log.info(f"  Saved snapshot -> {HISTORY_DIR}/{date_str}.json ({len(dates)} total snapshots)")


def send_digest_email(snapshot: dict, previous: dict) -> None:
    from_addr = os.environ.get("SES_FROM_ADDRESS", "")
    to_addr = os.environ.get("SES_TO_ADDRESS", "")
    region = os.environ.get("AWS_REGION", "eu-west-2")
    if not (from_addr and to_addr):
        log.warning("  SES_FROM_ADDRESS / SES_TO_ADDRESS not set — skipping email digest")
        return

    def delta_html(section, key):
        prev_val = (previous.get(section) or {}).get(key)
        curr_val = (snapshot.get(section) or {}).get(key)
        if prev_val is None or curr_val is None:
            return ""
        diff = curr_val - prev_val
        if diff == 0:
            return " (no change)"
        arrow = "&#9650;" if diff > 0 else "&#9660;"
        colour = "#1E7B34" if diff > 0 else "#B3261E"
        return f' <span style="color:{colour}">{arrow} {abs(diff):.0f}</span>'

    overview = snapshot.get("domain_overview") or {}
    backlinks = snapshot.get("backlinks") or {}
    keywords = snapshot.get("keywords") or []

    ranked = [k for k in keywords if k.get("rank_absolute") is not None]
    ranked_sorted = sorted(ranked, key=lambda k: k["rank_absolute"])
    not_ranked_count = len(keywords) - len(ranked)

    def kw_row(k):
        prev_k = next((p for p in (previous.get("keywords") or []) if p.get("keyword") == k["keyword"]), None)
        change = ""
        if prev_k and prev_k.get("rank_absolute") is not None:
            diff = prev_k["rank_absolute"] - k["rank_absolute"]  # positive = improved
            if diff != 0:
                arrow = "&#9650;" if diff > 0 else "&#9660;"
                colour = "#1E7B34" if diff > 0 else "#B3261E"
                change = f' <span style="color:{colour};font-size:11px;">{arrow}{abs(diff)}</span>'
        return (
            f'<tr><td style="padding:6px 8px;border-bottom:1px solid #333;">{k["keyword"]}</td>'
            f'<td style="padding:6px 8px;border-bottom:1px solid #333;text-align:right;">'
            f'#{k["rank_absolute"]}{change}</td></tr>'
        )

    rows = "".join(kw_row(k) for k in ranked_sorted)
    if not ranked_sorted:
        rows = '<tr><td colspan="2" style="padding:6px 8px;color:#999;">No tracked keywords currently in top 30</td></tr>'

    html = f"""
    <html><body style="margin:0;padding:0;background:#1a1a1a;font-family:-apple-system,Arial,sans-serif;">
      <div style="max-width:480px;margin:0 auto;background:#222;color:#eee;padding:24px;">
        <h2 style="color:#fff;margin-top:0;">Weekly SEO Snapshot — {snapshot['date']}</h2>
        <p style="font-size:14px;color:#aaa;">zxcloudsecurity.co.uk</p>
        <table style="width:100%;border-collapse:collapse;margin:16px 0;">
          <tr><td style="padding:6px 8px;">Organic traffic value (ETV)</td>
              <td style="padding:6px 8px;text-align:right;">{overview.get('organic_etv', 'n/a')}{delta_html('domain_overview','organic_etv')}</td></tr>
          <tr><td style="padding:6px 8px;">Ranking keywords</td>
              <td style="padding:6px 8px;text-align:right;">{overview.get('organic_count', 'n/a')}{delta_html('domain_overview','organic_count')}</td></tr>
          <tr><td style="padding:6px 8px;">Backlinks</td>
              <td style="padding:6px 8px;text-align:right;">{backlinks.get('backlinks', 'n/a')}{delta_html('backlinks','backlinks')}</td></tr>
          <tr><td style="padding:6px 8px;">Referring domains</td>
              <td style="padding:6px 8px;text-align:right;">{backlinks.get('referring_domains', 'n/a')}{delta_html('backlinks','referring_domains')}</td></tr>
        </table>
        <h3 style="color:#fff;font-size:15px;">Tracked keywords currently ranking ({len(ranked_sorted)}/{len(keywords)})</h3>
        <table style="width:100%;border-collapse:collapse;font-size:13px;">{rows}</table>
        <p style="font-size:11px;color:#777;margin-top:16px;">
          {not_ranked_count} tracked keyword(s) not in top 30. Data via DataForSEO, week-over-week vs. previous snapshot.
        </p>
      </div>
    </body></html>
    """

    ses = boto3.client("ses", region_name=region)
    try:
        ses.send_email(
            Source=from_addr,
            Destination={"ToAddresses": [to_addr]},
            Message={
                "Subject": {"Data": f"SEO snapshot — {snapshot['date']}"},
                "Body": {"Html": {"Data": html}},
            },
        )
        log.info("  Digest email sent")
    except ClientError as e:
        log.error(f"  SES send failed: {e}")


def run() -> dict:
    log.info("-" * 60)
    log.info("seo_dashboard.py — ZX Cloud Security")
    log.info("-" * 60)

    login, password = _auth()
    previous = load_previous_snapshot()

    log.info("[1/4] Fetching domain overview (DataForSEO Labs)...")
    overview = fetch_domain_overview(login, password)

    log.info("[2/4] Fetching backlinks summary...")
    backlinks = fetch_backlinks_summary(login, password)

    log.info(f"[3/4] Fetching rank for {len(TRACKED_KEYWORDS)} tracked keyword(s)...")
    keywords = []
    for kw in TRACKED_KEYWORDS:
        result = fetch_keyword_rank(kw, login, password)
        keywords.append(result)
        rank_str = f"#{result['rank_absolute']}" if result.get('rank_absolute') else "not in top 30"
        log.info(f"  {kw}: {rank_str}")

    snapshot = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "domain": DOMAIN,
        "domain_overview": overview,
        "backlinks": backlinks,
        "keywords": keywords,
    }

    log.info("[4/4] Saving snapshot and sending digest...")
    save_snapshot(snapshot)
    send_digest_email(snapshot, previous)

    log.info("Done.")
    return snapshot


if __name__ == "__main__":
    run()