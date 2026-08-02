+++
title = "Hotel Wi-Fi Hijacked to Deploy CornFlake RAT Malware"
date = "2025-08-01T06:29:05Z"
publishDate = "2026-08-01T06:29:05Z"
slug = "hotel-wifi-hijack-cornflake-rat-midnight-blizzard-captivecrunch"
description = "Russian threat group Midnight Blizzard uses hijacked hotel Wi-Fi to push fake browser updates delivering CornFlake RAT, capturing webcam, audio, and keystr"
categories = ["general"]
tags = ["midnight-blizzard", "storm-2945", "remote-access-trojan", "malware", "captive-portal-attack", "surveillance", "endpoint-security", "nation-state"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/hijacked-hotel-wi-fi-pushes-fake.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/hijacked-hotel-wi-fi-pushes-fake.html)

---

Russian state-linked threat actor Midnight Blizzard (via sub-cluster Storm-2945) has been observed hijacking hotel Wi-Fi networks to serve fake browser update prompts, deploying a remote access trojan called CornFlake. The malware can silently capture webcam footage, microphone audio, and keystrokes from compromised devices. This campaign, tracked as CaptiveCrunch, targets travellers likely connected to business and government sectors.


> **Security Architect's Take:** Enforce mandatory VPN-before-anything policies for corporate devices on untrusted networks, and block browser update prompts that originate from non-vendor domains via endpoint policy. Consider deploying application allowlisting to prevent unauthorised executables running from browser download paths, particularly on laptops issued to travelling employees or executives.


**Original advisory:** [Hijacked Hotel Wi-Fi Pushes Fake Updates to Deliver Surveillance Malware](https://thehackernews.com/2026/08/hijacked-hotel-wi-fi-pushes-fake.html)
