+++
title = "AWS ARC Adds Aurora & Neptune Failover Automation"
date = "2026-06-03T17:44:00Z"
slug = "aws-arc-region-switch-aurora-scaling-neptune-global-database-failover"
description = "AWS ARC Region switch gains automated Aurora scaling and Neptune global database failover blocks, reducing manual steps and recovery time in multi-region o"
categories = ["aws"]
tags = ["aws", "aurora", "neptune", "arc", "disaster-recovery", "multi-region", "resilience", "rto"]
severity = "Low"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/06/region-switch-aurora-scaling-neptune-failover/"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/region-switch-aurora-scaling-neptune-failover/)

---

AWS has added three new execution blocks to Amazon Application Recovery Controller (ARC) Region switch, automating database scaling and failover for Aurora (serverless and provisioned) and Neptune global databases during multi-region failover events. Previously, engineers had to manually right-size secondary clusters under incident pressure, adding precious minutes to recovery time. These new blocks remove that manual step, reducing recovery time and human error during outages.


> **Architect's Take:** Review your existing ARC Region switch runbooks and integrate the new Aurora and Neptune execution blocks to eliminate manual scaling steps from your recovery plans. This is particularly important if you run active-passive Aurora global database configurations with scaled-down secondaries, as automating right-sizing directly reduces your practical RTO and the risk of operator error during a live incident.


**Original advisory:** [ARC Region switch adds Amazon Aurora scaling and Amazon Neptune global database failover](https://aws.amazon.com/about-aws/whats-new/2026/06/region-switch-aurora-scaling-neptune-failover/)
