+++
title = "HollowFrame & Matryoshka Backdoor Target Law Firms"
date = "2025-07-31T16:39:31Z"
publishDate = "2026-07-31T16:39:31Z"
slug = "hollowframe-loader-matryoshka-backdoor-spear-phishing-law-firm"
description = "A new Go-based loader and Rust backdoor combo targets law firms via spear-phishing. Learn what cloud security teams should do to defend against this threat"
categories = ["general"]
tags = ["spear-phishing", "malware", "backdoor", "hollowframe", "matryoshka", "endpoint-security", "threat-intelligence", "lnk-abuse"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/hollowframe-loader-deploys-matryoshka.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/hollowframe-loader-deploys-matryoshka.html)

---

Researchers have uncovered a new attack chain targeting a law firm via spear-phishing, using a Go-based loader called HollowFrame and a Rust-based backdoor named Matryoshka. The attack begins with a malicious link in a phishing email leading to an encrypted archive containing a Windows Shortcut file, which triggers a multi-stage infection sequence. The use of lesser-known programming languages and layered delivery techniques suggests a deliberate effort to evade detection.


> **Security Architect's Take:** Enforce email gateway controls to block or quarantine encrypted archives and LNK file attachments, and ensure endpoint detection tooling has coverage for Go and Rust-based binaries. Review egress filtering and lateral movement controls for environments handling sensitive legal or professional services data, as law firms are high-value targets for espionage-motivated threat actors.


**Original advisory:** [HollowFrame Loader Deploys Matryoshka Backdoor in Spear-Phishing Attack on Law Firm](https://thehackernews.com/2026/07/hollowframe-loader-deploys-matryoshka.html)
