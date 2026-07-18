+++
title = "GoldenEyeDog Linked to DigiCert Code-Signing Breach"
date = "2025-07-17T16:39:16Z"
publishDate = "2026-07-17T16:39:16Z"
slug = "goldeneyedog-cylindricalcanine-digicert-breach-code-signing-certificate-theft"
description = "Chinese APT subgroup CylindricalCanine breached DigiCert in April 2026, stealing code-signing certificates. Learn the supply chain security implications."
categories = ["general"]
tags = ["apt", "supply-chain", "code-signing", "certificate-authority", "goldeneyedog", "digicert", "threat-intelligence", "malware"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/goldeneyedog-subgroup-linked-to.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/goldeneyedog-subgroup-linked-to.html)

---

A subgroup of the Chinese threat actor GoldenEyeDog (also known as APT-Q-27 and Dragon Breath), tracked as CylindricalCanine, has been attributed to a breach of certificate authority DigiCert in April 2026, resulting in the theft of code-signing certificates. This is significant because stolen code-signing certificates can be used to sign malicious software, making it appear legitimate and trusted by operating systems and security tools. The incident raises serious supply chain concerns for any organisation relying on DigiCert-issued certificates to verify software integrity.


> **Security Architect's Take:** Review your organisation's trust stores and CI/CD pipelines for any DigiCert code-signing certificates issued around or before April 2026, and check whether DigiCert has revoked affected certificates — if so, ensure your software verification processes enforce revocation checking (OCSP/CRL) to prevent trust in potentially compromised signatures.


**Original advisory:** [GoldenEyeDog Subgroup Linked to DigiCert Breach and Code-Signing Certificate Theft](https://thehackernews.com/2026/07/goldeneyedog-subgroup-linked-to.html)
