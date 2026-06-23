+++
title = "OXLOADER Malware Uses Google Ads to Drop CastleStealer"
date = "2025-06-22T13:20:12Z"
publishDate = "2026-06-22T13:20:12Z"
slug = "oxloader-malvertising-google-ads-castlestealer-infostealer"
description = "Elastic Security Labs exposes OXLOADER, a new malware loader using malicious Google Ads to deliver the CastleStealer infostealer. Learn what security teams"
categories = ["general"]
tags = ["malvertising", "infostealer", "malware-loader", "google-ads", "oxloader", "castlestealer", "initial-access", "endpoint-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/new-oxloader-loader-uses-malicious.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/new-oxloader-loader-uses-malicious.html)

---

A newly identified malware loader called OXLOADER is being distributed via malicious Google Ads, ultimately delivering an information-stealing payload known as CastleStealer. The campaign is attributed to a likely Russian-speaking, financially motivated threat actor. This matters because malvertising via Google Ads is a highly effective initial access vector that bypasses traditional perimeter defences by exploiting trusted ad infrastructure.


> **Security Architect's Take:** Review and enforce DNS filtering and web proxy policies to block known malvertising domains, and consider deploying endpoint detection rules for OXLOADER behavioural indicators published by Elastic Security Labs. Ensure browser isolation or ad-blocking controls are in place for corporate endpoints, particularly for users with access to sensitive cloud credentials.


**Original advisory:** [New OXLOADER Loader Uses Malicious Google Ads to Deliver CastleStealer](https://thehackernews.com/2026/06/new-oxloader-loader-uses-malicious.html)
