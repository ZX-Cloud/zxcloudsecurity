+++
title = "GCP-2025-058: AMD Zen 5 RDSEED Flaw on Compute Engine"
date = "2024-08-11T18:14:49Z"
publishDate = "2026-08-11T18:14:49Z"
slug = "gcp-2025-058-amd-zen5-rdseed-cryptographic-randomness-flaw"
description = "AMD Zen 5 Turin processors have a flaw causing 16/32-bit RDSEED to silently fail, risking weak cryptographic randomness in GCP Compute Engine workloads."
categories = ["gcp"]
tags = ["gcp", "compute-engine", "amd-zen5", "cryptography", "random-number-generation", "hardware-vulnerability", "rdseed"]
severity = "Medium"
source = "GCP Compute Engine Security Bulletins"
source_url = "https://docs.cloud.google.com/compute/docs/security-bulletins#gcp-2025-058"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [GCP Compute Engine Security Bulletins](https://docs.cloud.google.com/compute/docs/security-bulletins#gcp-2025-058)

---

A hardware flaw in AMD Zen 5 (Turin) processors causes the 16-bit and 32-bit variants of the RDSEED instruction — used to generate cryptographic random numbers — to silently fail under certain load conditions. Applications that directly use these instruction widths may produce weak or predictable random numbers, undermining cryptographic security. The 64-bit variant is unaffected, meaning standard Linux kernel random number generation via /dev/[u]random is safe.


> **Security Architect's Take:** Audit any workloads running on AMD Zen 5 (Turin) GCP instances that directly invoke RDSEED at the application or library level — particularly custom cryptographic code or language runtimes that bypass the OS entropy pool. Ensure all such code uses the 64-bit RDSEED variant or delegates to /dev/urandom; no kernel-level patching is required at this time, but monitor AMD's investigation for further guidance.


**Original advisory:** [GCP-2025-058](https://docs.cloud.google.com/compute/docs/security-bulletins#gcp-2025-058)
