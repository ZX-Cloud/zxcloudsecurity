+++
title = "OVH Januscape Bug: Silent Mass Reboots Risk Downtime"
date = "2026-07-21T03:52:43Z"
publishDate = "2026-07-21T03:52:43Z"
slug = "ovh-januscape-critical-bug-mass-reboots-silent-patch"
description = "OVH patched the critical Januscape vulnerability via silent Debian backport and mass reboots, bypassing customer consent. Here's what cloud architects need"
categories = ["general"]
tags = ["ovh", "januscape", "patch-management", "hypervisor", "vulnerability", "cloud-provider-security", "availability", "incident-response"]
severity = "Critical"
source = "The Register — Security"
source_url = "https://www.theregister.com/virtualization/2026/07/21/ovh-reveals-semi-secret-plan-to-fix-critical-januscape-bug-with-mass-reboots-and-an-australian-crash-test-dummy/5275359"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/virtualization/2026/07/21/ovh-reveals-semi-secret-plan-to-fix-critical-januscape-bug-with-mass-reboots-and-an-australian-crash-test-dummy/5275359)

---

OVH implemented a patch for a critical vulnerability dubbed 'Januscape' by silently backporting a fix into Debian and scheduling mass reboots of customer infrastructure without explicit customer consent. The approach risked unplanned downtime for workloads not tolerant of unexpected restarts. This raises serious questions about cloud provider transparency and customer communication during emergency patching events.


> **Security Architect's Take:** Audit your OVH-hosted workloads immediately to confirm reboot resilience and check whether your instances were affected by this patching cycle. Beyond the immediate fix, review your cloud provider contracts and escalation procedures to ensure you have enforceable notification rights before unscheduled maintenance — and document your recovery posture for critical hypervisor-level vulnerabilities.


**Original advisory:** [OVH reveals semi-secret plan to fix critical Januscape bug with mass reboots – and an Australian crash-test dummy](https://www.theregister.com/virtualization/2026/07/21/ovh-reveals-semi-secret-plan-to-fix-critical-januscape-bug-with-mass-reboots-and-an-australian-crash-test-dummy/5275359)
