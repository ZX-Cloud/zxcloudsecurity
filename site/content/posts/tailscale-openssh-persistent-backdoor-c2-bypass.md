+++
title = "Tailscale & OpenSSH Abused for Persistent Backdoor Access"
date = "2024-06-17T16:00:56Z"
publishDate = "2026-06-17T16:00:56Z"
slug = "tailscale-openssh-persistent-backdoor-c2-bypass"
description = "A low-skilled attacker used Tailscale and OpenSSH to maintain access to a compromised machine after his C2 server went offline. Here's what architects need"
categories = ["general"]
tags = ["tailscale", "openssh", "persistence", "backdoor", "keylogger", "command-and-control", "endpoint-security", "living-off-the-land"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/junior-hacker-used-tailscale-and.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/junior-hacker-used-tailscale-and.html)

---

A low-skilled, French-speaking attacker compromised a small French automotive firm, deploying a keylogger to steal banking and email credentials. Crucially, before his command-and-control infrastructure went offline, he installed OpenSSH and Tailscale on the victim machine to create a resilient, C2-independent backdoor. This technique demonstrates how legitimate networking tools can be abused to maintain persistent access even after primary attacker infrastructure is taken down.


> **Security Architect's Take:** Audit your environment for unauthorised installations of legitimate remote-access and mesh-networking tools such as Tailscale, ZeroTier, and OpenSSH — these can bypass traditional C2 detection entirely. Implement application allowlisting and egress filtering to prevent unapproved software from establishing outbound tunnels, and alert on new SSH daemon processes or VPN agent installations on endpoints.


**Original advisory:** [Junior Hacker Used Tailscale and OpenSSH to Keep Access After His C2 Went Offline](https://thehackernews.com/2026/06/junior-hacker-used-tailscale-and.html)
