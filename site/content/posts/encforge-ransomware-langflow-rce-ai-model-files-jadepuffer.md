+++
title = "ENCFORGE Ransomware Targets AI Models via Langflow RCE"
date = "2025-07-21T07:34:32Z"
publishDate = "2026-07-21T07:34:32Z"
slug = "encforge-ransomware-langflow-rce-ai-model-files-jadepuffer"
description = "JADEPUFFER deploys ENCFORGE ransomware via Langflow RCE to encrypt AI model weights, vector indexes, and training datasets. Learn the risks and mitigations"
categories = ["general"]
tags = ["ransomware", "langflow", "rce", "ai-security", "jadepuffer", "model-weights", "data-protection", "supply-chain"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-encforge-ransomware-targets-ai.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-encforge-ransomware-targets-ai.html)

---

A threat actor tracked as JADEPUFFER has exploited a remote code execution vulnerability in Langflow, an open-source AI workflow platform, to deploy ENCFORGE — a new Go-based ransomware specifically designed to encrypt AI infrastructure assets such as model weights, vector indexes, and training datasets. This marks a notable evolution in ransomware targeting, moving beyond traditional data and business systems to attack AI pipeline components directly. The incident signals that AI development infrastructure is increasingly being treated as high-value by ransomware operators.


> **Security Architect's Take:** Audit any internet-exposed Langflow instances immediately and apply available patches or restrict access via network controls; additionally, ensure AI model artefacts, vector stores, and training datasets are covered by your backup and immutable storage strategy, as these are now confirmed ransomware targets.


**Original advisory:** [New ENCFORGE Ransomware Targets AI Model Files in Langflow RCE Attack](https://thehackernews.com/2026/07/new-encforge-ransomware-targets-ai.html)
