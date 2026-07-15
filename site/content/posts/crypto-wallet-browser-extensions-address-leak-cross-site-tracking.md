+++
title = "Crypto Wallet Extensions Leak Addresses & Track Users"
date = "2024-07-14T11:55:00Z"
publishDate = "2026-07-14T11:55:00Z"
slug = "crypto-wallet-browser-extensions-address-leak-cross-site-tracking"
description = "KU Leuven research finds 85 crypto wallet browser extensions leak blockchain addresses and enable cross-site tracking, undermining user privacy."
categories = ["general"]
tags = ["browser-extensions", "crypto-wallet", "privacy", "cross-site-tracking", "data-leakage", "web3", "user-tracking"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/study-of-85-crypto-wallet-extensions.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/study-of-85-crypto-wallet-extensions.html)

---

Researchers from KU Leuven analysed 85 popular cryptocurrency wallet browser extensions and found they leak data that can be used to link a user's separate blockchain addresses together and track them across websites. The communication patterns between wallets, websites, and blockchain nodes expose enough information for third parties to de-anonymise users — even on sites where a real name or email is already known. This undermines a core assumption of crypto wallet privacy.


> **Security Architect's Take:** Organisations permitting staff to use crypto wallet extensions on corporate or managed browsers should review acceptable use policies and consider blocking such extensions via browser management controls. Where Web3 tooling is required for business purposes, evaluate dedicated non-browser wallet solutions and ensure endpoint DLP policies account for cross-site tracking risks introduced by browser extensions.


**Original advisory:** [Study of 85 Crypto Wallet Extensions Finds Address Leaks and Cross-Site Tracking Risks](https://thehackernews.com/2026/07/study-of-85-crypto-wallet-extensions.html)
