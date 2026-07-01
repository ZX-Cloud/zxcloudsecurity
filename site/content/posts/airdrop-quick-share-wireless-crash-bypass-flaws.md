+++
title = "AirDrop & Quick Share Flaws: Crash Attacks via Wi-Fi"
date = "2025-06-30T09:27:58Z"
publishDate = "2026-06-30T09:27:58Z"
slug = "airdrop-quick-share-wireless-crash-bypass-flaws"
description = "Six flaws in Apple AirDrop and Google Quick Share let nearby attackers crash devices or bypass checks with no user interaction. What security teams must do"
categories = ["general"]
tags = ["apple", "airdrop", "quick-share", "android", "denial-of-service", "proximity-attack", "mdm", "zero-interaction"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/airdrop-and-quick-share-flaws-let.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/airdrop-and-quick-share-flaws-let.html)

---

Six security vulnerabilities have been discovered in Apple AirDrop and Google Quick Share, the wireless file-transfer features built into macOS, iOS, and Android devices. An attacker within Wi-Fi or Bluetooth range can crash the sharing service on devices configured to receive from anyone, requiring no prior pairing, authentication, or user interaction. The flaws pose a real risk in high-density environments such as offices, conferences, and public spaces where corporate devices are common.


> **Security Architect's Take:** Enforce device management policies (MDM/EMM) to restrict AirDrop to 'Contacts Only' or disable it entirely on corporate Apple devices, and configure Quick Share to 'Your devices only' on managed Android endpoints. Review endpoint policy compliance across your fleet now, ahead of patches, as the zero-interaction crash vector is readily exploitable in shared office environments.


**Original advisory:** [AirDrop and Quick Share Flaws Let Nearby Attackers Trigger Crashes and Bypass Checks](https://thehackernews.com/2026/06/airdrop-and-quick-share-flaws-let.html)
