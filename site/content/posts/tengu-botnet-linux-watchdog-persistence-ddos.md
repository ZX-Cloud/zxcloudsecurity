+++
title = "Tengu Botnet Uses Linux Watchdog to Survive Removal"
date = "2025-07-28T15:01:33Z"
publishDate = "2026-07-28T15:01:33Z"
slug = "tengu-botnet-linux-watchdog-persistence-ddos"
description = "The Mirai-derived Tengu botnet abuses Linux hardware watchdog timers to reboot compromised devices when defenders kill its process, evading manual remediat"
categories = ["general"]
tags = ["botnet", "linux", "mirai", "ddos", "iot-security", "persistence", "telnet", "edge-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/tengu-botnet-reboots-compromised-linux.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/tengu-botnet-reboots-compromised-linux.html)

---

A new botnet called Tengu, derived from the well-known Mirai malware, can hijack a Linux device's hardware watchdog timer to force a reboot if defenders try to kill its process — giving its persistence mechanisms another chance to re-establish control. It spreads via brute-forced Telnet credentials and supports at least 25 DDoS attack methods. The self-healing capability makes manual incident response significantly harder on affected devices.


> **Security Architect's Take:** Audit and restrict access to hardware watchdog interfaces on Linux-based edge and IoT devices, and enforce strong, unique credentials with Telnet disabled in favour of SSH. Where possible, deploy endpoint detection that monitors watchdog device file access (e.g. /dev/watchdog) as an early indicator of compromise.


**Original advisory:** [Tengu Botnet Reboots Compromised Linux Devices When Defenders Kill Its Process](https://thehackernews.com/2026/07/tengu-botnet-reboots-compromised-linux.html)
