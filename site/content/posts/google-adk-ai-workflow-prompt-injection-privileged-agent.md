+++
title = "Google Removes ADK AI Workflows After Prompt Injection Risk"
date = "2025-08-04T11:16:23Z"
publishDate = "2026-08-04T11:16:23Z"
slug = "google-adk-ai-workflow-prompt-injection-privileged-agent"
description = "Google deleted three ADK AI agent workflows after researchers showed a malicious GitHub issue could trigger a privileged code-fixing agent via prompt injec"
categories = ["general"]
tags = ["gcp", "agent-development-kit", "prompt-injection", "agentic-ai", "github-actions", "privilege-escalation", "supply-chain", "ai-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/google-deletes-3-adk-ai-workflows-after.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/google-deletes-3-adk-ai-workflows-after.html)

---

Google has removed three AI agent workflows from its Agent Development Kit (ADK) Python repository after researchers at Pillar Security demonstrated that a malicious GitHub issue could manipulate a public triage agent into triggering a privileged code-fixing agent. The attack exploited prompt injection, where crafted text in a public GitHub issue caused the triage agent to post a specific command comment that satisfied the privileged agent's authorisation check. This highlights the real-world risk of agentic AI pipelines inadvertently treating untrusted user input as trusted instructions.


> **Security Architect's Take:** If you are deploying agentic AI workflows — particularly those that act on GitHub events or public user input — ensure strict separation between trusted and untrusted input channels, and never use bot-generated comments as a sole authorisation mechanism. Audit any AI agent that has write or execution privileges to confirm it cannot be triggered via publicly accessible inputs.


**Original advisory:** [Google Deletes 3 ADK AI Workflows After Malicious GitHub Issue Could Trigger Privileged Agent](https://thehackernews.com/2026/08/google-deletes-3-adk-ai-workflows-after.html)
