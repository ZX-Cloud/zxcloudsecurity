+++
title = "Cisco SD-WAN Manager Root Bug Actively Exploited"
date = "2026-06-15T21:48:25Z"
publishDate = "2026-06-15T21:48:25Z"
slug = "cisco-catalyst-sd-wan-manager-root-privilege-escalation-zero-day"
description = "A second Cisco Catalyst SD-WAN Manager zero-day this month allows attackers to gain root access. Patch immediately and restrict management plane exposure."
categories = ["general"]
tags = ["cisco", "sd-wan", "privilege-escalation", "zero-day", "network-security", "remote-code-execution", "patch-management"]
severity = "Critical"
source = "The Register — Security"
source_url = "https://www.theregister.com/patches/2026/06/15/cisco-sd-wan-make-me-root-bug-under-attack/5255916"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/patches/2026/06/15/cisco-sd-wan-make-me-root-bug-under-attack/5255916)

---

A privilege escalation vulnerability in Cisco Catalyst SD-WAN Manager is being actively exploited as a zero-day, allowing attackers to gain root-level access on affected systems. This is the second Cisco Catalyst SD-WAN Manager flaw exploited in the wild this month, suggesting targeted or opportunistic campaigns against network infrastructure. SD-WAN management planes are high-value targets as compromise can provide broad visibility and control over enterprise network traffic.


> **Security Architect's Take:** Patch Cisco Catalyst SD-WAN Manager immediately and audit management plane access logs for any anomalous privilege escalation activity. If patching cannot be done immediately, restrict access to the SD-WAN Manager interface to trusted IP ranges only and ensure it is not exposed to the public internet.


**Original advisory:** [Cisco SD-WAN make-me-root bug under attack](https://www.theregister.com/patches/2026/06/15/cisco-sd-wan-make-me-root-bug-under-attack/5255916)
