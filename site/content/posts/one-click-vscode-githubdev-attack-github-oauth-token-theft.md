+++
title = "One-Click VS Code Attack Steals GitHub OAuth Tokens"
date = "2026-06-03T17:58:00Z"
slug = "one-click-vscode-githubdev-attack-github-oauth-token-theft"
description = "A one-click attack via VS Code's GitHub.dev feature can steal full GitHub OAuth tokens, exposing private repos to read/write access."
categories = ["general"]
tags = ["github", "oauth-token-theft", "vscode", "supply-chain", "credential-theft", "github.dev", "developer-tools", "token-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/one-click-github-dev-attack-lets.html"
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/one-click-github-dev-attack-lets.html)

---

A one-click attack targeting Microsoft VS Code's GitHub.dev feature allows an attacker to steal a victim's GitHub OAuth token simply by tricking them into clicking a crafted link. The stolen token grants read and write access to all repositories the victim can access, including private ones. This poses a significant supply chain risk, as compromised tokens could be used to inject malicious code into codebases.


> **Architect's Take:** Enforce short-lived, scoped OAuth tokens across your organisation and audit any GitHub Apps or integrations permitted in VS Code. Consider restricting or monitoring use of GitHub.dev in your developer environment policy, and enable GitHub token scanning and push protection to limit the blast radius of any token compromise.


**Original advisory:** [One-Click GitHub Dev Attack Lets Attackers Steal Full GitHub OAuth Tokens](https://thehackernews.com/2026/06/one-click-github-dev-attack-lets.html)
