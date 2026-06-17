+++
title = "Rokarolla Android Trojan Steals PINs & Crypto Funds"
date = "2025-06-16T13:10:17Z"
publishDate = "2026-06-16T13:10:17Z"
slug = "rokarolla-android-banking-trojan-pin-sms-crypto-theft"
description = "Rokarolla Android malware targets 217 banking and crypto apps, stealing PINs, intercepting SMS MFA codes, and hijacking crypto payments via clipboard rewri"
categories = ["general"]
tags = ["android", "mobile-malware", "banking-trojan", "cryptocurrency", "mfa-bypass", "sms-interception", "clipboard-hijacking", "zimperium"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/new-rokarolla-android-malware-steals.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/new-rokarolla-android-malware-steals.html)

---

A newly documented Android banking trojan called Rokarolla targets 217 banking and cryptocurrency applications, giving attackers near-complete control of infected devices. It can steal lock-screen PINs, intercept SMS-based two-factor authentication codes, and hijack cryptocurrency transactions by silently rewriting clipboard content. With 137 remote commands at an operator's disposal, the potential for account takeover and financial theft is significant.


> **Security Architect's Take:** Enforce mobile device management (MDM) policies that restrict sideloading and require app allowlisting on any corporate or BYOD devices accessing cloud workloads or financial systems. Additionally, review whether SMS-based MFA is used to protect privileged accounts and migrate to hardware tokens or authenticator apps, as SMS interception renders that second factor useless against this threat.


**Original advisory:** [New Rokarolla Android Malware Steals PINs, SMS Codes, and Crypto Wallet Funds](https://thehackernews.com/2026/06/new-rokarolla-android-malware-steals.html)
