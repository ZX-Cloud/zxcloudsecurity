+++
title = "Passkey Attacks Bypass Phishing-Resistant MFA (2026)"
date = "2025-08-10T12:25:04Z"
publishDate = "2026-08-10T12:25:04Z"
slug = "passkey-attacks-synced-private-key-theft-mfa-bypass-2026"
description = "Three new attack techniques defeat passkey protections by stealing synced private keys or replaying signed auth material — without breaking passkey cryptog"
categories = ["general"]
tags = ["passkeys", "mfa-bypass", "phishing-resistant-mfa", "windows", "credential-theft", "authentication", "endpoint-security", "identity"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/new-passkey-attacks-can-recover-synced.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/new-passkey-attacks-can-recover-synced.html)

---

Three independent research teams have demonstrated practical attacks against passkeys that bypass their phishing-resistance without breaking the underlying cryptography. The techniques include extracting cloud-synced private keys from a compromised machine, replaying signed authentication material exposed by Windows, and abusing a legitimate passkey flow to circumvent phishing-resistant MFA. This matters because passkeys are increasingly being positioned as a gold-standard replacement for passwords, and these findings show that implementation and sync-layer weaknesses can undermine that guarantee.


> **Security Architect's Take:** Review your organisation's passkey deployment to understand whether synced (cloud-backed) or device-bound passkeys are in use — device-bound keys are significantly harder to exfiltrate. Where passkeys are used as a phishing-resistant MFA factor, ensure endpoint detection controls are in place, as several of these attacks require prior code execution on the victim's machine; a compromised endpoint negates most authentication-layer protections regardless of credential type.


**Original advisory:** [New Passkey Attacks Can Recover Synced Private Keys or Bypass Phishing-Resistant MFA](https://thehackernews.com/2026/08/new-passkey-attacks-can-recover-synced.html)
