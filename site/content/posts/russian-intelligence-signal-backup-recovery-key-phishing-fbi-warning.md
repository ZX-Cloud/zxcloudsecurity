+++
title = "FBI: Russian Hackers Steal Signal Backup Recovery Keys"
date = "2025-06-26T19:38:29Z"
publishDate = "2026-06-26T19:38:29Z"
slug = "russian-intelligence-signal-backup-recovery-key-phishing-fbi-warning"
description = "Russian intelligence actors are phishing Signal Backup Recovery Keys, granting persistent access to full message history. FBI and CISA issue updated adviso"
categories = ["general"]
tags = ["signal", "phishing", "russian-apt", "social-engineering", "credential-theft", "account-takeover", "end-to-end-encryption"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/fbi-warns-russian-intelligence-hackers.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/fbi-warns-russian-intelligence-hackers.html)

---

Russian intelligence operatives have evolved their Signal phishing campaign to specifically target users' Backup Recovery Keys — a static credential that grants full access to message history and account control. Unlike a password reset, the key remains valid indefinitely once compromised, giving attackers persistent, silent access. The FBI and CISA have updated their advisory to reflect this escalated tactic.


> **Security Architect's Take:** Advise staff and privileged users to treat Signal Backup Recovery Keys with the same sensitivity as MFA seed phrases — never share them and store them offline in a secrets manager or physical safe. Consider issuing guidance that no legitimate service or authority will ever request this key, and review whether Signal is approved for handling sensitive organisational communications given this persistent credential risk.


**Original advisory:** [FBI Warns Russian Intelligence Hackers Target Signal Backup Recovery Keys](https://thehackernews.com/2026/06/fbi-warns-russian-intelligence-hackers.html)
