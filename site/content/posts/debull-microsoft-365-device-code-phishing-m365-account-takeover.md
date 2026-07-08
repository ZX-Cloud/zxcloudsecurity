+++
title = "DEBULL: Microsoft 365 Device Code Phishing Attack"
date = "2025-07-07T15:14:14Z"
publishDate = "2026-07-07T15:14:14Z"
slug = "debull-microsoft-365-device-code-phishing-m365-account-takeover"
description = "The DEBULL campaign abuses Microsoft's device code authentication flow to hijack M365 accounts without fake login pages, bypassing MFA."
categories = ["general"]
tags = ["azure", "microsoft-365", "entra-id", "device-code-flow", "phishing", "account-takeover", "oauth", "mfa-bypass"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/debull-tooling-abuses-microsoft-device.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/debull-tooling-abuses-microsoft-device.html)

---

A phishing campaign dubbed DEBULL is exploiting Microsoft's legitimate device code authentication flow to hijack Microsoft 365 accounts, without requiring a fake login page. Attackers use collaboration-themed lures to trick users into entering a device code on Microsoft's own login portal, granting the attacker a valid access token. This technique is particularly dangerous because it bypasses traditional phishing indicators and can circumvent MFA.


> **Security Architect's Take:** Review and restrict device code flow (OAuth 2.0 device authorisation grant) in your Microsoft Entra ID Conditional Access policies — block or limit it to trusted, managed devices where possible. Additionally, enable sign-in risk policies and monitor for device code authentication events in your Entra ID sign-in logs, particularly from unfamiliar locations or user agents.


**Original advisory:** [DEBULL Tooling Abuses Microsoft Device-Code Flow to Target M365 Accounts](https://thehackernews.com/2026/07/debull-tooling-abuses-microsoft-device.html)
