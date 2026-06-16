+++
title = "ShinyHunters Breach: PeopleSoft Attacks Hit 100+ Orgs"
date = "2025-06-15T17:44:00Z"
publishDate = "2026-06-15T17:44:00Z"
slug = "shinyhunters-oracle-peoplesoft-breach-council-of-europe"
description = "ShinyHunters exploits Oracle PeopleSoft to breach the Council of Europe, Nottingham University, and 100+ other victims. What architects need to know."
categories = ["general"]
tags = ["oracle", "peoplesoft", "shinyhunters", "data-breach", "erp-security", "threat-actor", "vulnerability-exploitation", "supply-chain"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/cyber-crime/2026/06/15/council-of-europe-hacked-in-shinyhunters-peoplesoft-heist/5255757"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/cyber-crime/2026/06/15/council-of-europe-hacked-in-shinyhunters-peoplesoft-heist/5255757)

---

The hacking group ShinyHunters has breached the Council of Europe by exploiting vulnerabilities in Oracle PeopleSoft, the enterprise HR and administrative software used by many large organisations. The attack also affected Nottingham University and over 100 other unnamed victims, suggesting a widespread, opportunistic campaign targeting PeopleSoft deployments. The breach raises serious concerns about the exposure of sensitive personnel and organisational data held within ERP systems.


> **Security Architect's Take:** Audit all internet-facing PeopleSoft instances immediately — ensure they are patched to the latest Oracle CPU release, restrict access via IP allowlisting or VPN, and review whether PeopleSoft admin interfaces are unnecessarily exposed to the public internet. If PeopleSoft is hosted on cloud infrastructure, validate that security groups and network ACLs limit exposure appropriately.


**Original advisory:** [Council of Europe hacked in ShinyHunters' PeopleSoft heist](https://www.theregister.com/cyber-crime/2026/06/15/council-of-europe-hacked-in-shinyhunters-peoplesoft-heist/5255757)
