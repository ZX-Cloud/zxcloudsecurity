+++
title = "Trojanised NuGet Package Targets Digitain Betting Platform"
date = "2025-07-22T06:00:06Z"
publishDate = "2026-07-22T06:00:06Z"
slug = "trojanised-nuget-newtonsoftt-json-digitain-game-rigging-supply-chain"
description = "A typosquatted NuGet fork of Newtonsoft.Json hides game-rigging code targeting the Digitain platform. Learn how to protect your supply chain."
categories = ["general"]
tags = ["nuget", "supply-chain", "typosquatting", "newtonsoft-json", "malware", "software-composition-analysis", "open-source-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/trojanized-newtonsoftjson-fork-hides.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/trojanized-newtonsoftjson-fork-hides.html)

---

A malicious NuGet package named 'Newtonsoftt.Json.Net' has been discovered masquerading as the widely-used Newtonsoft.Json library through typosquatting. Unlike typical supply chain attacks targeting credential theft, this trojanised fork embeds code designed to manipulate live game results on the Digitain sports betting platform. Seven versions of the package were published, making it a persistent and targeted threat.


> **Security Architect's Take:** Audit your organisation's NuGet package references immediately for typosquatted dependencies, paying particular attention to high-usage libraries like Newtonsoft.Json. Enforce private package feeds with allowlisting policies and integrate software composition analysis (SCA) tooling into your CI/CD pipelines to flag unverified or suspicious package names before build.


**Original advisory:** [Trojanized Newtonsoft.Json Fork Hides Game-Rigging Code in a Working Library](https://thehackernews.com/2026/07/trojanized-newtonsoftjson-fork-hides.html)
