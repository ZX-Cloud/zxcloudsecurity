+++
title = "ClickLock macOS Stealer: App-Kill Password Theft"
date = "2025-07-16T12:33:42Z"
publishDate = "2026-07-16T12:33:42Z"
slug = "clicklock-macos-infostealer-app-kill-password-theft"
description = "ClickLock is a new macOS infostealer that kills system apps every 210ms to coerce login credential entry. Here's what security teams need to know."
categories = ["general"]
tags = ["macos", "infostealer", "launchagent", "credential-theft", "social-engineering", "endpoint-security", "malware", "persistence"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-clicklock-macos-stealer-kills-apps.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-clicklock-macos-stealer-kills-apps.html)

---

ClickLock is a newly discovered macOS infostealer that coerces victims into handing over their login password by repeatedly killing core system applications every 210 milliseconds until they comply. It is delivered via a Terminal command — likely through social engineering — and persists across reboots using macOS LaunchAgents, even if the victim initially refuses the fake system password prompt. The technique is notable for its aggressive, user-harassment-based approach to credential theft rather than silent exploitation.


> **Security Architect's Take:** Enforce Endpoint Detection and Response (EDR) tooling on all macOS endpoints with rules to flag LaunchAgent creation by non-standard processes and Terminal-based execution of downloaded payloads. Review your macOS fleet's exposure to social engineering via developer portals, AI coding assistants, or third-party onboarding scripts, and consider restricting Terminal access for non-technical staff via MDM policy.


**Original advisory:** [New ClickLock macOS Stealer Kills Apps Every 210ms Until Victims Type Their Password](https://thehackernews.com/2026/07/new-clicklock-macos-stealer-kills-apps.html)
