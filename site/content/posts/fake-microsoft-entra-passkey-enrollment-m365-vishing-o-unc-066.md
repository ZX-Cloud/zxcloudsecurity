+++
title = "Fake Entra Passkey Enrolment Used to Hijack M365"
date = "2025-07-10T10:30:20Z"
publishDate = "2026-07-10T10:30:20Z"
slug = "fake-microsoft-entra-passkey-enrollment-m365-vishing-o-unc-066"
description = "Attackers use vishing and a phishing kit to enrol rogue Microsoft Entra passkeys, gaining persistent M365 access for data extortion. Here's what to do."
categories = ["general"]
tags = ["azure", "microsoft-365", "microsoft-entra", "passkey", "vishing", "phishing", "mfa-bypass", "credential-theft"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/hackers-use-fake-microsoft-entra.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/hackers-use-fake-microsoft-entra.html)

---

A threat actor tracked as O-UNC-066 is using vishing (voice phishing) calls to trick Microsoft 365 users into enrolling an attacker-controlled passkey in Microsoft Entra, effectively handing over persistent account access. Once enrolled, the attacker can authenticate as the victim without needing a password or MFA, enabling data extortion. The attack uses a panel-controlled phishing kit specifically designed to abuse the passkey registration flow.


> **Security Architect's Take:** Review and restrict who can register new Entra passkeys by enforcing Conditional Access policies that require a trusted, managed device and a compliant network location for any authentication method registration. Additionally, enable Microsoft Entra ID Protection alerts for suspicious registration events and train users to treat any unsolicited calls requesting security re-enrolment as a red flag.


**Original advisory:** [Hackers Use Fake Microsoft Entra Passkey Enrollment to Gain Microsoft 365 Access](https://thehackernews.com/2026/07/hackers-use-fake-microsoft-entra.html)
