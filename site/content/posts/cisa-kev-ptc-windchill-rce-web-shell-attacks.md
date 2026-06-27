+++
title = "PTC Windchill RCE Flaw Added to CISA KEV Catalog"
date = "2026-06-26T12:31:56Z"
publishDate = "2026-06-26T12:31:56Z"
slug = "cisa-kev-ptc-windchill-rce-web-shell-attacks"
description = "CISA adds critical PTC Windchill RCE vulnerability to its KEV catalog amid active web shell attacks targeting PDM and PLM systems."
categories = ["general"]
tags = ["ptc-windchill", "remote-code-execution", "web-shell", "cisa-kev", "plm-pdm", "critical-infrastructure", "active-exploitation", "manufacturing"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/cisa-adds-exploited-ptc-windchill-rce.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/cisa-adds-exploited-ptc-windchill-rce.html)

---

CISA has added a critical remote code execution vulnerability in PTC Windchill PDMLink and FlexPLM — software used to manage product data and lifecycles in industrial and manufacturing environments — to its Known Exploited Vulnerabilities catalogue. Attackers are actively exploiting the flaw to deploy web shells, giving them persistent, unauthorised access to affected systems. This is particularly concerning given the prevalence of Windchill in critical manufacturing and defence supply chains.


> **Security Architect's Take:** Organisations running PTC Windchill PDMLink or FlexPLM should treat patching as urgent — apply available vendor patches immediately and audit internet-facing instances for signs of web shell deployment. If these systems are cloud-hosted or accessible via cloud-based DMZs, review network segmentation and WAF rules to restrict external access whilst remediation is underway.


**Original advisory:** [CISA Adds Exploited PTC Windchill RCE Flaw to KEV as Web Shell Attacks Continue](https://thehackernews.com/2026/06/cisa-adds-exploited-ptc-windchill-rce.html)
