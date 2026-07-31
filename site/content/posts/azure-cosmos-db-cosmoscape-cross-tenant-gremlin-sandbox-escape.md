+++
title = "Azure Cosmos DB CosmosEscape Flaw: Cross-Tenant Risk"
date = "2026-07-30T13:34:09Z"
publishDate = "2026-07-30T13:34:09Z"
slug = "azure-cosmos-db-cosmoscape-cross-tenant-gremlin-sandbox-escape"
description = "A patched Azure Cosmos DB vulnerability let attackers escape the Gremlin sandbox and access databases across all customer tenants using a platform-wide key"
categories = ["general"]
tags = ["azure", "cosmos-db", "sandbox-escape", "cross-tenant", "gremlin", "data-exfiltration", "privilege-escalation", "paas-security"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/azure-cosmos-db-flaw-exposed-platform.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/azure-cosmos-db-flaw-exposed-platform.html)

---

A now-patched vulnerability in Azure Cosmos DB allowed an attacker to escape the Gremlin query sandbox and gain full read/write access to databases belonging to other tenants on the same platform. Discovered by Wiz and dubbed CosmosEscape, the exploit chain started with a specially crafted Gremlin query on an attacker-controlled database, ultimately yielding a platform-wide key. This is significant because a single exploit could have compromised data across every customer using the affected service.


> **Security Architect's Take:** Although Microsoft has patched this server-side, review your Cosmos DB audit logs and access history for any anomalous Gremlin query patterns or unexpected key usage as a precautionary measure. Additionally, treat this as a prompt to validate your data-tier isolation assumptions — platform-managed services can still carry cross-tenant blast radius, so ensure sensitive workloads have compensating controls such as customer-managed keys and network restrictions.


**Original advisory:** [Azure Cosmos DB Flaw Exposed Platform-Wide Key That Could Access Any Database](https://thehackernews.com/2026/07/azure-cosmos-db-flaw-exposed-platform.html)
