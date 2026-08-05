+++
title = "SMOKE#SCREEN: Fake Adobe & Zoom Updates Deploy ScreenConnect"
date = "2025-08-04T13:11:22Z"
publishDate = "2026-08-04T13:11:22Z"
slug = "smoke-screen-fake-adobe-zoom-updates-screenconnect-persistent-remote-access"
description = "The SMOKE#SCREEN campaign uses fake Adobe and Zoom updates to silently install ConnectWise ScreenConnect, giving attackers persistent remote access."
categories = ["general"]
tags = ["connectwise-screenconnect", "rmm-abuse", "social-engineering", "malware-distribution", "persistent-access", "endpoint-security", "phishing"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/fake-adobe-and-zoom-updates-install.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/fake-adobe-and-zoom-updates-install.html)

---

Attackers are running a multi-wave social engineering campaign, dubbed SMOKE#SCREEN, that tricks users into installing ConnectWise ScreenConnect by disguising it as legitimate Adobe or Zoom software updates, document reviews, or system maintenance tools. Once installed, ScreenConnect gives attackers persistent, legitimate-looking remote access to compromised machines. Because RMM tools are trusted by most security controls, this activity is difficult to detect and evict.


> **Security Architect's Take:** Audit your environment for unauthorised or unexpected ScreenConnect/ConnectWise installations and enforce application allowlisting to block unapproved RMM tools. Ensure endpoint policies restrict the execution of software installers downloaded from the web by standard users, and consider blocking ScreenConnect's known C2 domains at your proxy or firewall if the tool is not sanctioned in your organisation.


**Original advisory:** [Fake Adobe and Zoom Updates Install ScreenConnect for Persistent Remote Access](https://thehackernews.com/2026/08/fake-adobe-and-zoom-updates-install.html)
