+++
title = "QuimaRAT MaaS RAT Targets Windows, Linux & macOS"
date = "2025-07-06T08:13:33Z"
publishDate = "2026-07-06T08:13:33Z"
slug = "quimarat-java-maas-rat-windows-linux-macos"
description = "QuimaRAT is a Java-based RAT sold as a MaaS service targeting Windows, Linux, and macOS. Learn what cloud architects need to know to protect hybrid environ"
categories = ["general"]
tags = ["malware", "remote-access-trojan", "maas", "cross-platform", "linux", "java", "endpoint-security", "threat-intelligence"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-java-based-quimarat-maas-built-to.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-java-based-quimarat-maas-built-to.html)

---

QuimaRAT is a new Java-based remote access trojan sold as a subscription service, capable of compromising Windows, Linux, and macOS systems. Its cross-platform design makes it particularly dangerous in cloud and hybrid environments where mixed operating systems are common. Priced from £150/month, its low barrier to entry means a wide range of threat actors can deploy it.


> **Security Architect's Take:** Audit your cloud workloads for unauthorised Java runtimes and ensure EDR coverage extends to Linux-based instances and containers, as these are frequently under-monitored. Block outbound connections from compute instances to known MaaS infrastructure using egress filtering and enforce application allowlisting where feasible.


**Original advisory:** [New Java-Based QuimaRAT MaaS Built to Run on Windows, Linux, and macOS](https://thehackernews.com/2026/07/new-java-based-quimarat-maas-built-to.html)
