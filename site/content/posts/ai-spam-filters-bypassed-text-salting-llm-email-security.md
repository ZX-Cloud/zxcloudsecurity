+++
title = "AI Spam Filters Bypassed by Text Salting Tricks"
date = "2024-07-17T16:15:22Z"
publishDate = "2026-07-17T16:15:22Z"
slug = "ai-spam-filters-bypassed-text-salting-llm-email-security"
description = "Old-school text salting techniques are bypassing LLM-powered spam filters. Here's what cloud security architects need to know."
categories = ["general"]
tags = ["email-security", "ai-security", "llm", "spam-filtering", "evasion", "defence-evasion", "social-engineering"]
severity = "Medium"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/17/ai-spam-filters-are-getting-suckered-by-old-school-text-salting/5274434"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/17/ai-spam-filters-are-getting-suckered-by-old-school-text-salting/5274434)

---

Researchers have found that classic email obfuscation techniques — such as inserting invisible or random characters into spam messages (known as text salting) — can fool modern AI-powered spam filters built on large language models. These decades-old tricks, previously defeated by traditional rule-based filters, appear to bypass the pattern-recognition approach used by LLM-based systems. This matters because organisations adopting AI-driven email security tools may have inadvertently reintroduced a vulnerability that was considered solved.


> **Security Architect's Take:** Avoid relying solely on LLM-based email filtering; ensure your email security stack retains traditional rule-based and heuristic layers alongside AI components. Review your vendor's published test methodology to confirm they account for text-salting and similar obfuscation techniques before committing to AI-first filtering solutions.


**Original advisory:** [AI spam filters are getting suckered by old-school text salting](https://www.theregister.com/security/2026/07/17/ai-spam-filters-are-getting-suckered-by-old-school-text-salting/5274434)
