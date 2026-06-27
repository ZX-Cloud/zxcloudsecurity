+++
title = "One Million Passports Leaked via ID Verification Breach"
date = "2025-06-26T11:03:21Z"
publishDate = "2026-06-26T11:03:21Z"
slug = "one-million-passports-leaked-id-verification-data-breach"
description = "Nearly 1 million passport scans leaked from cannabis dispensary ID verification systems, exposing high-value credentials held by low-security third parties"
categories = ["general"]
tags = ["data-breach", "identity-verification", "pii", "third-party-risk", "supply-chain", "document-fraud", "data-minimisation"]
severity = "High"
source = "Schneier on Security"
source_url = "https://www.schneier.com/blog/archives/2026/06/one-million-passports-leaked-online.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [Schneier on Security](https://www.schneier.com/blog/archives/2026/06/one-million-passports-leaked-online.html)

---

A database of nearly one million passport scans, collected by cannabis dispensaries for ID verification, was exposed online. The breach illustrates a systemic risk where high-value government-issued credentials are entrusted to low-security third-party systems. The passports themselves are not compromised at source, but the leaked data can enable identity fraud, account takeover, and document forgery at scale.


> **Security Architect's Take:** Audit any third-party or SaaS identity verification vendors in your supply chain — demand evidence of encryption at rest, access controls, and data minimisation practices. Where possible, push for tokenised or hashed identity assertions rather than storing raw document scans, and ensure vendor contracts include breach notification SLAs and data retention limits.


**Original advisory:** [One Million Passports Leaked Online](https://www.schneier.com/blog/archives/2026/06/one-million-passports-leaked-online.html)
