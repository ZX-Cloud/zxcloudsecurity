+++
title = "Greatness PhaaS Adds Device Code Phishing to Bypass MFA"
date = "2025-08-04T17:27:39Z"
publishDate = "2026-08-04T17:27:39Z"
slug = "greatness-phaas-device-code-phishing-bypass-mfa-oauth-token-theft"
description = "The Greatness PhaaS toolkit now supports OAuth 2.0 device code phishing, bypassing MFA to steal tokens. Learn how cloud architects can defend against it."
categories = ["general"]
tags = ["azure", "phishing", "oauth", "mfa-bypass", "entra-id", "adversary-in-the-middle", "token-theft", "phaas"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/greatness-phaas-adds-device-code.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/greatness-phaas-adds-device-code.html)

---

The Greatness phishing-as-a-service toolkit has added support for device code phishing, a technique that abuses the OAuth 2.0 Device Authorization Grant flow to bypass MFA and steal authentication tokens. Attackers trick users into entering a device code on a legitimate Microsoft login page, handing over a valid session token without ever exposing their credentials. This makes the attack particularly dangerous because MFA provides no protection — the victim authenticates legitimately, and the attacker receives a fully authorised token.


> **Security Architect's Take:** Restrict or block the OAuth 2.0 Device Authorization Grant flow in your tenant via Conditional Access policies unless it is explicitly required for device scenarios — in Microsoft Entra ID, this can be enforced by blocking device code flow authentication. Additionally, deploy token protection (token binding) in Conditional Access and monitor for anomalous device code authentication attempts, particularly from unexpected locations or user agents.


**Original advisory:** [Greatness PhaaS Adds Device Code Phishing to Bypass MFA and Steal Tokens](https://thehackernews.com/2026/08/greatness-phaas-adds-device-code.html)
