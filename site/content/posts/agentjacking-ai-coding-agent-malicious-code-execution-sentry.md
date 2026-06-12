+++
title = "Agentjacking: AI Coding Agents Tricked Into Running Maliciou"
date = "2025-06-12T12:04:33Z"
publishDate = "2026-06-12T12:04:33Z"
slug = "agentjacking-ai-coding-agent-malicious-code-execution-sentry"
description = "Agentjacking exploits AI coding agents via fake Sentry error reports, tricking them into executing arbitrary code on developer machines."
categories = ["general"]
tags = ["ai-security", "agentic-ai", "sentry", "supply-chain", "code-execution", "developer-security", "prompt-injection", "ide-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/agentjacking-attack-tricks-ai-coding.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/agentjacking-attack-tricks-ai-coding.html)

---

A newly identified attack technique called 'Agentjacking' manipulates AI coding agents — such as those integrated into developer IDEs — into executing malicious code on developer machines. The attack is triggered by injecting a crafted fake error report via Sentry, a widely used error-tracking platform, which the AI agent then acts upon without sufficient validation. This is significant because AI coding agents operate with broad system permissions and are increasingly prevalent in software development workflows.


> **Security Architect's Take:** Enforce least-privilege execution environments for AI coding agents and treat their runtime as an untrusted surface — sandbox agent execution, audit the tools and integrations agents are permitted to invoke, and implement controls to validate the provenance of external data sources such as error-tracking platforms before agents act on them.


**Original advisory:** [Agentjacking Attack Tricks AI Coding Agents Into Running Malicious Code](https://thehackernews.com/2026/06/agentjacking-attack-tricks-ai-coding.html)
