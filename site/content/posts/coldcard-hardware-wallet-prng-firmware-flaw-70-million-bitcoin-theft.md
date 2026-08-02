+++
title = "Coldcard Wallet PRNG Flaw Behind $70M Bitcoin Theft"
date = "2026-08-01T17:17:22Z"
publishDate = "2026-08-01T17:17:22Z"
slug = "coldcard-hardware-wallet-prng-firmware-flaw-70-million-bitcoin-theft"
description = "A 2021 Coldcard firmware bug routed seed generation to a software PRNG, enabling an attacker to steal 1,082 BTC worth $70M in 41 minutes."
categories = ["general"]
tags = ["hardware-wallet", "coldcard", "prng", "cryptographic-key-generation", "firmware-vulnerability", "supply-chain", "cryptocurrency", "entropy"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/coldcard-hardware-wallet-flaw-linked-to.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/coldcard-hardware-wallet-flaw-linked-to.html)

---

A firmware bug introduced into Coldcard hardware wallets in March 2021 routed Bitcoin seed generation through a deterministic software PRNG rather than a true hardware random number generator, making private keys predictable. An attacker exploited this to sweep 1,196 Bitcoin addresses in just 41 minutes on 30 July, stealing approximately $70.2 million worth of BTC. The incident highlights the critical dependency on entropy quality in cryptographic key generation, even within dedicated hardware security devices.


> **Security Architect's Take:** If your organisation holds cryptocurrency assets or integrates hardware security modules for key generation, audit firmware changelogs for any modifications to entropy sources and validate that RNG pathways route through certified hardware components — never software PRNGs. Treat firmware supply chain integrity with the same rigour as software dependencies, enforcing reproducible builds and cryptographic signing verification before any deployment.


**Original advisory:** [Coldcard Hardware Wallet Flaw Linked to $70 Million Bitcoin Theft in 41 Minutes](https://thehackernews.com/2026/08/coldcard-hardware-wallet-flaw-linked-to.html)
