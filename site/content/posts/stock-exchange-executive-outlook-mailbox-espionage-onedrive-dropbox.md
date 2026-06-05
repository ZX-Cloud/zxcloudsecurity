+++
title = "Executive Outlook Mailbox Spied on via OneDrive & Dropbox"
date = "2026-06-04T09:33:57Z"
slug = "stock-exchange-executive-outlook-mailbox-espionage-onedrive-dropbox"
description = "Attackers silently exfiltrated a stock exchange executive's Outlook email for five months, hiding data theft behind Dropbox and OneDrive traffic."
categories = ["general"]
tags = ["microsoft-365", "outlook", "onedrive", "dropbox", "email-exfiltration", "espionage", "financial-sector", "data-exfiltration"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/hackers-spied-on-stock-exchange.html"
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/hackers-spied-on-stock-exchange.html)

---

Unknown threat actors maintained covert access to a senior stock exchange executive's Outlook mailbox for at least five months, quietly exfiltrating email data in small batches to evade detection. The stolen data was routed through legitimate cloud storage services — Dropbox and OneDrive — to blend with normal business traffic. Symantec and Carbon Black attribute the campaign to espionage, suggesting a nation-state or sophisticated threat actor targeting financial sector intelligence.


> **Architect's Take:** Review Microsoft 365 audit logs and Conditional Access policies for unusual mailbox delegation, mail forwarding rules, or OAuth app consents — particularly any third-party app with access to Mail.Read scopes. Implement Cloud App Security (Defender for Cloud Apps) policies to alert on bulk email access or large data transfers to consumer cloud storage services such as Dropbox and OneDrive.


**Original advisory:** [Hackers Spied on a Stock Exchange Executive's Outlook Mailbox for Five Months](https://thehackernews.com/2026/06/hackers-spied-on-stock-exchange.html)
