+++
title = "PCI DSS v4 & Third-Party Scripts: Checkout Page Risk"
date = "2025-06-18T11:00:00Z"
publishDate = "2026-06-18T11:00:00Z"
slug = "pci-dss-v4-third-party-scripts-checkout-page-compliance"
description = "PCI DSS v4.0 makes third-party checkout scripts a compliance requirement. Learn what cloud architects must do to protect payment pages and pass QSA audits."
categories = ["general"]
tags = ["pci-dss", "supply-chain", "client-side-security", "e-commerce", "script-injection", "compliance", "web-skimming", "third-party-risk"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/the-scripts-on-your-checkout-page-are.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/the-scripts-on-your-checkout-page-are.html)

---

PCI DSS v4.0 now explicitly requires merchants to control and monitor third-party scripts running on payment pages, closing a long-standing blind spot where analytics, tag managers, and support widgets could exfiltrate card data without detection. A QSA assessment of the Reflectiz platform evaluated how well it addresses these new requirements. Any organisation taking card payments online needs to demonstrate they have visibility and control over client-side scripts or risk failing their next PCI audit.


> **Security Architect's Take:** Audit every third-party script loaded on your checkout pages and implement a client-side integrity monitoring solution that satisfies PCI DSS v4.0 requirements 6.4.3 and 11.6.1; ensure your CSP headers, Subresource Integrity tags, and a continuous behavioural monitoring tool are all in place before your next QSA assessment.


**Original advisory:** [The Scripts on Your Checkout Page Are Now a PCI DSS Problem](https://thehackernews.com/2026/06/the-scripts-on-your-checkout-page-are.html)
