+++
title = "Microsoft 365 Copilot SearchLeak Flaw: Data Theft Risk"
date = "2025-06-15T15:09:05Z"
publishDate = "2026-06-15T15:09:05Z"
slug = "microsoft-365-copilot-searchleak-one-click-data-exfiltration"
description = "Varonis uncovered a one-click exploit chain in Microsoft 365 Copilot Enterprise Search that could exfiltrate emails, files, and MFA codes via a trusted Mic"
categories = ["general"]
tags = ["azure", "microsoft-365", "copilot", "enterprise-search", "data-exfiltration", "phishing-bypass", "mfa", "zero-click-attack"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/one-click-microsoft-365-copilot-flaw.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/one-click-microsoft-365-copilot-flaw.html)

---

Researchers at Varonis Threat Labs discovered a chain of three vulnerabilities in Microsoft 365 Copilot Enterprise Search, dubbed 'SearchLeak', that could be triggered by a single click on a legitimate microsoft.com link. The attack could silently exfiltrate emails, calendar entries, indexed files, and MFA codes without any obvious warning signs. Because the malicious link originated from a trusted Microsoft domain, standard phishing filters and URL-blocking tools would not have flagged it.


> **Security Architect's Take:** Verify that Microsoft's patch for the SearchLeak vulnerability chain has been applied across your Microsoft 365 tenant and review Copilot Enterprise Search permissions to ensure data access is scoped to least-privilege. Additionally, consider whether your existing DLP and CASB controls can detect abnormal Copilot-driven data access patterns, as perimeter URL filtering alone is insufficient against same-domain attack chains.


**Original advisory:** [One-Click Microsoft 365 Copilot Flaw Could Have Let Attackers Steal Emails, Files, and MFA Codes](https://thehackernews.com/2026/06/one-click-microsoft-365-copilot-flaw.html)
