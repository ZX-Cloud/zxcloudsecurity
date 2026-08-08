+++
title = "N-able N-central God Mode Flaw: Customer Networks Breached"
date = "2026-08-07T15:01:00Z"
publishDate = "2026-08-07T15:01:00Z"
slug = "n-able-n-central-god-mode-privilege-escalation-customer-networks-breached"
description = "N-able confirms attackers exploited a privilege escalation flaw in N-central to reach customer networks. A second hotfix is now available — patch immediate"
categories = ["general"]
tags = ["n-able", "n-central", "rmm", "privilege-escalation", "supply-chain", "managed-service-provider", "lateral-movement", "patch-management"]
severity = "Critical"
source = "The Register — Security"
source_url = "https://www.theregister.com/networks/2026/08/07/n-able-god-mode-flaw-vendor-confirms-attackers-reached-customer-networks-as-second-hotfix-lands/5284730"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/networks/2026/08/07/n-able-god-mode-flaw-vendor-confirms-attackers-reached-customer-networks-as-second-hotfix-lands/5284730)

---

N-able has confirmed that attackers exploited a critical privilege escalation flaw in its N-central remote monitoring and management platform, using administrative access to pivot downstream into customer networks. A second hotfix has been issued after the first proved insufficient. The incident highlights the severe supply chain risk posed by RMM tools, which by design hold broad access to managed environments.


> **Security Architect's Take:** If your organisation uses N-central, apply the latest hotfix immediately and audit downstream access logs for lateral movement or unusual admin activity originating from N-able infrastructure. Consider temporarily restricting N-central's network reach to only essential endpoints until you can confirm your environment was not traversed.


**Original advisory:** [N-able God mode flaw: Vendor confirms attackers reached customer networks as second hotfix lands](https://www.theregister.com/networks/2026/08/07/n-able-god-mode-flaw-vendor-confirms-attackers-reached-customer-networks-as-second-hotfix-lands/5284730)
