+++
title = "AWS Bedrock Guardrails Now Feed Into Security Lake"
date = "2024-08-06T19:00:15Z"
publishDate = "2026-08-06T19:00:15Z"
slug = "aws-bedrock-guardrails-amazon-security-lake-integration"
description = "Route Amazon Bedrock Guardrails violations to Security Lake to unify AI safety events with identity, network, and application security telemetry for incide"
categories = ["aws"]
tags = ["aws", "amazon-bedrock", "amazon-security-lake", "generative-ai", "prompt-injection", "ai-security", "security-monitoring", "data-lake"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/route-amazon-bedrock-guardrails-interventions-to-amazon-security-lake/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/route-amazon-bedrock-guardrails-interventions-to-amazon-security-lake/)

---

AWS has introduced an integration that routes Amazon Bedrock Guardrails intervention events — such as blocked prompt injections and PII redactions — directly into Amazon Security Lake. This allows security teams to query AI safety events alongside existing identity, network, and application telemetry in a unified data store. The capability improves visibility into AI-related threats and simplifies incident investigation for organisations deploying generative AI workloads.


> **Security Architect's Take:** If you are running Amazon Bedrock in production, enable this integration to ensure guardrail events are captured in Security Lake and included in your SIEM or SOAR workflows — treat prompt injection attempts and content policy violations as first-class security signals alongside network and identity events.


**Original advisory:** [Route Amazon Bedrock Guardrails interventions to Amazon Security Lake](https://aws.amazon.com/blogs/security/route-amazon-bedrock-guardrails-interventions-to-amazon-security-lake/)
