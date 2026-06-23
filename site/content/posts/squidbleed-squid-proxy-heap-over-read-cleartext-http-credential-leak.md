+++
title = "Squidbleed: 29-Year-Old Squid Proxy Bug Leaks HTTP Credentia"
date = "2025-06-22T14:29:46Z"
publishDate = "2026-06-22T14:29:46Z"
slug = "squidbleed-squid-proxy-heap-over-read-cleartext-http-credential-leak"
description = "The Squidbleed vulnerability in Squid Proxy exposes cleartext HTTP requests, credentials, and session tokens to other proxy users. Learn the security impac"
categories = ["general"]
tags = ["squid-proxy", "squidbleed", "heap-over-read", "credential-leak", "forward-proxy", "information-disclosure", "network-security", "web-proxy"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/29-year-old-squid-proxy-bug-squidbleed.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/29-year-old-squid-proxy-bug-squidbleed.html)

---

A 29-year-old heap over-read vulnerability in the Squid web proxy, dubbed 'Squidbleed', allows any user already permitted to send traffic through a shared proxy to read another user's cleartext HTTP requests, including credentials and session tokens. The flaw originates from a 1997 FTP-parsing change and remains exploitable in Squid's default configuration today. Exposure is broad given Squid's widespread use as a forward proxy in enterprise and cloud environments.


> **Security Architect's Take:** Audit all environments running Squid as a shared forward proxy — particularly where multiple tenants or workloads share the same proxy instance — and apply vendor patches or mitigations immediately; if no patch is yet available, consider restricting Squid to single-tenant deployments or replacing it with an alternative until a fix is confirmed.


**Original advisory:** [29-Year-Old Squid Proxy Bug 'Squidbleed' Can Leak Cleartext HTTP Requests](https://thehackernews.com/2026/06/29-year-old-squid-proxy-bug-squidbleed.html)
