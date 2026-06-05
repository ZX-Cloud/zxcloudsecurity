+++
title = "Google Gemini Android Hijack via Notification Prompt Injecti"
date = "2026-06-03T19:11:15Z"
slug = "google-gemini-android-prompt-injection-notification-hijack"
description = "A prompt injection flaw let malicious WhatsApp, Slack, or SMS notifications hijack Google Gemini on Android — no malware required. Here's what architects n"
categories = ["general"]
tags = ["gcp", "google-gemini", "android", "prompt-injection", "ai-security", "mobile-security", "whatsapp", "slack"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/whatsapp-slack-notifications-could.html"
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/whatsapp-slack-notifications-could.html)

---

A vulnerability in Google Gemini's Android integration allowed malicious content embedded in notifications from apps such as WhatsApp, Slack, Signal, and SMS to hijack the AI assistant without requiring any installed malware. An attacker could craft a poisoned notification that caused Gemini to open browser windows, impersonate contacts, initiate calls, or corrupt the assistant's long-term memory. This is a prompt injection attack exploiting the trust Gemini places in notification content it processes.


> **Architect's Take:** Organisations deploying Android devices with Gemini enabled should review mobile device management (MDM) policies to restrict AI assistant access to sensitive notification streams, and treat AI assistants as untrusted data processors when designing data-handling workflows. Raise awareness with security teams about prompt injection as a realistic attack vector on enterprise mobile estates.


**Original advisory:** [WhatsApp, Slack Notifications Could Hijack Google Gemini on Android](https://thehackernews.com/2026/06/whatsapp-slack-notifications-could.html)
