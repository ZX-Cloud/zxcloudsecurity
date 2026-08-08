+++
title = "Phishing Attack Breaches US Defence Supplier M365"
date = "2025-08-07T11:32:00Z"
publishDate = "2026-08-07T11:32:00Z"
slug = "phishing-attack-us-defence-supplier-microsoft-365-breach-ieh-corp"
description = "A phishing attack gave an attacker access to IEH Corp's Microsoft 365 tenant, exposing engineering files and potentially export-controlled technical data."
categories = ["general"]
tags = ["azure", "microsoft-365", "phishing", "itar", "data-breach", "conditional-access", "mfa", "defence-sector"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/08/07/ieh-corp-says-phished-staffer-opened-gates-to-company-m365/5284523"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/08/07/ieh-corp-says-phished-staffer-opened-gates-to-company-m365/5284523)

---

A US defence supplier, IEH Corp, suffered a data breach after an employee fell victim to a phishing attack that gave the attacker access to the company's Microsoft 365 environment. The intruder was able to access engineering files and potentially export-controlled technical data, which may carry serious legal and national security implications. This incident highlights the ongoing risk of phishing as an initial access vector into cloud productivity platforms holding sensitive data.


> **Security Architect's Take:** Review and enforce phishing-resistant MFA (e.g. FIDO2/passkeys) across all Microsoft 365 accounts, particularly for staff handling sensitive or export-controlled data — password-based MFA alone is insufficient against modern phishing kits that proxy credentials in real time. Additionally, implement Conditional Access policies restricting M365 access to managed, compliant devices and consider Microsoft Purview sensitivity labels to limit exfiltration of controlled technical documents.


**Original advisory:** [Attacker phished way into US defense supplier's Microsoft 365 account](https://www.theregister.com/security/2026/08/07/ieh-corp-says-phished-staffer-opened-gates-to-company-m365/5284523)
