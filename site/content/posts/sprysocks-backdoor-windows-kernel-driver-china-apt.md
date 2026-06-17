+++
title = "SprySOCKS Backdoor Now Targets Windows via Kernel Driver"
date = "2025-06-16T09:44:34Z"
publishDate = "2026-06-16T09:44:34Z"
slug = "sprysocks-backdoor-windows-kernel-driver-china-apt"
description = "Chinese-linked SprySOCKS backdoor expands from Linux to Windows with driver-based stealth variants. Learn the risks for cloud Windows workloads."
categories = ["general"]
tags = ["sprysocks", "apt", "backdoor", "windows", "kernel-driver", "stealth-malware", "threat-intelligence", "china-linked"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/china-linked-sprysocks-backdoor-expands.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/china-linked-sprysocks-backdoor-expands.html)

---

Researchers at ESET have discovered two previously unknown Windows variants of SprySOCKS, a backdoor previously thought to be Linux-only and linked to Chinese threat actors. The new variants, internally labelled WIN_DRV and WIN_PLUS, use kernel-level drivers to evade detection and communicate with attacker infrastructure over TCP and UDP. This significantly expands the threat's attack surface to Windows environments, including cloud-hosted Windows workloads.


> **Security Architect's Take:** Review endpoint detection coverage on Windows-based cloud workloads (e.g. Azure VMs, AWS EC2 Windows instances) to ensure kernel-level driver activity and unsigned or anomalous driver loads are monitored; consider enforcing Windows Defender Application Control (WDAC) or equivalent allowlisting policies to block unauthorised kernel drivers.


**Original advisory:** [China-Linked SprySOCKS Backdoor Expands to Windows with Driver-Based Stealth](https://thehackernews.com/2026/06/china-linked-sprysocks-backdoor-expands.html)
