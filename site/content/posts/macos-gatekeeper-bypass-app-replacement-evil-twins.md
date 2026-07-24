+++
title = "macOS Gatekeeper Bypass: Apps Swapped for Evil Twins"
date = "2025-07-23T23:24:27Z"
publishDate = "2026-07-23T23:24:27Z"
slug = "macos-gatekeeper-bypass-app-replacement-evil-twins"
description = "Researchers show macOS Gatekeeper can be bypassed by replacing downloaded apps with malicious versions. Apple has declined to fix the issue."
categories = ["general"]
tags = ["macos", "apple", "gatekeeper", "supply-chain", "endpoint-security", "malware", "application-security"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/24/researchers-replace-downloaded-macos-apps-with-evil-twins-apple-shrugs/5277858"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/24/researchers-replace-downloaded-macos-apps-with-evil-twins-apple-shrugs/5277858)

---

Security researchers have demonstrated a technique allowing malicious actors to swap legitimate macOS applications with trojanised versions after download, bypassing Gatekeeper — Apple's primary defence against unauthorised software. The attack exploits weaknesses in how Gatekeeper validates apps post-download rather than at execution time. Apple has reportedly declined to address the issue, leaving users of affected software exposed.


> **Security Architect's Take:** Organisations deploying macOS endpoints should enforce application allowlisting via MDM solutions such as Jamf or Microsoft Intune, and consider supplementing Gatekeeper with third-party endpoint detection tools that monitor file integrity at execution. Audit your software distribution pipelines to ensure downloads are verified via cryptographic hashes independently of Gatekeeper.


**Original advisory:** [Researchers replace downloaded macOS apps with evil twins, Apple shrugs](https://www.theregister.com/security/2026/07/24/researchers-replace-downloaded-macos-apps-with-evil-twins-apple-shrugs/5277858)
