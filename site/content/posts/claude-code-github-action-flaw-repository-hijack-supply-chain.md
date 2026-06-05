+++
title = "Claude Code GitHub Action Flaw Enabled Repo Hijack"
date = "2026-06-04T15:15:26Z"
slug = "claude-code-github-action-flaw-repository-hijack-supply-chain"
description = "A flaw in Anthropic's Claude Code GitHub Action let attackers hijack public repos via a single issue, risking supply chain compromise across downstream pro"
categories = ["general"]
tags = ["github-actions", "anthropic", "supply-chain", "ci-cd", "code-execution", "privilege-escalation", "workflow-security"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html"
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html)

---

A flaw in Anthropic's Claude Code GitHub Action allowed an attacker to hijack public repositories simply by opening a malicious GitHub issue, requiring no authentication or special access. Because Anthropic's own repository used the same vulnerable workflow, a successful attack could have injected malicious code into the action itself, poisoning every downstream project that consumes it. Researcher RyotaK of GMO discovered and reported the issue.


> **Architect's Take:** Audit any GitHub Actions workflows that trigger on untrusted events such as 'issues' or 'pull_request_target' and ensure they do not have write permissions or access to secrets without explicit trust gates. If you use Claude Code GitHub Action, verify you are pinned to a patched version and review your workflow permissions using the principle of least privilege.


**Original advisory:** [Claude Code GitHub Action Flaw Let One Malicious Issue Hijack Repositories](https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html)
