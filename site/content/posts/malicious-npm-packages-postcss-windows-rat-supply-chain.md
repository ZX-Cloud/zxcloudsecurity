+++
title = "Malicious npm Packages Deliver Windows RAT via PostCSS Typos"
date = "2025-06-23T08:54:32Z"
publishDate = "2026-06-23T08:54:32Z"
slug = "malicious-npm-packages-postcss-windows-rat-supply-chain"
description = "Three malicious npm packages impersonating PostCSS tools have been found delivering a Windows RAT. Over 1,000 downloads recorded — check your pipelines now"
categories = ["general"]
tags = ["npm", "supply-chain", "remote-access-trojan", "typosquatting", "postcss", "malware", "ci-cd", "developer-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/malicious-npm-packages-pose-as-postcss.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/malicious-npm-packages-pose-as-postcss.html)

---

Three malicious npm packages masquerading as legitimate PostCSS tooling have been discovered delivering a Windows remote access trojan (RAT). The packages accumulated over 1,000 combined downloads before detection, indicating real-world exposure. This is a classic supply chain attack targeting developers who install what appear to be routine CSS processing utilities.


> **Security Architect's Take:** Audit your CI/CD pipelines and developer environments for the packages aes-decode-runner-pro, postcss-minify-selector, and postcss-minify-selector-parser, and remove them immediately. Enforce npm package integrity checks, restrict installation of unvetted packages in build environments, and consider implementing a private registry with an approved package allowlist to reduce supply chain risk.


**Original advisory:** [Malicious npm Packages Pose as PostCSS Tools to Deliver Windows RAT](https://thehackernews.com/2026/06/malicious-npm-packages-pose-as-postcss.html)
