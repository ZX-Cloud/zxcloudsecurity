+++
title = "Hijacked npm & Go Packages Deploy Python Infostealer"
date = "2025-06-29T05:36:06Z"
publishDate = "2026-06-29T05:36:06Z"
slug = "hijacked-npm-go-packages-vscode-tasks-python-infostealer"
description = "Attackers hijacked npm and Go packages to silently deploy a Python infostealer via VS Code tasks, bypassing npm v12 security controls on Windows, Linux and"
categories = ["general"]
tags = ["supply-chain", "npm", "golang", "infostealer", "vscode", "malware", "developer-tools", "ci-cd"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/hijacked-npm-and-go-packages-use-vs.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/hijacked-npm-and-go-packages-use-vs.html)

---

Attackers have hijacked legitimate npm and Go packages, weaponising them to deploy a Python-based infostealer across Windows, Linux, and macOS. The attack is notable for bypassing npm's lifecycle script execution — a common detection vector — by using Visual Studio Code task configurations instead, suggesting deliberate evasion of npm v12 security controls. Any developer or CI/CD pipeline consuming these packages risks credential and secret theft from the compromised host.


> **Security Architect's Take:** Audit your organisation's software supply chain immediately: enforce package integrity checks (e.g. lockfile pinning, provenance attestation via Sigstore/npm provenance), restrict outbound network access from build environments, and scan developer workstations and CI runners for unexpected VS Code task file modifications. Consider blocking or alerting on Python spawned from IDE task runners in environments where it is not expected.


**Original advisory:** [Hijacked npm and Go Packages Use VS Code Tasks to Deploy Python Infostealer](https://thehackernews.com/2026/06/hijacked-npm-and-go-packages-use-vs.html)
