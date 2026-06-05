+++
title = "AWS Step Functions Adds AI Agent Steps via AgentCore"
date = "2026-06-03T20:00:00Z"
slug = "aws-step-functions-bedrock-agentcore-agentic-reasoning-integration"
description = "AWS Step Functions integrates with Amazon Bedrock AgentCore to add AI reasoning steps in workflows. Key security considerations for architects around IAM a"
categories = ["aws"]
tags = ["aws", "step-functions", "bedrock", "agentcore", "iam", "ai-security", "audit-logging", "least-privilege"]
severity = "Low"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/06/aws-step-functions-agentcore/"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-step-functions-agentcore/)

---

AWS Step Functions now integrates with Amazon Bedrock AgentCore (currently in preview) to allow AI agent reasoning steps within automated workflows. This enables teams to embed LLM-based tasks such as document classification and data extraction directly into orchestrated pipelines, with parallel execution and human approval gates. Audit trails are available via CloudWatch, capturing agent inputs, outputs, and token usage.


> **Architect's Take:** Review IAM permissions granted to Step Functions execution roles that invoke AgentCore harnesses — ensure least-privilege policies are applied, particularly around model invocation and tool access. Treat human approval steps as a mandatory control for any agentic action with write or destructive scope, and validate that CloudWatch audit logging is enabled before promoting any AgentCore-integrated workflow to production.


**Original advisory:** [AWS Step Functions adds AgentCore-powered agentic reasoning step](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-step-functions-agentcore/)
