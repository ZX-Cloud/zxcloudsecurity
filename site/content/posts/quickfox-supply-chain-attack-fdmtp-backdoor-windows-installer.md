+++
title = "QuickFox Supply Chain Attack Drops FDMTP Backdoor"
date = "2025-08-05T05:47:19Z"
publishDate = "2026-08-05T05:47:19Z"
slug = "quickfox-supply-chain-attack-fdmtp-backdoor-windows-installer"
description = "A trojanised QuickFox Windows installer has delivered the FDMTP backdoor since August 2025. Learn what cloud security teams should do now."
categories = ["general"]
tags = ["supply-chain", "backdoor", "windows", "vpn", "fdmtp", "quickfox", "malware", "endpoint-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/quickfox-supply-chain-attack-delivers.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/quickfox-supply-chain-attack-delivers.html)

---

A trojanised version of QuickFox, a VPN tool popular with overseas Chinese users, has been used to deliver a backdoor called FDMTP in a supply chain attack active since at least August 2025. Attackers compromised the Windows installer to silently deploy malware alongside the legitimate application. Supply chain attacks of this nature are particularly dangerous because users trust the software source and security tools may not flag a signed or expected installer.


> **Security Architect's Take:** Audit your organisation's approved software list for QuickFox or similar niche VPN tools, and enforce application allowlisting and binary integrity checks on all Windows endpoints. Consider blocking installer execution from unmanaged or personal devices that access corporate cloud resources, and ensure endpoint detection tooling covers post-installation backdoor behaviour such as FDMTP's C2 communications.


**Original advisory:** [QuickFox Supply Chain Attack Delivers FDMTP Backdoor via Trojanized Windows Installer](https://thehackernews.com/2026/08/quickfox-supply-chain-attack-delivers.html)
