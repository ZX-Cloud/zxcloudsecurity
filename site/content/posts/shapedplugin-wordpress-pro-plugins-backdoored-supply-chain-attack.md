+++
title = "ShapedPlugin WordPress Plugins Backdoored in Supply Chain At"
date = "2025-06-22T18:00:48Z"
publishDate = "2026-06-22T18:00:48Z"
slug = "shapedplugin-wordpress-pro-plugins-backdoored-supply-chain-attack"
description = "ShapedPlugin's Pro WordPress plugins were backdoored via a compromised build pipeline. Find out which plugins are affected and what to do now."
categories = ["general"]
tags = ["wordpress", "supply-chain", "backdoor", "plugin-security", "malware", "wordfence", "software-integrity", "third-party-risk"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/shapedplugin-wordpress-pro-plugins.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/shapedplugin-wordpress-pro-plugins.html)

---

Multiple premium WordPress plugins developed by ShapedPlugin were backdoored after attackers compromised the vendor's build and distribution pipeline, injecting malicious code into official licensed updates. Any site running affected Pro plugin versions may have received the backdoor automatically through the standard update mechanism. This is a classic supply chain attack, meaning legitimate, trusted channels were weaponised to distribute malware.


> **Security Architect's Take:** Audit all WordPress installations for ShapedPlugin Pro plugins and treat any recently updated versions as potentially compromised — roll back to known-good versions or remove the plugins entirely until clean releases are confirmed. Review your software supply chain controls more broadly: enforce plugin update staging environments and integrity verification (checksums/signatures) before deploying updates to production WordPress estates.


**Original advisory:** [ShapedPlugin WordPress Pro Plugins Backdoored in Supply Chain Attack](https://thehackernews.com/2026/06/shapedplugin-wordpress-pro-plugins.html)
