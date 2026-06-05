+++
title = "AWS Deadline Cloud Adds Persistent EBS Storage for SMF"
date = "2026-06-02T17:00:00Z"
slug = "aws-deadline-cloud-persistent-ebs-storage-service-managed-fleets"
description = "AWS Deadline Cloud now supports persistent EBS volumes for Service-Managed Fleets. Learn the security implications for cloud architects managing rendering "
categories = ["aws"]
tags = ["aws", "deadline-cloud", "ebs", "persistent-storage", "data-retention", "encryption-at-rest", "iam", "storage-security"]
severity = "Low"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/06/deadline-cloud/persistent-storage"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/deadline-cloud/persistent-storage)

---

AWS Deadline Cloud now supports persistent EBS volumes for Service-Managed Fleet workers, preserving software environments and assets across worker lifecycle events. Previously, workers used only ephemeral storage, meaning software had to be reinstalled on every recycle. This change reduces startup times and improves job throughput for compute-intensive rendering and simulation workloads.


> **Architect's Take:** Review IAM policies and EBS volume access controls to ensure persistent volumes cannot be accessed by unintended workers or principals across lifecycle boundaries. Consider enabling EBS encryption at rest for all SMF persistent volumes and validate that TTL policies are configured to minimise unnecessary data retention in line with your data classification requirements.


**Original advisory:** [AWS Deadline Cloud now supports persistent storage for Service Managed Fleets](https://aws.amazon.com/about-aws/whats-new/2026/06/deadline-cloud/persistent-storage)
