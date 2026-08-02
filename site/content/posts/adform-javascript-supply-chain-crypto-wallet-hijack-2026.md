+++
title = "Adform Script Poisoned to Hijack Crypto Wallets"
date = "2025-08-01T09:03:07Z"
publishDate = "2026-08-01T09:03:07Z"
slug = "adform-javascript-supply-chain-crypto-wallet-hijack-2026"
description = "Attackers modified an Adform JavaScript file to swap cryptocurrency wallet addresses on visitor sites on 27 July 2026 — a supply-chain attack with broad bl"
categories = ["general"]
tags = ["supply-chain", "javascript", "cryptojacking", "adform", "browser-security", "subresource-integrity", "third-party-scripts"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/hackers-poison-adform-script-to-swap.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/hackers-poison-adform-script-to-swap.html)

---

Attackers compromised a JavaScript file distributed by advertising technology firm Adform, injecting code that silently replaced cryptocurrency wallet addresses in users' browsers on 27 July 2026. Any visitor to an affected site who copied a crypto wallet address during that window may have unknowingly sent funds to an attacker-controlled address. The incident is a classic supply-chain attack targeting third-party scripts loaded by multiple customer websites simultaneously.


> **Security Architect's Take:** Audit your estate for third-party advertising or analytics scripts and enforce Subresource Integrity (SRI) hashes so browsers reject modified files. Additionally, review your Content Security Policy to restrict which external script domains can execute on your properties.


**Original advisory:** [Hackers Poison Adform Script to Swap Crypto Wallet Addresses Across Customer Sites](https://thehackernews.com/2026/08/hackers-poison-adform-script-to-swap.html)
