---
title: "Recent Cloud Security CVEs: What Practitioners Need to Know in 2026"
date: 2026-07-11
description: "A practitioner's guide to recent cloud security CVEs in 2026, covering key vulnerabilities, AWS detection approaches, and what the NVD enrichment crisis means for your programme."
tags: ["cloud security", "cve", "vulnerability management", "aws", "azure"]
slug: "recent-cloud-security-cves"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2405
draft: false
---

# Recent Cloud Security CVEs: what practitioners need to know in 2026

If you run cloud security for a UK enterprise, tracking recent cloud security CVEs has always been painful. In 2026 it got measurably worse. In February, FIRST forecast an additional 50,000 CVEs this year, and some estimates run higher. At the same time, the database most teams depend on for enrichment just had its operating model overhauled. More vulnerabilities, less metadata. That combination creates real gaps in cloud security programmes that FCA-regulated firms and government suppliers cannot leave open. This guide covers the specific CVEs worth tracking right now, what the NVD shake-up means for your tooling, and how to build an AWS-native detection pipeline that does not depend on a single upstream feed.

<!-- INTERNAL_LINK: cloud security vulnerability management overview | cloud-security-vulnerability-management -->

---

## The NVD enrichment crisis and why it matters for cloud teams

On 15 April 2026, NIST announced a fundamental change to the National Vulnerability Database. Driven by CVE volumes that essentially tripled over five years, NIST is moving to a constrained, risk-based enrichment model.

In practice, three things change:

1. 
CVEs outside NIST's priority parameters will still be published but will be categorised as "Not Scheduled"
 — 
deemed lowest priority and not immediately enriched by NIST
.
2. 
The NVD will no longer routinely supply its own CVSS scores for CVEs already scored by the submitting CNA
.
3. Earlier backlogged CVEs with a publish date before 1 March 2026 have moved to 
"Not Scheduled."
 That is not a queue-management artefact. It is a formal declaration that universal manual enrichment is finished.

The downstream effect is immediate. Scanners that depend on NVD-supplied CVSS scores are now flying partially blind. Without that enrichment, tools will report systems as clean when they are not.

For UK enterprises, this hits an already stretched function. Your GRC tooling, your CSPM findings, and your Jira-integrated scanner outputs all assumed NVD enrichment as a baseline. You need to treat CVE.org, CNA disclosures, vendor advisories, GitHub Advisories, and the CISA KEV catalogue as primary operational sources rather than waiting for NVD to catch up.

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->
<!-- INTERNAL_LINK: AWS Inspector for vulnerability management | aws-inspector-vulnerability-management -->

---

## Key recent cloud security CVEs worth tracking

### CVE-2026-57111: Apache Helix permissive CORS (CVSS 7.5, high)

CVE-2026-57111 is a permissive Cross-Origin Resource Sharing vulnerability in the Apache Helix REST API, specifically in `org.apache.helix.rest.server.filters.CORSFilter`, 
affecting versions through 2.0.0
. A remote attacker controlling a malicious web page can make cross-origin requests to the API.

Apache Helix is a cluster management framework used in data-intensive workloads. LinkedIn's infrastructure is the most cited deployment, but it surfaces in self-managed Elasticsearch and Kafka setups running on EC2 and EKS. This matters if you are running any Helix-managed component with a REST API exposed inside your VPC, and especially if your security groups are broader than they need to be.

Remediation: 
upgrade to version 2.0.1, which fixes this issue
. As a further control, restrict `cors.allowed.origins` to an explicit allowlist and confirm your security groups do not expose the Helix REST port beyond the segments that genuinely need it.

<!-- INTERNAL_LINK: AWS WAF configuration and CORS hardening | aws-waf-configuration -->

---

### CVE-2026-14440: Cloudflare Universal SSL CAA bypass (CVSS 0, informational)

A CVSS of zero will cause most automated scanners to skip this entirely. That is a mistake for any organisation using Cloudflare for DNS and TLS management, which covers a significant portion of UK financial services and SaaS companies.

The problem is that 
Cloudflare's DNS infrastructure automatically manages CAA resource records and overrides any customer-defined CAA settings with a permissive default
. The auto-managed record set includes directives such as 
`issue "letsencrypt.org"` without account binding or validation method constraints, effectively nullifying the protections intended by RFC 8659 and RFC 8657
.

