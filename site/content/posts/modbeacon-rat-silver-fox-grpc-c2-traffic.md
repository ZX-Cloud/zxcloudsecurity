+++
title = "MODBEACON RAT: Silver Fox Uses gRPC for C2 Traffic"
date = "2025-07-10T13:15:23Z"
publishDate = "2026-07-10T13:15:23Z"
slug = "modbeacon-rat-silver-fox-grpc-c2-traffic"
description = "Silver Fox's MODBEACON RAT uses gRPC streaming to hide C2 traffic. Learn what cloud security architects should do to detect and block this threat."
categories = ["general"]
tags = ["rat", "malware", "grpc", "command-and-control", "silver-fox", "seo-poisoning", "rust-malware", "threat-intelligence"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/new-modbeacon-rat-uses-grpc-streaming.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/new-modbeacon-rat-uses-grpc-streaming.html)

---

A China-linked threat group called Silver Fox has deployed a new Rust-based remote access trojan named MODBEACON, which uses gRPC streaming to disguise its command-and-control traffic as legitimate encrypted communications. The malware is distributed via fake software installers promoted through SEO poisoning. Despite appearing unsophisticated, the group demonstrates significant operational organisation, making detection and attribution more difficult.


> **Security Architect's Take:** Review egress controls and TLS inspection policies to ensure gRPC traffic on port 443 is inspected or allowlisted only for trusted endpoints — MODBEACON exploits the assumption that gRPC traffic is benign. Additionally, enforce software installation controls (e.g. allowlisting) on cloud-connected workstations to block counterfeit installers reaching your estate.


**Original advisory:** [New MODBEACON RAT Uses gRPC Streaming for Encrypted C2 Traffic](https://thehackernews.com/2026/07/new-modbeacon-rat-uses-grpc-streaming.html)
