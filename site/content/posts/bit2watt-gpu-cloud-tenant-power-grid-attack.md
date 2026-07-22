+++
title = "Bit2Watt: GPU Attack Threatens Power Grid Stability"
date = "2025-07-21T11:24:50Z"
publishDate = "2026-07-21T11:24:50Z"
slug = "bit2watt-gpu-cloud-tenant-power-grid-attack"
description = "Bit2Watt lets cloud tenants use standard GPU access to rapidly spike power draw in data centres, threatening grid stability — no exploit needed."
categories = ["general"]
tags = ["gpu", "data-centre-security", "power-grid", "side-channel", "cloud-infrastructure", "physical-security", "multi-tenancy"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-bit2watt-attack-could-let-cloud.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-bit2watt-attack-could-let-cloud.html)

---

Bit2Watt is a newly disclosed attack technique that allows a cloud tenant with standard GPU access to rapidly fluctuate a data centre's power consumption, potentially destabilising the electrical grid it relies on — no exploit or privileged access required. Researchers from Zhejiang University demonstrated this by deliberately crafting GPU workloads that cause large, rapid swings in power draw. The significance is that it crosses the boundary between cyber and physical infrastructure risk, threatening grid stability as a side effect of legitimate-looking cloud usage.


> **Security Architect's Take:** Raise this with your data centre and cloud provider counterparts now — ask specifically what power-draw rate-limiting or anomaly detection controls exist at the hypervisor and facility level for GPU workloads. In the interim, consider whether your threat model for critical or grid-adjacent deployments should include physical infrastructure impact scenarios, and flag this to your operational technology (OT) or physical security teams.


**Original advisory:** [New Bit2Watt Attack Could Let Cloud Tenants Disrupt Power Grids Without an Exploit](https://thehackernews.com/2026/07/new-bit2watt-attack-could-let-cloud.html)
