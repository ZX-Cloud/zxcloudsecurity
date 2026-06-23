+++
title = "DifyTap Flaws Let Attackers Read AI Chats Across Tenants"
date = "2025-06-22T16:13:28Z"
publishDate = "2026-06-22T16:13:28Z"
slug = "difytap-dify-vulnerabilities-cross-tenant-ai-conversation-exposure"
description = "Four DifyTap vulnerabilities in the Dify AI platform allow unauthenticated attackers to access other tenants' AI conversations, posing serious multi-tenanc"
categories = ["general"]
tags = ["dify", "difytap", "multi-tenancy", "ai-security", "unauthenticated-access", "agentic-ai", "data-exposure", "open-source"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/researchers-detail-difytap-flaws-in.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/researchers-detail-difytap-flaws-in.html)

---

Four vulnerabilities collectively dubbed DifyTap have been found in Dify, a widely-used open-source AI workflow platform, that allow attackers to read AI conversations belonging to other tenants without needing to log in. Discovered by Zafran Security, the flaws represent a serious multi-tenancy isolation failure in a platform used to build and deploy AI agents. This matters because AI conversations often contain sensitive business data, proprietary prompts, and potentially personal information.


> **Security Architect's Take:** If your organisation self-hosts Dify or uses a shared Dify deployment, audit your instance version immediately and apply available patches — prioritise this if Dify is exposed to the internet or used across multiple teams or customers. Until patched, consider restricting network access to Dify's API endpoints and reviewing audit logs for unexpected cross-tenant data access patterns.


**Original advisory:** [Researchers Detail DifyTap Flaws in Dify That Could Expose AI Chats Across Tenants](https://thehackernews.com/2026/06/researchers-detail-difytap-flaws-in.html)
