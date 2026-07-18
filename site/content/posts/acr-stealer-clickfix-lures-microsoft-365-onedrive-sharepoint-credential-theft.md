+++
title = "ACR Stealer ClickFix Attack Targets M365 & OneDrive"
date = "2025-07-17T08:56:39Z"
publishDate = "2026-07-17T08:56:39Z"
slug = "acr-stealer-clickfix-lures-microsoft-365-onedrive-sharepoint-credential-theft"
description = "ACR Stealer uses ClickFix lures to steal browser credentials, session tokens, and Microsoft 365 files from OneDrive and SharePoint. Here's what to do."
categories = ["general"]
tags = ["azure", "microsoft-365", "onedrive", "sharepoint", "infostealer", "clickfix", "session-hijacking", "social-engineering"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/acr-stealer-uses-clickfix-lures-to.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/acr-stealer-uses-clickfix-lures-to.html)

---

ACR Stealer is an infostealer that tricks users into running malicious commands via ClickFix social engineering lures, harvesting saved browser credentials, live session tokens, and Microsoft 365 documents including files synced via OneDrive and SharePoint. Once a user pastes and executes the delivered command, the malware silently exfiltrates sensitive data without requiring any elevated privileges. This is particularly dangerous in enterprise environments where browser-stored credentials and active sessions provide direct access to cloud resources.


> **Security Architect's Take:** Enforce application control policies (e.g. via Microsoft Defender Application Control or AppLocker) to block arbitrary command execution from the Run dialogue, and deploy Conditional Access policies with token binding and continuous access evaluation in Entra ID to limit the utility of stolen session tokens.


**Original advisory:** [ACR Stealer Uses ClickFix Lures to Steal Browser Tokens and Microsoft 365 Files](https://thehackernews.com/2026/07/acr-stealer-uses-clickfix-lures-to.html)
