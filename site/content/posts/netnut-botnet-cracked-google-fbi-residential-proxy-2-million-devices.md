+++
title = "NetNut Botnet Cracked: FBI & Google Hit 2M-Device Network"
date = "2025-07-03T12:03:00Z"
publishDate = "2026-07-03T12:03:00Z"
slug = "netnut-botnet-cracked-google-fbi-residential-proxy-2-million-devices"
description = "Google and the FBI have disrupted the NetNut residential proxy botnet spanning 2 million devices. Other proxy services may share the same infrastructure."
categories = ["general"]
tags = ["botnet", "residential-proxy", "netnut", "credential-stuffing", "fraud", "threat-intelligence", "network-security", "fbi"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/03/netnut-cracked-as-google-and-fbi-target-2-million-device-botnet/5266414"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/03/netnut-cracked-as-google-and-fbi-target-2-million-device-botnet/5266414)

---

Google and the FBI have taken action against a botnet of approximately 2 million compromised devices linked to the residential proxy service NetNut. Residential proxy networks of this scale are frequently abused to route malicious traffic — including credential stuffing, scraping, and fraud — through legitimate-looking IP addresses. The operation raises concerns that other residential proxy brands may be drawing on the same underlying compromised infrastructure.


> **Security Architect's Take:** Review your WAF and authentication logs for traffic sourced from residential proxy IP ranges; consider integrating a reputable proxy/threat-intelligence feed to detect and block known residential proxy egress nodes, and ensure rate-limiting and anomaly detection are tuned to catch low-and-slow abuse patterns that blend with legitimate residential traffic.


**Original advisory:** [NetNut cracked as Google and FBI target 2 million-device botnet](https://www.theregister.com/security/2026/07/03/netnut-cracked-as-google-and-fbi-target-2-million-device-botnet/5266414)
