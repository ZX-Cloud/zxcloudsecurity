+++
title = "ModHeader Removed: Hidden Data Collector in 1.6M-Install Ext"
date = "2025-07-13T17:17:24Z"
publishDate = "2026-07-13T17:17:24Z"
slug = "modheader-extension-removed-hidden-browsing-history-collector-chrome-edge"
description = "Google and Microsoft pulled ModHeader after a dormant browsing-history collector was found in the extension. Learn what cloud security teams should do now."
categories = ["general"]
tags = ["browser-extension", "supply-chain", "chrome", "edge", "data-collection", "insider-threat", "endpoint-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/google-and-microsoft-pull-modheader.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/google-and-microsoft-pull-modheader.html)

---

Google and Microsoft have removed the ModHeader browser extension — which had 1.6 million installs across Chrome and Edge — after researchers discovered a hidden browsing-history collection mechanism embedded in the official store release. The collector was dormant, controlled by an empty allow-list that prevented it from activating, and there is currently no evidence that any user data was ever harvested or transmitted. Despite the lack of confirmed exploitation, the presence of undisclosed data-collection code in a widely trusted developer tool raises significant supply-chain and insider-threat concerns.


> **Security Architect's Take:** Audit your organisation's approved browser extension inventory and remove or block ModHeader immediately via endpoint management or browser policy. More broadly, enforce a vetted allow-list of permitted extensions across managed devices, and consider periodic automated scans of installed extensions against known-bad or recently pulled packages — dormant payloads like this can be activated remotely at any time.


**Original advisory:** [Google and Microsoft Pull ModHeader With 1.6 Million Installs After Dormant Collector Found](https://thehackernews.com/2026/07/google-and-microsoft-pull-modheader.html)
