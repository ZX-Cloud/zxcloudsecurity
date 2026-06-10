"""
generate_guides.py
ZX Cloud Security — Evergreen SEO Content Generator

One-off / occasional script. Generates in-depth evergreen guide pages via the
Claude API and writes them as Hugo markdown into site/content/guides/.

These are long-tail SEO pages aimed at cloud security architects. Run this
manually when you want to add or regenerate guide content — it is NOT part of
the daily pipeline.

Usage:
    set ANTHROPIC_API_KEY=your-key
    python generate_guides.py
"""

import json
import logging
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 4096
MAX_RETRIES = 3
RETRY_DELAY = 5

OUTPUT_DIR = Path("site/content/guides")

# ---------------------------------------------------------------------------
# Guide topics — each becomes one evergreen page
# ---------------------------------------------------------------------------

GUIDES = [
    {
        "slug": "shared-responsibility-model-cloud-security",
        "title": "What is the Shared Responsibility Model in Cloud Security?",
        "keywords": ["shared responsibility model", "cloud security", "AWS", "Azure", "GCP"],
        "brief": "Explain the shared responsibility model across AWS, Azure and GCP. Cover what the cloud provider secures vs what the customer secures, common misconceptions, and how it differs between IaaS, PaaS and SaaS.",
    },
    {
        "slug": "what-is-cspm-cloud-security-posture-management",
        "title": "What is CSPM (Cloud Security Posture Management)?",
        "keywords": ["CSPM", "cloud security posture management", "misconfiguration", "compliance"],
        "brief": "Explain what CSPM is, why misconfigurations are the leading cause of cloud breaches, what CSPM tools do, and how architects should approach posture management across multi-cloud environments.",
    },
    {
        "slug": "what-is-zero-trust-architecture",
        "title": "What is Zero Trust Architecture?",
        "keywords": ["zero trust", "identity", "least privilege", "network security"],
        "brief": "Explain Zero Trust ('never trust, always verify'), why identity has become the new perimeter, the core principles, and a practical roadmap for adopting Zero Trust in a cloud environment.",
    },
    {
        "slug": "aws-iam-security-best-practices",
        "title": "AWS IAM Security Best Practices",
        "keywords": ["AWS IAM", "least privilege", "roles", "policies", "MFA"],
        "brief": "Provide a practical, actionable set of AWS IAM best practices: least privilege, roles over users, MFA, avoiding long-lived keys, permission boundaries, SCPs, and access analysis. Aimed at experienced architects.",
    },
    {
        "slug": "securing-ai-agents-cloud-infrastructure",
        "title": "Securing AI Agents with Access to Cloud Infrastructure",
        "keywords": ["AI agents", "agentic AI", "cloud security", "model security", "least privilege"],
        "brief": "A 2026-relevant guide on the risks of giving AI agents access to production cloud infrastructure: prompt injection, over-privileged agents, supply chain risks, and how to apply least privilege and guardrails to autonomous agents.",
    },
    {
        "slug": "what-is-dspm-data-security-posture-management",
        "title": "What is DSPM (Data Security Posture Management)?",
        "keywords": ["DSPM", "data security posture management", "data discovery", "classification"],
        "brief": "Explain DSPM: discovering and classifying sensitive data across cloud environments, why it matters, how it differs from CSPM, and practical steps for architects to reduce data exposure risk.",
    },
    {
        "slug": "what-is-ciem-cloud-infrastructure-entitlement-management",
        "title": "What is CIEM (Cloud Infrastructure Entitlement Management)?",
        "keywords": ["CIEM", "entitlements", "permissions", "least privilege", "identity"],
        "brief": "Explain CIEM: managing identities and entitlements at cloud scale, the problem of permission sprawl and excessive privileges, and how CIEM tools help architects enforce least privilege across multi-cloud.",
    },
    {
        "slug": "kubernetes-security-best-practices",
        "title": "Kubernetes Security Best Practices",
        "keywords": ["Kubernetes", "K8s security", "container security", "RBAC", "CKS"],
        "brief": "A practical guide to Kubernetes security: RBAC, network policies, pod security standards, secrets management, image scanning, and runtime security. Aligned with CKS exam topics. Aimed at architects running EKS/GKE/AKS.",
    },
]

# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a senior cloud security architect writing in-depth evergreen
educational content for zxcloudsecurity.co.uk, a UK-based cloud security publication.

Write authoritative, genuinely useful long-form content in professional UK English.
Your readers are experienced cloud security architects and engineers — write at their level,
be specific and practical, avoid fluff and filler. Use concrete examples, real service names,
and actionable guidance. Aim for 900-1300 words.

Return ONLY clean Markdown body content. Do NOT include a top-level H1 title (the site adds that).
Use ## and ### subheadings, bullet points, and short paragraphs. No preamble, no meta-commentary."""


def build_prompt(guide: dict) -> str:
    return f"""Write an in-depth evergreen guide titled "{guide['title']}".

Brief: {guide['brief']}

Target keywords (work in naturally, do not stuff): {', '.join(guide['keywords'])}

Structure:
- Open with a concise 2-3 sentence summary answering the core question directly (good for featured snippets)
- Then ## subheadings breaking down the topic logically
- Include a practical "Best practices" or "What architects should do" section with actionable bullets
- End with a short "Key takeaways" section

Write 900-1300 words of genuinely useful content. UK English. No H1 title."""


def call_claude(guide: dict, api_key: str) -> str | None:
    prompt = build_prompt(guide)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                ANTHROPIC_API_URL,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=60,
            )
            if resp.status_code in (429, 529):
                wait = RETRY_DELAY * attempt
                log.warning(f"  Rate limited/overloaded — waiting {wait}s")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            text = ""
            for block in data.get("content", []):
                if block.get("type") == "text":
                    text += block.get("text", "")
            return text.strip()
        except requests.RequestException as e:
            log.error(f"  API error (attempt {attempt}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
    return None


def build_frontmatter(guide: dict) -> str:
    date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    title = guide["title"].replace('"', '\\"')
    keywords_toml = ", ".join(f'"{k}"' for k in guide["keywords"])
    description = f"{guide['title']} — a practical guide for cloud security architects."
    return f"""+++
title = "{title}"
date = "{date}"
slug = "{guide['slug']}"
description = "{description}"
keywords = [{keywords_toml}]
type = "guides"
draft = false
+++
"""


def generate_guides(api_key: str | None = None, force: bool = False) -> int:
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    skipped = 0

    for i, guide in enumerate(GUIDES, 1):
        filepath = OUTPUT_DIR / f"{guide['slug']}.md"

        # Skip guides that already exist (add-only mode) unless --force is passed.
        # This protects published, indexed content from being regenerated/changed.
        if filepath.exists() and not force:
            log.info(f"[{i}/{len(GUIDES)}] Skipping (already exists): {guide['slug']}")
            skipped += 1
            continue

        log.info(f"[{i}/{len(GUIDES)}] Generating: {guide['title']}")
        body = call_claude(guide, api_key)
        if not body:
            log.warning(f"  ✗ Failed — skipping {guide['slug']}")
            continue

        # Strip any accidental H1 the model added
        body = re.sub(r"^#\s+.*\n", "", body).strip()

        content = build_frontmatter(guide) + "\n" + body + "\n"
        filepath = OUTPUT_DIR / f"{guide['slug']}.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        log.info(f"  ✓ Wrote {filepath.name} ({len(body)} chars)")
        written += 1
        time.sleep(1)

    log.info(f"Generated {written} new guide(s), skipped {skipped} existing, in {OUTPUT_DIR}")
    return written


if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    if force:
        print("⚠️  --force enabled: existing guides WILL be regenerated and overwritten.\n")
    count = generate_guides(force=force)
    print(f"\n{'─'*50}")
    print(f"  New guide pages generated : {count}")
    print(f"  Output directory          : {OUTPUT_DIR}")
    print(f"{'─'*50}\n")
    print("Now run: cd site && hugo server  (check /guides/)")
    print("Then commit and push — the daily pipeline will keep them live.")
