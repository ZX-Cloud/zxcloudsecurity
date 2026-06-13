+++
title = "Velvet Ant Backdoors Linux PAM & OpenSSH for 10 Years"
date = "2026-06-12T18:17:55Z"
publishDate = "2026-06-12T18:17:55Z"
slug = "velvet-ant-china-linux-pam-openssh-backdoor-persistent-access"
description = "China-linked Velvet Ant compromised PAM and OpenSSH to maintain stealthy Linux access for nearly a decade. Here's what cloud architects must do now."
categories = ["general"]
tags = ["linux", "pam", "openssh", "velvet-ant", "persistent-access", "supply-chain", "threat-actor", "lateral-movement"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/china-linked-hackers-backdoored-linux.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/china-linked-hackers-backdoored-linux.html)

---

A China-linked threat actor tracked as Velvet Ant spent nearly a decade maintaining persistent access to a targeted network by backdooring PAM (Pluggable Authentication Modules) and OpenSSH — the core Linux components that control who can log in. By compromising the authentication layer itself rather than higher-visibility applications, the group was able to survive routine security clean-up efforts. This matters because the same Linux authentication stack underpins the vast majority of cloud workloads, container hosts, and on-premises infrastructure.


> **Security Architect's Take:** Audit the integrity of PAM configuration files and OpenSSH binaries across all Linux hosts using file integrity monitoring or a trusted read-only baseline — pay particular attention to shared services and jump hosts where a single compromise yields the broadest access. Consider deploying centralised SSH certificate authorities (e.g. HashiCorp Vault SSH, AWS EC2 Instance Connect) to reduce reliance on static authorised_keys files and make backdoored local auth paths easier to detect.


**Original advisory:** [China-Linked Hackers Backdoored Linux Login Software to Hide for Nearly a Decade](https://thehackernews.com/2026/06/china-linked-hackers-backdoored-linux.html)
