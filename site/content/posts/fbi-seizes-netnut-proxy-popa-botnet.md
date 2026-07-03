+++
title = "FBI Seizes NetNut Proxy & Popa Botnet Domains"
date = "2025-07-02T19:27:33Z"
publishDate = "2026-07-02T19:27:33Z"
slug = "fbi-seizes-netnut-proxy-popa-botnet"
description = "The FBI seized hundreds of NetNut domains tied to the Popa botnet, a 2M+ device network used to anonymise malicious traffic. Here's what cloud architects n"
categories = ["general"]
tags = ["botnet", "residential-proxy", "netnut", "popa-botnet", "fraud-detection", "bot-mitigation", "threat-intelligence", "law-enforcement"]
severity = "High"
source = "Krebs on Security"
source_url = "https://krebsonsecurity.com/2026/07/fbi-seizes-netnut-proxy-platform-popa-botnet/"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [Krebs on Security](https://krebsonsecurity.com/2026/07/fbi-seizes-netnut-proxy-platform-popa-botnet/)

---

The FBI has seized hundreds of domains linked to NetNut, a residential proxy service run by Nasdaq-listed Israeli firm Alarum Technologies, following revelations that it was connected to the Popa botnet — a network of over two million compromised devices enrolled without meaningful user consent. Residential proxy networks like this are routinely abused to anonymise malicious traffic, making them a significant threat to cloud-based fraud detection, rate limiting, and access controls. The seizure follows investigative reporting by KrebsOnSecurity and coordinated action with industry partners.


> **Security Architect's Take:** Review your WAF and API gateway logs for traffic originating from residential proxy ranges — tools such as IPQualityScore, IPDB, or Cloudflare's bot management can help identify and block known residential proxy infrastructure. Consider tightening bot detection policies and flagging unusual geographic or ASN anomalies in authentication and scraping-sensitive endpoints.


**Original advisory:** [FBI Seizes NetNut Proxy Platform, Popa Botnet](https://krebsonsecurity.com/2026/07/fbi-seizes-netnut-proxy-platform-popa-botnet/)
