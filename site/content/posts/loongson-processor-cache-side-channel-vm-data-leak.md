+++
title = "Loongson CPU Cache Flaw Leaks Data from Guest VMs"
date = "2025-08-13T02:14:11Z"
publishDate = "2026-08-13T02:14:11Z"
slug = "loongson-processor-cache-side-channel-vm-data-leak"
description = "Researchers find cache side-channel flaws in Loongson processors allowing data extraction from guest VMs, threatening cloud workload isolation."
categories = ["general"]
tags = ["loongson", "side-channel", "cache-attack", "virtualisation", "hardware-security", "vm-escape", "cpu-vulnerability", "cloud-infrastructure"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/08/13/chinese-loongson-processors-have-leaky-caches-researchers-find/5287137"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/08/13/chinese-loongson-processors-have-leaky-caches-researchers-find/5287137)

---

Researchers have discovered cache side-channel vulnerabilities in Chinese-made Loongson processors that allow attackers to extract sensitive data from memory. Critically, the attack can be executed from within a guest virtual machine, meaning cloud or virtualised environments running on Loongson hardware could be at risk. This class of vulnerability is particularly serious as it bypasses traditional isolation boundaries between workloads.


> **Security Architect's Take:** If your organisation operates or procures infrastructure — particularly in Asia-Pacific supply chains or sovereign cloud environments — that may include Loongson-based hardware, audit your vendor hardware inventory immediately and assess whether workload isolation controls are sufficient pending a microcode or firmware patch from the vendor.


**Original advisory:** [Chinese Loongson processors have leaky caches, researchers find](https://www.theregister.com/security/2026/08/13/chinese-loongson-processors-have-leaky-caches-researchers-find/5287137)
