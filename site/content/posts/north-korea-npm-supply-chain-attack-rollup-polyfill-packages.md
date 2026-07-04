+++
title = "North Korea npm Supply Chain Attack Targets Devs"
date = "2025-07-03T16:07:15Z"
publishDate = "2026-07-03T16:07:15Z"
slug = "north-korea-npm-supply-chain-attack-rollup-polyfill-packages"
description = "North Korea-linked actors published malicious npm packages mimicking Rollup polyfill tools to steal developer credentials via supply chain attack."
categories = ["general"]
tags = ["npm", "supply-chain", "north-korea", "malware", "developer-security", "credential-theft", "open-source", "ci-cd"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/north-korea-linked-npm-packages-mimic.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/north-korea-linked-npm-packages-mimic.html)

---

North Korea-linked threat actors have published malicious npm packages that impersonate legitimate Rollup polyfill tooling, enabling remote access and credential theft from developer machines. The packages closely mimic the real 'rollup-plugin-polyfill-node' project, including metadata and repository details, making them difficult to spot. This is a software supply chain attack targeting developers who may unknowingly install the counterfeit packages.


> **Security Architect's Take:** Audit your CI/CD pipelines and developer workstations for the packages 'rollup-packages-polyfill-core' and 'rollup-runtime-polyfill-core', and remove them immediately. Enforce package allowlists or integrity checks (e.g. via npm audit, Artifactory Xray, or Socket.dev) to prevent unapproved packages entering your build environments.


**Original advisory:** [North Korea-Linked npm Packages Mimic Rollup Polyfills to Steal Developer Secrets](https://thehackernews.com/2026/07/north-korea-linked-npm-packages-mimic.html)
