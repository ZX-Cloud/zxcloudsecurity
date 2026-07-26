+++
title = "Insurance Phishing Evolves Into Real-Time Account Hijacking"
date = "2025-07-25T10:14:21Z"
publishDate = "2026-07-25T10:14:21Z"
slug = "insurance-phishing-real-time-account-hijacking-adversary-in-the-middle"
description = "CTM360 research reveals insurance phishing has shifted to real-time session hijacking, bypassing MFA and rendering stolen credentials instantly usable."
categories = ["general"]
tags = ["phishing", "account-hijacking", "adversary-in-the-middle", "mfa-bypass", "session-hijacking", "credential-theft", "financial-services", "identity-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/ctm360-research-reveals-how-insurance.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/ctm360-research-reveals-how-insurance.html)

---

Phishing campaigns targeting insurance customers have evolved beyond simple credential harvesting into real-time account hijacking, where attackers intercept sessions as they happen rather than using stolen passwords later. This adversary-in-the-middle approach bypasses traditional defences such as password resets and basic MFA, making compromise immediate and harder to detect. The shift represents a significant escalation in sophistication for financially motivated phishing operations.


> **Security Architect's Take:** Review your identity protection controls to ensure MFA implementations use phishing-resistant methods such as FIDO2/passkeys rather than OTP or SMS, which are vulnerable to real-time relay attacks. Additionally, implement continuous session validation and anomalous login detection in your cloud identity platforms to catch hijacked sessions even after initial authentication succeeds.


**Original advisory:** [CTM360 Research Reveals How Insurance Phishing Has Evolved Into Real-Time Account Hijacking](https://thehackernews.com/2026/07/ctm360-research-reveals-how-insurance.html)
