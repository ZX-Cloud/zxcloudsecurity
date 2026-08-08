+++
title = "UNC6671 Vishing Attacks Target SaaS Credentials"
date = "2025-08-07T18:16:13Z"
publishDate = "2026-08-07T18:16:13Z"
slug = "unc6671-vishing-attacks-saas-data-extortion"
description = "UNC6671 is using vishing to impersonate IT help desks and steal SaaS data from financial and professional services firms. Here's what to do."
categories = ["general"]
tags = ["vishing", "social-engineering", "saas", "data-extortion", "identity", "mfa-bypass", "financial-services", "credential-theft"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/unc6671-vishing-attacks-target-personal.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/unc6671-vishing-attacks-target-personal.html)

---

A threat group called UNC6671 is conducting voice phishing (vishing) attacks against employees in financial services, private equity, and professional services, impersonating IT help desk staff to steal SaaS credentials and data. Attackers contact victims on their personal mobile phones, making traditional enterprise call-filtering controls ineffective. The end goal is data extortion, making this a significant threat to organisations handling sensitive client or financial data.


> **Security Architect's Take:** Implement out-of-band identity verification procedures for any IT help desk interaction involving credential resets or security migrations, and brief staff explicitly that legitimate IT will never request credentials or MFA codes via unsolicited calls. Review SaaS access policies to enforce phishing-resistant MFA (e.g. FIDO2) and consider restricting OAuth token issuance to known, managed devices to limit the blast radius if credentials are compromised.


**Original advisory:** [UNC6671 Vishing Attacks Target Personal Phones to Steal SaaS Data](https://thehackernews.com/2026/08/unc6671-vishing-attacks-target-personal.html)
