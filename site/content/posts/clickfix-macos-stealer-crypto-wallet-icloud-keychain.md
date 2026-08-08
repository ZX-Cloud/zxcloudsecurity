+++
title = "ClickFix macOS Stealer Drains Crypto Wallets"
date = "2025-08-07T18:29:08Z"
publishDate = "2026-08-07T18:29:08Z"
slug = "clickfix-macos-stealer-crypto-wallet-icloud-keychain"
description = "ClickFix attacks now deliver a Go-based macOS stealer targeting crypto wallets, iCloud Keychain, and browser credentials. Here's what security teams need t"
categories = ["general"]
tags = ["macos", "stealer-malware", "clickfix", "cryptocurrency", "credential-theft", "social-engineering", "icloud-keychain", "go-malware"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/clickfix-attacks-deliver-macos-stealer.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/clickfix-attacks-deliver-macos-stealer.html)

---

A ClickFix-style social engineering attack is being used to deploy a Go-based macOS stealer capable of draining cryptocurrency wallets, harvesting browser-saved passwords, Apple iCloud Keychain credentials, and cached application credentials. The infection chain uses a shell script to fingerprint the victim's hardware before delivering an architecture-compatible payload. This matters because ClickFix techniques require minimal user sophistication to exploit and increasingly target macOS users who may assume lower risk exposure.


> **Security Architect's Take:** Ensure endpoint detection and response (EDR) tooling covers macOS devices in your fleet, particularly for developers and finance staff with crypto or cloud credential access. Review whether privileged macOS endpoints enforce application allowlisting and restrict shell script execution from untrusted sources.


**Original advisory:** [ClickFix Attacks Deliver macOS Stealer That Can Drain Crypto Wallets](https://thehackernews.com/2026/08/clickfix-attacks-deliver-macos-stealer.html)
