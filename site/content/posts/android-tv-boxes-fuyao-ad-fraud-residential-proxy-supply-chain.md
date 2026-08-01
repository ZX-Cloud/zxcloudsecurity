+++
title = "Android TV Boxes Turn Broadband Into Proxy Networks"
date = "2024-07-31T14:45:01Z"
publishDate = "2026-07-31T14:45:01Z"
slug = "android-tv-boxes-fuyao-ad-fraud-residential-proxy-supply-chain"
description = "Cheap Android TV boxes ship with apps that fake device identity for ad fraud and enrol owners' broadband as residential proxies. What architects need to kn"
categories = ["general"]
tags = ["android", "iot", "supply-chain", "ad-fraud", "residential-proxy", "malware", "device-spoofing"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/cheap-android-tv-boxes-pose-as-phones.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/cheap-android-tv-boxes-pose-as-phones.html)

---

Cheap Android TV boxes manufactured by a Chinese IoT firm have been found pre-loaded with apps that spoof their device identity to impersonate major smartphone brands, committing ad fraud on behalf of the manufacturer. The same apps also silently enrol owners' home broadband connections into a residential proxy network, effectively monetising victims' internet bandwidth without consent. Dubbed 'Fuyao' by Bitsight researchers, the operation has been attributed to Zhejiang Fengwo IoT Technology Co., Ltd.


> **Security Architect's Take:** Treat consumer-grade Android TV boxes and similar low-cost IoT devices as untrusted endpoints — enforce network segmentation so they cannot reach internal resources or be used as pivot points, and consider blocking or monitoring residential proxy traffic egressing your corporate or cloud environments. If your organisation allows BYOD or guest network access, audit what device categories can connect and review egress anomaly detection for unusual outbound proxy patterns.


**Original advisory:** [Cheap Android TV Boxes Pose as Phones and Turn Owners’ Broadband Into Proxies](https://thehackernews.com/2026/07/cheap-android-tv-boxes-pose-as-phones.html)
