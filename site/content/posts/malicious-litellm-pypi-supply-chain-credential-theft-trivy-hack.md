+++
title = "Malicious LiteLLM PyPI Releases Expose 2,100+ Orgs"
date = "2026-08-12T08:04:52Z"
publishDate = "2026-08-12T08:04:52Z"
slug = "malicious-litellm-pypi-supply-chain-credential-theft-trivy-hack"
description = "Two trojanised LiteLLM PyPI packages stole cloud keys, SSH keys and Kubernetes tokens. Over 2,100 organisations may be affected. Find out what to do now."
categories = ["general"]
tags = ["supply-chain", "pypi", "credential-theft", "kubernetes", "litellm", "trivy", "cloud-security", "secrets-management"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/malicious-litellm-releases-tied-to.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/malicious-litellm-releases-tied-to.html)

---

Two malicious versions of the LiteLLM Python package were published to PyPI in March and remained available for approximately 40 minutes before removal. The packages contained credential-stealing code capable of harvesting cloud provider keys, SSH keys, Kubernetes tokens, and database credentials from any system that installed them. Threat intelligence firm CloudSEK has linked the incident to the earlier Trivy scanner compromise and estimates over 2,100 organisations may have been exposed based on a dataset of roughly 434,000 captured files.


> **Security Architect's Take:** Audit your Python environments and CI/CD pipelines for LiteLLM installations from the affected March release window and rotate any cloud credentials, SSH keys, and Kubernetes service account tokens on systems that may have installed the malicious versions. Implement package integrity controls such as pip hash pinning and consider a private package mirror with allow-listing to reduce exposure to future PyPI supply chain attacks.


**Original advisory:** [Malicious LiteLLM Releases Tied to Trivy Hack May Have Exposed 2,100+ Organizations](https://thehackernews.com/2026/08/malicious-litellm-releases-tied-to.html)
