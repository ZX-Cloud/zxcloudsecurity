+++
title = "Amazon Q Flaw: Git Repos Could Steal AWS Cloud Creds"
date = "2025-06-26T15:34:00Z"
publishDate = "2026-06-26T15:34:00Z"
slug = "amazon-q-flaw-git-repo-code-execution-cloud-credential-theft"
description = "A flaw in Amazon Q allowed malicious Git repos to execute code and steal cloud credentials. Learn what cloud security architects should do now."
categories = ["general"]
tags = ["aws", "amazon-q", "ai-coding-assistant", "credential-theft", "supply-chain", "code-execution", "developer-security", "prompt-injection"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/cyber-crime/2026/06/26/amazon-q-flaw-let-booby-trapped-git-repos-execute-code-swipe-cloud-creds/5263202"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/cyber-crime/2026/06/26/amazon-q-flaw-let-booby-trapped-git-repos-execute-code-swipe-cloud-creds/5263202)

---

A vulnerability in Amazon Q, AWS's AI coding assistant, allowed malicious Git repositories to execute arbitrary code and steal cloud credentials on a developer's machine. Attackers could craft a booby-trapped repository that, when opened with Amazon Q, would trigger commands from project configuration files without explicit user consent. Researchers highlight this as a broader pattern affecting many AI coding assistants that blindly execute instructions from project-level config files.


> **Security Architect's Take:** Audit which AI coding assistants your engineering teams use and review their policies around executing project-level configuration files — restrict or disable automatic command execution from untrusted repositories. Treat AI assistant integrations as a new supply-chain attack surface and ensure developer workstations follow least-privilege principles for cloud credential access.


**Original advisory:** [Amazon Q flaw let booby-trapped Git repos execute code, swipe cloud creds](https://www.theregister.com/cyber-crime/2026/06/26/amazon-q-flaw-let-booby-trapped-git-repos-execute-code-swipe-cloud-creds/5263202)
