+++
title = "GitHub Actions Abused to Attack cPanel & WHM Servers"
date = "2025-07-23T11:28:54Z"
publishDate = "2026-07-23T11:28:54Z"
slug = "github-actions-supply-chain-attack-cpanel-whm-packagist"
description = "Attackers weaponised compromised GitHub repos and malicious Packagist packages to target cPanel and WHM hosting servers at scale via CI/CD pipelines."
categories = ["general"]
tags = ["github", "github-actions", "packagist", "cpanel", "whm", "supply-chain", "ci-cd", "malicious-packages"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/attackers-weaponize-github-actions.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/attackers-weaponize-github-actions.html)

---

Attackers compromised GitHub repositories belonging to a legitimate PHP developer to distribute malicious Packagist packages that weaponise GitHub Actions runners against cPanel and WHM hosting control panel instances. The campaign involved at least 10 tampered development-version packages published over a two-day window in July, effectively turning trusted CI/CD infrastructure into a distributed attack platform. This matters because it demonstrates how supply chain compromise via package registries can be used to pivot into web hosting infrastructure at scale.


> **Security Architect's Take:** Audit all Packagist dependencies — particularly development versions — for unexpected maintainer changes or suspicious release activity, and enforce allowlists for third-party GitHub Actions in your CI/CD pipelines. If your organisation runs cPanel or WHM, review access logs for anomalous authentication attempts and consider restricting API access to known IP ranges.


**Original advisory:** [Attackers Weaponize GitHub Actions Runners to Target cPanel and WHM Servers](https://thehackernews.com/2026/07/attackers-weaponize-github-actions.html)
