+++
title = "Google Disrupts NetNut Residential Proxy Network"
date = "2024-07-02T18:54:06Z"
publishDate = "2026-07-02T18:54:06Z"
slug = "google-disrupts-netnut-residential-proxy-network"
description = "Google and the FBI disrupt NetNut, a 2-million-device residential proxy network used to anonymise malicious traffic. What cloud security teams should know."
categories = ["general"]
tags = ["residential-proxy", "netnut", "botnet", "threat-intelligence", "google", "anonymisation", "fraud", "credential-stuffing"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/google-disrupts-netnut-residential.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/google-disrupts-netnut-residential.html)

---

Google, working with the FBI and other partners, has significantly disrupted NetNut (also known as Popa), a large residential proxy network that recruited over two million home devices to relay third-party internet traffic without owners' knowledge. Such networks are frequently exploited by threat actors to anonymise malicious activity, bypass geo-restrictions, and evade detection. The takedown reduces the available pool of compromised devices by millions, degrading a key tool used for fraud, credential stuffing, and other attacks.


> **Security Architect's Take:** Review your WAF, SIEM, and threat intelligence feeds for traffic originating from known residential proxy ranges — NetNut/Popa indicators of compromise should now be available from Lumen and Google GTIG. Consider enriching your IP reputation blocking rules and ensuring anomaly detection covers residential ASN traffic patterns, which are increasingly used to evade corporate IP blocklists.


**Original advisory:** [Google Disrupts NetNut Residential Proxy Network Spanning 2 Million Home Devices](https://thehackernews.com/2026/07/google-disrupts-netnut-residential.html)
