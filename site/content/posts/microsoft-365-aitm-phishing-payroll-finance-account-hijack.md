+++
title = "Microsoft 365 AitM Phishing Targets Payroll & Finance"
date = "2025-08-07T10:38:27Z"
publishDate = "2026-08-07T10:38:27Z"
slug = "microsoft-365-aitm-phishing-payroll-finance-account-hijack"
description = "Attackers use adversary-in-the-middle phishing to hijack Microsoft 365 accounts, bypassing MFA to target payroll and finance staff email."
categories = ["general"]
tags = ["azure", "microsoft-365", "phishing", "aitm", "entra-id", "mfa-bypass", "business-email-compromise", "conditional-access"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/microsoft-365-aitm-phishing-hijacks.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/microsoft-365-aitm-phishing-hijacks.html)

---

Attackers are running a large-scale phishing campaign that uses adversary-in-the-middle (AitM) techniques to bypass multi-factor authentication and hijack Microsoft 365 accounts. Once inside, they specifically target staff involved in payroll and finance workflows to harvest sensitive emails and likely enable further fraud. Residential proxies are used to make the malicious logins appear as normal consumer traffic, helping evade detection.


> **Security Architect's Take:** Enforce phishing-resistant MFA (FIDO2/passkeys) across all Microsoft 365 accounts, particularly for finance and HR personas, and deploy Conditional Access policies that flag or block sign-ins from residential proxy ranges and unexpected locations. Review Entra ID sign-in logs for token replay indicators and anomalous session activity, and consider enabling Microsoft Defender for Office 365's URL detonation and session anomaly alerts.


**Original advisory:** [Microsoft 365 AitM Phishing Hijacks Accounts to Collect Payroll and Finance Emails](https://thehackernews.com/2026/08/microsoft-365-aitm-phishing-hijacks.html)
