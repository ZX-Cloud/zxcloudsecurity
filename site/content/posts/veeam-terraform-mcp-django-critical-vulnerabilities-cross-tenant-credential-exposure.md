+++
title = "Critical Flaws Patched in Veeam, Terraform MCP & Django"
date = "2026-08-05T14:27:30Z"
publishDate = "2026-08-05T14:27:30Z"
slug = "veeam-terraform-mcp-django-critical-vulnerabilities-cross-tenant-credential-exposure"
description = "HashiCorp, Veeam, and Django patch 11 flaws including a CVSS 10.0 cross-tenant Terraform token bug and a CVSS 9.5 Veeam credential exposure issue."
categories = ["general"]
tags = ["veeam", "hashicorp", "terraform", "django", "cross-tenant", "credential-exposure", "patch-management", "multi-tenant-security"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/08/veeam-terraform-mcp-django-patch.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/08/veeam-terraform-mcp-django-patch.html)

---

HashiCorp, Veeam, and the Django Software Foundation have issued patches addressing 11 vulnerabilities, including two critical flaws: a CVSS 10.0 cross-tenant token reuse bug in HashiCorp's Terraform MCP Server and a CVSS 9.5 unauthenticated credential exposure flaw in Veeam Service Provider Console. These vulnerabilities could allow attackers to hijack Terraform operations across tenant boundaries or extract managed agent credentials without authentication. Organisations using these tools in multi-tenant or service provider environments face significant exposure if unpatched.


> **Security Architect's Take:** Prioritise patching the Terraform MCP Server and Veeam Service Provider Console immediately — the cross-tenant token reuse flaw is particularly dangerous in shared or SaaS-style deployments where blast radius extends beyond a single customer. Audit recent Terraform MCP Server usage logs for any anomalous token activity that could indicate prior exploitation, and verify Veeam VSPC is not exposed to untrusted networks pending patching.


**Original advisory:** [Veeam, Terraform MCP, Django Patch Critical Flaws, Led by CVSS 10.0 Cross-Tenant Bug](https://thehackernews.com/2026/08/veeam-terraform-mcp-django-patch.html)
