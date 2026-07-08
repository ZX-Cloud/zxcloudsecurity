+++
title = "Enforce Zero Data Retention in AWS Bedrock with SCPs"
date = "2024-07-07T18:18:52Z"
publishDate = "2026-07-07T18:18:52Z"
slug = "aws-bedrock-zero-data-retention-bedrock-projects-service-control-policies"
description = "Learn how to use Amazon Bedrock Projects and AWS Service Control Policies to centrally enforce zero data retention across all accounts using third-party AI"
categories = ["aws"]
tags = ["aws", "amazon-bedrock", "service-control-policies", "data-retention", "generative-ai", "data-privacy", "organisations", "third-party-models"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/enforce-zero-data-retention-on-amazon-bedrock-with-bedrock-projects-and-service-control-policies/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/enforce-zero-data-retention-on-amazon-bedrock-with-bedrock-projects-and-service-control-policies/)

---

AWS has published guidance on enforcing zero data retention policies in Amazon Bedrock, particularly relevant now that some third-party models such as Claude Fable 5 may share data with external providers. Organisations can use Bedrock Projects alongside AWS Service Control Policies (SCPs) to centrally enforce data retention settings across all accounts in an AWS Organisation. This matters because without central enforcement, individual teams or accounts could inadvertently permit prompt and response data to be retained or shared beyond organisational boundaries.


> **Security Architect's Take:** Implement SCPs at the AWS Organisation level to deny any Bedrock inference calls that do not explicitly set data retention to zero, and scope Bedrock Projects to enforce this consistently — especially before onboarding any third-party or marketplace models that carry data-sharing agreements.


**Original advisory:** [Enforce zero data retention on Amazon Bedrock with Bedrock Projects and service control policies](https://aws.amazon.com/blogs/security/enforce-zero-data-retention-on-amazon-bedrock-with-bedrock-projects-and-service-control-policies/)
