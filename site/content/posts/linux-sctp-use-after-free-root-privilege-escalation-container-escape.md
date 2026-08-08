+++
title = "Linux SCTP Use-After-Free: Root Exploit & Container Escape"
date = "2025-08-07T11:10:33Z"
publishDate = "2026-08-07T11:10:33Z"
slug = "linux-sctp-use-after-free-root-privilege-escalation-container-escape"
description = "An 18-year-old Linux SCTP kernel flaw enables local privilege escalation to root and container escape. Patch to kernel 6.6.148+ immediately."
categories = ["general"]
tags = ["linux", "kernel", "sctp", "use-after-free", "privilege-escalation", "container-escape", "kubernetes", "container-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/18-year-old-linux-sctp-flaw-could-let.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/18-year-old-linux-sctp-flaw-could-let.html)

---

An 18-year-old use-after-free vulnerability in the Linux kernel's SCTP networking code allows a local user to escalate privileges to root. Tencent researchers demonstrated that the flaw can also be used to break out of a container and compromise the underlying host. Patched kernels were released on 3 August 2026; any system running an older kernel with SCTP accessible is at risk.


> **Security Architect's Take:** Prioritise kernel updates to 6.6.148, 6.12.101, 6.18.42, or 7.1.6 across all Linux-based workloads, paying particular attention to container hosts and Kubernetes nodes where container-escape risk is highest. If immediate patching is not possible, disable or restrict access to SCTP via kernel module blocklisting or network policy as a temporary mitigation.


**Original advisory:** [18-Year-Old Linux SCTP Flaw Could Let Local Users Gain Root and Escape Containers](https://thehackernews.com/2026/08/18-year-old-linux-sctp-flaw-could-let.html)
