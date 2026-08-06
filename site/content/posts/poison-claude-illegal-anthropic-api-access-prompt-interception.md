+++
title = "Poison Claude: Stolen Anthropic API Access Logs Your Prompts"
date = "2025-08-05T15:36:03Z"
publishDate = "2026-08-05T15:36:03Z"
slug = "poison-claude-illegal-anthropic-api-access-prompt-interception"
description = "Underground service Poison Claude sells cut-price access to Anthropic's LLMs while its operators secretly log every customer prompt. Here's what architects"
categories = ["general"]
tags = ["anthropic", "claude", "llm-security", "api-credential-abuse", "data-exfiltration", "ai-security", "underground-marketplace", "prompt-privacy"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/poison-claude-sells-discounted-claude.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/poison-claude-sells-discounted-claude.html)

---

Researchers have uncovered underground services selling unauthorised access to Anthropic's Claude AI models at discounted rates, with at least one operator — 'Poison Claude' — intercepting and logging every prompt submitted by customers. These services likely operate by abusing stolen or resold API credentials, meaning users unknowingly hand their queries to a malicious third party. The risk extends beyond credential theft to sensitive data exfiltration, as any prompt containing business or personal information is visible to the threat actor.


> **Security Architect's Take:** Audit your organisation's AI API key usage and enforce strict controls on who can provision or share Anthropic API credentials; consider implementing data-loss prevention policies to flag employees using unofficial or third-party Claude access services, and remind teams that any prompt submitted via an unverified service may be logged by a hostile operator.


**Original advisory:** [Poison Claude Sells Discounted Claude Access While Its Operator Sees Every Customer Prompt](https://thehackernews.com/2026/08/poison-claude-sells-discounted-claude.html)
