+++
title = "AWS ACM Adds ACME Support for Auto TLS Certs"
date = "2024-08-06T22:03:36Z"
publishDate = "2026-08-06T22:03:36Z"
slug = "aws-certificate-manager-acme-support-automated-tls-renewal"
description = "AWS Certificate Manager now supports ACME protocol for automated TLS certificate renewal, essential as CA/Browser Forum cuts max validity to 47 days by 202"
categories = ["aws"]
tags = ["aws", "acm", "tls", "certificate-management", "acme", "pki", "automation", "compliance"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/automate-certificates-with-acme-support-in-aws-certificate-manager/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/automate-certificates-with-acme-support-in-aws-certificate-manager/)

---

AWS Certificate Manager (ACM) is introducing support for the ACME protocol, enabling automated TLS certificate issuance and renewal. This is increasingly important because the CA/Browser Forum is mandating shorter certificate lifespans — down to 100 days by March 2027 and 47 days by March 2029 — making manual renewal processes unmanageable at scale. Organisations that don't automate now risk widespread certificate expiry incidents as validity windows shrink.


> **Security Architect's Take:** Begin evaluating ACME integration with ACM now, particularly for workloads with large certificate inventories; map existing manual or semi-automated renewal workflows and prioritise migrating them before the March 2027 validity reduction takes effect to avoid operational risk.


**Original advisory:** [Automate certificates with ACME support in AWS Certificate Manager](https://aws.amazon.com/blogs/security/automate-certificates-with-acme-support-in-aws-certificate-manager/)
