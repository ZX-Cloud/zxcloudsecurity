+++
title = "GigaWiper Backdoor: Wiper, Spyware & Fake Ransomware"
date = "2025-07-09T18:08:07Z"
publishDate = "2026-07-09T18:08:07Z"
slug = "gigawiper-windows-backdoor-disk-wiper-fake-ransomware-spyware"
description = "Microsoft analyses GigaWiper, a Windows backdoor combining disk wiping, fake ransomware with no recovery key, and spyware. What cloud architects need to kn"
categories = ["general"]
tags = ["windows", "wiper-malware", "ransomware", "backdoor", "spyware", "destructive-malware", "incident-response", "endpoint-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-gigawiper-windows-backdoor-bundles.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-gigawiper-windows-backdoor-bundles.html)

---

Microsoft has analysed a new Windows backdoor called GigaWiper that combines three destructive capabilities — full disk wiping, Windows drive overwriting, and fake ransomware that encrypts files without saving the decryption key — into a single operator-controlled toolkit. Because the encryption key is discarded, victims cannot recover files even if they pay a ransom, making it a pure destructive tool masquerading as financially motivated malware. The modular design lowers the bar for threat actors to cause irreversible damage to targeted systems.


> **Security Architect's Take:** Prioritise immutable, offsite backups for Windows workloads — including cloud-hosted VMs — that cannot be reached or deleted by a compromised host, and validate recovery procedures regularly. Review endpoint detection coverage for disk-write and volume shadow copy deletion events, as these are reliable early indicators of wiper-class malware regardless of ransomware branding.


**Original advisory:** [New GigaWiper Windows Backdoor Bundles Disk Wiping, Fake Ransomware, and Spyware](https://thehackernews.com/2026/07/new-gigawiper-windows-backdoor-bundles.html)
