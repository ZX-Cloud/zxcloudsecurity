+++
title = "Millions of Cars Hijackable via Shared Bluetooth Key Flaw"
date = "2025-07-23T16:12:58Z"
publishDate = "2026-07-23T16:12:58Z"
slug = "karr-swds-bluetooth-hardcoded-key-vehicle-hijack-california"
description = "UCSD researchers find KARR/SWDS aftermarket car security systems share a single hardcoded key, allowing Bluetooth-range attackers to hijack millions of veh"
categories = ["general"]
tags = ["iot-security", "hardcoded-credentials", "bluetooth", "embedded-systems", "karr-swds", "vehicle-security", "key-management", "supply-chain"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/23/millions-of-california-bought-cars-can-be-hijacked-via-bluetooth/5277315"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/23/millions-of-california-bought-cars-can-be-hijacked-via-bluetooth/5277315)

---

Researchers at UC San Diego have discovered that KARR/SWDS aftermarket vehicle security systems, installed by dealers across California, all share a single hardcoded cryptographic key. This means an attacker within Bluetooth range can authenticate to any affected vehicle and potentially unlock, track, or remotely start millions of cars. The scale of deployment makes this a widespread physical security risk affecting everyday consumers.


> **Security Architect's Take:** While this is not a direct cloud infrastructure issue, it is a sharp reminder of the risks of hardcoded shared secrets and the importance of per-device unique key provisioning in any IoT or embedded system your organisation procures or oversees. If your fleet management or connected vehicle strategy involves aftermarket telematics devices, audit vendor key management practices immediately and enforce unique credential requirements in procurement contracts.


**Original advisory:** [Millions of California-bought cars can be hijacked via Bluetooth](https://www.theregister.com/security/2026/07/23/millions-of-california-bought-cars-can-be-hijacked-via-bluetooth/5277315)
