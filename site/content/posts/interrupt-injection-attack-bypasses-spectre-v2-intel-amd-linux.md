+++
title = "INTERRUPT INJECTION Bypasses Spectre v2 on Intel & AMD"
date = "2025-08-06T16:17:13Z"
publishDate = "2026-08-06T16:17:13Z"
slug = "interrupt-injection-attack-bypasses-spectre-v2-intel-amd-linux"
description = "MIT CSAIL's INTERRUPT INJECTION attack bypasses all default Spectre v2 CPU mitigations on Linux, affecting Intel and AMD. Learn the cloud security impact."
categories = ["general"]
tags = ["spectre", "side-channel", "cpu-vulnerability", "linux-kernel", "intel", "amd", "privilege-escalation", "cloud-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/new-interrupt-injection-attack-can.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/new-interrupt-injection-attack-can.html)

---

Researchers at MIT CSAIL have discovered a new CPU side-channel attack called INTERRUPT INJECTION that can bypass all default Spectre v2 mitigations on Intel and AMD processors running Linux. An unprivileged user-space process can time a hardware interrupt to re-poison the branch predictor immediately after the kernel has sanitised it, rendering existing defences ineffective. This matters because it affects any shared Linux environment — including cloud virtual machines — where untrusted workloads run alongside sensitive kernel operations.


> **Security Architect's Take:** Until kernel patches are available and deployed by cloud providers, consider enforcing stronger workload isolation by running sensitive workloads on dedicated bare-metal instances or single-tenant VMs, and engage your cloud provider on their patch timeline. For multi-tenant environments, evaluate whether disabling simultaneous multithreading (SMT) is operationally feasible as an interim risk reduction measure.


**Original advisory:** [New Interrupt Injection Attack Can Bypass Spectre v2 Defenses on Intel and AMD CPUs](https://thehackernews.com/2026/08/new-interrupt-injection-attack-can.html)
