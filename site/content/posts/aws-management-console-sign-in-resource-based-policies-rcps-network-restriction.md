+++
title = "Restrict AWS Console Access with Sign-In RCPs"
date = "2024-06-24T20:01:47Z"
publishDate = "2026-06-24T20:01:47Z"
slug = "aws-management-console-sign-in-resource-based-policies-rcps-network-restriction"
description = "AWS now supports resource-based policies and RCPs for Sign-In, letting you restrict Management Console and CLI access to trusted networks only."
categories = ["aws"]
tags = ["aws", "aws-sign-in", "resource-control-policies", "aws-organizations", "iam", "network-security", "access-control", "console-security"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/restrict-aws-management-console-access-to-expected-networks-with-sign-in-resource-based-policies-and-rcps/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/restrict-aws-management-console-access-to-expected-networks-with-sign-in-resource-based-policies-and-rcps/)

---

AWS has introduced support for resource-based policies and resource control policies (RCPs) on AWS Sign-In, allowing organisations to restrict who can access the AWS Management Console and CLI based on network origin. This means administrators can limit sign-in attempts to known corporate networks, on-premises data centres, or specific VPCs. It is a significant preventive control against unauthorised console access from unexpected or untrusted locations.


> **Security Architect's Take:** Evaluate deploying RCPs at the AWS Organizations level to enforce network-based sign-in restrictions across all member accounts — this is a strong detective and preventive control that can block credential-based attacks originating outside your trusted network perimeter. Combine with existing SCPs and IAM policies for defence-in-depth.


**Original advisory:** [Restrict AWS Management Console access to expected networks with sign-in resource-based policies and RCPs](https://aws.amazon.com/blogs/security/restrict-aws-management-console-access-to-expected-networks-with-sign-in-resource-based-policies-and-rcps/)
