+++
title = "North Korean Hackers Target NPM Supply Chain | AWS"
date = "2025-07-29T21:00:12Z"
publishDate = "2026-07-29T21:00:12Z"
slug = "north-korean-hackers-npm-supply-chain-attack-aws"
description = "Amazon links North Korean state hackers to NPM library compromises. Learn what cloud security architects should do to protect their software supply chains."
categories = ["aws"]
tags = ["aws", "supply-chain", "npm", "dprk", "threat-intelligence", "open-source", "malware", "ci-cd"]
severity = "High"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/amazon-identifies-north-korean-hacker-group-behind-open-source-supply-chain-attacks/"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/amazon-identifies-north-korean-hacker-group-behind-open-source-supply-chain-attacks/)

---

Amazon's threat intelligence team has attributed a series of attacks on popular NPM libraries to a North Korean state-sponsored hacking group. The attackers are compromising open-source packages used widely in application development, meaning malicious code could be silently introduced into software built by organisations around the world. This is a significant supply chain threat, as developers often trust and automatically consume these shared libraries.


> **Security Architect's Take:** Audit your CI/CD pipelines and dependency manifests for recently updated NPM packages, and implement software composition analysis (SCA) tooling to flag unexpected changes in transitive dependencies. Consider enforcing package integrity checks via lockfiles and private registries with allowlisting to reduce exposure to compromised upstream packages.


**Original advisory:** [Amazon identifies North Korean hacker group behind open-source supply chain attacks](https://aws.amazon.com/blogs/security/amazon-identifies-north-korean-hacker-group-behind-open-source-supply-chain-attacks/)
