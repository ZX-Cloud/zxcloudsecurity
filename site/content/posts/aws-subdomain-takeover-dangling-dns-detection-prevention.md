+++
title = "AWS Subdomain Takeover: Detect & Prevent Dangling DNS"
date = "2024-06-16T17:53:20Z"
publishDate = "2026-06-16T17:53:20Z"
slug = "aws-subdomain-takeover-dangling-dns-detection-prevention"
description = "Learn how attackers exploit dangling DNS records for subdomain takeover on AWS, and how to detect and prevent it using Route 53 and AWS security services."
categories = ["aws"]
tags = ["aws", "route53", "dns", "subdomain-takeover", "cloudfront", "s3", "dangling-dns", "threat-detection"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/threat-tactic-spotlight-subdomain-takeover/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/threat-tactic-spotlight-subdomain-takeover/)

---

Subdomain takeover occurs when DNS records point to resources that no longer exist, allowing attackers to claim those resources and serve malicious content under a legitimate domain. This is a well-known but frequently overlooked risk in cloud environments where infrastructure is regularly provisioned and decommissioned. The AWS Security Blog post explains how to identify dangling DNS records and use AWS services to prevent or mitigate this attack vector.


> **Security Architect's Take:** Audit your Route 53 hosted zones and any externally managed DNS for records pointing to decommissioned AWS resources such as Elastic Beanstalk environments, CloudFront distributions, or S3 buckets. Implement automated checks — consider AWS Config rules or a third-party DNS monitoring tool — to alert on dangling CNAMEs before attackers can exploit them.


**Original advisory:** [Threat tactic spotlight: Subdomain takeover](https://aws.amazon.com/blogs/security/threat-tactic-spotlight-subdomain-takeover/)
