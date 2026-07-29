+++
title = "Claude AI Breaks HAWK-256 Post-Quantum Scheme"
date = "2025-07-28T18:59:07Z"
publishDate = "2026-07-28T18:59:07Z"
slug = "claude-ai-hawk-256-post-quantum-key-recovery-attack-aes-128"
description = "Anthropic's Claude AI derived a full key-recovery attack on HAWK-256 in under 4 hours and accelerated a 7-round AES-128 attack. What cloud architects must "
categories = ["general"]
tags = ["post-quantum-cryptography", "cryptanalysis", "hawk-256", "aes", "ai-security", "lattice-cryptography", "cryptographic-agility"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/claude-ai-just-cracked-post-quantum.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/claude-ai-just-cracked-post-quantum.html)

---

Anthropic's Claude AI has independently derived a practical key-recovery attack against HAWK-256, a post-quantum digital signature scheme, exploiting an unused symmetry in its underlying lattice structure and achieving a full end-to-end attack in under four hours on commodity server hardware. It also found a 200- to 800-fold speedup for an existing attack on seven-round AES-128. This demonstrates that AI-assisted cryptanalysis is maturing rapidly, with implications for organisations relying on post-quantum cryptographic standards.


> **Security Architect's Take:** Review your cryptographic agility posture now — if you have dependencies on HAWK-256 in any signing or key-exchange workflows, treat it as compromised and plan migration to an alternative NIST-approved post-quantum scheme such as ML-DSA (CRYSTALS-Dilithium). More broadly, this is a signal to prioritise crypto-inventory tooling so you can respond quickly when future AI-assisted breaks emerge.


**Original advisory:** [Claude AI Just Cracked a Post-Quantum Test Scheme and Found a Faster 7-Round AES Attack](https://thehackernews.com/2026/07/claude-ai-just-cracked-post-quantum.html)
