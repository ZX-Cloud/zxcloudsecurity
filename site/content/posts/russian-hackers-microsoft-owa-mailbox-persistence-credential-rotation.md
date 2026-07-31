+++
title = "Russian Hackers Exploit Microsoft OWA Flaw for Mailbox Persi"
date = "2025-07-30T07:40:48Z"
publishDate = "2026-07-30T07:40:48Z"
slug = "russian-hackers-microsoft-owa-mailbox-persistence-credential-rotation"
description = "Russian threat actors are exploiting a Microsoft OWA vulnerability to retain mailbox access after credential rotation, targeting government and critical se"
categories = ["general"]
tags = ["azure", "microsoft-365", "exchange-online", "owa", "credential-theft", "persistence", "apt", "email-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/russian-hackers-exploit-microsoft-owa.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/russian-hackers-exploit-microsoft-owa.html)

---

Russian threat actors are exploiting a vulnerability in Microsoft Outlook Web Access (OWA) to maintain persistent access to mailboxes even after victims rotate their credentials — a technique that effectively defeats a common incident response measure. The campaign, active since 22 July 2026, targets US and European government bodies alongside telecoms, finance, hospitality, and aerospace organisations. This follows the same group's recent exploitation of a similar flaw in Zimbra, indicating a deliberate focus on webmail persistence techniques.


> **Security Architect's Take:** Audit all Exchange Online and OWA-connected application tokens, OAuth grants, and delegated permissions immediately, as credential rotation alone will not evict an attacker exploiting this class of vulnerability. Ensure conditional access policies enforce device compliance and revoke all active sessions as part of any incident response runbook, and prioritise applying the relevant Microsoft patch across hybrid Exchange environments.


**Original advisory:** [Russian Hackers Exploit Microsoft OWA Flaw to Keep Mailbox Access After Credential Rotation](https://thehackernews.com/2026/07/russian-hackers-exploit-microsoft-owa.html)