The attack path is worth understanding. This default configuration reopens the architectural gap exploited in the 2023 jabber.ru incident. If an attacker can intercept traffic during the ACME HTTP-01 domain validation phase, they can issue a legitimate certificate for your domain through Cloudflare, bypassing your CAA restrictions. You will not detect it unless you are monitoring Certificate Transparency logs.

Remediation: customers who require strict RFC 8657 enforcement need to disable Universal SSL on the affected zone. 
The automatic CAA management that comes with Universal SSL and customer-set RFC 8657 `accounturi` and `validationmethods` constraints are mutually exclusive. There is no in-product workaround that preserves both.
 Certificate Transparency monitoring is the right general detection control regardless.

For FCA-regulated firms, TLS certificate management is typically in scope for operational resilience reviews. Confirm which zones use Universal SSL and whether RFC 8657 binding appears as a stated control in your certificate policy.

---

### CVE-2026-26118: Azure MCP Server SSRF and privilege escalation (CVSS 8.8, high)

This is the most architecturally significant cloud CVE of the first half of 2026, and it points to a vulnerability category that will keep appearing as AI-native infrastructure matures.


CVE-2026-26118 details a server-side request forgery (SSRF) vulnerability in Azure MCP (Model Context Protocol) Server, published 10 March 2026
. 
An authorised attacker can exploit it to elevate privileges over the network
.

The mechanics are straightforward. An attacker interacting with an MCP-backed agent submits a malicious URL where a standard Azure resource identifier is expected. The MCP Server processes the tool call, makes an outbound HTTP request to the attacker-controlled URL, and attaches its managed identity token to that request. The attacker captures the token.

Because MCP tools commonly carry elevated permissions to manage Azure Machine Learning resources, a stolen token can grant broad access across Azure subscriptions. Training data, model repositories, and inference endpoints are all potentially in scope.

Affected packages: 
`@azure/mcp` (npm) versions >= 2.0.0-beta.1 and < 2.0.0-beta.17, and >= 1.0.0 and < 1.0.2; `Azure.Mcp` (NuGet) in the same version ranges; `msmcp-azure` (pip) >= 2.0.0b14 and < 2.0.0b17
.

Remediation: update to the patched versions. As an interim network-level control, restrict outbound egress from MCP hosts to an explicit allowlist of trusted destinations so a poisoned resource identifier cannot route a token to attacker infrastructure, and validate resource identifiers before the server dereferences them. Blocking access to the Azure IMDS endpoint at `169.254.169.254` is a worthwhile complementary control against the credential-fetch SSRF variant, but it does not on its own stop token exfiltration to an external URL.

<!-- INTERNAL_LINK: AI and LLM security guide | beginners-guide-ai-llm-security -->
<!-- INTERNAL_LINK: Zero trust architecture and microsegmentation | what-is-zero-trust-architecture -->

---

### The June 2026 Microsoft Patch Tuesday: cloud-relevant highlights


Microsoft's June 2026 release covered 208 CVEs across Windows, Office, Azure, Exchange, Hyper-V, Secure Boot, BitLocker, and a range of AI tooling
, plus Edge, .NET, Visual Studio, GitHub Copilot, and Defender. Two are worth calling out specifically for cloud practitioners.

CVE-2026-45657 is a critical remote code execution vulnerability in the Windows kernel with a 
CVSS base score of 9.8
. 
Use-after-free and heap-based buffer overflow flaws allow remote, unauthenticated attackers to execute code at SYSTEM level without user interaction.
 The exploit path is 
specially crafted network traffic that triggers a flaw in how the Windows kernel processes certain TCP/IP data, potentially allowing the attacker to run code with system-level privileges without needing to sign in or interact with a user
. Any Windows-based EC2 or Azure VM is potentially affected.

CVE-2026-44815 is a critical RCE in the Windows DHCP Client Service, also 
CVSS 9.8
. 
A stack-based buffer overflow in Windows DHCP Client allows an unauthorized attacker to execute code over a network.
 The attack requires operating a rogue DHCP server on the network and responding to DHCP requests from vulnerable clients with crafted data.


Three vulnerabilities in the June release were publicly disclosed before patches were available
, and 15 were rated "Exploitation More Likely" by Microsoft.

---

## Building a cloud-native CVE detection pipeline on AWS

Relying solely on NVD is no longer a workable approach. The following AWS-native pattern supplements vendor feeds with automated detection.

