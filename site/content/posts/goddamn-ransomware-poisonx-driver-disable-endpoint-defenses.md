+++
title = "GodDamn Ransomware: PoisonX Driver Disables EDR"
date = "2025-07-09T10:43:09Z"
publishDate = "2026-07-09T10:43:09Z"
slug = "goddamn-ransomware-poisonx-driver-disable-endpoint-defenses"
description = "GodDamn ransomware uses the PoisonX kernel driver to disable endpoint defences before encrypting systems. Learn what cloud security architects should do no"
categories = ["general"]
tags = ["ransomware", "byovd", "kernel-driver", "endpoint-security", "defense-evasion", "beast-ransomware", "edr-bypass", "threat-hunting"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/goddamn-ransomware-uses-poisonx-driver.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/goddamn-ransomware-uses-poisonx-driver.html)

---

A new ransomware strain called GodDamn, believed to be a rebrand of the Beast ransomware family, uses a malicious kernel driver called PoisonX to disable endpoint security tools before encrypting systems. First observed in the wild in May 2026, it employs a Bring Your Own Vulnerable Driver (BYOVD)-style technique to operate at the kernel level, bypassing traditional defences. This approach makes it particularly dangerous as it can neutralise EDR and antivirus solutions before the payload deploys.


> **Security Architect's Take:** Ensure your cloud workloads and hybrid endpoints enforce kernel driver signing policies and blocklist known vulnerable drivers using tools such as Microsoft's recommended driver blocklist or equivalent controls. Prioritise deploying tamper-protection features on EDR solutions and consider network-level detection for lateral movement patterns consistent with pre-ransomware activity.


**Original advisory:** [GodDamn Ransomware Uses PoisonX Driver to Disable Endpoint Defenses](https://thehackernews.com/2026/07/goddamn-ransomware-uses-poisonx-driver.html)
