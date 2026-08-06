+++
title = "Trojanized npm Packages Hide C2 via Blockchain NullReceiver"
date = "2025-08-05T13:41:27Z"
publishDate = "2026-08-05T13:41:27Z"
slug = "trojanized-npm-packages-nullreceiver-blockchain-c2-etherhiding"
description = "Two malicious npm packages use a new NullReceiver blockchain technique to conceal C2 server IPs, evading traditional security controls. Here's what to do."
categories = ["general"]
tags = ["npm", "supply-chain", "malware", "blockchain", "command-and-control", "etherhiding", "dead-drop-resolver", "open-source-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/trojanized-npm-packages-decode-c2-ip.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/trojanized-npm-packages-decode-c2-ip.html)

---

Two malicious npm packages, 'bianira-ui' and 'fluid-type-ui', have been found using a novel technique called NullReceiver to hide a command-and-control server's IP address inside a zero-value Ethereum blockchain transaction. This is an evolution of the known EtherHiding method, making the malicious infrastructure significantly harder to detect and block. Because the C2 address is stored on a public, immutable blockchain rather than a traditional server, conventional takedown and blocklist approaches are ineffective.


> **Security Architect's Take:** Audit your organisation's npm dependency trees immediately for 'bianira-ui' and 'fluid-type-ui', and enforce allowlisting of approved packages via a private registry such as Artifactory or AWS CodeArtifact. Additionally, implement egress controls and DNS monitoring to detect unusual outbound traffic patterns, including unexpected connections to Ethereum RPC endpoints from your build and runtime environments.


**Original advisory:** [Trojanized npm Packages Employ NullReceiver Tactic to Decode C2 IP from Blockchain](https://thehackernews.com/2026/08/trojanized-npm-packages-decode-c2-ip.html)
