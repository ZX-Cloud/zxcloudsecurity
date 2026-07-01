+++
title = "Microsoft: Poisoned MCP Tools Can Make AI Agents Leak Data"
date = "2025-06-30T17:46:07Z"
publishDate = "2026-06-30T17:46:07Z"
slug = "microsoft-poisoned-mcp-tool-descriptions-ai-agent-data-exfiltration"
description = "Microsoft research reveals attackers can hijack AI agents via poisoned MCP tool descriptions, silently exfiltrating corporate data without triggering alert"
categories = ["general"]
tags = ["azure", "ai-agents", "mcp", "prompt-injection", "data-exfiltration", "supply-chain", "llm-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/microsoft-warns-poisoned-mcp-tool.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/microsoft-warns-poisoned-mcp-tool.html)

---

Microsoft researchers have demonstrated how attackers can manipulate AI agents by embedding malicious instructions inside MCP (Model Context Protocol) tool descriptions, causing the agent to silently exfiltrate sensitive company data without triggering standard security alerts. Because the agent follows its programmed logic at every step, the behaviour appears entirely routine. This highlights a significant emerging attack surface as organisations increasingly deploy AI agents with access to internal systems and data.


> **Security Architect's Take:** Audit all MCP tool descriptions and third-party tool registries your AI agents consume, treating them as untrusted input — apply strict allowlisting and integrity checks. Implement output monitoring and data-loss prevention controls on agent egress paths, and consider least-privilege scoping for any agent identity tokens to limit blast radius if manipulation occurs.


**Original advisory:** [Microsoft Warns Poisoned MCP Tool Descriptions Can Make AI Agents Leak Data](https://thehackernews.com/2026/06/microsoft-warns-poisoned-mcp-tool.html)
