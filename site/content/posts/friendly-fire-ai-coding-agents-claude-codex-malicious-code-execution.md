+++
title = "Friendly Fire: AI Code Agents Tricked Into Running Malicious"
date = "2025-07-09T05:15:02Z"
publishDate = "2026-07-09T05:15:02Z"
slug = "friendly-fire-ai-coding-agents-claude-codex-malicious-code-execution"
description = "The 'Friendly Fire' PoC shows Claude Code and OpenAI Codex can be manipulated into executing attacker code when scanning open-source repos in autonomous mo"
categories = ["general"]
tags = ["anthropic", "openai", "claude-code", "codex", "ai-agents", "prompt-injection", "supply-chain", "code-execution"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/friendly-fire-ai-agents-built-to-catch.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/friendly-fire-ai-agents-built-to-catch.html)

---

Researchers at the AI Now Institute have demonstrated a 'Friendly Fire' attack in which malicious code embedded in open-source repositories can trick AI coding agents — specifically Anthropic's Claude Code and OpenAI's Codex in autonomous mode — into executing that code on the analyst's own machine. The attack exploits the agents' self-approval behaviour when running without human oversight, turning a security scanning tool into an unwitting attack vector. This matters because the very tools used to find vulnerabilities can be weaponised to introduce or execute them.


> **Security Architect's Take:** Disable or strictly restrict autonomous/self-approving execution modes in AI coding agents such as Claude Code and Codex, particularly when scanning untrusted or third-party open-source repositories; enforce sandboxed, network-isolated environments (e.g. ephemeral containers with no write access to host systems) for any AI-driven code analysis workloads.


**Original advisory:** [Top AI Agents Built to Catch Malicious Code Can Be Tricked Into Running It](https://thehackernews.com/2026/07/friendly-fire-ai-agents-built-to-catch.html)
