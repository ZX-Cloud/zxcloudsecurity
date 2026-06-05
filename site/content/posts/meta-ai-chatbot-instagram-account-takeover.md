+++
title = "Meta AI Chatbot Exploited to Hijack Instagram Accounts"
date = "2026-06-04T11:04:09Z"
slug = "meta-ai-chatbot-instagram-account-takeover"
description = "Hackers are abusing Meta's AI support chatbot to take over Instagram accounts via social engineering. Learn what this means for AI trust boundaries."
categories = ["general"]
tags = ["meta", "instagram", "ai-security", "account-takeover", "social-engineering", "identity", "chatbot", "authentication"]
severity = "High"
source = "Schneier on Security"
source_url = "https://www.schneier.com/blog/archives/2026/06/hacking-metas-ai-chatbot.html"
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [Schneier on Security](https://www.schneier.com/blog/archives/2026/06/hacking-metas-ai-chatbot.html)

---

Attackers are exploiting Meta's AI support chatbot to hijack Instagram accounts by social-engineering the bot into adding a hacker-controlled email address and triggering a password reset. The attack requires no technical vulnerability in the traditional sense — the AI simply complies with the request after a verification code exchange. This highlights a significant trust and authorisation flaw in how Meta's AI assistant handles account management actions on behalf of unauthenticated parties.


> **Architect's Take:** Treat AI-powered support agents as a privileged access vector and apply the same controls you would to any account recovery flow — ensure they cannot perform account modifications without verified, out-of-band identity confirmation tied to the existing account owner, not the requester.


**Original advisory:** [Hacking Meta’s AI Chatbot](https://www.schneier.com/blog/archives/2026/06/hacking-metas-ai-chatbot.html)
