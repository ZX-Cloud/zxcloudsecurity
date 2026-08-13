+++
title = "737 Chrome VPN Extensions Routing Traffic via Proxies"
date = "2025-08-12T14:09:50Z"
publishDate = "2026-08-12T14:09:50Z"
slug = "737-chrome-vpn-extensions-proxy-traffic-interception"
description = "737 Chrome VPN extensions caught secretly routing browser traffic through attacker proxies. Over 75,000 installs affected. Find out if your org is exposed."
categories = ["general"]
tags = ["chrome", "browser-extensions", "vpn", "proxy", "supply-chain", "traffic-interception", "data-exfiltration", "endpoint-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/737-chrome-vpn-extensions-caught.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/737-chrome-vpn-extensions-caught.html)

---

737 free VPN and proxy extensions on the Chrome Web Store were found to secretly route users' browser traffic through attacker-controlled proxy infrastructure, primarily targeting Russian-speaking users. The extensions, spread across 40 developer accounts, amassed over 75,000 installs and many impersonated legitimate tools. This creates significant risk of traffic interception, credential theft, and data exfiltration.


> **Security Architect's Take:** Audit your organisation's managed Chrome browser policies to block unapproved extensions using the ExtensionInstallBlocklist or allowlist controls via Chrome Enterprise. Consider enforcing a zero-trust approach where only explicitly approved browser extensions can be installed on corporate devices, and review existing installs against the published list of affected extensions.


**Original advisory:** [737 Chrome VPN Extensions Caught Routing Traffic Through Proxies. Check If You Have One](https://thehackernews.com/2026/08/737-chrome-vpn-extensions-caught.html)
