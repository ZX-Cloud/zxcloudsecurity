+++
title = "Russian Zero-Click Email Attacks: What You Must Know"
date = "2025-07-23T16:47:02Z"
publishDate = "2026-07-23T16:47:02Z"
slug = "russian-zero-click-email-phishing-campaign-2026"
description = "A year-long Russian phishing campaign infects users the moment they preview an email. Learn what cloud security architects must do to defend their organisa"
categories = ["general"]
tags = ["phishing", "zero-click", "email-security", "russia", "threat-intelligence", "malware", "microsoft-365", "google-workspace"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/patches/2026/07/23/year-long-russian-attacks-infect-users-as-soon-as-they-look-at-an-email/5277358"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/patches/2026/07/23/year-long-russian-attacks-infect-users-as-soon-as-they-look-at-an-email/5277358)

---

A year-long Russian-linked phishing campaign has been exploiting a vulnerability that allows malware to execute simply by a user previewing or opening an email, without clicking any link or attachment. The technique likely abuses zero-click or render-time exploitation, making it exceptionally dangerous as traditional user-awareness training offers little protection. Organisations relying on standard email security controls may be inadequately protected against this class of attack.


> **Security Architect's Take:** Review your email security stack immediately — ensure advanced sandboxing and pre-delivery detonation are enabled in your mail gateway (Microsoft Defender for Office 365, Google Workspace's pre-delivery scanning, or equivalent), and consider enforcing plain-text email rendering policies to reduce the HTML/script attack surface. Audit mail flow rules to ensure external HTML content and remote resource loading are blocked at the gateway level.


**Original advisory:** [Year-long Russian attacks infect users as soon as they look at an email](https://www.theregister.com/patches/2026/07/23/year-long-russian-attacks-infect-users-as-soon-as-they-look-at-an-email/5277358)
