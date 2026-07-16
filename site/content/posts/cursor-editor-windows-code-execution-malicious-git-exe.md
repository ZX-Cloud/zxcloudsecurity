+++
title = "Cursor Editor Flaw: Malicious git.exe Runs on Open"
date = "2025-07-15T10:55:22Z"
publishDate = "2026-07-15T10:55:22Z"
slug = "cursor-editor-windows-code-execution-malicious-git-exe"
description = "A Cursor AI editor flaw on Windows silently executes a malicious git.exe from a repo root, exposing SSH keys and cloud tokens with no user prompt."
categories = ["general"]
tags = ["cursor", "windows", "code-execution", "supply-chain", "developer-tools", "credential-theft", "ide-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/cursor-flaw-lets-malicious-cloned.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/cursor-flaw-lets-malicious-cloned.html)

---

A vulnerability in the Cursor AI code editor on Windows allows a malicious file named git.exe placed in a project root to execute automatically when the repository is opened, with no user prompt or warning. The binary runs with the victim's full privileges, giving an attacker access to source code, SSH keys, and cloud credentials. The execution persists for as long as the project remains open.


> **Security Architect's Take:** Enforce policies that prevent developers from opening unvetted or externally cloned repositories in Cursor on Windows until a patch is confirmed and applied; consider adding detection rules for unexpected git.exe binaries in repository root directories, and audit CI/CD pipelines and developer workstations for signs of credential compromise if Cursor has been in use.


**Original advisory:** [Cursor Flaw Lets Malicious Cloned Repositories Trigger Windows Code Execution](https://thehackernews.com/2026/07/cursor-flaw-lets-malicious-cloned.html)
