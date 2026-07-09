+++
title = "GitHub Verified Commits Can Be Spoofed Without Signing Key"
date = "2025-07-08T11:51:24Z"
publishDate = "2026-07-08T11:51:24Z"
slug = "github-verified-commits-signature-spoofing-supply-chain"
description = "New research shows GitHub's Verified badge can be replicated without the signing key, undermining commit integrity checks in software supply chains."
categories = ["general"]
tags = ["github", "git", "commit-signing", "supply-chain", "code-integrity", "ci-cd", "software-provenance"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/github-verified-commits-can-be.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/github-verified-commits-can-be.html)

---

Researchers have found that GitHub's 'Verified' badge on signed commits can be spoofed without access to the original signing key. An attacker can create a duplicate commit containing identical files, author details, and timestamp, complete with a valid signature, whilst producing a different commit hash. This undermines a core assumption in software supply chain security: that a verified commit is uniquely trustworthy.


> **Security Architect's Take:** Do not rely solely on GitHub's 'Verified' badge as a supply chain integrity control. Supplement commit signing policies with hash-pinning in CI/CD pipelines, enforce SLSA provenance attestations, and cross-reference commit hashes in your build manifests against expected values rather than trusting the UI indicator alone.


**Original advisory:** [GitHub 'Verified' Commits Can Be Rewritten Into New Hashes Without Breaking Signatures](https://thehackernews.com/2026/07/github-verified-commits-can-be.html)
