+++
title = "Stock Exchange Exec Outlook Hacked via OneDrive Exfil"
date = "2026-06-04T09:33:57Z"
slug = "stock-exchange-executive-outlook-mailbox-espionage-onedrive-dropbox-exfiltration"
description = "Attackers spent five months silently exfiltrating a stock exchange executive's Outlook mailbox via OneDrive and Dropbox. Here's what cloud architects need "
categories = ["general"]
tags = ["microsoft-365", "outlook", "onedrive", "dropbox", "email-exfiltration", "espionage", "data-exfiltration", "cloud-misuse"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/hackers-spied-on-stock-exchange.html"
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/hackers-spied-on-stock-exchange.html)

---

Unknown threat actors maintained covert access to a senior stock exchange executive's Microsoft Outlook mailbox for at least five months, systematically exfiltrating email data in small batches to avoid detection. The stolen data was routed through Dropbox and OneDrive to blend with legitimate cloud traffic, making it harder for security tools to flag the activity. The campaign bears the hallmarks of a state-sponsored or sophisticated espionage operation targeting high-value financial intelligence.


> **Architect's Take:** Review Microsoft 365 audit logs and Defender for Cloud Apps policies for anomalous mail export activity, particularly incremental inbox syncs or delegated access from unfamiliar locations — and enforce conditional access policies that restrict OAuth app permissions for third-party cloud storage providers such as Dropbox and OneDrive to prevent data staging and exfiltration via trusted cloud channels.


**Original advisory:** [Hackers Spied on a Stock Exchange Executive's Outlook Mailbox for Five Months](https://thehackernews.com/2026/06/hackers-spied-on-stock-exchange.html)
