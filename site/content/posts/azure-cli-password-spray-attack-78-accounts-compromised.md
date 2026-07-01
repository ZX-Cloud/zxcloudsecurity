+++
title = "Azure CLI Password Spray Attack: 78 Accounts Compromised"
date = "2025-07-01T05:46:03Z"
publishDate = "2026-07-01T05:46:03Z"
slug = "azure-cli-password-spray-attack-78-accounts-compromised"
description = "An automated password spray targeting Azure CLI has made 81M+ attempts, compromising 78+ accounts. Learn how to detect and defend against this ongoing thre"
categories = ["general"]
tags = ["azure", "azure-cli", "password-spray", "credential-attack", "mfa", "identity", "brute-force", "microsoft-entra-id"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/azure-cli-password-spray-hits-at-least.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/azure-cli-password-spray-hits-at-least.html)

---

A large-scale automated password spray attack is actively targeting Microsoft Azure's command-line interface (CLI), with over 81 million login attempts recorded between 12 and 26 June, compromising at least 78 accounts. The attack originates from an IPv6 range linked to infrastructure provider LSHIY LLC and is ongoing. This is significant because Azure CLI access can grant broad programmatic control over cloud resources, making compromised accounts a serious risk.


> **Security Architect's Take:** Immediately review Azure AD sign-in logs for authentication attempts from the 2a0a:d683::/32 IPv6 range and enforce phishing-resistant MFA (e.g. FIDO2 or certificate-based auth) for all Azure CLI and service principal access — password-only authentication should be disabled for any account with programmatic cloud access.


**Original advisory:** [Azure CLI Password Spray Hits at Least 78 Microsoft Accounts in 81M+ Attempts](https://thehackernews.com/2026/07/azure-cli-password-spray-hits-at-least.html)
