+++
title = "Apple iCloud Private Relay IP Leak via WebKit Bypass"
date = "2024-08-06T11:33:08Z"
publishDate = "2026-08-06T11:33:08Z"
slug = "apple-icloud-private-relay-ip-leak-webkit-proxy-bypass"
description = "A WebKit proxy bypass flaw exposes real IP addresses of iCloud Private Relay users, undermining Apple's dual-hop privacy architecture on iOS and macOS."
categories = ["general"]
tags = ["apple", "icloud-private-relay", "webkit", "ip-leak", "privacy", "proxy-bypass", "ios", "network-security"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/webkit-proxy-bypasses-can-expose-real.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/webkit-proxy-bypasses-can-expose-real.html)

---

A security flaw in Apple's iCloud Private Relay allows a user's real IP address to be exposed through WebKit proxy bypass techniques, undermining the privacy guarantees of the service. iCloud Private Relay, available since iOS 15, is designed to anonymise Safari traffic by routing it through two separate relay hops so no single party can identify the user's origin. This bypass defeats that protection, potentially allowing websites or threat actors to correlate user identities and locations.


> **Security Architect's Take:** Organisations that rely on iCloud Private Relay as a privacy control for managed Apple devices should treat it as compromised until Apple issues a patch — advise users to consider alternative VPN solutions in the interim and review any zero-trust or network access policies that assume IP anonymisation from this feature.


**Original advisory:** [Apple iCloud Private Relay Can Expose Real IPs Through WebKit Proxy Bypasses](https://thehackernews.com/2026/08/webkit-proxy-bypasses-can-expose-real.html)
