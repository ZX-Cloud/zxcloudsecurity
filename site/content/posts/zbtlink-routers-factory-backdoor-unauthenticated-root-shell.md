+++
title = "Zbtlink Routers Ship With Root Shell Backdoor"
date = "2026-08-06T08:05:22Z"
publishDate = "2026-08-06T08:05:22Z"
slug = "zbtlink-routers-factory-backdoor-unauthenticated-root-shell"
description = "Zbtlink routers contain a factory-installed backdoor enabling unauthenticated root access across 20+ models. Learn what security teams should do now."
categories = ["general"]
tags = ["supply-chain", "backdoor", "router-security", "hardware-security", "network-security", "unauthenticated-access", "firmware", "zbtlink"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/chinese-made-zbtlink-routers-ship-with.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/chinese-made-zbtlink-routers-ship-with.html)

---

At least 20 router models from Chinese manufacturer Zbtlink have been found to ship with a pre-installed backdoor that grants unauthenticated root-level access. The backdoor is present across all 21 firmware images available from the vendor, spanning over two years of production, and automatically beacons to external infrastructure. This represents a supply chain compromise affecting any organisation using these devices, as the backdoor is baked in before the hardware reaches the customer.


> **Security Architect's Take:** Audit your network inventory immediately for any Zbtlink router models and treat them as fully compromised; isolate or replace affected devices and do not attempt to remediate via firmware update alone, as the implant is factory-shipped. If these devices are used in any network segment with cloud connectivity, review access logs for unexpected outbound traffic and rotate any credentials that may have been exposed.


**Original advisory:** [Chinese-Made Zbtlink Routers Ship With Backdoor That Opens Unauthenticated Root Shells](https://thehackernews.com/2026/08/chinese-made-zbtlink-routers-ship-with.html)
