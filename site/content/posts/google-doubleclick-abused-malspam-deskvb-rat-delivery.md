+++
title = "Google DoubleClick Abused to Deliver DesckVB RAT"
date = "2026-06-03T16:29:16Z"
slug = "google-doubleclick-abused-malspam-deskvb-rat-delivery"
description = "A new malspam campaign exploits Google's trusted DoubleClick domain to bypass security tools and deliver the DesckVB remote access trojan to victims."
categories = ["general"]
tags = ["gcp", "doubleclick", "malspam", "remote-access-trojan", "email-security", "defence-evasion", "phishing"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/google-doubleclick-abused-in-new.html"
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/google-doubleclick-abused-in-new.html)

---

Attackers are exploiting Google's DoubleClick ad-serving domain as a redirect hop in malicious email campaigns, using its trusted reputation to bypass security filters before delivering the DesckVB remote access trojan. Because many email and web security tools whitelist or deprioritise scrutiny of well-known Google-owned domains, the technique significantly increases the likelihood of successful delivery. Once installed, a RAT gives attackers persistent remote control over the victim's machine.


> **Architect's Take:** Review your email and web proxy security policies to ensure that redirects through trusted domains — including Google-owned properties like DoubleClick — are still subject to full URL chain inspection and sandbox detonation. Consider enforcing policies that follow and evaluate the final destination URL rather than trusting the initial domain at face value.


**Original advisory:** [Google DoubleClick Abused in New Malspam Campaign to Deliver DesckVB RAT](https://thehackernews.com/2026/06/google-doubleclick-abused-in-new.html)
