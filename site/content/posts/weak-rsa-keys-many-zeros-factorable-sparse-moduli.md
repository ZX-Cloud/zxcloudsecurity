+++
title = "Weak RSA Keys With Many Zeros Found in the Wild"
date = "2025-06-29T16:05:18Z"
publishDate = "2026-06-29T16:05:18Z"
slug = "weak-rsa-keys-many-zeros-factorable-sparse-moduli"
description = "Researchers found a new class of factorable RSA keys with sparse moduli in real-world TLS, SSH, and PGP deployments. Check your keys with badkeys now."
categories = ["general"]
tags = ["rsa", "cryptography", "public-key-infrastructure", "tls", "ssh", "key-management", "badkeys", "factorisation"]
severity = "High"
source = "Schneier on Security"
source_url = "https://www.schneier.com/blog/archives/2026/06/factoring-rsa-keys-with-many-zeros.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [Schneier on Security](https://www.schneier.com/blog/archives/2026/06/factoring-rsa-keys-with-many-zeros.html)

---

Researchers have identified a new class of weak RSA keys characterised by an unusually high number of zero bits in the modulus, making them vulnerable to factorisation attacks. Analysis of real-world key datasets — including Certificate Transparency logs, TLS/SSH scans, and PGP keys — confirmed these vulnerable keys exist in production environments. If an attacker can factorise an RSA key, they can decrypt communications or forge signatures protected by that key.


> **Security Architect's Take:** Run your organisation's public RSA keys through the badkeys tool to check for sparse moduli and other known weaknesses; prioritise any keys used in TLS certificates, SSH host keys, or code signing. Consider enforcing key generation through vetted, standards-compliant libraries and adding automated key-quality checks to your certificate lifecycle management pipeline.


**Original advisory:** [Factoring RSA Keys with Many Zeros](https://www.schneier.com/blog/archives/2026/06/factoring-rsa-keys-with-many-zeros.html)
