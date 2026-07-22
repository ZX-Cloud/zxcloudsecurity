+++
title = "LG Bans Smart TV Apps Used as Residential Proxies"
date = "2024-07-22T01:10:38Z"
publishDate = "2026-07-22T01:10:38Z"
slug = "lg-webos-smart-tv-residential-proxy-ban"
description = "LG will suspend webOS apps that route third-party traffic through smart TVs. Over 42% of apps were found enabling residential proxy abuse without user cons"
categories = ["general"]
tags = ["residential-proxy", "smart-tv", "webos", "iot-security", "network-abuse", "supply-chain", "privacy", "credential-stuffing"]
severity = "Medium"
source = "Krebs on Security"
source_url = "https://krebsonsecurity.com/2026/07/lg-to-ban-residential-proxies-from-smart-tv-apps/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [Krebs on Security](https://krebsonsecurity.com/2026/07/lg-to-ban-residential-proxies-from-smart-tv-apps/)

---

Over 42% of apps on LG's webOS smart TV platform were found to be silently routing third-party internet traffic through users' televisions, effectively turning them into residential proxy nodes without consent. LG has announced it will suspend any apps that exploit this capability. This matters because residential proxies are frequently abused to bypass fraud detection, conduct credential stuffing attacks, and obscure malicious traffic origins.


> **Security Architect's Take:** Review your organisation's network egress policies and threat intelligence feeds to flag traffic originating from known residential proxy networks, including those sourced from IoT and smart TV devices. If your environment processes authentication or fraud signals, consider whether residential proxy detection is sufficiently robust to account for non-traditional proxy sources such as consumer electronics.


**Original advisory:** [LG to Ban Residential Proxies from Smart TV Apps](https://krebsonsecurity.com/2026/07/lg-to-ban-residential-proxies-from-smart-tv-apps/)
