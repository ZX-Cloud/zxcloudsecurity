+++
title = "Malicious JetBrains Plugins Steal AI API Keys"
date = "2025-06-17T13:51:58Z"
publishDate = "2026-06-17T13:51:58Z"
slug = "malicious-jetbrains-plugins-steal-ai-api-keys-supply-chain"
description = "15 malicious JetBrains Marketplace plugins disguised as AI coding assistants are stealing AI API keys. Chrome extensions also capture chatbot conversations"
categories = ["general"]
tags = ["jetbrains", "supply-chain", "api-key-theft", "malicious-plugins", "chrome-extensions", "ai-security", "developer-tools", "secrets-exfiltration"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/malicious-jetbrains-plugins-steal-ai.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/malicious-jetbrains-plugins-steal-ai.html)

---

Attackers published at least 15 malicious plugins to the JetBrains Marketplace, disguising them as AI coding assistants powered by DeepSeek and similar models. These plugins silently steal API keys for AI services such as OpenAI, Anthropic, and others from developers' machines. A related wave of malicious Chrome extensions is also capturing conversations from AI chatbot interfaces, broadening the attack surface.


> **Security Architect's Take:** Audit all JetBrains plugins installed across your engineering fleet immediately and remove any AI assistant plugins not sourced from a verified, internal allowlist. Enforce secrets scanning in CI/CD pipelines and rotate any AI provider API keys that may have been exposed on developer workstations, treating them as compromised until confirmed otherwise.


**Original advisory:** [Malicious JetBrains Plugins Steal AI API Keys as Chrome Extensions Capture Chatbot Chats](https://thehackernews.com/2026/06/malicious-jetbrains-plugins-steal-ai.html)
