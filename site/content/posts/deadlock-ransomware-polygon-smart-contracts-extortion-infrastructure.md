+++
title = "DeadLock Ransomware Abuses Polygon Blockchain Infrastructure"
date = "2025-08-11T16:35:27Z"
publishDate = "2026-08-11T16:35:27Z"
slug = "deadlock-ransomware-polygon-smart-contracts-extortion-infrastructure"
description = "DeadLock ransomware uses Polygon smart contracts and Session messaging to build resilient extortion infrastructure that's harder to disrupt or take down."
categories = ["general"]
tags = ["ransomware", "blockchain", "polygon", "decentralised-infrastructure", "extortion", "threat-intelligence", "session-network", "command-and-control"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/deadlock-ransomware-uses-polygon-smart.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/deadlock-ransomware-uses-polygon-smart.html)

---

The DeadLock ransomware group is leveraging Polygon blockchain smart contracts and the Session decentralised messaging network to host extortion infrastructure, making it significantly harder for law enforcement and defenders to take down. By moving victim communications and data leak operations onto decentralised platforms, the group reduces its reliance on traditional web hosting that can be seized or disrupted. This represents a notable evolution in ransomware operational security that other threat actors are likely to adopt.


> **Security Architect's Take:** Review your organisation's egress filtering and DNS policies to detect or block connections to known decentralised messaging endpoints (e.g. Session network nodes) and blockchain RPC providers not required for business operations; consider threat-hunting for unusual outbound traffic to Polygon RPC endpoints, which may indicate compromised hosts communicating with attacker-controlled smart contracts.


**Original advisory:** [DeadLock Ransomware Uses Polygon Smart Contracts to Make Extortion Infra Harder to Disrupt](https://thehackernews.com/2026/08/deadlock-ransomware-uses-polygon-smart.html)
