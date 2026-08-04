+++
title = "Google Password Manager Passkey Attack: Unit 42"
date = "2025-08-03T16:24:47Z"
publishDate = "2026-08-03T16:24:47Z"
slug = "google-password-manager-passkey-hijack-pass-ta-key-unit42"
description = "Unit 42 reveals three attack paths letting Windows malware silently hijack passkey-protected Google accounts via Chrome's Password Manager."
categories = ["general"]
tags = ["gcp", "google-password-manager", "chrome", "passkeys", "fido2", "malware", "credential-theft", "endpoint-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/google-password-manager-attacks-could.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/google-password-manager-attacks-could.html)

---

Unit 42 researchers have identified three attack techniques — collectively dubbed 'Pass-ta-key' — that allow malware running with standard user privileges on Windows to silently authenticate to passkey-protected accounts via Google Password Manager, bypassing biometric or PIN prompts entirely. The attacks target Chrome's cloud authenticator and, in the most severe variant, compromise a master key that could expose multiple accounts. This is significant because passkeys are widely promoted as a phishing-resistant replacement for passwords, and this research demonstrates that local malware can undermine that protection without any user interaction.


> **Security Architect's Take:** Organisations relying on Google Password Manager for passkey storage should treat endpoint compromise as a full account compromise event — enforce endpoint detection and response (EDR) tooling capable of detecting credential-harvesting behaviour at the Chrome process level, and consider mandating hardware security keys (FIDO2 roaming authenticators) rather than platform authenticators for privileged or sensitive accounts.


**Original advisory:** [Google Password Manager Attacks Could Let Malware Hijack Passkey-Protected Accounts](https://thehackernews.com/2026/08/google-password-manager-attacks-could.html)
