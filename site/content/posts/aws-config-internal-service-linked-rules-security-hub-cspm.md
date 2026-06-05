+++
title = "AWS Config Internal Service Linked Rules Explained"
date = "2026-06-02T18:00:00Z"
slug = "aws-config-internal-service-linked-rules-security-hub-cspm"
description = "AWS Config now supports internal service linked rules, letting AWS services like Security Hub CSPM run independent rule evaluations at no extra cost to cus"
categories = ["aws"]
tags = ["aws", "aws-config", "security-hub", "cspm", "compliance", "cloud-governance", "config-rules"]
severity = "Low"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/06/aws-config-supports-internal-service-linked-rules"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-config-supports-internal-service-linked-rules)

---

AWS Config now supports internal service linked rules, allowing AWS services like Security Hub CSPM to deploy and manage their own Config rule evaluations independently of customer-managed rules. Evaluation results are delivered directly to the originating AWS service at no additional charge to customers. This separation means AWS services can run compliance checks without interfering with customer-configured Config setups.


> **Architect's Take:** No immediate action is required, but architects should review their AWS Config cost models and compliance dashboards — internal service linked rules operate independently and won't affect existing customer rules or recorders, so there is no risk of unintended interference. Take note that Security Hub CSPM will now leverage this mechanism, which may affect how you interpret Config rule counts and evaluation results in your environment.


**Original advisory:** [AWS Config now supports internal service linked rules](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-config-supports-internal-service-linked-rules)
