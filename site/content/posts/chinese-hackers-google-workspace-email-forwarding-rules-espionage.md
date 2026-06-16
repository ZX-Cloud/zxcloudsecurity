+++
title = "Chinese Hackers Abused Google Workspace Rules to Steal Email"
date = "2025-06-15T19:44:06Z"
publishDate = "2026-06-15T19:44:06Z"
slug = "chinese-hackers-google-workspace-email-forwarding-rules-espionage"
description = "A China-linked group backdoored REDCap servers to steal credentials, then abused Google Workspace forwarding rules to exfiltrate sensitive research and def"
categories = ["general"]
tags = ["gcp", "google-workspace", "espionage", "credential-theft", "email-exfiltration", "redcap", "living-off-the-land", "apt"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/chinese-hackers-abused-google-workspace.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/chinese-hackers-abused-google-workspace.html)

---

A Chinese state-linked espionage group compromised North American medical, academic, and military research organisations by planting a backdoor on REDCap research data servers to harvest credentials. Once inside, the attackers manipulated Google Workspace email forwarding rules to silently copy and exfiltrate sensitive research and defence communications over an extended period. The attack is notable for its stealth and abuse of legitimate platform features, making detection significantly harder.


> **Security Architect's Take:** Audit all Google Workspace email delegation and forwarding rules immediately, particularly for accounts with access to sensitive data — legitimate users rarely set rules to copy all mail externally. Enforce Workspace alert policies for new forwarding rules, restrict rule creation via Admin Console, and treat REDCap or other self-hosted research platforms as high-risk ingress points requiring MFA and privileged access controls.


**Original advisory:** [Chinese Hackers Abused Google Workspace Rules to Steal Research and Defense Emails](https://thehackernews.com/2026/06/chinese-hackers-abused-google-workspace.html)
