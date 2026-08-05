+++
title = "DOUBLECUP ClickFix Attack Delivers DeviceManager RAT"
date = "2025-08-04T09:03:23Z"
publishDate = "2026-08-04T09:03:23Z"
slug = "doublecup-clickfix-cached-png-steganography-countloader-devicemanager-rat"
description = "Russian LaaS operation DOUBLECUP uses ClickFix lures and steganographic PNGs cached in browsers to deploy CountLoader and DeviceManager RAT."
categories = ["general"]
tags = ["malware", "remote-access-trojan", "steganography", "clickfix", "loader-as-a-service", "social-engineering", "endpoint-security", "browser-cache"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/doublecup-uses-clickfix-and-cached-pngs.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/doublecup-uses-clickfix-and-cached-pngs.html)

---

DOUBLECUP is a Russian loader-as-a-service operation that uses ClickFix social engineering to trick users into executing malicious code, which then hides malware inside PNG images stored in the browser cache using steganography. This two-stage approach ultimately delivers CountLoader and a new remote access trojan called DeviceManager. The technique is notable because it abuses legitimate browser cache storage to conceal malicious payloads, making detection harder for traditional security tools.


> **Security Architect's Take:** Review endpoint and browser security controls to detect unusual execution of content retrieved from browser cache directories, and consider deploying script execution policies that block ClickFix-style clipboard-based PowerShell lures. Ensure EDR solutions are tuned to flag steganographic extraction patterns and outbound RAT command-and-control traffic from managed endpoints.


**Original advisory:** [DOUBLECUP Uses ClickFix and Cached PNGs to Deliver CountLoader and DeviceManager RAT](https://thehackernews.com/2026/08/doublecup-uses-clickfix-and-cached-pngs.html)
