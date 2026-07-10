+++
title = "npm 12 Disables Install Scripts to Cut Supply Chain Risk"
date = "2024-07-09T16:49:02Z"
publishDate = "2026-07-09T16:49:02Z"
slug = "npm-12-disables-install-scripts-default-supply-chain-risk"
description = "npm 12 disables install scripts by default and deprecates granular access tokens that bypassed 2FA, reducing supply chain attack risk for Node.js ecosystem"
categories = ["general"]
tags = ["npm", "supply-chain", "github", "2fa", "access-tokens", "nodejs", "package-security", "ci-cd"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/npm-12-disables-install-scripts-by.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/npm-12-disables-install-scripts-by.html)

---

npm version 12 has been released with install scripts disabled by default, meaning packages can no longer automatically execute arbitrary code during installation without explicit opt-in. GitHub is also deprecating granular access tokens that could be used to circumvent two-factor authentication. These changes directly reduce the attack surface for supply chain attacks via malicious npm packages.


> **Security Architect's Take:** Review your CI/CD pipelines and developer workstation tooling for any reliance on automatic install scripts — you will need to explicitly enable allowScripts for legitimate use cases. Audit existing npm tokens and rotate any granular access tokens (GATs) ahead of their deprecation, ensuring all service accounts use 2FA-compliant authentication.


**Original advisory:** [npm 12 Disables Install Scripts by Default to Reduce Supply Chain Risk](https://thehackernews.com/2026/07/npm-12-disables-install-scripts-by.html)
