+++
title = "Google Vertex AI SDK Flaw: Bucket Squatting Attack"
date = "2025-06-16T19:05:41Z"
publishDate = "2026-06-16T19:05:41Z"
slug = "google-vertex-ai-sdk-bucket-squatting-pickle-in-the-middle"
description = "A Vertex AI Python SDK flaw let attackers hijack ML model uploads via predictable GCS bucket names, enabling code execution in Google's serving infrastruct"
categories = ["general"]
tags = ["gcp", "vertex-ai", "google-cloud-storage", "supply-chain", "code-execution", "bucket-squatting", "machine-learning-security", "pickle-deserialization"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/google-vertex-ai-sdk-flaw-let-attackers.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/google-vertex-ai-sdk-flaw-let-attackers.html)

---

A vulnerability in the Google Cloud Vertex AI Python SDK allowed an attacker with no prior access to a victim's project to intercept and replace machine learning model uploads by claiming a predictable Google Cloud Storage bucket name — a technique dubbed 'Pickle in the Middle' by Palo Alto Networks Unit 42. Because ML models are typically serialised using the Python Pickle format, a malicious model could execute arbitrary code within Google's Vertex AI serving infrastructure. No exploitation in the wild has been observed, and the issue was responsibly disclosed via Google's bug bounty programme.


> **Security Architect's Take:** Audit your Vertex AI pipelines to ensure model artefacts are uploaded to explicitly defined, organisation-owned GCS buckets rather than relying on SDK-generated bucket names. Additionally, consider enforcing GCS bucket policies that prevent creation of predictably named buckets by external parties, and restrict Pickle-format model loading in favour of safer serialisation formats where your toolchain permits.


**Original advisory:** [Google Vertex AI SDK Flaw Let Attackers Hijack Model Uploads via Bucket Squatting](https://thehackernews.com/2026/06/google-vertex-ai-sdk-flaw-let-attackers.html)
