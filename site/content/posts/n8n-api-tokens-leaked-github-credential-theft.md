+++
title = "Leaked n8n API Tokens Expose Live Instances on GitHub"
date = "2025-08-05T10:35:29Z"
publishDate = "2026-08-05T10:35:29Z"
slug = "n8n-api-tokens-leaked-github-credential-theft"
description = "GitGuardian found 4,576 n8n API tokens in public GitHub commits. 321 live instances were exploitable for credential theft without any software vulnerabilit"
categories = ["general"]
tags = ["n8n", "secrets-management", "credential-exposure", "github", "workflow-automation", "supply-chain", "api-security", "secrets-scanning"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/leaked-n8n-api-tokens-exposed-live.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/leaked-n8n-api-tokens-exposed-live.html)

---

GitGuardian researchers discovered 4,576 n8n API tokens exposed in public GitHub commits, with 321 live instances confirmed vulnerable to exploitation. Attackers could use these tokens to access workflow data, exfiltrate downstream credentials stored within n8n, and pivot to connected third-party services — all without exploiting any software vulnerability. The risk stems entirely from poor secrets hygiene rather than a flaw in n8n itself.


> **Security Architect's Take:** Audit your organisation's GitHub repositories immediately for exposed n8n API tokens using a secrets scanning tool such as GitGuardian or Trufflehog, and enforce pre-commit hooks or CI/CD pipeline checks to prevent future leakage. Rotate any exposed tokens, restrict n8n API access to known IP ranges, and review stored credentials within n8n workflows for blast radius assessment.


**Original advisory:** [Leaked n8n API Tokens Exposed Live Instances to Credential Theft](https://thehackernews.com/2026/08/leaked-n8n-api-tokens-exposed-live.html)
