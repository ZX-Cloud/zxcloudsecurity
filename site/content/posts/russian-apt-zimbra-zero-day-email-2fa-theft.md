+++
title = "Russian APT Exploits Zimbra Zero-Day to Steal Email & 2FA"
date = "2026-07-23T18:36:08Z"
publishDate = "2026-07-23T18:36:08Z"
slug = "russian-apt-zimbra-zero-day-email-2fa-theft"
description = "A Russian espionage group exploited a Zimbra webmail zero-day to steal 90 days of email, contact directories, and 2FA recovery codes. NSA and CISA have iss"
categories = ["general"]
tags = ["zimbra", "zero-day", "russian-apt", "espionage", "2fa-bypass", "email-security", "cisa-advisory", "credential-theft"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/russian-espionage-group-exploited.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/russian-espionage-group-exploited.html)

---

A Russian state-sponsored espionage group exploited an undisclosed zero-day vulnerability in the Zimbra webmail client to silently harvest emails, contact directories, saved browser passwords, and two-factor authentication recovery codes from targeted Western organisations. The attack was triggered simply by opening a malicious message — no further user interaction was required. The NSA, CISA, and partner agencies have since issued a joint advisory disclosing the campaign.


> **Security Architect's Take:** Audit your organisation's use of Zimbra and apply any patches referenced in the NSA/CISA advisory immediately; if running Zimbra on-premises or via a managed service, treat it as actively compromised until patched and reviewed. Critically, review your 2FA strategy — recovery codes stored client-side or in browsers represent a systemic weakness; enforce hardware tokens or passkeys where possible and purge stored recovery codes from browser password managers.


**Original advisory:** [Russian Espionage Group Exploited Zimbra Zero-Day to Steal Mail and 2FA Codes](https://thehackernews.com/2026/07/russian-espionage-group-exploited.html)
