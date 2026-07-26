+++
title = "GitLab RCE PoC: Patch Self-Managed Instances Now"
date = "2026-07-25T10:14:26Z"
publishDate = "2026-07-25T10:14:26Z"
slug = "gitlab-rce-poc-authenticated-user-code-execution-self-managed"
description = "A public RCE exploit for GitLab 18.11.3 lets any authenticated user run commands as git. Self-managed instances must patch immediately."
categories = ["general"]
tags = ["gitlab", "rce", "remote-code-execution", "self-managed", "jupyter-notebook", "heap-leak", "authenticated-exploit", "patch-management"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/researcher-publishes-gitlab-rce-poc.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/researcher-publishes-gitlab-rce-poc.html)

---

A working proof-of-concept exploit has been published for a remote code execution flaw in GitLab, allowing any authenticated user with push access to run arbitrary commands as the 'git' system user on unpatched self-managed instances. The vulnerability is triggered by committing a specially crafted Jupyter notebook and viewing its diff, which leaks heap memory and enables code execution. GitLab patched the flaw on 10 June, but any self-managed instance still running version 18.11.3 without the update is directly at risk.


> **Security Architect's Take:** Prioritise patching all self-managed GitLab instances beyond version 18.11.3 immediately — with a working public PoC now available, exploitation in the wild is a near-term certainty. If patching cannot be done immediately, restrict push access to trusted users only and consider taking the instance offline or behind a VPN until the update is applied.


**Original advisory:** [Researcher Publishes GitLab RCE PoC Letting Authenticated Users Run Commands as Git](https://thehackernews.com/2026/07/researcher-publishes-gitlab-rce-poc.html)
