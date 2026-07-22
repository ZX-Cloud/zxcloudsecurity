+++
title = "AWS Kiro Prompt Injection Flaw Enables RCE"
date = "2025-07-21T16:06:12Z"
publishDate = "2026-07-21T16:06:12Z"
slug = "aws-kiro-prompt-injection-rce-agentic-ide"
description = "A prompt injection flaw in AWS Kiro let poisoned web pages rewrite config files and execute code on developer machines. AWS has patched the issue."
categories = ["general"]
tags = ["aws", "kiro", "prompt-injection", "remote-code-execution", "agentic-ai", "developer-tools", "supply-chain"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/aws-kiro-flaw-let-poisoned-web-page.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/aws-kiro-flaw-let-poisoned-web-page.html)

---

A prompt injection vulnerability in AWS Kiro, an agentic AI coding IDE, allowed a malicious web page to manipulate the tool into rewriting its own configuration file and executing arbitrary code on a developer's machine. The attack required no user interaction beyond asking Kiro to summarise a page, and existing approval mechanisms provided no protection. AWS has patched the flaw, though no CVE has been assigned.


> **Security Architect's Take:** Audit your developer tooling policies to restrict or prohibit agentic AI IDE features — particularly those that fetch and process external web content — until tools have demonstrably robust sandboxing and prompt injection mitigations. Treat AI coding assistants as high-risk endpoints with access to source code, credentials, and local execution, and apply the same scrutiny you would to any privileged developer workstation.


**Original advisory:** [AWS Kiro Flaw Let a Poisoned Web Page Rewrite Its Config and Run Code](https://thehackernews.com/2026/07/aws-kiro-flaw-let-poisoned-web-page.html)
