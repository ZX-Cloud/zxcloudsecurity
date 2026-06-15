+++
title = "WordPress Plugin Supply-Chain Backdoor: PushEngage & OptinMo"
date = "2025-06-15T09:59:38Z"
publishDate = "2026-06-15T09:59:38Z"
slug = "wordpress-plugin-supply-chain-backdoor-pushengage-optinmonster-trustpulse"
description = "Attackers tampered with JavaScript in PushEngage, OptinMonster, and TrustPulse plugins to plant hidden backdoors and rogue admin accounts on WordPress site"
categories = ["general"]
tags = ["wordpress", "supply-chain", "backdoor", "pushengage", "optinmonster", "privilege-escalation", "javascript-tampering", "web-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/popular-wordpress-plugin-scripts.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/popular-wordpress-plugin-scripts.html)

---

Attackers tampered with JavaScript files distributed by three popular WordPress plugins — PushEngage, OptinMonster, and TrustPulse — injecting malicious code that creates a rogue admin account and installs a hidden backdoor plugin when a logged-in administrator loads the compromised script. The attack is a supply-chain compromise targeting the plugin delivery mechanism rather than WordPress itself, meaning sites that kept plugins updated may still have been affected. Any site running these plugins while an admin was active during the compromise window should be treated as potentially backdoored.


> **Security Architect's Take:** Audit all WordPress sites running PushEngage, OptinMonster, or TrustPulse for unexpected admin accounts and unauthorised plugins created during the suspected compromise window, and consider implementing subresource integrity (SRI) checks or a web application firewall rule to alert on unexpected script modifications from third-party plugin CDNs.


**Original advisory:** [Popular WordPress Plugin Scripts Tampered to Plant Hidden Backdoors on Sites](https://thehackernews.com/2026/06/popular-wordpress-plugin-scripts.html)
