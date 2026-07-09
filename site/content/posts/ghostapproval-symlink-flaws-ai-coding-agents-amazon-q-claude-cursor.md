+++
title = "GhostApproval: Symlink Flaws in AI Coding Agents"
date = "2025-07-09T04:27:18Z"
publishDate = "2026-07-09T04:27:18Z"
slug = "ghostapproval-symlink-flaws-ai-coding-agents-amazon-q-claude-cursor"
description = "Wiz discovers GhostApproval symlink flaws in AI coding tools including Amazon Q, Claude Code and Cursor, enabling malicious repos to hijack developer machi"
categories = ["general"]
tags = ["aws", "amazon-q-developer", "claude-code", "cursor", "ai-coding-agents", "symlink-attack", "supply-chain", "code-execution"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/ghostapproval-symlink-flaws-could-let.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/ghostapproval-symlink-flaws-could-let.html)

---

A class of symlink vulnerabilities dubbed GhostApproval, discovered by Wiz, affects six major AI coding assistants including Amazon Q Developer, Claude Code, Cursor, and others. When a malicious code repository tricks the agent into writing to a symlinked file, the actual write is redirected to a sensitive system file — despite the developer only approving what appeared to be a harmless operation. This effectively allows an untrusted repository to execute arbitrary actions on a developer's machine under the guise of legitimate AI assistance.


> **Security Architect's Take:** Audit any developer workstations or CI/CD pipelines running AI coding agents and enforce strict sandboxing (e.g. containers or VMs with minimal filesystem permissions) around agent operations; additionally, restrict or monitor symlink resolution in project directories and ensure agents are updated once vendor patches are released.


**Original advisory:** [GhostApproval Symlink Flaws Could Let Malicious Repos Run Code in AI Coding Agents](https://thehackernews.com/2026/07/ghostapproval-symlink-flaws-could-let.html)