```python
# Example: Lambda function to ingest CISA KEV feed and 
# cross-reference against AWS Inspector findings via Security Hub
# Deploy with least-privilege IAM role scoped to 
# securityhub:GetFindings (read-only)

import boto3
import requests
import json
from datetime import datetime, timezone

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

def lambda_handler(event, context):
    # Fetch CISA KEV catalogue
    resp = requests.get(KEV_URL, timeout=10)
    kev_data = resp.json()
    kev_cves = {v["cveID"] for v in kev_data.get("vulnerabilities", [])}
    
    # Pull Inspector findings from Security Hub
    hub = boto3.client("securityhub", region_name="eu-west-2")
    paginator = hub.get_paginator("get_findings")
    
    critical_findings = []
    pages = paginator.paginate(
        Filters={
            "ProductName": [{"Value": "Inspector", "Comparison": "EQUALS"}],
            "RecordState": [{"Value": "ACTIVE", "Comparison": "EQUALS"}],
        }
    )
    
    for page in pages:
        for finding in page["Findings"]:
            # Extract CVE IDs from the finding's Vulnerabilities list:
            # each entry's Id plus its RelatedVulnerabilities (strings)
            cve_ids = {
                vuln_id
                for vuln in finding.get("Vulnerabilities", [])
                for vuln_id in [vuln.get("Id", "")]
                    + vuln.get("RelatedVulnerabilities", [])
                if vuln_id.startswith("CVE-")
            }
            for cve_id in cve_ids:
                if cve_id in kev_cves:
                    critical_findings.append({
                        "cve": cve_id,
                        "resource": finding.get("Resources", [{}])[0]
                                          .get("Id", "unknown"),
                        "severity": finding.get("Severity", {})
                                           .get("Label", "UNKNOWN"),
                        "account": finding.get("AwsAccountId"),
                    })
    
    # Log or route to SNS/Jira for immediate triage
    if critical_findings:
        print(json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "kev_matched_findings": critical_findings,
            "count": len(critical_findings),
        }))
    
    return {"statusCode": 200, "body": f"{len(critical_findings)} KEV-matched findings"}
```

Schedule this Lambda hourly via EventBridge. The CISA KEV feed is currently the highest-signal prioritisation input available. NVD has confirmed it will prioritise enriching 
vulnerabilities already added to the CISA Known Exploited Vulnerabilities catalog, those affecting software used within the US federal government, and those affecting critical software as defined by Executive Order 14028
. Aligning your triage to KEV means you are working the same priority queue that NVD itself considers most important.

<!-- INTERNAL_LINK: CloudTrail configuration for security logging | aws-cloudtrail-configuration-best-practices -->
<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->

---

## Prioritisation: moving beyond CVSS scores

One of the most damaging habits in cloud vulnerability management is treating raw CVSS scores as the primary triage signal. The NVD changes make this worse, but the underlying problem exists regardless of enrichment quality.

A medium-severity CVE on an internet-exposed workload with a path to a customer database outranks a critical one on an isolated internal host. That is not a controversial position, but most teams' SLAs are not built to reflect it.

The prioritisation hierarchy that works in cloud environments:

1. Is it on CISA KEV? If yes, treat as P1 regardless of CVSS score.
2. Is the affected resource internet-facing? An exploitable CVE on a public API or load balancer is a different problem from one on an isolated dev instance.
3. What IAM permissions does the affected workload hold? Scope each workload identity to the resources it actually uses. Compromising the workload should not hand an attacker everything the role can reach.
4. Is there a known exploit or proof-of-concept? Vendor exploitability ratings are imperfect but they are actionable signal.
5. Does the vulnerability have a plausible path to regulated data? For UK financial services, any CVE that could reach customer data or payment systems is automatically escalated under FCA operational resilience obligations.

Quarterly scans are obsolete the moment they complete. Vulnerability management has to be continuous, automated, and prioritised by exploitability, exposure, and business impact.

<!-- INTERNAL_LINK: Cloud incident response runbook | cloud-incident-response -->
<!-- INTERNAL_LINK: What is CSPM | what-is-cspm-cloud-security-posture-management -->

---

## Common pitfalls when managing recent cloud security CVEs

These are the patterns I see most often across UK enterprise and financial services AWS environments.

### 1. Treating NVD as a single source of truth

