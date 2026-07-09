+++
title = "Ghost Phishing Bypasses Email Security | EvilTokens"
date = "2025-07-08T13:00:00Z"
publishDate = "2026-07-08T13:00:00Z"
slug = "eviltokens-ghost-phishing-bypasses-email-security-microsoft-365"
description = "The EvilTokens ghost phishing campaign evades URL scanning by decrypting malicious pages in-browser, putting Microsoft 365 accounts at risk across the US a"
categories = ["general"]
tags = ["phishing", "microsoft-365", "azure", "email-security", "browser-based-attack", "credential-theft", "evilTokens", "mfa-bypass"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-ghost-phishing-wave-is-breaking.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-ghost-phishing-wave-is-breaking.html)

---

A phishing campaign dubbed EvilTokens is using 'ghost phishing' to evade traditional email security tools by keeping malicious payloads encrypted until they are decrypted and rendered live inside the victim's browser. This means standard URL reputation checks and email gateway scanners see nothing suspicious at the point of delivery. Businesses using Microsoft 365 are particularly at risk, as successful attacks can result in account compromise and sensitive data exposure.


> **Security Architect's Take:** Review your reliance on static URL scanning at the email gateway — consider deploying browser isolation or remote browser rendering for all inbound links, and enable Microsoft 365 Defender's Safe Links with dynamic, time-of-click detonation to catch payloads that only materialise in the browser. Audit conditional access policies and enforce phishing-resistant MFA (e.g. FIDO2) to limit the blast radius if credentials are harvested.


**Original advisory:** [New Ghost Phishing Wave Is Breaking Traditional Email Security](https://thehackernews.com/2026/07/new-ghost-phishing-wave-is-breaking.html)
