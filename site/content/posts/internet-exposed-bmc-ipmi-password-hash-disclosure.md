+++
title = "24,650 BMCs Leak IPMI Password Hashes Pre-Login"
date = "2026-07-28T14:41:36Z"
publishDate = "2026-07-28T14:41:36Z"
slug = "internet-exposed-bmc-ipmi-password-hash-disclosure"
description = "Over 24,000 internet-exposed BMC interfaces are leaking IPMI password hashes before login, enabling offline cracking and full server takeover."
categories = ["general"]
tags = ["ipmi", "bmc", "out-of-band-management", "credential-exposure", "CVE-2013-4786", "network-exposure", "server-security", "password-hashing"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/24650-internet-exposed-bmcs-disclose.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/24650-internet-exposed-bmcs-disclose.html)

---

Researchers have discovered over 36,000 server management interfaces (BMCs) exposed directly to the public internet, of which nearly 24,650 leak password hashes to anyone who connects — even before authentication is required. This is due to a known weakness in the IPMI protocol (CVE-2013-4786), which has been publicly documented for over a decade yet remains widely unpatched. An attacker who obtains these hashes can attempt to crack them offline and gain full out-of-band control of physical servers, bypassing all operating system and hypervisor-level security controls.


> **Security Architect's Take:** Audit your estate immediately for any BMC or IPMI interfaces reachable from the public internet or untrusted network segments — these should be isolated on dedicated out-of-band management networks with strict firewall rules. If IPMI cannot be disabled or network-isolated, enforce strong, unique passwords to slow offline cracking, and treat any exposed BMC as potentially compromised pending remediation.


**Original advisory:** [24,650 Internet-Exposed BMCs Disclose IPMI Password Hashes Before Login](https://thehackernews.com/2026/07/24650-internet-exposed-bmcs-disclose.html)
