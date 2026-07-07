+++
title = "TrojPix: Data Exfiltration from Air-Gapped PCs via Video Cab"
date = "2024-07-06T08:50:54Z"
publishDate = "2026-07-06T08:50:54Z"
slug = "trojpix-air-gapped-data-exfiltration-video-cable-emissions"
description = "TrojPix exploits video cable radio emissions to leak data from air-gapped systems. Learn what this side-channel attack means for high-security environments"
categories = ["general"]
tags = ["air-gap", "side-channel", "data-exfiltration", "malware", "physical-security", "covert-channel", "endpoint-security"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-trojpix-attack-leaks-data-from-air.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-trojpix-attack-leaks-data-from-air.html)

---

Researchers have demonstrated a technique called TrojPix that exfiltrates data from air-gapped computers by subtly manipulating on-screen pixels to generate detectable radio emissions from the video cable, which a nearby receiver can decode. The attack requires malware to already be present on the target machine. It represents a novel side-channel threat for high-security environments that rely on physical isolation as a primary defence.


> **Security Architect's Take:** For environments handling sensitive workloads on air-gapped systems — including on-premises infrastructure supporting classified or regulated data — review physical security controls around terminal access and consider RF shielding or Faraday enclosures for the most sensitive machines. Prioritise preventing initial malware compromise, as TrojPix is entirely dependent on a prior foothold.


**Original advisory:** [New TrojPix Attack Leaks Data From Air-Gapped Systems via Video Cable Emissions](https://thehackernews.com/2026/07/new-trojpix-attack-leaks-data-from-air.html)
