+++
title = "Google Gemini Android Prompt Injection via Notifications"
date = "2026-06-03T19:11:15Z"
slug = "google-gemini-android-prompt-injection-whatsapp-slack-notifications"
description = "A prompt injection flaw let hostile WhatsApp, Slack, and Signal notifications hijack Google Gemini on Android — no malicious app required."
categories = ["general"]
tags = ["gcp", "google-gemini", "android", "prompt-injection", "ai-security", "whatsapp", "slack", "mobile-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/whatsapp-slack-notifications-could.html"
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/whatsapp-slack-notifications-could.html)

---

A prompt injection vulnerability in Google Gemini on Android allowed hostile content embedded in notifications from apps such as WhatsApp, Slack, Signal, and SMS to hijack the AI assistant without requiring any malicious app to be installed. An attacker could craft a poisoned message or notification that caused Gemini to perform unauthorised actions — including impersonating contacts, initiating calls, or corrupting its long-term memory. The attack required no user interaction beyond the assistant processing the notification, making it particularly dangerous for enterprise users relying on AI-assisted workflows.


> **Architect's Take:** Review your organisation's mobile device management (MDM) policies to restrict or audit Gemini's access to third-party app notifications, particularly on corporate Android devices. Until Google confirms a fully patched release, consider disabling Gemini's notification-reading capabilities via app permissions and assess whether AI assistant integrations meet your acceptable risk threshold for enterprise use.


**Original advisory:** [WhatsApp, Slack Notifications Could Hijack Google Gemini on Android](https://thehackernews.com/2026/06/whatsapp-slack-notifications-could.html)
