+++
title = "AWS Security Hub Adds Active Network Scanning"
date = "2024-07-08T21:00:00Z"
publishDate = "2026-07-08T21:00:00Z"
slug = "aws-security-hub-network-scanning-public-reachability"
description = "AWS Security Hub now actively probes resources to confirm internet reachability across AWS and Azure, surfacing exposed ports and services beyond config-ba"
categories = ["aws"]
tags = ["aws", "azure", "security-hub", "attack-surface-management", "network-scanning", "exposure-management", "cloud-posture", "internet-exposure"]
severity = "Medium"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/07/aws-security-hub-network-scanning/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/07/aws-security-hub-network-scanning/)

---

AWS Security Hub has launched Network Scanning, a capability that actively probes your AWS and Azure resources from the internet to confirm genuine public reachability — going beyond theoretical reachability based on firewall rules alone. It identifies exposed IP addresses, virtual machines, load balancers, open ports, and running services, generating findings that Security Hub Exposures then correlates with other risk signals. This gives security teams confirmed attack surface visibility rather than relying solely on configuration analysis.


> **Security Architect's Take:** Enable Network Scanning in Security Hub and integrate its findings into your existing triage workflow — prioritise remediation of any confirmed internet-reachable ports that host unexpected or unintended services. Cross-reference results against your asset inventory to identify shadow infrastructure or misconfigured resources that configuration-based tools may have missed.


**Original advisory:** [AWS Security Hub now offers Network Scanning to identify publicly reachable resources](https://aws.amazon.com/about-aws/whats-new/2026/07/aws-security-hub-network-scanning/)
