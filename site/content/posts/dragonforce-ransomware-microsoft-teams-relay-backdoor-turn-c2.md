+++
title = "DragonForce Abuses Microsoft Teams C2 Traffic"
date = "2025-06-18T13:30:07Z"
publishDate = "2026-06-18T13:30:07Z"
slug = "dragonforce-ransomware-microsoft-teams-relay-backdoor-turn-c2"
description = "DragonForce ransomware uses a Go-based RAT to hide C2 traffic inside Microsoft Teams relay infrastructure, evading detection on enterprise networks."
categories = ["general"]
tags = ["azure", "microsoft-teams", "ransomware", "dragonforce", "command-and-control", "backdoor", "c2-evasion", "rat"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/dragonforce-hackers-abuse-microsoft.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/dragonforce-hackers-abuse-microsoft.html)

---

The DragonForce ransomware group has deployed a custom Go-based backdoor, Backdoor.Turn, that tunnels command-and-control traffic through Microsoft Teams relay infrastructure to evade detection. By blending malicious traffic with legitimate Teams communications, the group makes it significantly harder for defenders to identify or block C2 activity. The technique was observed in an attack against a major US services organisation, flagged by Symantec and Carbon Black.


> **Security Architect's Take:** Review your Microsoft Teams egress traffic and ensure your CASB or network monitoring tools can inspect and baseline Teams relay communications — legitimate use should never involve unusual outbound patterns or unexpected relay endpoints. Consider implementing Zero Trust network segmentation so that even if a host is compromised, lateral movement and C2 exfiltration via trusted SaaS channels is detected and restricted.


**Original advisory:** [DragonForce Hackers Abuse Microsoft Teams Relays to Hide Backdoor.Turn C2 Traffic](https://thehackernews.com/2026/06/dragonforce-hackers-abuse-microsoft.html)
