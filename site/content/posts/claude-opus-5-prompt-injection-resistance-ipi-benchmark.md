+++
title = "Claude Opus 5 Leads on Prompt Injection Resistance"
date = "2024-07-31T17:23:16Z"
publishDate = "2026-07-31T17:23:16Z"
slug = "claude-opus-5-prompt-injection-resistance-ipi-benchmark"
description = "Anthropic's Claude Opus 5 cuts prompt injection attack success to 2% in 15 attempts, outperforming GPT 5.6 variants by 10x on the IPI benchmark."
categories = ["general"]
tags = ["anthropic", "llm-security", "prompt-injection", "ai-security", "agentic-ai", "model-evaluation", "claude"]
severity = "Medium"
source = "Schneier on Security"
source_url = "https://www.schneier.com/blog/archives/2026/07/anthropics-opus-5-is-better-at-resisting-prompt-injection.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [Schneier on Security](https://www.schneier.com/blog/archives/2026/07/anthropics-opus-5-is-better-at-resisting-prompt-injection.html)

---

Anthropic's Claude Opus 5 model demonstrates significantly improved resistance to indirect prompt injection (IPI) attacks, reducing attacker success rates to 2.0% within 15 attempts compared to over 20% for the best-performing GPT 5.6 variant. Prompt injection is a key attack vector against AI-powered applications, where malicious instructions embedded in external content attempt to hijack model behaviour. These benchmark results matter because organisations deploying LLMs in agentic or automated workflows face real exposure if their chosen model is susceptible.


> **Security Architect's Take:** When evaluating LLMs for agentic pipelines, document management, or any workflow where the model processes untrusted external content, factor IPI benchmark performance into your model selection criteria alongside capability metrics — Opus 5's results suggest a material security advantage worth weighing against cost and latency trade-offs.


**Original advisory:** [Anthropic’s Opus 5 Is Better at Resisting Prompt Injection](https://www.schneier.com/blog/archives/2026/07/anthropics-opus-5-is-better-at-resisting-prompt-injection.html)
