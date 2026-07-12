+++
title = "jscrambler 8.14.0 npm Supply Chain Attack: Infostealer"
date = "2026-07-11T17:59:26Z"
publishDate = "2026-07-11T17:59:26Z"
slug = "jscrambler-8-14-0-npm-supply-chain-attack-rust-infostealer"
description = "jscrambler npm 8.14.0 was compromised with a preinstall hook dropping a Rust infostealer on Windows, macOS & Linux. Check your pipelines now."
categories = ["general"]
tags = ["supply-chain", "npm", "jscrambler", "infostealer", "malware", "ci-cd", "software-composition-analysis", "preinstall-hook"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/compromised-jscrambler-8140-npm-release.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/compromised-jscrambler-8140-npm-release.html)

---

The jscrambler npm package version 8.14.0 was compromised and contained a malicious preinstall hook that automatically downloaded and executed a Rust-based infostealer on Windows, macOS, and Linux. Any developer or CI/CD pipeline that ran 'npm install' with this version was immediately exposed without any further interaction required. Socket detected the malicious release within six minutes of publication, but the window of exposure remains a concern for any environment that pulled the package during that period.


> **Security Architect's Take:** Audit CI/CD pipelines and developer machines for any install of jscrambler 8.14.0, treat affected systems as fully compromised and rotate all credentials and secrets accessible from those environments. Enforce npm lockfiles pinned to known-good versions, enable real-time software composition analysis (SCA) tooling such as Socket or Socket Security in your pipelines to catch malicious packages before they execute.


**Original advisory:** [Compromised jscrambler 8.14.0 npm Release Drops Rust Infostealer During Install](https://thehackernews.com/2026/07/compromised-jscrambler-8140-npm-release.html)
