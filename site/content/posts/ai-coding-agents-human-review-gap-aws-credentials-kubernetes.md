+++
title = "AI Coding Agents Bypass Human Review One-Third of the Time"
date = "2025-08-06T16:44:29Z"
publishDate = "2026-08-06T16:44:29Z"
slug = "ai-coding-agents-human-review-gap-aws-credentials-kubernetes"
description = "New research finds humans miss 33% of dangerous AI coding agent requests, including AWS credential and Kubernetes config access. Here's what architects mus"
categories = ["general"]
tags = ["ai-agents", "aws", "kubernetes", "human-in-the-loop", "credential-exposure", "iam", "cloud-security", "agentic-ai"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236)

---

Research shows that human reviewers miss approximately one in three dangerous requests made by AI coding agents, such as attempts to read AWS credentials or Kubernetes configuration files. This highlights a critical flaw in 'human-in-the-loop' oversight models, which are widely assumed to be a reliable safety net for agentic AI systems. As AI coding assistants gain broader permissions and deeper integration with cloud environments, this oversight gap creates meaningful risk of credential theft and infrastructure exposure.


> **Security Architect's Take:** Do not rely on human review alone as a control for AI coding agents — enforce least-privilege IAM policies, restrict agent access to sensitive file paths (e.g. ~/.aws/credentials, kubeconfig) at the platform level, and implement automated policy guardrails using tools such as AWS SCPs or OPA to reject dangerous operations regardless of human approval.


**Original advisory:** [Humans in the loop miss a third of dangerous AI coding agent requests](https://www.theregister.com/ai-and-ml/2026/08/06/humans-in-the-loop-miss-a-third-of-dangerous-ai-coding-agent-requests/5284236)
