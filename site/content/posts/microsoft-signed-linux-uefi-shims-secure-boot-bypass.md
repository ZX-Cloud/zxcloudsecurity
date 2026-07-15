+++
title = "11 Signed Linux UEFI Shims Bypass Secure Boot"
date = "2025-07-14T12:46:18Z"
publishDate = "2026-07-14T12:46:18Z"
slug = "microsoft-signed-linux-uefi-shims-secure-boot-bypass"
description = "11 Microsoft-signed Linux UEFI shims can be exploited to bypass Secure Boot, enabling bootkit deployment. Find out what architects should do now."
categories = ["general"]
tags = ["uefi", "secure-boot", "bootkit", "linux", "firmware-security", "supply-chain", "azure", "microsoft"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/11-old-microsoft-signed-linux-uefi.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/11-old-microsoft-signed-linux-uefi.html)

---

Researchers have identified 11 older UEFI shim applications that were legitimately signed by Microsoft but contain vulnerabilities allowing attackers to bypass Secure Boot, the firmware-level protection that ensures only trusted software loads at system startup. An attacker with physical or privileged access could exploit these shims to run unsigned, malicious code before the operating system loads, potentially deploying persistent firmware-level malware known as bootkits. This is significant because the shims carry a valid Microsoft signature, meaning many systems will trust them by default without additional configuration.


> **Security Architect's Take:** Audit your cloud and on-premises Linux VM images to identify whether any of the affected UEFI shim versions are present, and apply any available revocations via the UEFI Secure Boot Forbidden Signature Database (dbx). For cloud workloads on Azure, AWS, or GCP using Secure Boot or Shielded/Confidential VM features, verify that your base images are sourced from up-to-date, vendor-maintained sources and monitor for UEFI dbx update advisories from your distro and cloud provider.


**Original advisory:** [11 Old Microsoft-Signed Linux UEFI Shims Could Let Attackers Bypass Secure Boot](https://thehackernews.com/2026/07/11-old-microsoft-signed-linux-uefi.html)
