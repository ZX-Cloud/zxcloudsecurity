+++
title = "GentleKiller EDR Killer: RaaS Targets 400 Security Tools"
date = "2025-06-19T18:33:07Z"
publishDate = "2026-06-19T18:33:07Z"
slug = "gentlemen-raas-gentlekiller-edr-killer-ransomware"
description = "The Gentlemen RaaS group distributes GentleKiller, an EDR-killing framework targeting 400+ security processes to disable defences before ransomware deploym"
categories = ["general"]
tags = ["ransomware", "edr-evasion", "defence-evasion", "raas", "endpoint-security", "threat-actor", "malware"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/the-gentlemen-raas-uses-gentlekiller.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/the-gentlemen-raas-uses-gentlekiller.html)

---

A ransomware-as-a-service group called 'The Gentlemen' is distributing a sophisticated toolkit called GentleKiller to its affiliates, designed to disable or kill endpoint detection and response (EDR) and security software before deploying ransomware. The framework reportedly targets around 400 security-related processes, making it capable of neutering a wide range of enterprise security tooling. This represents a mature, industrialised approach to defence evasion that significantly lowers the bar for affiliates to bypass security controls.


> **Security Architect's Take:** Audit your EDR deployment for tamper protection features and ensure agents are running in a protected mode that resists process termination — many EDR platforms offer kernel-level self-protection that should be explicitly enabled. Complement this with cloud-native controls such as immutable logging (e.g. CloudTrail, Azure Monitor), network segmentation, and privileged access management so that even a successful EDR kill does not grant unrestricted lateral movement or exfiltration capability.


**Original advisory:** [The Gentlemen RaaS Uses GentleKiller EDR Framework Targeting 400 Security Processes](https://thehackernews.com/2026/06/the-gentlemen-raas-uses-gentlekiller.html)
