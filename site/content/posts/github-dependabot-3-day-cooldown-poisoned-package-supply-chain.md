+++
title = "GitHub Dependabot 3-Day Cooldown Blocks Poisoned Packages"
date = "2024-07-27T08:01:23Z"
publishDate = "2026-07-27T08:01:23Z"
slug = "github-dependabot-3-day-cooldown-poisoned-package-supply-chain"
description = "GitHub adds a 3-day Dependabot cooldown to delay PRs for new package releases, reducing the risk of poisoned or malicious packages being auto-adopted."
categories = ["general"]
tags = ["github", "dependabot", "supply-chain", "dependency-management", "package-security", "open-source", "devsecops"]
severity = "Medium"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/07/github-adds-3-day-dependabot-cooldown.html"
weight = 30
draft = false
+++

🟡 **Medium** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/07/github-adds-3-day-dependabot-cooldown.html)

---

GitHub has introduced a default three-day cooldown period in Dependabot, delaying automated pull requests for newly published package versions. This gives time for the security community to identify poisoned or malicious packages before they are automatically adopted into codebases. The cooldown is configurable via dependabot.yml for teams with different risk tolerances.


> **Security Architect's Take:** Review your organisation's dependabot.yml configurations and consider whether the default three-day cooldown is appropriate or whether a longer window — such as seven days — better balances security and velocity for your projects. Pair this with private registry mirroring and package integrity checks to further reduce supply chain risk.


**Original advisory:** [GitHub Adds 3-Day Dependabot Cooldown to Limit Poisoned Package Adoption](https://thehackernews.com/2026/07/github-adds-3-day-dependabot-cooldown.html)
