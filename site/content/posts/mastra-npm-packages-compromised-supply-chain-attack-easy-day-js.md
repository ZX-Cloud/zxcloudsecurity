+++
title = "144 Mastra npm Packages Hijacked in Supply Chain Attack"
date = "2025-06-17T07:38:24Z"
publishDate = "2026-06-17T07:38:24Z"
slug = "mastra-npm-packages-compromised-supply-chain-attack-easy-day-js"
description = "144 @mastra/* npm packages were compromised via a hijacked contributor account in the 'easy-day-js' supply chain attack. Find out what architects should do"
categories = ["general"]
tags = ["npm", "supply-chain", "mastra", "javascript", "typescript", "account-hijack", "software-composition-analysis", "open-source"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/144-mastra-npm-packages-compromised-via.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/144-mastra-npm-packages-compromised-via.html)

---

144 npm packages in the Mastra AI framework namespace were compromised after an attacker hijacked a contributor's npm account, in an attack dubbed 'easy-day-js'. The malicious packages could have been pulled into AI application builds by developers unaware of the compromise. This is a classic software supply chain attack, where trust in a legitimate open-source project is exploited to distribute malicious code at scale.


> **Security Architect's Take:** Audit your dependency trees immediately for any '@mastra/*' packages and verify package integrity against known-good checksums or publish timestamps. Enforce npm account MFA requirements for all contributors in internally mirrored or approved package registries, and consider implementing a software composition analysis (SCA) tool with real-time supply chain monitoring to catch future account hijack incidents before they reach your builds.


**Original advisory:** [144 Mastra npm Packages Compromised via Hijacked Contributor Account](https://thehackernews.com/2026/06/144-mastra-npm-packages-compromised-via.html)
