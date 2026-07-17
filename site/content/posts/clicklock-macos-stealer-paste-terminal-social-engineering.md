+++
title = "ClickLock macOS Stealer Uses Paste-to-Terminal Trick"
date = "2024-07-16T15:33:01Z"
publishDate = "2026-07-16T15:33:01Z"
slug = "clicklock-macos-stealer-paste-terminal-social-engineering"
description = "ClickLock malware targets macOS users with social engineering, tricking them into pasting malicious Terminal commands to steal data. Here's what to do."
categories = ["general"]
tags = ["macos", "clicklock", "infostealer", "social-engineering", "endpoint-security", "malware"]
severity = "Medium"
source = "The Register — Security"
source_url = "https://www.theregister.com/cyber-crime/2026/07/16/cmon-just-copy-this-text-string-and-paste-it-into-your-macos-terminal-itll-fix-your-computer-honest/5273701"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/cyber-crime/2026/07/16/cmon-just-copy-this-text-string-and-paste-it-into-your-macos-terminal-itll-fix-your-computer-honest/5273701)

---

A newly documented macOS information-stealing malware called ClickLock uses social engineering to trick users into copying and pasting malicious commands into their Terminal, granting the malware elevated access. The technique requires no technical exploit — it relies entirely on convincing the victim to run the payload themselves. This makes it particularly difficult to block with traditional endpoint controls, as the user is the attack vector.


> **Security Architect's Take:** Enforce endpoint controls that restrict Terminal and shell execution to authorised users via MDM policies, and ensure macOS fleet monitoring captures shell command telemetry. Consider user awareness training specifically covering 'paste-and-run' social engineering tactics, which are increasingly common on both macOS and Windows.


**Original advisory:** [C'mon, just copy this text string and paste it into your macOS Terminal – it'll fix your computer, honest](https://www.theregister.com/cyber-crime/2026/07/16/cmon-just-copy-this-text-string-and-paste-it-into-your-macos-terminal-itll-fix-your-computer-honest/5273701)
