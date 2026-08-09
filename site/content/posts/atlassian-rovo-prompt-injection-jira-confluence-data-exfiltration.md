+++
title = "Atlassian Rovo Prompt Injection Leaks Jira & Confluence Data"
date = "2025-08-08T08:54:50Z"
publishDate = "2026-08-08T08:54:50Z"
slug = "atlassian-rovo-prompt-injection-jira-confluence-data-exfiltration"
description = "Atlassian Rovo AI assistant is vulnerable to prompt injection attacks that can exfiltrate Jira and Confluence data to attacker-controlled servers. One rout"
categories = ["general"]
tags = ["atlassian", "rovo", "jira", "confluence", "prompt-injection", "ai-security", "data-exfiltration", "llm-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/atlassian-rovo-can-be-tricked-into.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/atlassian-rovo-can-be-tricked-into.html)

---

Atlassian's AI assistant Rovo can be manipulated via prompt injection attacks to exfiltrate Jira and Confluence data accessible to a signed-in user, sending it to an attacker-controlled server. Two independent security firms discovered separate attack routes; at least one remains unpatched. This is a significant risk for organisations using Rovo across sensitive project management and documentation platforms.


> **Security Architect's Take:** Review and restrict Rovo's access to sensitive Jira projects and Confluence spaces immediately, and audit what external content Rovo is permitted to read. Consider disabling Rovo in high-sensitivity environments until Atlassian confirms all identified attack vectors are fully remediated.


**Original advisory:** [Atlassian Rovo Can Be Tricked Into Sending Jira and Confluence Data to Attackers](https://thehackernews.com/2026/08/atlassian-rovo-can-be-tricked-into.html)
