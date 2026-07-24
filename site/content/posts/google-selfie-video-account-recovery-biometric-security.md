+++
title = "Google Selfie Video Account Recovery: Security Risks"
date = "2024-07-23T10:00:00Z"
publishDate = "2026-07-23T10:00:00Z"
slug = "google-selfie-video-account-recovery-biometric-security"
description = "Google introduces selfie video as an account recovery option. Cloud security architects should assess deepfake risks and review Workspace recovery policies"
categories = ["general"]
tags = ["gcp", "google-workspace", "identity", "authentication", "biometrics", "account-recovery", "deepfake", "access-management"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/google-adds-selfie-video-recovery-for.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/google-adds-selfie-video-recovery-for.html)

---

Google has introduced selfie video verification as an additional account recovery option for users locked out of their accounts, supplementing existing methods such as recovery email and phone number. The feature uses biometric video matching to confirm identity during the recovery process. Whilst designed to improve legitimate user access, it introduces a new biometric attack surface that security teams should be aware of.


> **Security Architect's Take:** Review your organisation's Google Workspace account recovery policies to assess whether selfie video recovery can be enabled or restricted at the admin level, and evaluate the risk of deepfake or presentation attacks being used to bypass recovery controls for privileged accounts.


**Original advisory:** [Google Adds Selfie Video Recovery for Users Locked Out of Their Accounts](https://thehackernews.com/2026/07/google-adds-selfie-video-recovery-for.html)
