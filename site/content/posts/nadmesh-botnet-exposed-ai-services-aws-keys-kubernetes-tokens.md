+++
title = "NadMesh Botnet Targets Exposed AI Services for AWS Keys"
date = "2025-07-17T17:12:23Z"
publishDate = "2026-07-17T17:12:23Z"
slug = "nadmesh-botnet-exposed-ai-services-aws-keys-kubernetes-tokens"
description = "The NadMesh botnet is scanning for exposed AI tools like Ollama and ComfyUI to steal AWS keys and Kubernetes tokens. Here's what architects need to know."
categories = ["general"]
tags = ["aws", "kubernetes", "credential-theft", "botnet", "ollama", "comfyui", "exposed-services", "cloud-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-nadmesh-botnet-hunts-exposed-ai.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-nadmesh-botnet-hunts-exposed-ai.html)

---

A newly discovered Go-based botnet called NadMesh is actively scanning the internet for exposed AI services — including ComfyUI, Ollama, n8n, and Gradio — to harvest AWS keys and Kubernetes tokens. The botnet's own operator dashboard reportedly counts over 3,800 unique AWS keys already compromised. This targets a common blind spot: AI tooling stood up quickly by development and ML teams without adequate network controls.


> **Security Architect's Take:** Audit your organisation's exposure of AI service endpoints via Shodan or similar tooling immediately, and enforce network-level controls (VPC-only access, authenticated reverse proxies) on any AI workbench or workflow tool. Rotate any AWS credentials and Kubernetes service account tokens associated with environments running ComfyUI, Ollama, n8n, Open WebUI, Langflow, or Gradio as a precautionary measure.


**Original advisory:** [New NadMesh Botnet Hunts Exposed AI Services for Cloud Keys and Kubernetes Tokens](https://thehackernews.com/2026/07/new-nadmesh-botnet-hunts-exposed-ai.html)
