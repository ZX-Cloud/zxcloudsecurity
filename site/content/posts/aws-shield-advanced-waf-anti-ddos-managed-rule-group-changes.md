+++
title = "AWS Shield Advanced WAF Anti-DDoS Rule Group Changes"
date = "2024-07-27T19:01:23Z"
publishDate = "2026-07-27T19:01:23Z"
slug = "aws-shield-advanced-waf-anti-ddos-managed-rule-group-changes"
description = "AWS Shield Advanced is adopting the new WAF Anti-DDoS managed rule group for HTTP flood protection. Here's what changes and how to prepare your setup."
categories = ["aws"]
tags = ["aws", "shield-advanced", "aws-waf", "ddos", "http-flood", "managed-rules", "application-layer-security"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/aws-shield-advanced-is-embracing-the-aws-waf-anti-ddos-managed-rule-group-what-changes-and-how-to-prepare/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/aws-shield-advanced-is-embracing-the-aws-waf-anti-ddos-managed-rule-group-what-changes-and-how-to-prepare/)

---

AWS is integrating its new WAF Anti-DDoS managed rule group into Shield Advanced, providing automated, purpose-built protection against HTTP request flood attacks at the application layer. Launched in June 2025, this rule group is designed to detect and block DDoS traffic that closely mimics legitimate user behaviour. The change affects how Shield Advanced customers manage application-layer protections and requires preparation to avoid disruption.


> **Security Architect's Take:** Review your existing Shield Advanced application-layer protections and WAF rule configurations before the integration takes effect — specifically check for any custom rate-based rules that may conflict with or duplicate the new Anti-DDoS managed rule group, and test in count mode before switching to block to avoid false positives on legitimate traffic.


**Original advisory:** [AWS Shield Advanced is embracing the AWS WAF Anti-DDoS managed rule group: What changes and how to prepare](https://aws.amazon.com/blogs/security/aws-shield-advanced-is-embracing-the-aws-waf-anti-ddos-managed-rule-group-what-changes-and-how-to-prepare/)
