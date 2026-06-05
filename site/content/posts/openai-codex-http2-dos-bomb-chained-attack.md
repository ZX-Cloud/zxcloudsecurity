+++
title = "OpenAI Codex Chains HTTP/2 DoS Attacks Autonomously"
date = "2026-06-04T19:08:00Z"
slug = "openai-codex-http2-dos-bomb-chained-attack"
description = "OpenAI's Codex AI agent autonomously chained decade-old HTTP/2 DoS techniques to crash web servers in seconds — here's what architects need to know."
categories = ["general"]
tags = ["openai", "codex", "denial-of-service", "http2", "ai-security", "web-server", "llm-agents", "threat-research"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/06/04/openais-codex-chains-decade-old-dos-techniques-into-http/2-bomb/5251377"
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/06/04/openais-codex-chains-decade-old-dos-techniques-into-http/2-bomb/5251377)

---

OpenAI's Codex AI agent independently discovered and chained together multiple decade-old HTTP/2 denial-of-service techniques to bring down web servers within seconds, creating what researchers are calling an HTTP/2 bomb. This demonstrates that AI coding agents can autonomously rediscover and combine legacy attack methods into novel, highly effective exploits without human guidance. The incident raises significant concerns about the offensive security capabilities of large language model-based agents operating with minimal oversight.


> **Architect's Take:** Review your HTTP/2 implementation and ensure rate limiting, connection throttling, and request flood protections are in place at your load balancer or WAF layer — AWS WAF, Azure Front Door, and GCP Cloud Armor all offer relevant rule sets that should be validated against HTTP/2-specific DoS vectors. Consider whether any AI coding agents in your environment have unrestricted outbound network access, and apply least-privilege controls accordingly.


**Original advisory:** [OpenAI's agent chained decade-old DoS attacks to crash web servers in seconds](https://www.theregister.com/security/2026/06/04/openais-codex-chains-decade-old-dos-techniques-into-http/2-bomb/5251377)
