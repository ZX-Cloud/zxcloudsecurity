+++
title = "EvilTokens BEC Kit: Device-Code Phishing Threat"
date = "2025-07-01T21:50:25Z"
publishDate = "2026-07-01T21:50:25Z"
slug = "eviltokens-device-code-phishing-bec-microsoft365"
description = "EvilTokens is a full BEC operations platform exploiting OAuth device-code flow to steal tokens and bypass MFA in Microsoft 365 environments."
categories = ["general"]
tags = ["azure", "microsoft-365", "phishing", "bec", "oauth", "device-code-flow", "token-theft", "mfa-bypass"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/cyber-crime/2026/07/01/eviltokens-device-code-phishing-kit-totally-more-evil-than-we-all-thought/5265409"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/cyber-crime/2026/07/01/eviltokens-device-code-phishing-kit-totally-more-evil-than-we-all-thought/5265409)

---

EvilTokens is a device-code phishing kit that has been revealed to be far more capable than initially understood, functioning as a full business email compromise (BEC) operations platform according to Cisco Talos researchers. It exploits the OAuth device authorisation flow to steal authentication tokens from victims without requiring them to enter credentials on a fake login page. This makes it particularly dangerous as it bypasses multi-factor authentication and can grant persistent access to Microsoft 365 and other cloud services.


> **Security Architect's Take:** Audit your Azure AD and Microsoft 365 conditional access policies to block or restrict device code flow authentication (OAuth 2.0 device authorisation grant) where it is not operationally required, and monitor for unusual token issuance events via Microsoft Entra ID sign-in logs. Consider deploying Defender for Cloud Apps policies to alert on anomalous delegated permissions or token-based access from unexpected locations.


**Original advisory:** [EvilTokens device-code phishing kit totally more evil than we all thought](https://www.theregister.com/cyber-crime/2026/07/01/eviltokens-device-code-phishing-kit-totally-more-evil-than-we-all-thought/5265409)
