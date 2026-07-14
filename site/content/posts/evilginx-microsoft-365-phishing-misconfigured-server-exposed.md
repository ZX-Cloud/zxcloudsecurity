+++
title = "Evilginx M365 Phishing Op Exposed by Misconfigured Server"
date = "2025-07-13T07:30:00Z"
publishDate = "2026-07-13T07:30:00Z"
slug = "evilginx-microsoft-365-phishing-misconfigured-server-exposed"
description = "A misconfigured Python HTTP server exposed three live Evilginx phishing campaigns targeting Microsoft 365. Learn what architects should do to defend agains"
categories = ["general"]
tags = ["azure", "microsoft-365", "evilginx", "phishing", "adversary-in-the-middle", "mfa-bypass", "credential-theft", "opsec"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/misconfigured-server-reveals-three.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/misconfigured-server-reveals-three.html)

---

A threat actor running a Microsoft 365 phishing campaign using the Evilginx adversary-in-the-middle framework accidentally exposed their entire operation by leaving a Python HTTP server with directory listing enabled on a public port. French security firm Lexfo discovered the misconfiguration, recovered the attacker's toolkit and .bash_history, and used that intelligence to pivot to two additional active phishing operations. The incident highlights how attackers make the same operational security mistakes they exploit in their targets.


> **Security Architect's Take:** Review your organisation's Microsoft 365 conditional access policies and enforce phishing-resistant MFA (FIDO2/hardware tokens) rather than TOTP or push-based methods, as Evilginx-style AiTM proxies can bypass traditional MFA entirely. Additionally, deploy Microsoft Defender for Cloud Apps or a CASB to detect anomalous token usage and session hijacking indicators post-authentication.


**Original advisory:** [Misconfigured Server Reveals Three Evilginx Phishing Operations Targeting Microsoft 365](https://thehackernews.com/2026/07/misconfigured-server-reveals-three.html)
