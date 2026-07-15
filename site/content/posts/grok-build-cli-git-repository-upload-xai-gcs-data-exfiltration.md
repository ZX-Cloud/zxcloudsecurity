+++
title = "Grok Build CLI Leaked Full Git Repos to xAI GCS Bucket"
date = "2025-07-14T09:02:48Z"
publishDate = "2026-07-14T09:02:48Z"
slug = "grok-build-cli-git-repository-upload-xai-gcs-data-exfiltration"
description = "xAI's Grok Build CLI uploaded entire Git repositories to a Google Cloud Storage bucket, exposing source code and commit history beyond intended scope."
categories = ["general"]
tags = ["gcp", "xai", "grok-build", "google-cloud-storage", "ai-coding-tools", "data-exfiltration", "supply-chain", "secret-exposure"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/grok-build-uploads-entire-git.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/grok-build-uploads-entire-git.html)

---

xAI's Grok Build CLI tool (version 0.2.93) was found to be uploading entire Git repositories — including full commit history — to an xAI-controlled Google Cloud Storage bucket, rather than only the specific files required for a given coding task. A researcher intercepted these uploads and was able to retrieve file contents that the agent had been explicitly instructed not to access, raising serious concerns about data exfiltration and instruction-following failures. This behaviour means any developer using Grok Build on a codebase could have inadvertently exposed proprietary source code, credentials, and sensitive history to xAI's infrastructure.


> **Security Architect's Take:** Immediately prohibit use of Grok Build (and similar AI coding CLI tools) on any codebase containing sensitive data, secrets, or proprietary code until xAI issues a verified fix and publishes a clear data handling policy. Review your developer workstation policies to ensure AI coding assistants are subject to egress monitoring and that pre-commit hooks or secret scanning are in place to limit the blast radius of any unintended uploads.


**Original advisory:** [Grok Build Uploaded Entire Git Repositories to xAI Storage, Not Just Files It Read](https://thehackernews.com/2026/07/grok-build-uploads-entire-git.html)
