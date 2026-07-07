+++
title = "SkillCloak: Malicious AI Agent Skills Evade Scanners"
date = "2025-07-06T06:33:56Z"
publishDate = "2026-07-06T06:33:56Z"
slug = "skillcloak-malicious-ai-agent-skills-evade-static-scanners"
description = "SkillCloak uses self-extracting packing to bypass static scanners for AI coding agent skills 90%+ of the time — here's what security architects need to kno"
categories = ["general"]
tags = ["ai-security", "supply-chain", "malware-evasion", "ai-coding-agents", "static-analysis", "runtime-detection", "plugin-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-skillcloak-technique-lets-malicious.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-skillcloak-technique-lets-malicious.html)

---

Researchers at Hong Kong University of Science and Technology have demonstrated a technique called SkillCloak that uses self-extracting packing to disguise malicious add-on 'skills' for AI coding agents, bypassing static security scanners over 90% of the time. This is significant because AI coding agents such as GitHub Copilot and Cursor increasingly rely on third-party skills or plugins, creating a new supply chain attack surface. The same research team also developed a runtime detection tool that catches the majority of evasion attempts.


> **Security Architect's Take:** Treat AI agent skill/plugin ecosystems as an untrusted supply chain: enforce allowlists of approved skills, mandate runtime behavioural scanning over static-only approaches, and sandbox AI agent environments with least-privilege network and filesystem access to limit blast radius if a malicious skill executes.


**Original advisory:** [SkillCloak Lets Malicious AI Agent Skills Evade Static Scanners with Self-Extracting Packing](https://thehackernews.com/2026/07/new-skillcloak-technique-lets-malicious.html)
