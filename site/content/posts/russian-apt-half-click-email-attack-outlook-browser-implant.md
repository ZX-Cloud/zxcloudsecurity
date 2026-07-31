+++
title = "Russian Spies Target Outlook with Persistent Email Attack"
date = "2025-07-30T10:29:00Z"
publishDate = "2026-07-30T10:29:00Z"
slug = "russian-apt-half-click-email-attack-outlook-browser-implant"
description = "Russian threat actors have extended their half-click email attack to Microsoft Outlook, deploying a browser implant that survives password resets and devic"
categories = ["general"]
tags = ["azure", "microsoft-365", "outlook", "apt", "phishing", "browser-implant", "persistence", "nation-state"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/30/russian-spies-take-their-half-click-email-attack-from-zimbra-to-outlook/5281033"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/30/russian-spies-take-their-half-click-email-attack-from-zimbra-to-outlook/5281033)

---

Russian state-sponsored threat actors have adapted their 'half-click' phishing technique — previously used against Zimbra — to target Microsoft Outlook users. Opening a malicious email deploys a browser implant that persists even after the victim changes their password or rebuilds their device. This makes the attack particularly dangerous as traditional remediation steps are insufficient to remove the compromise.


> **Security Architect's Take:** Review conditional access policies to enforce device compliance and phishing-resistant MFA (e.g. FIDO2) across your Microsoft 365 estate, as credential resets alone will not remediate this implant. Additionally, audit browser extension controls and consider deploying endpoint detection capable of identifying persistent browser-level implants.


**Original advisory:** [Russian spies take their half-click email attack from Zimbra to Outlook](https://www.theregister.com/security/2026/07/30/russian-spies-take-their-half-click-email-attack-from-zimbra-to-outlook/5281033)
