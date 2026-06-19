+++
title = "Popa Botnet Tied to Israeli Firm Alarum Technologies"
date = "2025-06-18T17:37:58Z"
publishDate = "2026-06-18T17:37:58Z"
slug = "popa-botnet-alarum-technologies-netnut-residential-proxy-ad-fraud"
description = "Researchers link the Popa Android botnet to NetNut and Alarum Technologies. Millions of TV boxes used for ad fraud and account takeovers via residential pr"
categories = ["general"]
tags = ["botnet", "residential-proxy", "android", "ad-fraud", "account-takeover", "data-scraping", "supply-chain", "threat-intelligence"]
severity = "High"
source = "Krebs on Security"
source_url = "https://krebsonsecurity.com/2026/06/popa-botnet-linked-to-publicly-traded-israeli-firm/"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [Krebs on Security](https://krebsonsecurity.com/2026/06/popa-botnet-linked-to-publicly-traded-israeli-firm/)

---

A large Android botnet called Popa has been operating for four years, silently turning millions of consumer TV boxes into proxies used for ad fraud, account takeovers, and data scraping. Security researchers have now linked the botnet to NetNut, a residential proxy service run by Alarum Technologies, a publicly-traded Israeli company on NASDAQ. The findings raise serious questions about the legitimacy of the residential proxy industry and how such services may be built on compromised consumer devices.


> **Security Architect's Take:** Review your organisation's use of any residential proxy services, particularly those sourced from third-party providers, and assess whether traffic from such proxies should be blocked at your perimeter or WAF. Additionally, audit cloud workloads and SaaS platforms for anomalous authentication activity originating from residential IP ranges, which are commonly used to bypass geo-restriction and rate-limiting controls.


**Original advisory:** [‘Popa’ Botnet Linked to Publicly-Traded Israeli Firm](https://krebsonsecurity.com/2026/06/popa-botnet-linked-to-publicly-traded-israeli-firm/)
