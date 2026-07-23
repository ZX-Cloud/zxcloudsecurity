+++
title = "Amazon Corretto July 2026 Security Updates | AWS"
date = "2024-07-22T18:00:00Z"
publishDate = "2026-07-22T18:00:00Z"
slug = "amazon-corretto-july-2026-quarterly-security-updates"
description = "Amazon releases July 2026 quarterly security updates for Corretto 8–26. Docker images now default to Amazon Linux 2023. Update Java workloads promptly."
categories = ["aws"]
tags = ["aws", "amazon-corretto", "openjdk", "patch-management", "container-security", "amazon-linux-2023", "java", "supply-chain"]
severity = "Medium"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-corretto-july-2026-quarterly-updates"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-corretto-july-2026-quarterly-updates)

---

Amazon has released quarterly security and critical updates for Amazon Corretto, its free OpenJDK distribution, covering versions 8 through 26. This release also shifts the default Docker images from Amazon Linux 2 to Amazon Linux 2023, and removes JavaFX binaries from Corretto 8. Organisations running Java workloads on AWS should apply these updates to address known security vulnerabilities in OpenJDK.


> **Security Architect's Take:** Prioritise updating all Corretto deployments to the latest patched versions, particularly in container environments — and validate that any Corretto 8 Docker images are rebuilt against Amazon Linux 2023 or explicitly pinned to the AL2 non-default variant if migration is not yet feasible. If your pipelines depend on JavaFX within Corretto 8, plan remediation now as binaries have been removed from this release.


**Original advisory:** [Amazon Corretto July 2026 Quarterly Updates](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-corretto-july-2026-quarterly-updates)
