+++
title = "Claude Cowork VM Sandbox Escape Hits 500k Mac Users"
date = "2025-07-23T13:27:59Z"
publishDate = "2026-07-23T13:27:59Z"
slug = "claude-cowork-sandbox-escape-macos-vm-file-access"
description = "A sandbox escape flaw in Anthropic's Claude Cowork lets an AI agent break out of its Linux VM and access any file on the host macOS system, affecting ~500,"
categories = ["general"]
tags = ["anthropic", "claude", "ai-agents", "sandbox-escape", "macos", "virtual-machine", "lateral-movement", "ai-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/claude-cowork-flaw-could-let-ai-agent.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/claude-cowork-flaw-could-let-ai-agent.html)

---

A sandbox escape vulnerability has been discovered in Anthropic's Claude Cowork desktop application, allowing an AI agent to break out of its Linux virtual machine and read or write files anywhere on the host macOS system. The flaw affects approximately 500,000 macOS users and means a compromised or manipulated AI agent could access sensitive files far beyond its intended boundaries. This is significant because it demonstrates that AI agent sandboxing is not yet a reliable security boundary.


> **Security Architect's Take:** Organisations permitting use of Claude Cowork or similar AI agent desktop tools should audit which local file systems and sensitive directories are accessible from the host machine, and consider restricting such tools to managed devices with endpoint DLP controls until a patch is confirmed. Review your AI tool approval and risk assessment processes to explicitly include sandbox integrity as a evaluation criterion.


**Original advisory:** [Claude Cowork Flaw Could Let AI Agent Escape Its VM and Access Mac Files](https://thehackernews.com/2026/07/claude-cowork-flaw-could-let-ai-agent.html)
