+++
title = "Flock Cameras Misused by Police for Stalking"
date = "2024-06-16T11:03:31Z"
publishDate = "2026-06-16T11:03:31Z"
slug = "flock-camera-alpr-police-stalking-insider-abuse"
description = "Officers are exploiting Flock ALPR surveillance systems to stalk individuals. Learn what this means for access controls on third-party surveillance platfor"
categories = ["general"]
tags = ["physical-surveillance", "alpr", "insider-threat", "data-misuse", "access-control", "privacy", "audit-logging"]
severity = "Medium"
source = "Schneier on Security"
source_url = "https://www.schneier.com/blog/archives/2026/06/flock-cameras-are-being-used-for-stalking.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [Schneier on Security](https://www.schneier.com/blog/archives/2026/06/flock-cameras-are-being-used-for-stalking.html)

---

Law enforcement officers in the United States have been found abusing Flock Safety's automated licence plate recognition (ALPR) camera network to stalk individuals, with over a dozen cases recorded nationally. Flock cameras are widely deployed by police departments and private communities, making insider misuse a significant concern. The pattern highlights how privileged access to surveillance infrastructure can be weaponised for personal misconduct.


> **Security Architect's Take:** If your organisation integrates with third-party physical surveillance or data-sharing platforms such as Flock, audit who holds query access and ensure all lookups are logged, attributed, and subject to anomaly detection — excessive or off-hours searches by a single user should trigger alerts, mirroring the least-privilege and monitoring controls you would apply to any sensitive cloud data store.


**Original advisory:** [Flock Cameras Are Being Used for Stalking](https://www.schneier.com/blog/archives/2026/06/flock-cameras-are-being-used-for-stalking.html)
