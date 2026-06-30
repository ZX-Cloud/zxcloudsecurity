+++
title = "Microsoft StegoAd: 119 Malicious Edge Extensions Removed"
date = "2025-06-29T08:32:31Z"
publishDate = "2026-06-29T08:32:31Z"
slug = "microsoft-stegoad-119-malicious-edge-extensions-steganography-credential-theft"
description = "Microsoft removed 119 Edge extensions hiding malware in images and fonts. The StegoAd campaign stole credentials and ran ad fraud from 2021 onwards."
categories = ["general"]
tags = ["azure", "microsoft-edge", "browser-extensions", "steganography", "credential-theft", "ad-fraud", "supply-chain", "malware"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/microsoft-removes-119-edge-extensions.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/microsoft-removes-119-edge-extensions.html)

---

Microsoft removed 119 malicious extensions from its Edge Add-ons store that used steganography to hide malware payloads inside image and font files, evading detection until days after installation. Dubbed StegoAd, the campaign combined credential theft with ad fraud and is attributed to a single threat actor active since at least 2021. The delayed activation technique was specifically designed to bypass automated security scanning at the point of submission.


> **Security Architect's Take:** Audit and restrict which browser extensions are permitted across your organisation using enterprise browser policies or an approved allowlist — Edge supports this via Microsoft Intune and Group Policy. Given the multi-year duration of this campaign, treat any unmanaged extension installed since 2021 as potentially suspect and review endpoint telemetry for anomalous credential access or ad-fraud traffic patterns.


**Original advisory:** [Microsoft Removes 119 Edge Extensions That Hid Malware in Images and Fonts](https://thehackernews.com/2026/06/microsoft-removes-119-edge-extensions.html)
