+++
title = "Microsoft 365 Android Debug Flag Exposes Account Tokens"
date = "2026-06-03T14:56:35Z"
slug = "microsoft-365-android-debug-flag-account-token-theft"
description = "A leftover debug flag in Microsoft 365 Android apps let any installed app steal account tokens silently, exposing email, files and calendar data."
categories = ["general"]
tags = ["azure", "microsoft-365", "android", "token-theft", "authentication", "mobile-security", "conditional-access", "msal"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/microsoft-365-android-apps-let-any-app.html"
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/microsoft-365-android-apps-let-any-app.html)

---

A debug flag accidentally left enabled in production builds of multiple Microsoft 365 Android apps disabled a security check that restricts account token sharing to trusted Microsoft applications. As a result, any app installed on the same Android device could silently request and receive the signed-in user's authentication token, granting full access to email, files, calendar, and the ability to send messages on their behalf. No user interaction, credentials, or elevated permissions were required to exploit this.


> **Architect's Take:** Audit your mobile application management (MAM) and Conditional Access policies to ensure app-based controls are enforced at the resource level and are not solely reliant on client-side token handling. Until Microsoft confirms a fully patched build is deployed, consider enforcing Continuous Access Evaluation (CAE) and restricting M365 access on Android to Intune-managed devices with compliant app versions.


**Original advisory:** [Microsoft 365 Android Apps Let Any App Steal Account Tokens via Leftover Debug Flag](https://thehackernews.com/2026/06/microsoft-365-android-apps-let-any-app.html)
