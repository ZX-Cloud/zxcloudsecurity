+++
title = "WP-SHELLSTORM: 1.4M WordPress Sites Targeted"
date = "2025-07-10T11:30:02Z"
publishDate = "2026-07-10T11:30:02Z"
slug = "wp-shellstorm-backdoor-wordpress-mass-compromise-campaign"
description = "The WP-SHELLSTORM campaign targeted 1.4 million WordPress sites. An exposed hacker server revealed tools, logs, and backdoor techniques used at scale."
categories = ["general"]
tags = ["wordpress", "web-application-security", "backdoor", "malware", "mass-exploitation", "threat-intelligence", "cms-security", "opsec-failure"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/exposed-hacker-server-reveals-wp.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/exposed-hacker-server-reveals-wp.html)

---

A cybercrime group accidentally left their attack infrastructure publicly accessible for three weeks, exposing their tools, logs, and a target list of over 1.4 million WordPress sites. Researchers were able to observe the full mechanics of a mass WordPress backdooring campaign, tracked as WP-SHELLSTORM. While the number of successfully compromised sites is lower than the target list, the exposure reveals the industrial scale at which these operations are conducted.


> **Security Architect's Take:** If your organisation hosts WordPress sites on cloud infrastructure, audit for the WP-SHELLSTORM indicators of compromise immediately and review Web Application Firewall rules to block known malicious plugin or theme upload patterns. Ensure WordPress instances are covered by file integrity monitoring and that admin interfaces are not publicly exposed without MFA.


**Original advisory:** [Exposed Hacker Server Reveals WP-SHELLSTORM Backdooring Thousands of WordPress Sites](https://thehackernews.com/2026/07/exposed-hacker-server-reveals-wp.html)
