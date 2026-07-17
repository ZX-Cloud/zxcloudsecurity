+++
title = "n8n JWT Issuer Flaw Allows Account Takeover"
date = "2025-07-16T13:33:25Z"
publishDate = "2026-07-16T13:33:25Z"
slug = "n8n-jwt-issuer-validation-flaw-account-takeover"
description = "A JWT validation flaw in n8n Enterprise ignores the issuer claim, letting attackers authenticate as other users across trusted identity providers."
categories = ["general"]
tags = ["n8n", "jwt", "authentication-bypass", "account-takeover", "oidc", "identity-and-access-management", "workflow-automation", "enterprise-security"]
severity = "High"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/n8n-token-exchange-flaw-could-let.html"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/n8n-token-exchange-flaw-could-let.html)

---

n8n's Enterprise workflow automation platform contains a flaw where JWT-based logins are matched to local users using only the 'sub' (subject) claim, without validating the 'iss' (issuer) claim. This means a valid token from one trusted identity provider can be used to authenticate as a completely different user registered under a separate issuer. An attacker with a legitimate account on one connected identity provider could potentially log in as any other user on the same n8n instance.


> **Security Architect's Take:** If you run n8n Enterprise with multiple OIDC or JWT issuers configured, treat this as a high-priority patch and update to the fixed version immediately. In the interim, reduce your trusted issuer list to the minimum necessary and audit recent login events for unexpected cross-issuer authentication activity.


**Original advisory:** [n8n Token Exchange Flaw Could Let Attackers Log In as Users From Another Issuer](https://thehackernews.com/2026/07/n8n-token-exchange-flaw-could-let.html)
