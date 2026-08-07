+++
title = "Snowflake Extortion: Canadian Hacker Pleads Guilty"
date = "2026-08-06T17:00:56Z"
publishDate = "2026-08-06T17:00:56Z"
slug = "snowflake-extortion-canadian-hacker-connor-moucka-guilty-plea"
description = "Connor Moucka pleads guilty to hacking 165+ Snowflake customers. Learn what cloud architects must do to prevent credential-based data breaches."
categories = ["general"]
tags = ["snowflake", "data-breach", "extortion", "credential-theft", "mfa", "cloud-security", "insider-threat", "access-controls"]
severity = "Critical"
source = "Krebs on Security"
source_url = "https://krebsonsecurity.com/2026/08/canadian-man-pleads-guilty-in-snowflake-extortions/"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [Krebs on Security](https://krebsonsecurity.com/2026/08/canadian-man-pleads-guilty-in-snowflake-extortions/)

---

Connor Riley Moucka, a 26-year-old Canadian, has pleaded guilty to hacking and extorting over 165 organisations that used the Snowflake cloud data platform, in one of 2024's most damaging cybercrime campaigns. The attacks exploited poor credential hygiene — specifically the absence of multi-factor authentication on Snowflake accounts — allowing mass data theft including over 100 million AT&T customer records. The case underscores the severe real-world consequences of inadequate access controls on cloud data warehousing platforms.


> **Security Architect's Take:** Audit all Snowflake (and wider SaaS data platform) accounts immediately to enforce MFA and review whether single-factor credentials are used anywhere in your data pipeline; also assess whether network policy objects in Snowflake restrict access to known IP ranges, as both controls would have significantly limited the blast radius of this campaign.


**Original advisory:** [Canadian Man Pleads Guilty in Snowflake Extortions](https://krebsonsecurity.com/2026/08/canadian-man-pleads-guilty-in-snowflake-extortions/)
