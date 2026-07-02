+++
title = "AWS Network Firewall Container Attribute Rules for EKS & ECS"
date = "2024-07-01T19:40:22Z"
publishDate = "2026-07-01T19:40:22Z"
slug = "aws-network-firewall-container-attribute-based-rules-eks-ecs"
description = "AWS Network Firewall now supports container attribute-based rules for EKS and ECS, enabling workload-level traffic control for AI/ML and containerised apps"
categories = ["aws"]
tags = ["aws", "network-firewall", "eks", "ecs", "container-security", "network-segmentation", "least-privilege", "ai-ml-security"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/secure-amazon-container-workloads-using-container-attribute-based-rules-in-aws-network-firewall/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/secure-amazon-container-workloads-using-container-attribute-based-rules-in-aws-network-firewall/)

---

AWS has introduced container attribute-based rules in AWS Network Firewall, enabling fine-grained traffic control for containerised workloads running on Amazon EKS and ECS. Security teams can now write firewall rules that reference container-level attributes such as pod labels or task metadata, rather than relying solely on IP addresses or VPC constructs. This is particularly valuable for AI/ML workloads where lateral movement or egress control is critical.


> **Security Architect's Take:** Review existing Network Firewall rule groups for EKS and ECS environments and consider migrating broad IP-based rules to container attribute-based rules to enforce least-privilege network access at the workload level — particularly for sensitive AI/ML pipelines such as model inference endpoints and JupyterHub instances.


**Original advisory:** [Secure Amazon container workloads using container attribute-based rules in AWS Network Firewall](https://aws.amazon.com/blogs/security/secure-amazon-container-workloads-using-container-attribute-based-rules-in-aws-network-firewall/)
