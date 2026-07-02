+++
title = "AWS GuardDuty Adds Sensitive File Modification Detections"
date = "2024-07-01T16:58:00Z"
publishDate = "2026-07-01T16:58:00Z"
slug = "aws-guardduty-runtime-sensitive-file-modification-detections"
description = "Amazon GuardDuty Runtime Monitoring now detects sensitive file modifications on EC2, EKS, and ECS — covering persistence, privilege escalation, and defence"
categories = ["aws"]
tags = ["aws", "guardduty", "runtime-monitoring", "ec2", "eks", "ecs", "privilege-escalation", "defence-evasion"]
severity = "Medium"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-guardduty-sfm/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-guardduty-sfm/)

---

Amazon GuardDuty Runtime Monitoring has added three new threat detections that alert on sensitive file modifications across EC2, EKS, and ECS workloads. The detections cover persistence, privilege escalation, and defence evasion tactics by monitoring five low-level file operations directly, making them effective even against obfuscated attacks that evade command-line monitoring. Each finding maps to MITRE ATT&CK tactics and includes remediation guidance, helping teams act quickly on post-compromise activity.


> **Security Architect's Take:** If GuardDuty Runtime Monitoring is already enabled in your environment, these detections are active at no additional configuration cost — verify Runtime Monitoring is enabled across all relevant EC2, EKS, and ECS workloads and ensure the new finding types (Persistence, PrivilegeEscalation, and DefenseEvasion prefixed SensitiveFileModified) are included in your Security Hub or SIEM alerting rules.


**Original advisory:** [Amazon GuardDuty adds sensitive file modification threat detections](https://aws.amazon.com/about-aws/whats-new/2026/07/amazon-guardduty-sfm/)
