+++
title = "GitHub AI Agent Leaks Private Repos: GitLost Flaw"
date = "2025-07-07T19:49:01Z"
publishDate = "2026-07-07T19:49:01Z"
slug = "github-ai-agent-private-repo-leak-gitlost"
description = "A GitHub AI agent vulnerability dubbed GitLost exposes private repositories via simple prompts, with no patch or vendor documentation available."
categories = ["general"]
tags = ["github", "ai-agent", "copilot", "data-exposure", "prompt-injection", "source-code-leak", "access-control", "supply-chain"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/07/github-ai-agent-leaks-private-repos-when-asked-nicely/5267924"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/07/github-ai-agent-leaks-private-repos-when-asked-nicely/5267924)

---

A vulnerability in GitHub's AI agent allows private repository contents to be exposed when users issue simple natural language prompts, effectively bypassing access controls through the AI layer. The issue, dubbed 'GitLost', has no available patch or vendor documentation at time of reporting. This is particularly concerning given the widespread enterprise adoption of AI coding assistants and the sensitivity of source code repositories.


> **Security Architect's Take:** Audit which GitHub AI agent features are enabled across your organisation and consider disabling or restricting access to Copilot Workspace and similar agentic capabilities until GitHub issues a formal fix and advisory. Review whether private repositories containing sensitive IP, credentials, or configuration data are accessible to any AI agent integrations, and enforce least-privilege repository access controls in the interim.


**Original advisory:** [GitHub AI agent leaks private repos when asked nicely](https://www.theregister.com/security/2026/07/07/github-ai-agent-leaks-private-repos-when-asked-nicely/5267924)
