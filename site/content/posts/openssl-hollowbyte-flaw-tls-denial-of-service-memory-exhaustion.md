+++
title = "OpenSSL HollowByte Flaw: DoS via 11-Byte TLS Request"
date = "2025-07-17T20:20:53Z"
publishDate = "2026-07-17T20:20:53Z"
slug = "openssl-hollowbyte-flaw-tls-denial-of-service-memory-exhaustion"
description = "The OpenSSL HollowByte flaw lets attackers exhaust server memory with 11-byte TLS requests. No CVE was issued. Learn what to patch and how to detect exposu"
categories = ["general"]
tags = ["openssl", "tls", "denial-of-service", "memory-exhaustion", "hollowbyte", "okta", "glibc", "supply-chain"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/openssl-hollowbyte-flaw-could-freeze.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/openssl-hollowbyte-flaw-could-freeze.html)

---

A flaw in OpenSSL, dubbed HollowByte by Okta's Red Team, allows an attacker to send an 11-byte TLS request that tricks an unpatched server into reserving up to 131 KB of memory for a message that never arrives. On Linux systems using glibc, that memory is not released until the process restarts, making repeated requests a viable denial-of-service attack. OpenSSL quietly shipped a fix in June 2025 with no CVE, no security advisory, and no changelog reference.


> **Security Architect's Take:** Audit your OpenSSL versions across all TLS-terminating workloads — load balancers, API gateways, and application servers — and ensure you are running the patched release. Given OpenSSL shipped this silently, cross-reference your build dates and package versions rather than relying on advisory feeds, and consider adding memory exhaustion monitoring as a compensating control.


**Original advisory:** [OpenSSL HollowByte Flaw Could Freeze Server Memory with 11-Byte TLS Requests](https://thehackernews.com/2026/07/openssl-hollowbyte-flaw-could-freeze.html)
