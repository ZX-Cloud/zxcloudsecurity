+++
title = "282 iOS AI Apps Leak API Keys in Traffic Study"
date = "2025-06-30T13:49:34Z"
publishDate = "2026-06-30T13:49:34Z"
slug = "ios-ai-apps-leak-llm-api-keys-network-traffic"
description = "A study found 282 of 444 iPhone AI apps expose LLM API keys in network traffic, enabling attackers to make model requests at the developer's expense."
categories = ["general"]
tags = ["api-security", "llm", "mobile-security", "secrets-management", "openai", "credential-exposure", "ios"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/282-ios-apps-found-leaking-llm-api-keys.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/282-ios-apps-found-leaking-llm-api-keys.html)

---

A study of 444 iPhone AI chatbot apps found that 282 of them — roughly 63% — exposed paid AI API keys or unauthenticated backend proxies in their network traffic. Attackers intercepting this traffic could make model requests billed to the developer's account at no cost to themselves. The scale of exposure suggests a systemic failure in how mobile developers handle API credential security.


> **Security Architect's Take:** Audit any mobile or third-party applications that consume LLM APIs on your organisation's behalf — ensure API keys are never embedded in client-side code or transmitted in plaintext, and enforce per-key rate limits, IP restrictions, and usage alerts to detect abuse early.


**Original advisory:** [282 iOS AI Apps Leak API Keys and Open AI Proxy Access in Network Traffic Study](https://thehackernews.com/2026/06/282-ios-apps-found-leaking-llm-api-keys.html)
