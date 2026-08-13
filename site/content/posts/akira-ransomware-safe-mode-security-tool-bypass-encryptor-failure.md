+++
title = "Akira Ransomware Disables Security Tools via Safe Mode"
date = "2025-08-12T13:00:00Z"
publishDate = "2026-08-12T13:00:00Z"
slug = "akira-ransomware-safe-mode-security-tool-bypass-encryptor-failure"
description = "Akira ransomware attempted to bypass endpoint security by booting victims into Safe Mode — but accidentally broke their own encryptor in the process."
categories = ["general"]
tags = ["ransomware", "akira", "endpoint-security", "defence-evasion", "safe-mode", "edr-bypass", "incident-response"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/research/2026/08/12/akira-ransomware-scum-blocked-victims-security-tools-and-broke-their-own-encryptor/5286515"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/research/2026/08/12/akira-ransomware-scum-blocked-victims-security-tools-and-broke-their-own-encryptor/5286515)

---

The Akira ransomware group attempted to disable victim security tools by booting compromised systems into Safe Mode, but inadvertently broke their own encryption process in doing so, preventing successful file encryption. This incident highlights both the evolving tactics ransomware operators use to bypass endpoint defences and the operational errors that can occur when attackers improvise. While the self-inflicted failure limited damage in this case, the underlying technique of neutralising security software remains a serious and repeatable threat.


> **Security Architect's Take:** Ensure endpoint detection and response (EDR) tools are configured to remain active and tamper-resistant in Safe Mode, and that Safe Mode reboots trigger alerts — many security agents are disabled by default in this boot state. Review your ransomware response runbooks to account for Safe Mode-based defence evasion as a known Akira TTP.


**Original advisory:** [Akira ransomware scum blocked victim's security tools – and broke their own encryptor](https://www.theregister.com/research/2026/08/12/akira-ransomware-scum-blocked-victims-security-tools-and-broke-their-own-encryptor/5286515)
