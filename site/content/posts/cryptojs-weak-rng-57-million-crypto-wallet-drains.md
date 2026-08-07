+++
title = "CryptoJS Weak RNG: $5.7M Crypto Wallet Drains Explained"
date = "2026-08-06T11:49:48Z"
publishDate = "2026-08-06T11:49:48Z"
slug = "cryptojs-weak-rng-57-million-crypto-wallet-drains"
description = "A 12-year-old weak RNG in CryptoJS has led to $5.7M in crypto wallet thefts. Learn what's affected and how to remediate the risk now."
categories = ["general"]
tags = ["cryptojs", "weak-rng", "javascript", "supply-chain", "cryptography", "wallet-security", "entropy", "key-generation"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/cryptojs-weak-rng-behind-57-million-in.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/cryptojs-weak-rng-behind-57-million-in.html)

---

A weak random number generator in the widely-used CryptoJS JavaScript library has been exploited to drain at least $5.7 million from five cryptocurrency wallet applications. The vulnerable function, CryptoJS.lib.WordArray.random(), has been present in the library for 12 years and produces insufficiently random entropy when generating wallet recovery phrases. Attackers were able to predict or reconstruct private keys derived from this weak entropy, leading to two waves of theft since late May.


> **Security Architect's Take:** Audit any application — not just crypto wallets — that uses CryptoJS for key generation, token creation, or any security-sensitive randomness; replace CryptoJS.lib.WordArray.random() immediately with the Web Crypto API's crypto.getRandomValues() or a platform-native CSPRNG. Additionally, review your software supply chain policies to ensure cryptographic primitives are sourced from actively maintained, audited libraries rather than legacy dependencies.


**Original advisory:** [CryptoJS Weak RNG Behind $5.7 Million in Drains Affects Five Crypto Wallet Apps](https://thehackernews.com/2026/08/cryptojs-weak-rng-behind-57-million-in.html)
