+++
title = "Storm-1175 Deploys StormEncryptor via N-central Flaw"
date = "2025-08-10T16:38:37Z"
publishDate = "2026-08-10T16:38:37Z"
slug = "storm-1175-stormencryptor-ransomware-n-central-flaw"
description = "China-linked Storm-1175 is deploying new StormEncryptor ransomware, likely via an N-central vulnerability. Learn what cloud architects need to do now."
categories = ["general"]
tags = ["ransomware", "storm-1175", "n-central", "china-apt", "microsoft-threat-intelligence", "lateral-movement", "endpoint-security", "patch-management"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/china-linked-hackers-deploy-new.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/china-linked-hackers-deploy-new.html)

---

Microsoft has identified a China-linked financially motivated threat actor, Storm-1175, deploying a new ransomware strain called StormEncryptor, believed to be delivered via a vulnerability in N-central, an IT management platform. Written in C++ and appending the '.encrypted' extension to files, StormEncryptor represents a shift away from the group's previous use of Medusa ransomware. This is notable because it signals the group is developing bespoke tooling, making detection and attribution more complex.


> **Security Architect's Take:** Prioritise patching N-central instances immediately and audit any systems managed via N-central for signs of lateral movement or unauthorised file encryption. Additionally, review endpoint detection rules to ensure coverage for novel ransomware strains, particularly those not yet in commercial threat intelligence feeds.


**Original advisory:** [China-Linked Hackers Deploy New StormEncryptor Ransomware, Likely via N-central Flaw](https://thehackernews.com/2026/08/china-linked-hackers-deploy-new.html)
