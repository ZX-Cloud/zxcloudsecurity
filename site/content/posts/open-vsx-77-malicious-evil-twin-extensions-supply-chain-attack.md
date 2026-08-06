+++
title = "Open VSX Malicious Extensions: 77 Evil Twins Removed"
date = "2025-08-05T09:23:03Z"
publishDate = "2026-08-05T09:23:03Z"
slug = "open-vsx-77-malicious-evil-twin-extensions-supply-chain-attack"
description = "77 malicious 'evil twin' extensions found on Open VSX exfiltrated developer system data. Learn what cloud security teams should do now."
categories = ["general"]
tags = ["supply-chain", "open-vsx", "vs-code", "malicious-extensions", "developer-security", "data-exfiltration", "software-supply-chain"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/open-vsx-removes-77-malicious-evil-twin.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/open-vsx-removes-77-malicious-evil-twin.html)

---

Seventy-seven malicious extensions were uploaded to the Open VSX marketplace between 26 July and 1 August 2026, masquerading as legitimate developer tools while silently harvesting system and development environment data. Discovered by Manifold Security, the 'evil twin' packages have since been removed. This is a supply chain attack targeting developers, meaning compromised machines could expose source code, credentials, and internal infrastructure details.


> **Security Architect's Take:** Audit your engineering teams' installed VS Code and VSX extensions immediately, cross-referencing against the list of 77 removed packages published by Manifold Security. Consider enforcing an allowlist of approved extensions via policy (e.g. VS Code extension marketplace controls or endpoint management tooling) and restrict developer workstations from installing extensions outside of a vetted, internal registry.


**Original advisory:** [Open VSX Removes 77 Malicious Evil Twin Extensions Exfiltrating Developer Data](https://thehackernews.com/2026/08/open-vsx-removes-77-malicious-evil-twin.html)
