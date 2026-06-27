+++
title = "Miasma Campaign Poisons 20+ npm Packages for Creds"
date = "2025-06-26T12:18:00Z"
publishDate = "2026-06-26T12:18:00Z"
slug = "miasma-campaign-npm-supply-chain-attack-developer-credentials"
description = "Microsoft uncovers the Miasma campaign targeting npm packages including Leo Platform and RStreams, stealing developer secrets and spreading via maintainer "
categories = ["general"]
tags = ["npm", "supply-chain", "credential-theft", "leo-platform", "rstreams", "microsoft", "developer-security", "malicious-package"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/06/26/miasma-campaign-poisons-20-plus-npm-packages-hunts-for-developer-secrets/5262886"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/06/26/miasma-campaign-poisons-20-plus-npm-packages-hunts-for-developer-secrets/5262886)

---

A threat campaign dubbed 'Miasma' has compromised over 20 npm packages — including those associated with the Leo Platform and RStreams ecosystems — by injecting malicious code designed to harvest developer credentials. Microsoft identified the campaign, which appears to target package maintainers to gain further footholds and spread the compromise across the npm supply chain. The attack is particularly dangerous because developers who install or update affected packages may unknowingly expose secrets stored in their local environments or CI/CD pipelines.


> **Security Architect's Take:** Audit your dependency trees immediately for any use of Leo Platform or RStreams packages, and rotate any credentials present in developer environments or CI/CD systems that may have been exposed. Enforce software composition analysis (SCA) tooling with integrity checks — such as lockfile validation and provenance attestation via npm audit signatures — to detect tampered packages before they reach your build pipelines.


**Original advisory:** [Miasma campaign poisons 20-plus npm packages, hunts for developer secrets](https://www.theregister.com/security/2026/06/26/miasma-campaign-poisons-20-plus-npm-packages-hunts-for-developer-secrets/5262886)
