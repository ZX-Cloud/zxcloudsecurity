+++
title = "npm Worm Poisons 800+ Packages via keyv Supply Chain"
date = "2026-08-04T13:30:23Z"
publishDate = "2026-08-04T13:30:23Z"
slug = "npm-worm-keyv-supply-chain-attack-hundreds-packages-poisoned-2026"
description = "A self-replicating npm worm originating in keyv@6.0.0 poisoned up to 868 packages with credential-stealing code and VS Code hooks in August 2026."
categories = ["general"]
tags = ["npm", "supply-chain", "keyv", "credential-theft", "worm", "vs-code", "open-source-security", "dependency-confusion"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/keyv-linked-npm-worm-poisons-hundreds.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/keyv-linked-npm-worm-poisons-hundreds.html)

---

A malicious npm worm, originating in keyv@6.0.0, self-propagated across the npm registry on 4 August 2026, poisoning hundreds of packages with credential-stealing code and injecting hooks into Claude Code and VS Code. Independent researchers confirmed between 353 and 868 affected packages across dozens of organisations. The self-replicating nature of the attack makes this one of the most significant npm supply chain incidents to date.


> **Security Architect's Take:** Audit your dependency trees immediately for any packages depending on keyv or cacheable and pin known-good versions; run npm audit and cross-reference against the SafeDep and Aikido IOC lists. Treat any CI/CD pipeline or developer machine that installed affected packages since 4 August 2026 as potentially compromised and rotate all secrets accessible from those environments.


**Original advisory:** [Keyv-Linked npm Worm Poisons Hundreds of Packages, Plants Claude Code and VS Code Hooks](https://thehackernews.com/2026/08/keyv-linked-npm-worm-poisons-hundreds.html)
