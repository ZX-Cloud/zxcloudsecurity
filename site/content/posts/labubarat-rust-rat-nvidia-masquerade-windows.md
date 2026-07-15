+++
title = "LabubaRAT: Rust RAT Disguised as NVIDIA Software"
date = "2025-07-14T16:52:37Z"
publishDate = "2026-07-14T16:52:37Z"
slug = "labubarat-rust-rat-nvidia-masquerade-windows"
description = "LabubaRAT is a Rust-based RAT that masquerades as NVIDIA software to gain persistent access to Windows hosts. Here's what security teams need to know."
categories = ["general"]
tags = ["windows", "remote-access-trojan", "malware", "rust", "nvidia", "endpoint-security", "defence-evasion", "persistence"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/labubarat-masquerades-as-nvidia.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/labubarat-masquerades-as-nvidia.html)

---

LabubaRAT is a newly discovered remote access trojan written in Rust that disguises itself as NVIDIA software to avoid detection on Windows systems. Once installed, it establishes a persistent foothold allowing attackers to profile the host and carry out hands-on activity. Its use of a legitimate-looking software identity makes it particularly effective at evading endpoint defences.


> **Security Architect's Take:** Enforce application allowlisting and code-signing policies to block unsigned or unexpected executables masquerading as GPU vendor software, particularly on cloud-connected Windows workloads and developer endpoints. Review EDR telemetry for Rust-compiled binaries impersonating NVIDIA processes and consider restricting outbound RAT command-and-control channels at the network perimeter.


**Original advisory:** [LabubaRAT Masquerades as NVIDIA Software to Control Windows Hosts](https://thehackernews.com/2026/07/labubarat-masquerades-as-nvidia.html)
