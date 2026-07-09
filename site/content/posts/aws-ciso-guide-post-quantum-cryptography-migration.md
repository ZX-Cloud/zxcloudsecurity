+++
title = "CISO Guide to Post-Quantum Cryptography on AWS"
date = "2024-07-08T15:00:05Z"
publishDate = "2026-07-08T15:00:05Z"
slug = "aws-ciso-guide-post-quantum-cryptography-migration"
description = "AWS outlines how CISOs can lead post-quantum cryptography migrations across complex organisations, meeting global PQC mandates before quantum threats mater"
categories = ["aws"]
tags = ["aws", "post-quantum-cryptography", "cryptography", "pqc", "compliance", "encryption", "risk-management", "ciso"]
severity = "Medium"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/the-cisos-guide-to-post-quantum-mandates-and-migrations/"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/the-cisos-guide-to-post-quantum-mandates-and-migrations/)

---

Post-quantum cryptography (PQC) migration has moved from theoretical planning to active regulatory mandate across major economies, with CISOs now expected to lead organisation-wide transitions. The core challenge is not selecting new algorithms — it is coordinating change across complex enterprises where asymmetric cryptography is deeply embedded in systems, supply chains, and third-party dependencies. Getting this wrong could leave organisations exposed once cryptographically relevant quantum computers emerge.


> **Security Architect's Take:** Begin a cryptographic inventory now if you haven't already — identify all systems, APIs, and third-party integrations relying on RSA, ECC, or Diffie-Hellman, then prioritise long-lived data and high-value communications for early migration to NIST-standardised PQC algorithms such as ML-KEM and ML-DSA. AWS services are progressively adding PQC support, so align your migration roadmap with AWS's published PQC capabilities and engage vendors on their own timelines.


**Original advisory:** [The CISO’s guide to post-quantum mandates and migrations](https://aws.amazon.com/blogs/security/the-cisos-guide-to-post-quantum-mandates-and-migrations/)
