+++
title = "JadeProx TriBack Loader: Alibaba Cloud APT Attack"
date = "2025-07-23T12:20:23Z"
publishDate = "2026-07-23T12:20:23Z"
slug = "china-nexus-jadeprox-triback-loader-alibaba-cloud-government-healthcare-attacks"
description = "China-nexus group JadeProx uses TriBack Loader in attacks on government and healthcare via exposed Alibaba Cloud infrastructure. What architects need to kn"
categories = ["general"]
tags = ["alibaba-cloud", "apt", "malware-loader", "espionage", "healthcare", "government", "threat-intelligence", "command-and-control"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/china-nexus-jadeprox-uses-new-triback.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/china-nexus-jadeprox-uses-new-triback.html)

---

A China-linked threat actor tracked as JadeProx has been targeting government, healthcare, and education organisations across Asia and Latin America using a newly discovered Windows malware loader called TriBack Loader. The operation was uncovered after Group-IB found an exposed Alibaba Cloud server in Singapore containing infrastructure and tooling linked to the campaign. The discovery highlights ongoing state-aligned espionage activity leveraging cloud infrastructure for staging and command-and-control.


> **Security Architect's Take:** Review egress controls and threat detection coverage for Alibaba Cloud workloads, particularly in Singapore-region deployments — ensure cloud storage buckets and compute instances are not publicly accessible and that outbound connections to unusual endpoints are alerted on. Organisations in targeted sectors (government, healthcare, education) should also validate endpoint detection capabilities against loader-style malware that may bypass traditional AV signatures.


**Original advisory:** [China-Nexus JadeProx Uses New TriBack Loader in Government and Healthcare Attacks](https://thehackernews.com/2026/07/china-nexus-jadeprox-uses-new-triback.html)
