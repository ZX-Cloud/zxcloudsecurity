+++
title = "Claude Code & Gemini CLI CI Secret Exposure Flaws"
date = "2025-08-07T08:18:35Z"
publishDate = "2026-08-07T08:18:35Z"
slug = "claude-code-gemini-cli-ci-secret-exposure-prompt-injection"
description = "Novee Security showed a GitHub issue alone can execute code on CI runners and expose secrets in Claude Code, Gemini CLI, and OpenAI's agent. Here's what ar"
categories = ["general"]
tags = ["gcp", "claude-code", "gemini-cli", "openai", "prompt-injection", "ci-cd", "supply-chain", "secrets-exposure"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/claude-code-and-gemini-cli-flaws-let.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/claude-code-and-gemini-cli-flaws-let.html)

---

Security researchers at Novee Security demonstrated that simply opening a GitHub issue — without any repository access — was enough to trigger code execution on CI runners used by Anthropic's Claude Code and Google's Gemini CLI projects, exposing secrets held in those pipelines. OpenAI's coding agent was similarly vulnerable, with the same technique able to hijack subsequent agent runs. The attacks exploited prompt injection flaws in AI coding agents operating in default, vendor-shipped configurations, meaning the risk applies broadly to any team adopting these tools as-shipped.


> **Security Architect's Take:** Audit any CI/CD pipelines that use AI coding agents — particularly Claude Code, Gemini CLI, or OpenAI's agent — and ensure they run in isolated environments with least-privilege credentials and no access to secrets beyond what is strictly necessary. Treat untrusted input channels (issues, PRs, comments) as a prompt injection attack surface and restrict agent permissions accordingly until vendors ship hardened defaults.


**Original advisory:** [Claude Code and Gemini CLI Flaws Let a GitHub Issue Reach CI Workflow Secrets](https://thehackernews.com/2026/08/claude-code-and-gemini-cli-flaws-let.html)
