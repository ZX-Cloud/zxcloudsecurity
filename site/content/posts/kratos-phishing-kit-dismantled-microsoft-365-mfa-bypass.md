+++
title = "Kratos Phishing Kit Dismantled: M365 MFA Bypass"
date = "2025-07-22T06:38:45Z"
publishDate = "2026-07-22T06:38:45Z"
slug = "kratos-phishing-kit-dismantled-microsoft-365-mfa-bypass"
description = "Law enforcement dismantles Kratos phishing kit that stole Microsoft 365 session tokens and bypassed MFA. What cloud architects need to know."
categories = ["general"]
tags = ["azure", "microsoft-365", "phishing", "mfa-bypass", "session-hijacking", "adversary-in-the-middle", "entra-id", "identity-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/police-dismantle-kratos-phishing-kit.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/police-dismantle-kratos-phishing-kit.html)

---

German and US law enforcement have dismantled the infrastructure behind Kratos, a widely-used phishing kit designed to steal Microsoft 365 session tokens and bypass multi-factor authentication. Indonesian authorities have arrested the individual alleged to have built and operated the service. The takedown is significant because adversary-in-the-middle phishing kits of this type represent one of the most effective methods for circumventing MFA protections that organisations rely upon.


> **Security Architect's Take:** Review your Microsoft 365 tenant for suspicious conditional access anomalies and unfamiliar session tokens, and prioritise deploying phishing-resistant MFA (FIDO2/passkeys) over SMS or TOTP, as these are immune to session-hijacking phishing kits like Kratos. Additionally, enable Microsoft Entra ID token protection and continuous access evaluation to limit the usefulness of stolen session tokens.


**Original advisory:** [Police Dismantle Kratos Phishing Kit Built to Steal Microsoft 365 Sessions and Bypass MFA](https://thehackernews.com/2026/07/police-dismantle-kratos-phishing-kit.html)
