+++
title = "800 Malicious npm Packages Drop RAT & Infostealer"
date = "2025-08-07T18:48:17Z"
publishDate = "2026-08-07T18:48:17Z"
slug = "malicious-npm-packages-cross-platform-rat-infostealer-supply-chain"
description = "Nearly 800 typo-squatted npm packages deliver a cross-platform RAT and infostealer targeting Windows, macOS, and Linux developer environments."
categories = ["general"]
tags = ["npm", "supply-chain", "malware", "infostealer", "remote-access-trojan", "typosquatting", "open-source-security", "ci-cd"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/nearly-800-malicious-npm-packages.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/nearly-800-malicious-npm-packages.html)

---

Nearly 800 malicious packages have been uploaded to the npm registry, using AI-generated or typo-squatted names to trick developers into installing them. Each package delivers a remote access trojan (RAT) and infostealer capable of running on Windows, macOS, and Linux. This represents a significant software supply chain threat, as compromised developer machines can lead to credential theft and backdoor access across entire development pipelines.


> **Security Architect's Take:** Audit your organisation's npm dependency trees immediately using tools such as Socket.dev or Snyk, and enforce allowlisting of approved packages in your CI/CD pipelines. Consider implementing registry mirroring with automated malware scanning to prevent unapproved or newly published packages from entering your build environments.


**Original advisory:** [Nearly 800 Malicious npm Packages Deliver Cross-Platform RAT and Infostealer](https://thehackernews.com/2026/08/nearly-800-malicious-npm-packages.html)
