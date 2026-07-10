+++
title = "Dormant GitHub Accounts Used to Map Corporate Orgs"
date = "2024-07-09T18:38:49Z"
publishDate = "2026-07-09T18:38:49Z"
slug = "dormant-github-ghost-accounts-corporate-org-enumeration-attack"
description = "Attackers use aged GitHub ghost accounts and compromised OAuth tokens to enumerate corporate GitHub orgs via the API. Here's what security teams should do."
categories = ["general"]
tags = ["github", "oauth", "reconnaissance", "supply-chain", "api-security", "threat-intelligence", "credential-compromise", "devops-security"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/dormant-github-accounts-help-attackers.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/dormant-github-accounts-help-attackers.html)

---

Attackers are systematically mapping corporate GitHub organisations, repositories, and user accounts using the GitHub API, according to Datadog Security Labs. They are using automated scraping tools disguised with legitimate-sounding user agents, alongside dormant 'ghost' accounts that are often years old, or compromised OAuth tokens. This intelligence-gathering activity likely precedes targeted attacks such as supply chain compromises, credential theft, or targeted phishing.


> **Security Architect's Take:** Audit your GitHub organisation's visibility settings and restrict public exposure of member lists, repositories, and team structures where possible. Review OAuth token grants and personal access tokens regularly, enforce token expiry policies, and enable GitHub's audit log streaming to a SIEM to detect unusual API enumeration patterns.


**Original advisory:** [Dormant GitHub Accounts Help Attackers Blend In While Mapping Corporate Orgs](https://thehackernews.com/2026/07/dormant-github-accounts-help-attackers.html)
