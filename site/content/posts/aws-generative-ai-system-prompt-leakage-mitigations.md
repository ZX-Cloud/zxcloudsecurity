+++
title = "AWS: System Prompt Leakage Risks in GenAI Apps"
date = "2024-07-08T18:58:42Z"
publishDate = "2026-07-08T18:58:42Z"
slug = "aws-generative-ai-system-prompt-leakage-mitigations"
description = "AWS outlines the risk of system prompt leakage in generative AI apps and provides architectural mitigations for cloud security teams to reduce exposure."
categories = ["aws"]
tags = ["aws", "generative-ai", "bedrock", "prompt-injection", "llm-security", "data-leakage", "application-security"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/designing-for-the-inevitable-system-prompt-leakage-and-mitigations-in-generative-ai-applications/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/designing-for-the-inevitable-system-prompt-leakage-and-mitigations-in-generative-ai-applications/)

---

System prompts in generative AI applications often contain sensitive proprietary information such as business logic, tool configurations, and role definitions. This AWS blog post addresses the risk of system prompt leakage — where an LLM is manipulated into revealing these instructions — and outlines architectural mitigations to reduce the impact when it occurs. As organisations deploy more AI-powered applications on AWS, understanding and designing around this risk is increasingly important.


> **Security Architect's Take:** Treat system prompts as sensitive configuration data: avoid embedding credentials or highly sensitive business logic directly within them, implement output filtering to detect leakage attempts, and design your AI application architecture to assume prompt contents will eventually be exposed — using least-privilege tool access and defence-in-depth accordingly.


**Original advisory:** [Designing for the inevitable: System prompt leakage and mitigations in generative AI applications](https://aws.amazon.com/blogs/security/designing-for-the-inevitable-system-prompt-leakage-and-mitigations-in-generative-ai-applications/)
