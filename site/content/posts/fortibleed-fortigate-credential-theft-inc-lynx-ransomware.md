+++
title = "FortiBleed Linked to INC & Lynx Ransomware Groups"
date = "2026-07-02T08:00:49Z"
publishDate = "2026-07-02T08:00:49Z"
slug = "fortibleed-fortigate-credential-theft-inc-lynx-ransomware"
description = "The FortiBleed FortiGate credential theft campaign is directly tied to INC and Lynx ransomware operations, enabling targeted follow-on intrusions."
categories = ["general"]
tags = ["fortinet", "fortigate", "fortibleed", "ransomware", "credential-theft", "inc-ransomware", "lynx-ransomware", "vpn-security"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/fortibleed-credential-theft-linked-to.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/fortibleed-credential-theft-linked-to.html)

---

A large-scale credential theft campaign targeting Fortinet FortiGate devices, dubbed 'FortiBleed', has been directly linked to the INC and Lynx ransomware groups. Stolen credentials are being harvested and fed into ransomware deployment pipelines, with one operator confirmed to be managing negotiation panels for both groups simultaneously. This confirms FortiBleed is not opportunistic scanning but a structured, financially motivated operation with ransomware as the end goal.


> **Security Architect's Take:** Audit all FortiGate device credentials immediately and rotate any that may have been exposed; prioritise checking for unauthorised VPN or management-plane access using those credentials. Review FortiGate firmware versions across your estate and ensure all devices are patched and not internet-exposed without strong authentication controls such as MFA.


**Original advisory:** [FortiBleed Credential Theft Linked to INC and Lynx Ransomware Operations](https://thehackernews.com/2026/07/fortibleed-credential-theft-linked-to.html)
