+++
title = "APT37 NarwhalRAT via Fake Microsoft Alerts"
date = "2025-06-16T08:14:55Z"
publishDate = "2026-06-16T08:14:55Z"
slug = "apt37-scarcruft-narwhalrat-fake-microsoft-security-alerts"
description = "North Korean group ScarCruft uses fake Microsoft security alerts to deliver NarwhalRAT malware. Learn the risks and how to protect your organisation."
categories = ["general"]
tags = ["apt37", "scarcruft", "narwhalrat", "spear-phishing", "microsoft", "remote-access-trojan", "north-korea", "email-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/fake-microsoft-alerts-used-to-deploy.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/fake-microsoft-alerts-used-to-deploy.html)

---

North Korean state-sponsored group ScarCruft (APT37) is running spear-phishing campaigns that impersonate Microsoft Account security alerts to deliver a remote access trojan called NarwhalRAT. The emails are crafted to alarm recipients about suspicious account activity, prompting them to interact with malicious content. This is a targeted threat with nation-state backing, making it higher risk than typical phishing campaigns.


> **Security Architect's Take:** Ensure your organisation's email security controls (DMARC, DKIM, SPF) are enforced and that Microsoft-themed phishing lures are included in user awareness training. Consider deploying conditional access policies that reduce the impact of credential theft, and review endpoint detection coverage for RAT-based payloads on any systems handling sensitive cloud workloads.


**Original advisory:** [Fake Microsoft Alerts Used to Deploy North Korean NarwhalRAT Malware](https://thehackernews.com/2026/06/fake-microsoft-alerts-used-to-deploy.html)
