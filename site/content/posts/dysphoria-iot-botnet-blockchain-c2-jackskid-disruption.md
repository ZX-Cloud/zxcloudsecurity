+++
title = "Dysphoria IoT Botnet Uses Blockchain C2 to Evade Takedown"
date = "2025-07-27T17:16:28Z"
publishDate = "2026-07-27T17:16:28Z"
slug = "dysphoria-iot-botnet-blockchain-c2-jackskid-disruption"
description = "The Dysphoria IoT botnet now uses blockchain name services and infected-device relays, making traditional C2 disruption tactics ineffective. Here's what ar"
categories = ["general"]
tags = ["iot-security", "botnet", "command-and-control", "blockchain-c2", "network-security", "egress-filtering", "threat-intelligence"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/dysphoria-iot-botnet-adds-blockchain-c2.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/dysphoria-iot-botnet-adds-blockchain-c2.html)

---

The Dysphoria IoT botnet has evolved its command-and-control infrastructure to use blockchain-based naming services and relay traffic through compromised devices, following a law enforcement takedown of the JackSkid botnet in March. This architectural shift makes traditional C2 disruption techniques — such as domain seizure and sinkholing — largely ineffective. The botnet poses a persistent threat to organisations with internet-exposed IoT devices, particularly those that are unpatched or using default credentials.


> **Security Architect's Take:** Audit your network perimeter for exposed IoT and OT devices and ensure they cannot reach arbitrary external endpoints — egress filtering and micro-segmentation are your primary controls here. Blockchain-based C2 cannot be sinkholed, so detection must rely on behavioural anomalies and DNS/network traffic analysis rather than blocklists alone.


**Original advisory:** [Dysphoria IoT Botnet Adds Blockchain C2 and Victim Relays After JackSkid Disruption](https://thehackernews.com/2026/07/dysphoria-iot-botnet-adds-blockchain-c2.html)
