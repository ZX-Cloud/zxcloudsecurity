+++
title = "AWS WAF Bot Control for AI Agent Traffic Auth"
date = "2024-07-14T15:18:42Z"
publishDate = "2026-07-14T15:18:42Z"
slug = "aws-waf-bot-control-ai-agent-traffic-authentication"
description = "Learn how AWS WAF Bot Control can authenticate legitimate AI agent traffic in multi-tenant environments like Amazon Bedrock AgentCore."
categories = ["aws"]
tags = ["aws", "aws-waf", "amazon-bedrock", "bot-control", "ai-agents", "bot-mitigation", "api-security", "zero-trust"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/authenticate-legitimate-ai-agent-traffic-with-aws-waf-bot-control/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/authenticate-legitimate-ai-agent-traffic-with-aws-waf-bot-control/)

---

AWS has published guidance on using WAF Bot Control to authenticate legitimate AI agent traffic, addressing a growing challenge as automated tools increasingly access web applications. Traditional IP-based filtering breaks down in multi-tenant environments like Amazon Bedrock AgentCore, where many workloads share the same IP space. This matters because organisations need a reliable way to permit genuine AI agent traffic without inadvertently opening the door to malicious bots.


> **Security Architect's Take:** If you are running APIs or web applications that serve or interact with AI agents — particularly via Amazon Bedrock — review your WAF Bot Control rules and consider implementing token-based or cryptographic authentication mechanisms to distinguish legitimate agent traffic from malicious automation at the edge.


**Original advisory:** [Authenticate legitimate AI agent traffic with AWS WAF Bot Control](https://aws.amazon.com/blogs/security/authenticate-legitimate-ai-agent-traffic-with-aws-waf-bot-control/)
