+++
title = "Silver Fox BYOVD Attack Delivers ValleyRAT to Manufacturers"
date = "2025-07-30T10:32:59Z"
publishDate = "2026-07-30T10:32:59Z"
slug = "silverfox-byovd-valleyrat-japanese-manufacturer-attack"
description = "Chinese threat group Silver Fox targets Japanese manufacturers with a 3-driver BYOVD chain to deploy ValleyRAT persistent remote access malware."
categories = ["general"]
tags = ["byovd", "valleyrat", "winos-4.0", "silver-fox", "windows-kernel", "malware", "industrial-manufacturing", "threat-actor"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/silverfox-targets-japanese-manufacturer.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/silverfox-targets-japanese-manufacturer.html)

---

The Chinese cybercrime group Silver Fox is deploying a sophisticated three-driver BYOVD (Bring Your Own Vulnerable Driver) attack chain against a Japanese industrial manufacturer, ultimately installing ValleyRAT (also known as Winos 4.0) for persistent remote access. The attack abuses legitimate but vulnerable Windows kernel drivers to bypass endpoint defences and gain elevated privileges. This is notable for its novel combination of driver abuse techniques and its targeting of critical industrial manufacturing infrastructure.


> **Security Architect's Take:** Enforce strict kernel driver allowlisting using Windows Defender Application Control (WDAC) policies and ensure your EDR solution has BYOVD detection capabilities enabled. Cross-reference your environment against Microsoft's vulnerable driver blocklist and consider network-level monitoring for ValleyRAT C2 indicators, particularly in OT/ICS-adjacent environments.


**Original advisory:** [SilverFox Targets Japanese Manufacturer with 3-Driver BYOVD Chain and ValleyRAT](https://thehackernews.com/2026/07/silverfox-targets-japanese-manufacturer.html)
