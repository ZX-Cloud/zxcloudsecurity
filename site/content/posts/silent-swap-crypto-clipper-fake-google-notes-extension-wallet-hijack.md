+++
title = "Silent Swap Crypto Clipper: Fake Browser Extension Alert"
date = "2025-06-30T15:40:18Z"
publishDate = "2026-06-30T15:40:18Z"
slug = "silent-swap-crypto-clipper-fake-google-notes-extension-wallet-hijack"
description = "McAfee Labs flags Silent Swap, a crypto clipper using a fake Google Notes browser extension to silently redirect wallet addresses during transactions."
categories = ["general"]
tags = ["cryptocurrency", "browser-extension", "clipper-malware", "supply-chain", "endpoint-security", "malware", "clipboard-hijacking"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/silent-swap-crypto-clipper-uses-fake.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/silent-swap-crypto-clipper-uses-fake.html)

---

A malicious browser extension posing as Google Notes is actively stealing cryptocurrency by silently replacing wallet addresses during transactions — a technique known as 'clipping'. Distributed via unsigned installers in both .NET and Golang variants, the campaign (dubbed Silent Swap by McAfee Labs) targets users across multiple browsers. It is particularly dangerous because victims have no visible indication that their funds are being redirected until it is too late.


> **Security Architect's Take:** Enforce browser extension allowlisting policies across managed endpoints using tools such as Chrome Enterprise or Microsoft Intune, and block installation of unsigned or unverified extensions. Consider adding clipboard-monitoring detections to your EDR ruleset, and brief development and finance teams — who frequently handle crypto wallet addresses — on the risk of clipboard hijacking.


**Original advisory:** [Silent Swap Crypto Clipper Uses Fake Google Notes Extension to Replace Wallet Addresses](https://thehackernews.com/2026/06/silent-swap-crypto-clipper-uses-fake.html)
