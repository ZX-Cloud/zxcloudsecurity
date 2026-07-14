+++
title = "Forg365 PhaaS: Microsoft 365 Device Code & AitM Attack"
date = "2025-07-13T13:03:33Z"
publishDate = "2026-07-13T13:03:33Z"
slug = "forg365-phaas-microsoft-365-device-code-aitm-session-theft"
description = "Forg365 PhaaS targets Microsoft 365 with device code phishing and AitM session theft, bypassing MFA. Learn what cloud architects should do now."
categories = ["general"]
tags = ["azure", "microsoft-365", "phishing-as-a-service", "device-code-phishing", "adversary-in-the-middle", "session-hijacking", "mfa-bypass", "entra-id"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/forg365-phaas-targets-microsoft-365.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/forg365-phaas-targets-microsoft-365.html)

---

Forg365 is a phishing-as-a-service platform sold via Telegram for $400/month that targets Microsoft 365 accounts using device code phishing and adversary-in-the-middle techniques to steal authenticated sessions, bypassing MFA entirely. It also incorporates AI-generated lures and antibot evasion to increase success rates and avoid detection. This is significant because it industrialises sophisticated attack techniques, lowering the barrier for threat actors to compromise enterprise M365 tenants at scale.


> **Security Architect's Take:** Disable device code flow authentication in Azure AD Conditional Access policies unless explicitly required, and enforce Continuous Access Evaluation (CAE) with token binding where possible to limit the usefulness of stolen session tokens. Monitor for anomalous OAuth token usage and unfamiliar device registrations as indicators of device code phishing attempts.


**Original advisory:** [Forg365 PhaaS Targets Microsoft 365 with Device Code and AitM Session Theft](https://thehackernews.com/2026/07/forg365-phaas-targets-microsoft-365.html)
