+++
title = "Windows Device ID Used to Trace Scattered Spider Hacker"
date = "2024-07-07T13:27:20Z"
publishDate = "2026-07-07T13:27:20Z"
slug = "windows-device-id-scattered-spider-hacker-fbi-trace"
description = "US prosecutors used a persistent Windows device ID and Microsoft records to link an alleged Scattered Spider hacker to a 2025 retail network intrusion."
categories = ["general"]
tags = ["scattered-spider", "windows", "azure", "threat-intelligence", "incident-response", "device-identity", "forensics", "social-engineering"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/court-filing-reveals-windows-device-id.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/court-filing-reveals-windows-device-id.html)

---

US prosecutors have used a persistent Windows device ID to link an alleged Scattered Spider member to a cyberattack on a luxury jewellery retailer in May 2025. Microsoft records tied the device ID to both the attacker's persistence account during the intrusion and to personal online accounts belonging to 19-year-old suspect Peter Stokes. The case highlights how hardware and software identifiers retained by cloud and identity providers can become powerful forensic artefacts in cybercrime investigations.


> **Security Architect's Take:** Review your organisation's logging strategy to ensure Windows device IDs, Entra ID (Azure AD) device registration records, and associated sign-in logs are retained and correlated — these artefacts can be pivotal for both threat hunting and incident response. Also ensure conditional access policies flag or block unregistered or anomalous devices attempting to maintain persistence via legitimate identity providers.


**Original advisory:** [Court Filing Reveals Windows Device ID Helped FBI Trace Alleged Scattered Spider Hacker](https://thehackernews.com/2026/07/court-filing-reveals-windows-device-id.html)
