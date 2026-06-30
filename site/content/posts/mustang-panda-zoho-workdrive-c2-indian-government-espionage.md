+++
title = "Mustang Panda Abuses Zoho WorkDrive for C2"
date = "2025-06-29T15:03:40Z"
publishDate = "2026-06-29T15:03:40Z"
slug = "mustang-panda-zoho-workdrive-c2-indian-government-espionage"
description = "China-linked Mustang Panda uses Zoho WorkDrive as a C2 channel in active espionage attacks on Indian government and hydropower targets."
categories = ["general"]
tags = ["zoho-workdrive", "mustang-panda", "apt", "command-and-control", "espionage", "living-off-trusted-services", "malware", "cloud-abuse"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/mustang-panda-uses-zoho-workdrive-as.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/mustang-panda-uses-zoho-workdrive-as.html)

---

Chinese state-aligned threat group Mustang Panda has been caught running two active espionage campaigns against Indian government and hydropower sector targets, using novel malware and abusing Zoho WorkDrive as a covert command-and-control channel. Acronis Threat Research Unit identified live compromises on machines belonging to senior Indian administrative staff. The abuse of a legitimate cloud productivity service makes detection significantly harder, as malicious traffic blends with normal business communications.


> **Security Architect's Take:** Review your organisation's egress controls and CASB policies to detect or block anomalous API usage patterns from sanctioned cloud storage services such as Zoho WorkDrive — legitimate tools used as C2 channels will bypass many traditional threat filters. Implement DNS and HTTP traffic inspection with behavioural baselines to flag unusual volumes or access patterns to cloud file-sharing platforms, particularly from server or privileged workstation endpoints.


**Original advisory:** [Mustang Panda Uses Zoho WorkDrive as Command Channel in Indian Government Attacks](https://thehackernews.com/2026/06/mustang-panda-uses-zoho-workdrive-as.html)
