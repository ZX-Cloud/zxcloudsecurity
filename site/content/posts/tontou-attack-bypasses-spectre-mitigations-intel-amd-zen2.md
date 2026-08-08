+++
title = "TONTOU Attack Bypasses Spectre Fixes on Intel & AMD"
date = "2025-08-07T14:15:00Z"
publishDate = "2026-08-07T14:15:00Z"
slug = "tontou-attack-bypasses-spectre-mitigations-intel-amd-zen2"
description = "MIT's TONTOU attack bypasses Spectre mitigations on Intel and AMD CPUs via timer interrupts, with a working Zen 2 exploit. Key risk for cloud infrastructur"
categories = ["general"]
tags = ["spectre", "side-channel", "intel", "amd", "cpu-vulnerability", "hypervisor-security", "branch-predictor", "microarchitecture"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/08/07/mit-boffins-tontou-attack-slips-through-spectre-defenses-on-intel-and-amd-cpus/5284081"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/08/07/mit-boffins-tontou-attack-slips-through-spectre-defenses-on-intel-and-amd-cpus/5284081)

---

MIT researchers have demonstrated a new 'TONTOU' (Time-Of-Notification, Time-Of-Use) attack that bypasses existing Spectre mitigations on Intel and AMD processors by exploiting the window created when timer interrupts temporarily reset branch predictor defences. The researchers produced a working exploit targeting AMD Zen 2 CPUs, showing an attacker can still poison the branch predictor and leak sensitive data from memory. This undermines confidence in widely deployed Spectre mitigations such as IBRS and retpolines, which are currently the primary defences across cloud infrastructure globally.


> **Security Architect's Take:** Monitor vendor microcode and OS kernel patch advisories from AMD and Intel closely — prioritise patching hypervisor hosts and bare-metal cloud instances running Zen 2 processors (e.g. AWS and Azure instances backed by EPYC Rome). In the interim, consider reducing the attack surface by enabling strict process isolation, reviewing use of shared-CPU tenancy models, and assessing whether confidential computing enclaves (e.g. AMD SEV-SNP) in your environment inherit this exposure.


**Original advisory:** [MIT boffins' TONTOU attack slips through Spectre defenses on Intel and AMD CPUs](https://www.theregister.com/security/2026/08/07/mit-boffins-tontou-attack-slips-through-spectre-defenses-on-intel-and-amd-cpus/5284081)
