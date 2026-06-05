+++
title = "Manage Unused AWS KMS Keys & Prevent Deletions"
date = "2026-06-02T19:01:54Z"
slug = "aws-kms-unused-keys-prevent-accidental-deletion"
description = "Learn how to audit unused AWS KMS keys, reduce costs, meet compliance requirements, and prevent accidental key deletions across multi-account environments."
categories = ["aws"]
tags = ["aws", "kms", "key-management", "encryption", "compliance", "data-protection", "cloudtrail", "cost-optimisation"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/identify-unused-aws-kms-keys-and-prevent-accidental-key-deletions/"
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/identify-unused-aws-kms-keys-and-prevent-accidental-key-deletions/)

---

AWS has published guidance on identifying unused KMS encryption keys and protecting them from accidental deletion across large, multi-account environments. Orphaned or forgotten keys can inflate costs, create compliance gaps, and pose a risk if unexpectedly deleted — potentially making encrypted data permanently inaccessible. The post outlines tooling and processes to audit key usage and apply deletion safeguards at scale.


> **Architect's Take:** Implement regular KMS key usage audits using AWS CloudTrail and CloudWatch metrics, and ensure deletion windows and key policies are configured to prevent accidental removal — particularly in multi-account organisations where key ownership can become unclear over time.


**Original advisory:** [Identify unused AWS KMS keys and prevent accidental key deletions](https://aws.amazon.com/blogs/security/identify-unused-aws-kms-keys-and-prevent-accidental-key-deletions/)
