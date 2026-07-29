+++
title = "Compromised joyfill npm Packages Deploy RAT Malware"
date = "2025-07-29T04:20:57Z"
publishDate = "2026-07-29T04:20:57Z"
slug = "joyfill-npm-packages-compromised-devpopper-rat-supply-chain"
description = "Two @joyfill npm beta packages are backdoored with a DEV#POPPER RAT that executes on import. Learn what to audit and how to protect your Node.js supply cha"
categories = ["general"]
tags = ["npm", "supply-chain", "remote-access-trojan", "dev-popper", "node-js", "malware", "software-composition-analysis"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/two-compromised-joyfill-npm-packages.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/two-compromised-joyfill-npm-packages.html)

---

Two beta-release npm packages in the @joyfill namespace have been backdoored to silently install a remote access trojan (RAT) from the DEV#POPPER malware family when a developer imports them into a Node.js project. The malware executes at import time, meaning simply installing and using the package is enough to trigger the infection. This is a supply chain attack targeting developers who may be testing pre-release versions of these UI component libraries.


> **Security Architect's Take:** Audit your Node.js dependency trees immediately for the two affected package versions and remove them if present. Enforce policies that restrict use of pre-release, beta, or release-candidate npm packages in pipelines, and consider implementing runtime import controls or software composition analysis (SCA) tooling that flags packages with known malicious payloads before they reach developer workstations or CI/CD environments.


**Original advisory:** [Two Compromised joyfill npm Packages Run RAT When Imported Into Node.js](https://thehackernews.com/2026/07/two-compromised-joyfill-npm-packages.html)
