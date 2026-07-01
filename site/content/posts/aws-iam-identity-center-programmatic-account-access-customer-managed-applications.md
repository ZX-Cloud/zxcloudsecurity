+++
title = "AWS IAM Identity Center: Programmatic Account Access for App"
date = "2024-06-30T16:00:00Z"
publishDate = "2026-06-30T16:00:00Z"
slug = "aws-iam-identity-center-programmatic-account-access-customer-managed-applications"
description = "AWS IAM Identity Center now lets customer-managed apps retrieve temporary AWS credentials via trusted token issuers. Key governance and security implicatio"
categories = ["aws"]
tags = ["aws", "iam-identity-center", "iam", "trusted-token-issuer", "credential-management", "identity-federation", "least-privilege", "access-governance"]
severity = "Medium"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/06/aws-iam-identity-center-account-access-customer-managed-apps/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-iam-identity-center-account-access-customer-managed-apps/)

---

AWS IAM Identity Center now allows customer-managed applications to programmatically access AWS accounts on behalf of users, using tokens from a trusted external identity provider. Applications can discover assigned accounts and roles, and retrieve temporary credentials without requiring users to re-authenticate. This simplifies access flows but introduces new governance considerations around which applications are permitted to obtain AWS account credentials.


> **Security Architect's Take:** Review all existing customer-managed applications integrated with IAM Identity Center and apply the principle of least privilege when deciding which applications to enable for AWS account access. Ensure only management account or delegated administrators can grant this capability, and audit trusted token issuer configurations regularly to prevent credential abuse via compromised third-party IdPs.


**Original advisory:** [IAM Identity Center now enables programmatic AWS account access for customer managed applications](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-iam-identity-center-account-access-customer-managed-apps/)
