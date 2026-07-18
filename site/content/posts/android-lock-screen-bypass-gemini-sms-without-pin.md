+++
title = "Android Lock Screen Bug Lets Gemini Send SMS Without PIN"
date = "2025-07-17T09:15:00Z"
publishDate = "2026-07-17T09:15:00Z"
slug = "android-lock-screen-bypass-gemini-sms-without-pin"
description = "A multi-touch gesture bypasses Android lock screen auth, letting Gemini send SMS without a PIN. Google is working on a fix. Here's what you need to know."
categories = ["general"]
tags = ["android", "gcp", "google", "gemini", "lock-screen-bypass", "authentication", "mobile-security", "physical-access"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/17/google-fixing-android-lock-screen-bug-that-lets-gemini-send-sms-without-a-pin/5273027"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/17/google-fixing-android-lock-screen-bug-that-lets-gemini-send-sms-without-a-pin/5273027)

---

A bug in Android allows a specific multi-touch gesture to bypass the lock screen authentication prompt, enabling Google's Gemini AI assistant to send SMS messages without requiring a PIN or biometric verification. The flaw means a physical attacker with access to a locked device could send arbitrary text messages, potentially impersonating the device owner. Google is actively working on a fix.


> **Security Architect's Take:** Ensure Android devices in your organisation's mobile fleet are updated promptly once Google releases the patch; in the interim, consider enforcing MDM policies that restrict AI assistant access from the lock screen, and review BYOD policies to assess exposure risk.


**Original advisory:** [Google fixing Android lock screen bug that lets Gemini send SMS without a PIN](https://www.theregister.com/security/2026/07/17/google-fixing-android-lock-screen-bug-that-lets-gemini-send-sms-without-a-pin/5273027)
