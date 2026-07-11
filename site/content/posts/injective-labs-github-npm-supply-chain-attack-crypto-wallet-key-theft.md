+++
title = "Injective Labs npm Supply Chain Attack Steals Crypto Keys"
date = "2025-07-10T16:29:00Z"
publishDate = "2026-07-10T16:29:00Z"
slug = "injective-labs-github-npm-supply-chain-attack-crypto-wallet-key-theft"
description = "A compromised GitHub repo pushed a malicious npm package stealing crypto wallet private keys. Find out what architects must do now."
categories = ["general"]
tags = ["supply-chain", "npm", "github", "cryptocurrency", "malware", "dependency-confusion", "blockchain", "secrets-exfiltration"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/injective-labs-github-compromise-pushes.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/injective-labs-github-compromise-pushes.html)

---

Attackers compromised the GitHub repository of Injective Labs, a blockchain SDK project, and used it to publish a malicious npm package (@injectivelabs/sdk-ts@1.20.21) that secretly steals cryptocurrency wallet private keys and seed phrases. The package disguised its theft mechanism as routine telemetry functionality, making it difficult to detect. This is a classic software supply chain attack targeting developers who build on the Injective blockchain ecosystem.


> **Security Architect's Take:** Audit your organisation's dependency trees immediately for @injectivelabs/sdk-ts and pin or remove version 1.20.21; implement npm package integrity checks and consider enforcing lockfiles with hash verification in your CI/CD pipelines to detect unexpected package changes before they reach production.


**Original advisory:** [Injective Labs GitHub Compromise Pushes Wallet-Key-Stealing npm Packages](https://thehackernews.com/2026/07/injective-labs-github-compromise-pushes.html)
