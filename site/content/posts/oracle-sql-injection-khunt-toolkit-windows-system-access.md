+++
title = "Oracle SQL Injection Leads to SYSTEM Access via khunt"
date = "2026-08-06T09:19:23Z"
publishDate = "2026-08-06T09:19:23Z"
slug = "oracle-sql-injection-khunt-toolkit-windows-system-access"
description = "Attackers used SQL injection to deploy the khunt toolkit inside Oracle, compiling Java in-database to execute OS commands and gain Windows SYSTEM privilege"
categories = ["general"]
tags = ["oracle", "sql-injection", "privilege-escalation", "fileless-malware", "post-exploitation", "windows", "database-security", "khunt"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/attackers-compile-khunt-inside-oracle.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/attackers-compile-khunt-inside-oracle.html)

---

Attackers exploited a SQL injection vulnerability in a public-facing web application to gain access to an Oracle database, then used a post-exploitation toolkit called 'khunt' to execute commands directly inside the database engine by compiling Java source code into stored schema objects — no executable written to disk. This technique effectively turns the Oracle database process itself into a command execution environment, bypassing many traditional endpoint detection controls. The attack ultimately resulted in SYSTEM-level access on the underlying Windows host, dramatically escalating the blast radius beyond the database.


> **Security Architect's Take:** Audit Oracle database instances for unauthorised Java stored procedures and schema objects immediately, and enforce the principle of least privilege on database service accounts to prevent OS-level command execution via DBMS_JAVA or UTL_FILE. Ensure public-facing web applications undergo regular SQL injection testing and consider deploying a WAF with virtualised patching as a compensating control while remediation is in progress.


**Original advisory:** [Attackers Compile khunt Inside Oracle to Turn SQL Injection Into Windows SYSTEM Access](https://thehackernews.com/2026/08/attackers-compile-khunt-inside-oracle.html)
