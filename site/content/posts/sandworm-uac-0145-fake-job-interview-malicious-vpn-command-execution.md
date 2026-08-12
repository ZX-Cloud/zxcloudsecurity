+++
title = "Sandworm UAC-0145 Fake Job VPN Malware Attack"
date = "2025-08-11T18:36:47Z"
publishDate = "2026-08-11T18:36:47Z"
slug = "sandworm-uac-0145-fake-job-interview-malicious-vpn-command-execution"
description = "Russian Sandworm subgroup UAC-0145 targets Ukrainian IT workers with fake recruiter lures, deploying a malicious VPN capable of remote command execution."
categories = ["general"]
tags = ["sandworm", "apt44", "uac-0145", "social-engineering", "malware", "spear-phishing", "remote-code-execution", "nation-state"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/sandworm-linked-uac-0145-uses-fake-job.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/sandworm-linked-uac-0145-uses-fake-job.html)

---

A Russian state-linked threat group (UAC-0145, a Sandworm subgroup) is targeting Ukrainian IT workers with fake job interview lures, tricking them into installing a malicious VPN client that grants attackers remote command execution on victims' machines. The campaign is a social engineering operation disguised as legitimate recruitment activity. This matters because IT workers with privileged access to infrastructure are high-value targets, and compromised endpoints can serve as footholds into cloud and enterprise environments.


> **Security Architect's Take:** Enforce strict controls on software installation across developer and IT workstations, and ensure VPN or remote-access tooling is allowlisted via MDM or endpoint policy. Brief engineering teams on recruitment-themed spear-phishing, particularly any unsolicited requests to install software as part of a 'technical interview' process.


**Original advisory:** [Sandworm-Linked UAC-0145 Uses Fake Job Interviews to Push VPN That Can Run Commands](https://thehackernews.com/2026/08/sandworm-linked-uac-0145-uses-fake-job.html)
