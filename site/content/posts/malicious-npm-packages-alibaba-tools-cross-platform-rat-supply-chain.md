+++
title = "Malicious npm Packages Target Alibaba Dev Tools with RAT"
date = "2025-08-03T18:43:53Z"
publishDate = "2026-08-03T18:43:53Z"
slug = "malicious-npm-packages-alibaba-tools-cross-platform-rat-supply-chain"
description = "18 malicious npm packages mimic Alibaba internal tools to deliver a cross-platform RAT. Learn what cloud architects should do to protect their pipelines."
categories = ["general"]
tags = ["npm", "supply-chain", "remote-access-trojan", "alibaba", "typosquatting", "package-confusion", "developer-tools", "malware"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/18-malicious-npm-packages-deliver-cross.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/18-malicious-npm-packages-deliver-cross.html)

---

Eighteen malicious npm packages have been discovered targeting developers who use Alibaba's internal tooling, delivering a cross-platform remote access trojan (RAT) capable of compromising Windows, macOS, and Linux systems. The attack uses typosquatting and package name confusion — mimicking a private Alibaba package called 'lib-mtop' — to deceive developers into installing malware. This represents a targeted software supply chain attack aimed primarily at Chinese-speaking developer environments.


> **Security Architect's Take:** Audit your organisation's npm dependency trees immediately for any Alibaba-related packages, particularly 'lib-mtop' and similar unscoped packages that shadow known private registries. Enforce the use of a private npm registry with an allowlist policy and configure `.npmrc` to scope internal packages, preventing resolution of unscoped public packages that could shadow internal dependencies.


**Original advisory:** [18 Malicious npm Packages Deliver Cross-Platform RAT to Alibaba Tool Users](https://thehackernews.com/2026/08/18-malicious-npm-packages-deliver-cross.html)
