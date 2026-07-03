+++
title = "SharePoint RCE Added to CISA KEV — Patch Now"
date = "2026-07-02T14:40:30Z"
publishDate = "2026-07-02T14:40:30Z"
slug = "microsoft-sharepoint-rce-cisa-kev-on-premises"
description = "CISA adds SharePoint RCE vulnerability to its KEV list. Attackers need only a valid account to exploit on-prem servers. Patch immediately."
categories = ["general"]
tags = ["microsoft", "sharepoint", "remote-code-execution", "cisa-kev", "on-premises", "patch-management", "active-exploitation"]
severity = "Critical"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/02/microsoft-said-exploitation-was-less-likely-but-cisa-just-added-sharepoint-rce-to-kev-list/5265886"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/02/microsoft-said-exploitation-was-less-likely-but-cisa-just-added-sharepoint-rce-to-kev-list/5265886)

---

A remote code execution vulnerability in Microsoft SharePoint on-premises servers has been added to CISA's Known Exploited Vulnerabilities catalogue, meaning it is actively being used in real-world attacks. Exploitation requires only a valid SharePoint account, making the barrier to attack unusually low. Microsoft had previously assessed exploitation as 'less likely', but CISA's addition signals that assessment was incorrect and patching is now urgent.


> **Security Architect's Take:** Audit your estate immediately for unpatched on-premises SharePoint deployments and apply Microsoft's available patch without delay — CISA's KEV listing means federal agencies have a binding deadline, but the low authentication requirement makes this a priority for all organisations running on-prem SharePoint. If patching cannot be done immediately, consider restricting SharePoint access to known IP ranges or VPN and reviewing authentication logs for anomalous account activity.


**Original advisory:** [Microsoft said exploitation was 'less likely' ... but CISA just added SharePoint RCE to KEV list](https://www.theregister.com/security/2026/07/02/microsoft-said-exploitation-was-less-likely-but-cisa-just-added-sharepoint-rce-to-kev-list/5265886)
