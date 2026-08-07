+++
title = "AI Prompt Injection via 'Ask AI' Buttons Poisons LLM Memory"
date = "2025-08-06T11:30:00Z"
publishDate = "2026-08-06T11:30:00Z"
slug = "ai-recommendation-poisoning-prompt-injection-ask-ai-buttons-llm-memory"
description = "Hidden prompt injections in 'Ask AI' deep links silently manipulate LLM memory and recommendations — no malware or exploits required. Here's what architect"
categories = ["general"]
tags = ["prompt-injection", "llm-security", "ai-assistant", "deep-link-abuse", "memory-poisoning", "supply-chain", "chatgpt", "copilot"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/ai-recommendation-poisoning-how-ask-ai.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/ai-recommendation-poisoning-how-ask-ai.html)

---

A newly documented prompt injection technique embeds hidden instructions inside 'Ask AI' deep-link buttons on commercial websites, causing AI assistants to silently absorb attacker-controlled content into their memory or context. The attack requires no malware, exploits, or compromised credentials — only a user clicking a standard-looking button. This is particularly concerning because it can manipulate AI-driven recommendations and persist across user sessions if memory features are enabled.


> **Security Architect's Take:** Audit any enterprise AI assistant deployments (e.g. ChatGPT, Copilot, Gemini) to understand whether persistent memory or deep-link pre-filling is enabled for users; consider disabling or restricting memory features and enforcing content security policies that block untrusted deep-link invocations in your organisation's browser fleet.


**Original advisory:** [AI Recommendation Poisoning: How "Ask AI" Buttons Silently Alter LLM Memory](https://thehackernews.com/2026/08/ai-recommendation-poisoning-how-ask-ai.html)
