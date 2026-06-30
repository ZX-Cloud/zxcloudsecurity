+++
title = "Fake Perplexity Chrome Extension Stole Search Data"
date = "2025-06-29T18:40:09Z"
publishDate = "2026-06-29T18:40:09Z"
slug = "malicious-perplexity-chrome-extension-search-interception"
description = "Microsoft uncovered a malicious Chrome extension posing as Perplexity AI that intercepted all searches and address bar input, routing data to attacker serv"
categories = ["general"]
tags = ["chrome-extension", "browser-security", "data-exfiltration", "supply-chain", "credential-harvesting", "endpoint-security", "ai-impersonation"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/malicious-perplexity-chrome-extension.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/malicious-perplexity-chrome-extension.html)

---

A malicious Chrome extension impersonating the AI search tool Perplexity was discovered by Microsoft, silently intercepting all search queries and address bar keystrokes and routing them through an attacker-controlled server. Users believed they were getting normal search results whilst their queries were being exfiltrated. Google has since removed the extension following responsible disclosure, but any users who installed it may have had sensitive searches or URLs captured.


> **Security Architect's Take:** Review your organisation's browser extension management policy and enforce an allowlist via enterprise browser controls (e.g. Chrome Browser Cloud Management or Intune). Audit installed extensions across managed endpoints for any recently installed or unrecognised AI-themed extensions, and consider blocking sideloaded or unvetted extensions as a baseline control.


**Original advisory:** [Malicious Perplexity Chrome Extension Intercepted Searches and Address Bar Input](https://thehackernews.com/2026/06/malicious-perplexity-chrome-extension.html)
