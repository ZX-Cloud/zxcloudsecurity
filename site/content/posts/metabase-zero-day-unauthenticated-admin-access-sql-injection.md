+++
title = "Metabase Zero-Day: Unauth Admin Access Exploited"
date = "2026-08-08T06:58:31Z"
publishDate = "2026-08-08T06:58:31Z"
slug = "metabase-zero-day-unauthenticated-admin-access-sql-injection"
description = "A CVSS 10.0 zero-day in Metabase allows unauthenticated attackers to inject SQL and gain admin access. Actively exploited — patch immediately."
categories = ["general"]
tags = ["metabase", "zero-day", "sql-injection", "unauthenticated-access", "privilege-escalation", "business-intelligence", "remote-code-execution", "active-exploitation"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/metabase-zero-day-exploited-in-wild.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/metabase-zero-day-exploited-in-wild.html)

---

A critical zero-day vulnerability in Metabase, a widely used business intelligence and data visualisation tool, is being actively exploited in the wild. The flaw carries a maximum CVSS score of 10.0 and allows unauthenticated attackers to inject arbitrary SQL into the Metabase database, potentially granting full administrative access. Because no CVE identifier has been assigned yet and exploitation is already occurring, organisations running Metabase face immediate risk.


> **Security Architect's Take:** Immediately audit your environment for any internet-exposed Metabase instances and apply the vendor's patch or mitigation guidance without delay. If patching is not immediately possible, restrict network access to Metabase to trusted IP ranges only and review database activity logs for signs of unauthorised SQL execution.


**Original advisory:** [Metabase Zero-Day Exploited in Wild Allows Admin Access Without Authentication](https://thehackernews.com/2026/08/metabase-zero-day-exploited-in-wild.html)
