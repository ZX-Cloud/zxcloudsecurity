+++
title = "Google DoubleClick Abused to Deliver DesckVB RAT"
date = "2026-06-03T16:29:16Z"
slug = "google-doubleclick-abused-malspam-dесkvb-rat-delivery"
description = "Attackers are exploiting Google's trusted DoubleClick domain to bypass email security filters and deliver the DesckVB remote access trojan via malspam."
categories = ["general"]
tags = ["gcp", "google-doubleclick", "malspam", "remote-access-trojan", "email-security", "defence-evasion", "phishing", "rat"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/google-doubleclick-abused-in-new.html"
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/google-doubleclick-abused-in-new.html)

---

Attackers are exploiting Google's DoubleClick ad-serving domain as a redirect layer in malicious spam emails, using its trusted reputation to bypass security filtering tools before routing victims to attacker-controlled infrastructure that delivers the DesckVB remote access trojan. Because DoubleClick is a widely trusted Google domain, many email and web security products will not flag the initial link as suspicious. This technique is a growing trend of abusing legitimate cloud services to obscure the early stages of an attack chain.


> **Architect's Take:** Review your email and web proxy security controls to ensure they inspect the full redirect chain rather than trusting links solely based on the root domain — allowlisting DoubleClick or similar Google domains without inspecting downstream redirects creates a blind spot. Consider enforcing URL rewriting and sandboxed link-following in your email security gateway, and ensure endpoint detection controls are tuned to flag RAT behaviour post-delivery.


**Original advisory:** [Google DoubleClick Abused in New Malspam Campaign to Deliver DesckVB RAT](https://thehackernews.com/2026/06/google-doubleclick-abused-in-new.html)
