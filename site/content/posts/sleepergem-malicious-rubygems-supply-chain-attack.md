+++
title = "SleeperGem: Malicious RubyGems Supply Chain Attack"
date = "2025-07-20T05:15:39Z"
publishDate = "2026-07-20T05:15:39Z"
slug = "sleepergem-malicious-rubygems-supply-chain-attack"
description = "Three malicious RubyGems packages in the SleeperGem campaign target developer machines via the Ruby package registry. Find out which gems to remove and how"
categories = ["general"]
tags = ["supply-chain", "rubygems", "ruby", "malware", "developer-security", "software-composition-analysis", "ci-cd", "package-registry"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/sleepergem-uses-three-malicious.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/sleepergem-uses-three-malicious.html)

---

Three malicious RubyGems packages, part of a campaign dubbed SleeperGem, were published to the RubyGems registry with the intent to compromise developer machines and deliver additional malicious payloads. The packages impersonate legitimate tools — including a convincing clone of the popular Git Credential Manager — making them likely to be installed by unsuspecting Ruby developers. Supply chain attacks targeting package registries pose a broad risk as a single compromised dependency can affect many downstream projects and CI/CD pipelines.


> **Security Architect's Take:** Audit your CI/CD pipelines and developer environments for the presence of git_credential_manager (versions 2.8.0–2.8.3) and Dendreo (versions 1.1.3–1.1.4), and remove them immediately. Enforce allowlists or lockfiles (Gemfile.lock) for RubyGems dependencies and consider integrating a software composition analysis (SCA) tool such as Dependabot or Snyk to flag newly published or suspicious package versions before they reach build environments.


**Original advisory:** [SleeperGem Uses Three Malicious RubyGems Packages to Target Developer Machines](https://thehackernews.com/2026/07/sleepergem-uses-three-malicious.html)
