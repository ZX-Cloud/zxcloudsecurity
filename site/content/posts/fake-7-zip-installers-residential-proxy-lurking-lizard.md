+++
title = "Fake 7-Zip Installers Create Residential Proxy Nodes"
date = "2024-07-09T04:01:49Z"
publishDate = "2026-07-09T04:01:49Z"
slug = "fake-7-zip-installers-residential-proxy-lurking-lizard"
description = "Lurking Lizard uses 230+ lookalike domains to spread fake 7-Zip installers, secretly enrolling victims' devices into a residential proxy network."
categories = ["general"]
tags = ["malware", "residential-proxy", "supply-chain", "dns", "typosquatting", "infosec", "endpoint-security"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/fake-7-zip-installers-turn-devices-into.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/fake-7-zip-installers-turn-devices-into.html)

---

A threat actor known as Lurking Lizard has been running a large-scale residential proxy network since at least August 2022, luring victims into downloading fake 7-Zip installers from over 230 lookalike domains. Once installed, the malware silently enrolls the victim's device as a proxy node, effectively monetising their internet connection and IP address without their knowledge. This is significant because residential proxies are frequently abused to bypass geo-restrictions, conduct credential stuffing, and obscure the origin of other malicious activity.


> **Security Architect's Take:** Enforce application allowlisting and restrict software installation to approved, signed packages from verified sources within your cloud workloads and end-user environments. Review egress traffic patterns for anomalous outbound proxy-like connections, and ensure DNS filtering blocks lookalike domains — consider deploying a protective DNS solution such as those compliant with NCSC's PDNS guidance.


**Original advisory:** [Fake 7-Zip Installers Turn Devices Into Residential Proxy Nodes](https://thehackernews.com/2026/07/fake-7-zip-installers-turn-devices-into.html)
