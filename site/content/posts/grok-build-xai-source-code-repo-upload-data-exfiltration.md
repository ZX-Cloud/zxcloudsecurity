+++
title = "Grok Build Sent Entire Code Repos to xAI Cloud"
date = "2025-07-14T12:39:03Z"
publishDate = "2026-07-14T12:39:03Z"
slug = "grok-build-xai-source-code-repo-upload-data-exfiltration"
description = "xAI's Grok Build AI coding tool was silently uploading full source code repos to the cloud. Here's what cloud security teams should do now."
categories = ["general"]
tags = ["xai", "grok-build", "data-exfiltration", "ai-coding-tools", "supply-chain", "developer-tools", "dlp", "shadow-it"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/ai-and-ml/2026/07/14/musk-promises-purge-after-grok-build-caught-sending-entire-repos-to-the-cloud/5271123"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/ai-and-ml/2026/07/14/musk-promises-purge-after-grok-build-caught-sending-entire-repos-to-the-cloud/5271123)

---

Grok Build, xAI's AI coding tool, was found to be silently uploading entire source code repositories to the cloud without clear user consent. A researcher confirmed the uploads have since stopped, but disputes that xAI's own privacy directive was the cause of the fix. This raises serious concerns about data exfiltration risks posed by AI-assisted development tools embedded in developer workflows.


> **Security Architect's Take:** Audit any AI coding assistants in use across your engineering teams — review network egress logs for unexpected outbound traffic to xAI or third-party AI endpoints, and enforce DLP policies that flag or block bulk code uploads. Consider restricting Grok Build or similar tools via endpoint controls until xAI provides transparent disclosure of what data is collected and how.


**Original advisory:** [Musk promises purge after Grok Build caught sending entire repos to the cloud](https://www.theregister.com/ai-and-ml/2026/07/14/musk-promises-purge-after-grok-build-caught-sending-entire-repos-to-the-cloud/5271123)
