+++
title = "DarkSword Kit Used to Deploy GHOSTBLADE on iOS via Fake AWS "
date = "2025-08-03T10:49:06Z"
publishDate = "2026-08-03T10:49:06Z"
slug = "chinese-threat-actor-darksword-ghostblade-ios-fake-aws-pages"
description = "A Chinese threat actor is targeting iOS devices with the leaked DarkSword exploit kit and GHOSTBLADE malware, using fake AWS sign-in pages to harvest crede"
categories = ["general"]
tags = ["aws", "ios", "ghostblade", "darksword", "credential-harvesting", "phishing", "exploit-kit", "mobile-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/chinese-threat-actor-uses-leaked.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/chinese-threat-actor-uses-leaked.html)

---

A Chinese-speaking threat actor is targeting Apple iOS devices using a publicly leaked version of the DarkSword exploit kit to deploy malware known as GHOSTBLADE. The campaign involves over 100 fake AWS sign-in pages, suggesting credential harvesting alongside device exploitation. The use of a leaked kit lowers the barrier to entry for this type of attack, broadening the potential threat landscape.


> **Security Architect's Take:** Audit your organisation's AWS sign-in flows and enforce phishing-resistant MFA (e.g. FIDO2/passkeys) to mitigate credential harvesting via fake login pages. Additionally, review mobile device management (MDM) policies to ensure iOS devices accessing corporate resources are patched and have web content filtering in place to block known malicious domains.


**Original advisory:** [Chinese Threat Actor Uses Leaked DarkSword Kit to Deploy GHOSTBLADE on iOS](https://thehackernews.com/2026/08/chinese-threat-actor-uses-leaked.html)
