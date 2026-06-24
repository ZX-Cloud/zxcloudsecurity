+++
title = "WhatsApp VBScript Attack Installs RMM Tool"
date = "2025-06-23T05:38:40Z"
publishDate = "2026-06-23T05:38:40Z"
slug = "whatsapp-vbscript-campaign-managengine-rmm-tool-install"
description = "Attackers use WhatsApp to deliver malicious VBScript files that silently install ManageEngine RMM software, granting persistent remote access to victims."
categories = ["general"]
tags = ["vbscript", "rmm", "manageengine", "whatsapp", "social-engineering", "living-off-the-land", "endpoint-security", "malware"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/whatsapp-vbscript-campaign-uses-fake.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/whatsapp-vbscript-campaign-uses-fake.html)

---

Attackers are sending malicious VBScript files via WhatsApp Direct Messages, disguised as legitimate documents, to silently install ManageEngine's RMM software on victims' machines. Once installed, the RMM tool gives attackers persistent remote access whilst blending in with legitimate IT management traffic. The campaign is actively targeting users across at least nine countries including the UK, making it a significant threat to both personal and corporate devices.


> **Security Architect's Take:** Review endpoint and DLP controls to detect and block unsolicited RMM tool installations, particularly ManageEngine, and ensure application whitelisting policies prevent VBScript execution from user-writeable directories. Consider alerting on outbound RMM traffic from endpoints that are not explicitly managed assets in your CMDB.


**Original advisory:** [WhatsApp VBScript Campaign Uses Fake Documents to Install ManageEngine RMM Tool](https://thehackernews.com/2026/06/whatsapp-vbscript-campaign-uses-fake.html)
