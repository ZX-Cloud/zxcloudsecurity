+++
title = "GitHub Blocks Pwn Request Attacks in actions/checkout"
date = "2025-06-23T14:22:03Z"
publishDate = "2026-06-23T14:22:03Z"
slug = "github-actions-checkout-blocks-pwn-request-pull-request-target"
description = "GitHub updates actions/checkout to block pwn request attacks exploiting pull_request_target workflows. What cloud security teams need to know."
categories = ["general"]
tags = ["github", "github-actions", "supply-chain", "ci-cd", "pwn-request", "pull-request-target", "secrets-exposure", "pipeline-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/github-updates-actionscheckout-to-block.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/github-updates-actionscheckout-to-block.html)

---

GitHub is updating its widely-used 'actions/checkout' action to block 'pwn request' attacks, where malicious code in pull requests gains full workflow privileges via the 'pull_request_target' trigger. Effective 18 June 2026, the new version introduces safeguards to prevent untrusted code from executing in privileged workflow contexts. This matters because successful exploitation allows attackers to exfiltrate secrets, tamper with pipelines, or compromise downstream software supply chains.


> **Security Architect's Take:** Audit all workflows using 'pull_request_target' to ensure untrusted code is never checked out into a privileged context, and pin 'actions/checkout' to the updated version as soon as it is released. Where 'pull_request_target' is genuinely required, enforce explicit trust boundaries by separating secret-access steps from any code sourced from forks.


**Original advisory:** [GitHub Updates actions/checkout to Block Common Pwn Request Attack Patterns](https://thehackernews.com/2026/06/github-updates-actionscheckout-to-block.html)
