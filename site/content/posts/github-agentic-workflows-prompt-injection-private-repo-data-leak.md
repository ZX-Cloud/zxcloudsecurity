+++
title = "GitHub Agentic Workflows Vulnerable to Prompt Injection"
date = "2025-07-07T14:04:50Z"
publishDate = "2026-07-07T14:04:50Z"
slug = "github-agentic-workflows-prompt-injection-private-repo-data-leak"
description = "A malicious public GitHub issue can trick AI agentic workflows into leaking private repo data — no credentials required. Here's what architects need to kno"
categories = ["general"]
tags = ["github", "prompt-injection", "agentic-ai", "data-exfiltration", "supply-chain", "least-privilege", "ai-security", "devops-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/public-github-issue-could-trick-github.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/public-github-issue-could-trick-github.html)

---

Researchers at Noma Security have demonstrated that a malicious actor can craft a seemingly innocent issue on a public GitHub repository to manipulate GitHub Agentic Workflows into exfiltrating data from an organisation's private repositories. The attack requires no credentials, no insider access, and no code changes — just a public issue post. If an AI agent has been granted broad read access across repositories, it can be prompted indirectly to leak sensitive private content, a classic prompt injection scenario applied to agentic AI pipelines.


> **Security Architect's Take:** Audit and aggressively restrict the repository permissions granted to any GitHub AI agents or Copilot-powered workflows — apply least-privilege so agents can only access the specific repositories they need. Additionally, treat any externally-sourced content (issues, PRs, comments) as untrusted input and evaluate whether your organisation's agentic workflows have adequate guardrails to prevent prompt injection from public surfaces.


**Original advisory:** [Public GitHub Issue Could Trick GitHub Agentic Workflows Into Leaking Private Repo Data](https://thehackernews.com/2026/07/public-github-issue-could-trick-github.html)
