+++
title = "Opera GX Flaw: Malicious Sites Auto-Install Data-Stealing Mo"
date = "2025-07-06T07:27:50Z"
publishDate = "2026-07-06T07:27:50Z"
slug = "opera-gx-flaw-malicious-sites-auto-install-extensions-data-theft"
description = "A patched Opera GX vulnerability let malicious sites silently install browser extensions to steal data from visited pages, including Gmail addresses."
categories = ["general"]
tags = ["opera-gx", "browser-security", "malicious-extensions", "data-exfiltration", "drive-by-install", "endpoint-security", "browser-extension"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/opera-gx-flaw-let-malicious-sites-auto.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/opera-gx-flaw-let-malicious-sites-auto.html)

---

A vulnerability in Opera GX allowed malicious websites to silently install browser extensions without user interaction, which could then extract data from pages the victim visited. Researchers demonstrated the flaw by reconstructing a user's full Gmail address from a single page visit with no clicks required. Opera has since patched the issue and reports no evidence of active exploitation.


> **Security Architect's Take:** Organisations permitting Opera GX on managed endpoints should verify the patched version is deployed via endpoint management tooling. More broadly, review browser extension governance policies — consider blocking unapproved extension installs via browser enterprise policy or EDR controls, particularly for browsers used in cloud console access.


**Original advisory:** [Opera GX Flaw Let Malicious Sites Auto-Install Mods to Steal Data From Visited Pages](https://thehackernews.com/2026/07/opera-gx-flaw-let-malicious-sites-auto.html)
