+++
title = "India .bank Domain Registry API Leaked Bank Officials' Data"
date = "2025-06-30T02:24:46Z"
publishDate = "2026-06-30T02:24:46Z"
slug = "india-rbi-bank-domain-registry-api-data-leak-impersonation"
description = "India's RBI-mandated .bank.in domain registry exposed an open API leaking sensitive registrant data, enabling impersonation of bank officials."
categories = ["general"]
tags = ["data-exposure", "api-security", "domain-registry", "impersonation", "phishing", "supply-chain", "financial-services", "information-disclosure"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/06/30/indias-central-bank-mandated-use-of-bank-domains-to-enhance-trust-but-its-registry-leaked-sensitive-info/5264152"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/06/30/indias-central-bank-mandated-use-of-bank-domains-to-enhance-trust-but-its-registry-leaked-sensitive-info/5264152)

---

The Reserve Bank of India mandated that banks use .bank.in domains to boost trust and reduce phishing, but the registry managing those domains exposed an open API leaking sensitive registrant data — including contact details and organisational information about bank officials. This undermines the very trust mechanism it was designed to create, giving attackers everything needed to craft convincing impersonation attacks.


> **Security Architect's Take:** If your organisation operates in or integrates with Indian financial services, review any third-party domain registry dependencies for unauthenticated API exposure. More broadly, this is a reminder that trust infrastructure (domain registries, certificate authorities, identity providers) must itself be subjected to rigorous security assurance — treat them as critical supply chain components and assess their security posture accordingly.


**Original advisory:** [India’s central bank mandated use of .bank domains to enhance trust – but its registry leaked sensitive info](https://www.theregister.com/security/2026/06/30/indias-central-bank-mandated-use-of-bank-domains-to-enhance-trust-but-its-registry-leaked-sensitive-info/5264152)
