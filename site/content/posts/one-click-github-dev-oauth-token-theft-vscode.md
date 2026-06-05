+++
title = "One-Click GitHub OAuth Token Theft via VS Code"
date = "2026-06-03T17:58:00Z"
slug = "one-click-github-dev-oauth-token-theft-vscode"
description = "A one-click attack exploiting GitHub.dev and VS Code lets attackers steal GitHub OAuth tokens, exposing private repositories to full read/write access."
categories = ["general"]
tags = ["github", "oauth", "token-theft", "vscode", "supply-chain", "repository-security", "developer-tools"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/one-click-github-dev-attack-lets.html"
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/one-click-github-dev-attack-lets.html)

---

A one-click attack targeting GitHub.dev, the browser-based VS Code environment, allows an attacker to steal a victim's GitHub OAuth token simply by having them click a crafted link. The stolen token grants full read and write access to both public and private repositories. This is particularly dangerous because it requires no malware installation and exploits a legitimate GitHub feature.


> **Architect's Take:** Audit OAuth token scopes granted to GitHub.dev within your organisation and consider enforcing fine-grained personal access tokens with minimal repository permissions instead of broad OAuth tokens. Ensure developer awareness training covers the risk of clicking unsolicited GitHub.dev links, and review whether your GitHub organisation policies can restrict OAuth app access.


**Original advisory:** [One-Click GitHub Dev Attack Lets Attackers Steal Full GitHub OAuth Tokens](https://thehackernews.com/2026/06/one-click-github-dev-attack-lets.html)
