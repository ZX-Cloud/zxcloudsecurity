+++
title = "Microsoft 365 Copilot Prompt Injection Spreads via Word Docs"
date = "2025-07-30T11:54:49Z"
publishDate = "2026-07-30T11:54:49Z"
slug = "microsoft-365-copilot-word-prompt-injection-self-replicating"
description = "Hidden prompts in Word documents can manipulate Microsoft 365 Copilot to alter content and self-replicate into new files, posing a serious enterprise risk."
categories = ["general"]
tags = ["azure", "microsoft-365", "copilot", "prompt-injection", "ai-security", "data-integrity", "supply-chain", "word"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/microsoft-copilot-for-word-can-copy.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/microsoft-copilot-for-word-can-copy.html)

---

A security researcher has demonstrated that hidden instructions embedded in a Word document can manipulate Microsoft 365 Copilot into silently altering document content — such as rewriting figures — and then propagating those same hidden instructions into any newly generated files. The attack is self-replicating across Copilot drafting sessions, meaning a single malicious document could poison multiple downstream outputs. This technique, disclosed 144 days after responsible reporting, represents a worm-like prompt injection risk within enterprise document workflows.


> **Security Architect's Take:** Treat AI-generated documents as untrusted inputs in your data classification and DLP policies. Until Microsoft issues a fix, consider restricting Copilot's ability to ingest externally sourced or user-submitted Word documents in sensitive workflows, and audit any Copilot-drafted outputs for unexpected content or embedded instructions before distribution.


**Original advisory:** [Microsoft Copilot for Word Can Copy Hidden Prompts Into New Documents](https://thehackernews.com/2026/07/microsoft-copilot-for-word-can-copy.html)
