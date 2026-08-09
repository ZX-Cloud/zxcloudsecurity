+++
title = "CSS Attacks Break Webmail Defences to Steal Tokens"
date = "2025-08-08T08:03:57Z"
publishDate = "2026-08-08T08:03:57Z"
slug = "css-attacks-webmail-defences-password-token-theft"
description = "New CSS injection research bypasses webmail sandboxing in Gmail, Outlook, and Proton Mail to steal passwords, tokens, and hijack UI actions."
categories = ["general"]
tags = ["webmail", "css-injection", "gmail", "outlook", "proton-mail", "session-hijacking", "content-security-policy", "email-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/new-css-attacks-can-break-webmail.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/new-css-attacks-can-break-webmail.html)

---

Newly published research demonstrates that malicious CSS embedded within emails can break out of the message rendering boundary in major webmail clients, including Gmail, Outlook, Proton Mail, and Yahoo Mail. Attackers can exploit these techniques to steal passwords and session tokens, hijack trusted UI elements, and manipulate AI-powered email assistants. The attack surface is broad, affecting widely used consumer and enterprise webmail platforms without requiring any user interaction beyond opening a message.


> **Security Architect's Take:** Review your organisation's webmail deployment and enforce strict Content Security Policy (CSP) headers on any self-hosted webmail infrastructure; for SaaS webmail, track vendor patch status for Outlook on the web and similar services and consider blocking HTML email rendering at the gateway for high-risk user populations pending fixes.


**Original advisory:** [New CSS Attacks Can Break Webmail Defenses to Steal Passwords and Tokens](https://thehackernews.com/2026/08/new-css-attacks-can-break-webmail.html)
