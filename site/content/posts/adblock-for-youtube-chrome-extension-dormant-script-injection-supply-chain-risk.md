+++
title = "Adblock for YouTube Chrome Extension: Script Injection Risk"
date = "2025-06-25T14:12:52Z"
publishDate = "2026-06-25T14:12:52Z"
slug = "adblock-for-youtube-chrome-extension-dormant-script-injection-supply-chain-risk"
description = "A Chrome extension with 10M+ installs can execute arbitrary JavaScript. Learn what cloud security architects should do to mitigate this supply-chain risk."
categories = ["general"]
tags = ["browser-extension", "chrome", "javascript-injection", "supply-chain", "endpoint-security", "data-exfiltration", "shadow-it"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/chrome-ad-blocker-with-10m-installs.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/chrome-ad-blocker-with-10m-installs.html)

---

A Chrome extension called 'Adblock for YouTube' with over 10 million installs has been found to contain hidden functionality capable of injecting and executing arbitrary JavaScript code in users' browsers. The extension carries a 'Featured' badge on the Chrome Web Store, lending it a false sense of legitimacy. This represents a significant supply-chain risk, as the dormant capability could be activated remotely to steal credentials, exfiltrate data, or compromise corporate environments.


> **Security Architect's Take:** Audit and restrict browser extensions permitted within your organisation via Chrome Enterprise policies or a Secure Access Service Edge (SASE) solution — specifically blocklist the extension ID cmedhionkhpnakcndndgjdbohmhepckk and review endpoint telemetry for any prior installations, particularly on devices with access to sensitive cloud consoles or SaaS platforms.


**Original advisory:** [Chrome Ad Blocker with 10M+ Installs Found with Dormant Script Injection Capability](https://thehackernews.com/2026/06/chrome-ad-blocker-with-10m-installs.html)
