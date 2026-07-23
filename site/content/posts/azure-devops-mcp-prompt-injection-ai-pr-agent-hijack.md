+++
title = "Azure DevOps MCP Prompt Injection Hijacks AI PR Agents"
date = "2025-07-22T04:57:52Z"
publishDate = "2026-07-22T04:57:52Z"
slug = "azure-devops-mcp-prompt-injection-ai-pr-agent-hijack"
description = "A prompt injection flaw in Microsoft's Azure DevOps MCP server lets attackers use hidden PR comments to hijack AI review agents and leak repository data."
categories = ["general"]
tags = ["azure", "azure-devops", "mcp", "prompt-injection", "ai-security", "supply-chain", "code-review", "lateral-movement"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/microsoft-azure-devops-mcp-flaw-lets.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/microsoft-azure-devops-mcp-flaw-lets.html)

---

A prompt injection vulnerability in Microsoft's official Azure DevOps MCP (Model Context Protocol) server allows an attacker to embed hidden malicious instructions within a pull request comment or description. When an AI coding agent reviews that PR, it can be manipulated into accessing repositories and resources beyond its intended scope, silently exfiltrating data. This matters because AI-assisted code review is rapidly becoming standard practice, and the attack requires no elevated privileges from the attacker — just the ability to post a PR comment.


> **Security Architect's Take:** Audit any AI review agent pipelines using the Azure DevOps MCP server and restrict their OAuth scopes and repository access to the minimum required; treat MCP tool outputs as untrusted input and ensure agents cannot act on cross-repository resources until Microsoft ships a guardrailed patch. Consider disabling automated AI PR review on public or external-contributor repositories as an interim control.


**Original advisory:** [Microsoft Azure DevOps MCP Flaw Lets Hidden PR Comments Hijack AI Review Agents](https://thehackernews.com/2026/07/microsoft-azure-devops-mcp-flaw-lets.html)
