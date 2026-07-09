+++
title = "GitHub Copilot Jailbreak via Code-Level Prompts"
date = "2024-07-08T19:19:35Z"
publishDate = "2026-07-08T19:19:35Z"
slug = "github-copilot-jailbreak-code-level-prompt-bypass"
description = "Researchers bypass GitHub Copilot safety filters using code-embedded prompts. Learn what this means for cloud security teams relying on AI guardrails."
categories = ["general"]
tags = ["github", "copilot", "ai-security", "jailbreak", "prompt-injection", "ai-guardrails", "supply-chain", "developer-tools"]
severity = "Medium"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/08/github-copilot-sorry-dave-i-cant-do-that-harmful-thing-unless-you-ask-me-in-code/5268654"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/08/github-copilot-sorry-dave-i-cant-do-that-harmful-thing-unless-you-ask-me-in-code/5268654)

---

Researchers have demonstrated a jailbreak technique against GitHub Copilot that bypasses its safety guardrails by embedding harmful instructions within code rather than natural language prompts. The flaw operates at the workflow level, meaning Copilot's content filters can be circumvented by framing requests programmatically. This matters because organisations relying on Copilot's built-in safeguards to prevent misuse may have a false sense of security.


> **Security Architect's Take:** Review your AI acceptable-use policies and do not treat Copilot's built-in content filters as a sufficient control boundary — consider supplementing with code review tooling, output scanning, and developer awareness training around AI jailbreak risks.


**Original advisory:** [GitHub Copilot: Sorry Dave, I can't do that harmful thing - unless you ask me in code](https://www.theregister.com/security/2026/07/08/github-copilot-sorry-dave-i-cant-do-that-harmful-thing-unless-you-ask-me-in-code/5268654)
