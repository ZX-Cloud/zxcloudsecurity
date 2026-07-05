+++
title = "North Korean PolinRider: 108 Malicious npm & Chrome Packages"
date = "2025-07-04T11:17:24Z"
publishDate = "2026-07-04T11:17:24Z"
slug = "north-korean-polinrider-108-malicious-npm-chrome-packages-supply-chain"
description = "North Korean hackers publish 108 malicious packages across npm, Go, Packagist and Chrome in the active PolinRider supply chain campaign."
categories = ["general"]
tags = ["supply-chain", "npm", "malware", "north-korea", "contagious-interview", "chrome-extensions", "open-source-security", "developer-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/north-korean-hackers-publish-108.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/north-korean-hackers-publish-108.html)

---

North Korean threat actors behind the Contagious Interview campaign have published 108 malicious packages and browser extensions across npm, Packagist, Go, and Chrome in an active campaign dubbed PolinRider. The attackers are compromising legitimate maintainer accounts to distribute malware through trusted package repositories. This is a supply chain attack targeting developers who install seemingly legitimate dependencies.


> **Security Architect's Take:** Audit your CI/CD pipelines and developer workstations for recently installed npm, Go, or Packagist packages, and enforce allowlisting of approved dependencies via a private registry or lock file integrity checks. Implement runtime behavioural monitoring on build agents and restrict outbound network access from CI environments to limit the blast radius of any compromise.


**Original advisory:** [North Korean Hackers Publish 108 Malicious Packages and Extensions in PolinRider Campaign](https://thehackernews.com/2026/07/north-korean-hackers-publish-108.html)
