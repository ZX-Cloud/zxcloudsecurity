+++
title = "94% of Security Incidents Use Anonymised Infrastructure"
date = "2024-06-16T11:30:00Z"
publishDate = "2026-06-16T11:30:00Z"
slug = "94-percent-incidents-anonymised-infrastructure-threat-intelligence-reactive"
description = "New survey finds 94% of security incidents involve anonymised infrastructure. Learn why threat intelligence teams remain reactive and what to do about it."
categories = ["general"]
tags = ["threat-intelligence", "ip-reputation", "anonymisation", "siem", "soar", "incident-response", "threat-attribution"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/survey-94-of-incidents-involve.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/survey-94-of-incidents-involve.html)

---

A new survey reveals that 94% of security incidents involve anonymised infrastructure such as VPNs, proxies, and hosting services, making it difficult to attribute attacks to real threat actors. Despite access to large volumes of IP enrichment and threat intelligence data, most security teams remain reactive rather than proactive. The core problem is signal-to-noise ratio — too much data, too little actionable context.


> **Security Architect's Take:** Review your threat intelligence pipeline for coverage of anonymising infrastructure (e.g. Tor exit nodes, residential proxies, bulletproof hosting ASNs) and ensure your SIEM or SOAR rules treat traffic from these sources with elevated suspicion by default. Consider integrating purpose-built IP context providers that specialise in anonymisation detection rather than relying solely on generic reputation feeds.


**Original advisory:** [Survey: 94% of Incidents Involve Anonymized Infrastructure. Teams Are Still Reactive](https://thehackernews.com/2026/06/survey-94-of-incidents-involve.html)
