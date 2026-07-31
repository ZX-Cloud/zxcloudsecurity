+++
title = "North Korea Hijacked npm debug & chalk Packages"
date = "2026-07-30T06:05:17Z"
publishDate = "2026-07-30T06:05:17Z"
slug = "north-korea-sapphire-sleet-npm-debug-chalk-hijack-supply-chain"
description = "Amazon attributes the 2025 hijack of npm packages debug and chalk to North Korea's Sapphire Sleet, exposing 2bn+ weekly downloads to crypto-draining malwar"
categories = ["general"]
tags = ["npm", "supply-chain", "sapphire-sleet", "north-korea", "aws", "software-composition-analysis", "cryptocurrency-theft", "malicious-packages"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/amazon-links-debug-and-chalk-npm-hijack.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/amazon-links-debug-and-chalk-npm-hijack.html)

---

North Korean threat actor Sapphire Sleet has been attributed by Amazon to the September 2025 hijacking of the widely used npm packages debug and chalk, which together account for over 2 billion weekly downloads. A maintainer was phished via a lookalike npm domain, allowing attackers to push a wallet-draining script into at least 18 downstream packages. The scale of the supply chain compromise makes this one of the most significant npm incidents on record.


> **Security Architect's Take:** Audit your dependency trees immediately for any packages that pulled updates to debug or chalk between September 2025 and the point of remediation, and review build pipeline artefact integrity. Enforce npm provenance attestation and consider pinning critical transitive dependencies to verified digests rather than version ranges.


**Original advisory:** [Amazon Links Debug and Chalk npm Hijack to North Korea’s Sapphire Sleet](https://thehackernews.com/2026/07/amazon-links-debug-and-chalk-npm-hijack.html)
