"""
indexnow.py
ZX Cloud Security — IndexNow URL submission

Reads new_post_slugs.json written by generate.py and submits the live
URLs to the IndexNow API (Bing, Yandex, etc.) for same-day indexing.

Called from daily-pipeline.yml after the S3 deploy step.
"""

import json
import logging
import sys
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

HOST        = "zxcloudsecurity.co.uk"
BASE_URL    = f"https://{HOST}"
KEY         = "ac748b50bbec4b2d92049c151fbe5374"
KEY_URL     = f"{BASE_URL}/{KEY}.txt"
API_URL     = "https://api.indexnow.org/IndexNow"
SLUGS_FILE  = "new_post_slugs.json"


def submit(urls: list[str]) -> bool:
    if not urls:
        log.info("No new URLs to submit to IndexNow.")
        return True

    payload = {
        "host":        HOST,
        "key":         KEY,
        "keyLocation": KEY_URL,
        "urlList":     urls,
    }

    log.info(f"Submitting {len(urls)} URL(s) to IndexNow ...")
    for u in urls:
        log.info(f"  {u}")

    try:
        r = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=15,
        )
        if r.status_code in (200, 202):
            log.info(f"IndexNow accepted: HTTP {r.status_code}")
            return True
        else:
            log.error(f"IndexNow rejected: HTTP {r.status_code} — {r.text[:200]}")
            return False
    except requests.RequestException as e:
        log.error(f"IndexNow request failed: {e}")
        return False


def main() -> int:
    slugs_path = Path(SLUGS_FILE)
    if not slugs_path.exists():
        log.warning(f"{SLUGS_FILE} not found — skipping IndexNow submission.")
        return 0

    slugs = json.loads(slugs_path.read_text())
    if not slugs:
        log.info("No new slugs in file — nothing to submit.")
        return 0

    urls = [f"{BASE_URL}/posts/{slug}/" for slug in slugs]
    success = submit(urls)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