Patching policies built around NVD-enriched CVSS scores are no longer reliable. That means policies written around score thresholds may not survive an audit. You need multiple feeds operating in parallel: AWS Security Bulletins, MSRC, GitHub Advisories, vendor-specific channels, and CISA KEV.

### 2. Ignoring informational-severity CVEs

CVE-2026-14440 has a CVSS of zero. Most scanners and most SLAs will never surface it. Your certificate management policy and threat model should. CVSS was not designed to capture architectural trust-boundary violations. Its base metrics measure exploitability and direct impact to confidentiality, integrity, and availability. Those are different things.

### 3. Overlooking managed service and AI infrastructure CVEs

A scanner will tell you OpenSSL is vulnerable inside a container. It may not tell you that AWS, Microsoft, or Google published an advisory for a managed service, agent, SDK, or platform component your workloads depend on. Shared responsibility does not absolve you of tracking the vendor side. CVE-2026-26118 in Azure MCP Server is the clearest 2026 example of this.

### 4. Not blocking IMDS access from untrusted workloads

SSRF vulnerabilities routinely escalate through the instance metadata endpoint, where an attacker forces a workload to fetch credentials on their behalf. On AWS, requiring IMDSv2 (token-based) significantly reduces the blast radius of that variant across your estate: set account-level instance metadata defaults to require IMDSv2 on new launches via the EC2 ModifyInstanceMetadataDefaults API, add an SCP using the ec2:MetadataHttpTokens condition key to deny ec2:RunInstances requests that do not require IMDSv2, and remediate existing instances with ModifyInstanceMetadataOptions. This is a preventive control you can enforce in an afternoon.

### 5. Vague ownership

Remediation fails when nobody owns the finding. The programmes that actually clear backlogs route findings through CMDB context: asset, application, owner, environment, SLA, ticket, exception, and verification evidence. "Security owns the queue" does not work when engineering owns the fix.

### 6. Conflating "no active exploitation" with "low urgency"

Microsoft frequently notes it is unaware of exploitation in the wild at the time of release. Several vulnerabilities from last month's Patch Tuesday landed on CISA KEV within days of publication. The window between "no known exploitation" and "actively exploited" can be hours once researchers start reverse-engineering a patch.

<!-- INTERNAL_LINK: AWS IAM Identity Centre and privilege access | aws-iam-identity-centre -->
<!-- INTERNAL_LINK: Kubernetes security best practices | kubernetes-security-best-practices -->

---

## Key takeaways

The NVD enrichment model has changed in a way that does not reverse. The question your programme needs to answer is no longer "what is the canonical CVSS score?" but "what do we know about exploitation, exposure, affected configurations, and exploit preconditions?" Supplement NVD with CISA KEV, vendor bulletins, and GitHub Advisories as primary inputs.

CVE-2026-26118 in Azure MCP Server is a category signal. As agentic AI infrastructure is adopted at pace, SSRF and privilege escalation vulnerabilities in AI middleware will keep appearing. Restrict outbound egress from MCP and agentic workloads — and block metadata endpoint access — as a standard hardening baseline now, before the next one arrives.

CVE-2026-14440 in Cloudflare Universal SSL demonstrates that a CVSS score of zero does not mean zero risk. Certificate authority control-plane weaknesses have direct impact for UK regulated entities. Implement Certificate Transparency monitoring across all production domains regardless of Cloudflare plan tier.

Apache Helix CORS (CVE-2026-57111) is a reminder that cloud-native data infrastructure carries its own CVE surface. If you run Kafka, Elasticsearch, or other Helix-managed clusters on EC2 or EKS, confirm REST API exposure and update now.

A well-prioritised short list beats an unactionable feed of thousands. Most cloud security incidents trace back to identity misuse, misconfigurations, and exposed workloads rather than unpatched software. The teams that manage this well are the ones that treat prioritisation as the product, not the output.

IMDSv2 enforcement and outbound egress controls are cheap and have a high return. They reduce the blast radius of the entire class of SSRF vulnerabilities currently hitting cloud AI infrastructure. If you have not enforced these across all AWS accounts, that is the first thing to do after closing this page.

<!-- INTERNAL_LINK: AWS Well-Architected security pillar review | aws-well-architected-security -->
<!-- INTERNAL_LINK: CIEM and cloud entitlement management | what-is-ciem-cloud-infrastructure-entitlement-management -->