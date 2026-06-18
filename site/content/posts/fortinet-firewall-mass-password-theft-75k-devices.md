+++
title = "Fortinet Firewall Attack Steals Passwords on 75k Devices"
date = "2026-06-17T17:27:40Z"
publishDate = "2026-06-17T17:27:40Z"
slug = "fortinet-firewall-mass-password-theft-75k-devices"
description = "A mass credential-theft attack has hit 75,000 Fortinet firewalls. Learn what cloud security architects should do now to protect their environments."
categories = ["general"]
tags = ["fortinet", "fortigate", "credential-theft", "firewall", "password-rotation", "network-security", "management-plane-exposure", "vpn"]
severity = "Critical"
source = "The Register — Security"
source_url = "https://www.theregister.com/cyber-crime/2026/06/17/massive-password-stealing-attack-hits-75k-fortinet-firewalls/5257877"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/cyber-crime/2026/06/17/massive-password-stealing-attack-hits-75k-fortinet-firewalls/5257877)

---

A large-scale credential-theft campaign has compromised approximately 75,000 Fortinet firewall devices, exfiltrating stored passwords. The attack exploits exposed management interfaces or known vulnerabilities to harvest credentials at scale. This poses a significant risk to organisations using FortiGate appliances, particularly those with internet-facing management planes.


> **Security Architect's Take:** Immediately rotate all credentials associated with affected Fortinet devices, including VPN accounts, local admin accounts, and any downstream systems that share those credentials. Audit your FortiGate estate for internet-exposed management interfaces and restrict access to trusted IP ranges via firewall policy or a jump host.


**Original advisory:** [Massive password-stealing attack hits 75k Fortinet firewalls](https://www.theregister.com/cyber-crime/2026/06/17/massive-password-stealing-attack-hits-75k-fortinet-firewalls/5257877)
