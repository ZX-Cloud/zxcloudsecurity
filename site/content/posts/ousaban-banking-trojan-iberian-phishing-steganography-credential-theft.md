+++
title = "Ousaban Trojan Targets Spanish & Portuguese Bank Users"
date = "2024-07-01T15:26:55Z"
publishDate = "2026-07-01T15:26:55Z"
slug = "ousaban-banking-trojan-iberian-phishing-steganography-credential-theft"
description = "Ousaban banking trojan uses fake PDF phishing and steganography to steal credentials from Windows users banking in Spain and Portugal."
categories = ["general"]
tags = ["banking-trojan", "phishing", "steganography", "credential-theft", "windows", "ousaban", "malware", "iberian"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/ousaban-banking-trojan-targets-iberian.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/ousaban-banking-trojan-targets-iberian.html)

---

Ousaban, a Brazilian banking trojan, is targeting Windows users in Spain and Portugal via phishing emails containing fake corrupted PDF files. The campaign, discovered by Fortinet's FortiGuard Labs in May 2026, uses geofencing to confirm the victim is in the target region and steganography to conceal its payload within an image file. The ultimate aim is credential theft from Iberian banking customers.


> **Security Architect's Take:** Ensure endpoint security controls block steganographic payload delivery and enforce email gateway policies that quarantine password-protected or visually 'corrupted' PDFs. For organisations with staff in Spain or Portugal, consider deploying browser isolation for online banking portals and validate that DNS/proxy controls can detect geofencing callbacks used by the dropper.


**Original advisory:** [Ousaban Banking Trojan Targets Iberian Bank Users with Fake PDF Lures](https://thehackernews.com/2026/07/ousaban-banking-trojan-targets-iberian.html)
