+++
title = "Daxin Rootkit & Stupig Backdoor Target Taiwan Firms"
date = "2025-07-16T11:17:23Z"
publishDate = "2026-07-16T11:17:23Z"
slug = "daxin-rootkit-stupig-backdoor-taiwan-manufacturing-espionage"
description = "China-linked Daxin rootkit resurfaces at a Taiwanese manufacturer alongside new Stupig pre-login SYSTEM backdoor. What security architects need to know."
categories = ["general"]
tags = ["rootkit", "apt", "china-nexus", "backdoor", "kernel-exploit", "espionage", "manufacturing", "endpoint-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/daxin-resurfaces-in-taiwan-alongside.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/daxin-resurfaces-in-taiwan-alongside.html)

---

Daxin, a sophisticated kernel-mode rootkit previously linked to Chinese state-sponsored threat actors, has reappeared at a Taiwanese manufacturing firm over four years after its initial public disclosure. Alongside it, researchers discovered a previously undocumented backdoor called Stupig, capable of operating before user login at SYSTEM-level privileges. The combination represents a highly capable, stealthy intrusion toolkit likely used for long-term espionage within critical industrial environments.


> **Security Architect's Take:** Review endpoint detection coverage for kernel-mode drivers — particularly unsigned or anomalous kernel modules such as 'srt64.sys' — and ensure EDR solutions are configured to alert on pre-boot and pre-login persistence mechanisms. Manufacturing and OT-adjacent environments should audit privileged access paths and verify integrity of kernel drivers as a priority given this threat actor's targeting pattern.


**Original advisory:** [Daxin Resurfaces in Taiwan Alongside Stupig Pre-Login SYSTEM Backdoor](https://thehackernews.com/2026/07/daxin-resurfaces-in-taiwan-alongside.html)
