+++
title = "Kali365 Abuses Microsoft Device Code Auth to Steal Tokens"
date = "2025-08-05T11:43:19Z"
publishDate = "2026-08-05T11:43:19Z"
slug = "kali365-microsoft-device-code-phishing-oauth-token-theft"
description = "The Kali365 phishing kit exploits Microsoft's device code authentication flow to harvest OAuth tokens, giving attackers persistent access to email and clou"
categories = ["general"]
tags = ["azure", "microsoft-entra-id", "phishing", "oauth", "device-code-flow", "token-theft", "identity-security", "microsoft-365"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/kali365-weaponizes-microsoft.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/kali365-weaponizes-microsoft.html)

---

A phishing kit called Kali365 abuses Microsoft's legitimate device code authentication flow to trick employees at US organisations into approving attacker-controlled login requests. Once approved, attackers obtain valid access and refresh tokens, granting persistent access to email, files, and cloud services without needing the victim's password. Because the authentication happens on Microsoft's genuine login page, traditional phishing indicators are absent, making this particularly difficult for end users to detect.


> **Security Architect's Take:** Audit and restrict device code flow authentication in your Microsoft Entra ID (Azure AD) conditional access policies — block or limit it to managed, compliant devices only, and consider disabling it entirely for users who have no legitimate need. Review token lifetimes and enable continuous access evaluation to reduce the window of exposure if tokens are compromised.


**Original advisory:** [Kali365 Weaponizes Microsoft Authentication Against US Companies: New Enterprise Risk](https://thehackernews.com/2026/08/kali365-weaponizes-microsoft.html)
