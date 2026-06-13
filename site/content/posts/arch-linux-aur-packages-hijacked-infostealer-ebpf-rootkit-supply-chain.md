+++
title = "400+ AUR Packages Hijacked to Drop Infostealer & eBPF Rootki"
date = "2025-06-12T19:33:25Z"
publishDate = "2026-06-12T19:33:25Z"
slug = "arch-linux-aur-packages-hijacked-infostealer-ebpf-rootkit-supply-chain"
description = "Over 400 Arch Linux AUR packages were compromised to deliver a Rust credential stealer and eBPF rootkit, posing a serious supply chain risk to developers a"
categories = ["general"]
tags = ["linux", "supply-chain", "aur", "infostealer", "ebpf", "rootkit", "ci-cd", "credential-theft"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/over-400-arch-linux-aur-packages.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/over-400-arch-linux-aur-packages.html)

---

Attackers compromised over 400 packages in the Arch User Repository (AUR) by rewriting build scripts to install a Rust-based credential stealer on any machine that compiled the affected packages. When executed with root privileges, the malware can also deploy an eBPF rootkit to conceal its presence. This is a significant supply chain attack targeting developers, particularly those building software in Linux-based CI/CD environments.


> **Security Architect's Take:** Audit any CI/CD pipelines or developer workstations using Arch Linux and AUR packages immediately — treat all AUR-sourced builds from this week as potentially compromised. Enforce a policy of never running AUR builds with root privileges, and consider migrating pipeline build environments to distributions with curated, signed package repositories.


**Original advisory:** [Over 400 Arch Linux AUR Packages Hijacked to Deploy Infostealer and eBPF Rootkit](https://thehackernews.com/2026/06/over-400-arch-linux-aur-packages.html)
