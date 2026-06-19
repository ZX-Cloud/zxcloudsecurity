+++
title = "US Telco Stored Credit Cards in Plaintext: Lessons"
date = "2024-06-18T07:00:00Z"
publishDate = "2026-06-18T07:00:00Z"
slug = "us-telco-credit-card-plaintext-storage-data-security-lessons"
description = "A major US carrier stored credit card data in plaintext in the early 2000s. What cloud security architects should learn and do today."
categories = ["general"]
tags = ["data-at-rest-encryption", "pci-dss", "plaintext-storage", "sensitive-data", "data-protection", "misconfiguration", "telco", "historical-breach"]
severity = "Medium"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/06/18/major-us-carrier-stored-credit-card-info-in-the-clear-employee-learned-on-first-day/5257932"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/06/18/major-us-carrier-stored-credit-card-info-in-the-clear-employee-learned-on-first-day/5257932)

---

A retrospective account has emerged of a major US telecommunications carrier storing customer credit card data in plaintext during the early 2000s, a practice discovered by an employee on their very first day. This highlights how poor data handling hygiene was commonplace before PCI DSS mandated encryption standards, and serves as a reminder of the long-term reputational and regulatory risks of inadequate data protection. While historical, the story resonates today as organisations continue to misconfigure data storage in cloud environments.


> **Security Architect's Take:** Use this as a prompt to audit your current data stores — particularly object storage buckets, databases, and logs — for any plaintext storage of sensitive cardholder or PII data. Enforce encryption at rest as a baseline control and implement automated scanning tools such as AWS Macie, Google Cloud DLP, or Microsoft Purview to detect sensitive data exposure before an employee stumbles upon it.


**Original advisory:** [Major US carrier stored credit card info in the clear, employee learned on first day](https://www.theregister.com/security/2026/06/18/major-us-carrier-stored-credit-card-info-in-the-clear-employee-learned-on-first-day/5257932)
