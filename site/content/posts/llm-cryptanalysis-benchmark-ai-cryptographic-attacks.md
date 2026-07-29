+++
title = "LLMs Break Crypto: CryptanalysisBench Results"
date = "2024-07-29T01:47:05Z"
publishDate = "2026-07-29T01:47:05Z"
slug = "llm-cryptanalysis-benchmark-ai-cryptographic-attacks"
description = "New benchmark CryptanalysisBench shows frontier LLMs, including Claude, can discover novel cryptographic attacks. What this means for cloud security."
categories = ["general"]
tags = ["cryptanalysis", "llm", "ai-security", "cryptography", "anthropic", "nist", "emerging-threats", "encryption"]
severity = "Medium"
source = "Schneier on Security"
source_url = "https://www.schneier.com/blog/archives/2026/07/measuring-llms-ability-to-perform-cryptanalysis.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [Schneier on Security](https://www.schneier.com/blog/archives/2026/07/measuring-llms-ability-to-perform-cryptanalysis.html)

---

A new benchmark called CryptanalysisBench tests whether large language models can discover cryptographic attacks across 191 tasks covering block ciphers, hash functions, and other primitives. Notably, Anthropic's Claude Opus model independently found previously unknown attacks, suggesting frontier AI is beginning to perform genuine cryptanalytic research. This has significant implications for the long-term security of cryptographic primitives underpinning digital infrastructure.


> **Security Architect's Take:** Monitor developments in AI-assisted cryptanalysis closely, particularly against legacy or non-standard cryptographic algorithms in your cloud workloads — begin auditing your use of weaker or deprecated primitives and prioritise migration to NIST-approved post-quantum and modern standards before AI tooling makes attacks more accessible.


**Original advisory:** [Measuring LLMs’ Ability to Perform Cryptanalysis](https://www.schneier.com/blog/archives/2026/07/measuring-llms-ability-to-perform-cryptanalysis.html)
