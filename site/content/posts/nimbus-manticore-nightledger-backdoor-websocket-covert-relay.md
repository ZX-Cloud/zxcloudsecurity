+++
title = "Nimbus Manticore NightLedger Backdoor & Covert Relays"
date = "2025-07-28T11:55:20Z"
publishDate = "2026-07-28T11:55:20Z"
slug = "nimbus-manticore-nightledger-backdoor-websocket-covert-relay"
description = "Iranian APT Nimbus Manticore deploys NightLedger Windows backdoor and WebSocket tunnellers to turn victim systems into covert relays across the Middle East"
categories = ["general"]
tags = ["apt", "nimbus-manticore", "unc1549", "nightledger", "backdoor", "websocket-tunnelling", "iran", "command-and-control"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/nimbus-manticore-deploys-nightledger.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/nimbus-manticore-deploys-nightledger.html)

---

Iranian state-sponsored threat actor Nimbus Manticore (also known as UNC1549 and several other aliases) has been linked to a new campaign targeting organisations across the Middle East, Africa, and South Asia. The group is deploying a previously unknown Windows backdoor called NightLedger alongside two custom WebSocket tunnelling tools to maintain covert access and route malicious traffic through compromised systems. This matters because the technique of turning victim infrastructure into relay nodes makes attribution and detection significantly harder for defenders.


> **Security Architect's Take:** Review egress filtering and anomaly detection for unusual WebSocket traffic patterns originating from internal systems, particularly to external endpoints — compromised hosts acting as covert relays will often exhibit long-lived, low-volume outbound WebSocket connections. Ensure endpoint detection tooling covers Windows backdoor persistence mechanisms and consider threat intelligence feed integration to block known Nimbus Manticore IOCs at your network perimeter and cloud security groups.


**Original advisory:** [Nimbus Manticore Deploys NightLedger and Turns Victim Systems Into Covert Relays](https://thehackernews.com/2026/07/nimbus-manticore-deploys-nightledger.html)
