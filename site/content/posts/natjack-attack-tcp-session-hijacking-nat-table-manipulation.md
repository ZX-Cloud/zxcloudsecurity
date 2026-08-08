+++
title = "NatJack Attack: TCP Hijacking via NAT Table Manipulation"
date = "2025-08-07T10:58:38Z"
publishDate = "2026-08-07T10:58:38Z"
slug = "natjack-attack-tcp-session-hijacking-nat-table-manipulation"
description = "NatJack exploits NAT state tables to hijack TCP sessions and spoof DNS. Learn what this Black Hat 2026 research means for cloud security architects."
categories = ["general"]
tags = ["natjack", "nat", "tcp-hijacking", "dns-spoofing", "network-security", "session-hijacking", "black-hat-2026"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/new-natjack-attacks-hijack-tcp-sessions.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/new-natjack-attacks-hijack-tcp-sessions.html)

---

Researcher Malcolm Stagg has disclosed NatJack, a new class of network attack that manipulates NAT (Network Address Translation) state tables to hijack live TCP connections, forge DNS responses, and exhaust NAT resources. The technique affects multiple independently developed NAT implementations, including Windows, making it broadly applicable. Presented at Black Hat USA 2026, the research highlights a fundamental weakness in how NAT devices track connection state.


> **Security Architect's Take:** Audit your perimeter and cloud NAT gateway configurations to ensure only legitimate traffic can manipulate connection state — specifically, restrict inbound packets that could forge NAT table entries. For cloud environments, review security group and firewall rules to limit unsolicited inbound UDP/TCP traffic, and monitor for anomalous NAT table exhaustion events as an early indicator of exploitation.


**Original advisory:** [New NatJack Attacks Hijack TCP Sessions and Spoof DNS by Manipulating NAT Tables](https://thehackernews.com/2026/08/new-natjack-attacks-hijack-tcp-sessions.html)
