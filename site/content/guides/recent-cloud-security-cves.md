---
title: "Recent Cloud Security CVEs: What Every AWS & Azure Architect Needs to Act On Now"
date: 2026-06-25
description: "A practitioner's breakdown of recent cloud security CVEs across Azure and AWS, covering exploitation risk, triage strategy, and detection with real AWS CLI and policy examples."
tags: ["cloud security", "CVE", "vulnerability management", "Azure", "AWS", "NCSC", "patch management"]
slug: "recent-cloud-security-cves"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2446
draft: false
---

# Recent cloud security CVEs: what every AWS and Azure architect needs to act on now

If your vulnerability management process still revolves around a monthly Patch Tuesday calendar and a CVSS score spreadsheet, the threat landscape has moved on without you. The volume and severity of recent cloud security CVEs in 2026 alone has exposed real gaps in how organisations track, triage, and respond to vulnerabilities, particularly across cloud-native services where the shared responsibility model blurs remediation ownership. This guide covers the most operationally significant CVEs from the past few months, explains what they mean for AWS and Azure environments specifically, and gives you the detection and remediation scaffolding to act on them today.

---

## Why 2026 has been a particularly brutal year for cloud CVEs

CVE submissions to the NVD increased 263% between 2020 and 2025, and the rate is still accelerating. Submissions during the first three months of 2026 are nearly one-third higher than the same period last year. The practical consequence: most vulnerabilities will now enter the CVE ecosystem without the CVSS metadata required for automated downstream tooling to prioritise them.

That last point matters enormously for security teams that rely on scanner integrations with NVD. NIST will now enrich only those CVEs that meet certain prioritisation criteria. CVEs that fall outside those criteria will still be listed in the NVD but deemed "lowest priority" and will not be immediately enriched. In plain English: your scanner's severity score may simply be absent for a significant chunk of newly published CVEs.

On the threat side, the emergence of frontier agentic models in early 2026 has materially changed the offensive timeline. These are AI systems that no longer just suggest code but actively test it, and they compress the window between discovery and weaponisation in ways that manual research simply cannot match. The NCSC's own CTO, writing in May 2026, advised that organisations should plan to deploy software security updates quickly, more frequently, and at scale, including across their supply chains, and specifically called out the need to prepare for a "vulnerability patch wave" as AI-assisted discovery scales.

The upshot: CVSS base scores alone are no longer a reliable triage mechanism, and the window between patch release and active exploitation keeps shrinking.

---

## High-severity cloud CVEs you should have already triaged

### CVE-2026-42826: Azure DevOps information disclosure (CVSS 10.0)

CVE-2026-42826 is a critical information disclosure vulnerability affecting Azure DevOps, published on 7 May 2026. The flaw allows an unauthenticated remote attacker to expose sensitive information over a network. No credentials required. No user interaction. Network-accessible.

Azure DevOps is the backbone of countless development pipelines. It stores source code, build definitions, release scripts, and often secrets such as connection strings and API keys. An information disclosure flaw in this platform is not a theoretical risk; it is a potential gateway to IP theft, supply chain compromise, or lateral movement into connected Azure resources.

Microsoft remediated this vulnerability within the cloud infrastructure without requiring customer intervention. The important nuance is that this does not necessarily mean the issues are unimportant. Cloud vulnerabilities sit outside direct customer control, leaving defenders to audit logs, review configurations, and trust the vendor's fix rather than deploy a patch themselves.

Your action here is not to patch, it is to audit. Review Azure DevOps access logs for any anomalous unauthenticated enumeration activity in the window between the flaw's introduction and remediation. If your pipelines store secrets as pipeline variables rather than Azure Key Vault references, this incident is your prompt to fix that.

<!-- INTERNAL_LINK: securing Azure DevOps pipelines | azure-devops-pipeline-security -->

### CVE-2026-41096: Windows DNS Client RCE (CVSS 9.8)

This is a heap-based buffer overflow in the Windows DNS Client that allows an unauthenticated attacker to execute code over a network. An attacker sends a specially crafted DNS response to a vulnerable Windows system, causing the DNS Client to misprocess the response and corrupt memory. No authentication required.

Practical exploitation does require a network position to intercept or respond to the target's DNS requests, whether through DNS spoofing, a rogue DNS server, or a machine-in-the-middle position on the network. For AWS workloads running Windows on EC2, that prerequisite is less reassuring than it sounds. If an attacker has already compromised another workload in the same VPC, or has positioned themselves between a Windows instance and the VPC DNS resolver at 169.254.169.253, this becomes exploitable. Patch your Windows AMIs.

### CVE-2026-41089: Windows Netlogon RCE (CVSS 9.8)

CVE-2026-41089 is a stack-based buffer overflow in Windows Netlogon. An unauthenticated attacker with network access can send a specially crafted request to a domain controller and execute code without any prior access. The targeted service sits on domain controllers, which makes this particularly serious. Successful exploitation means potential full domain takeover, followed by lateral movement, Kerberos and Entra tampering, and control over Group Policy and software deployment.

If you are running Active Directory on EC2, which remains a common pattern for AWS-based financial services clients who have not yet moved to AWS Managed Microsoft AD, this is your highest-priority patch. An unauthenticated attacker with network access to your domain controllers on port 445 or 135 can own your entire Windows estate.

### CVE-2026-35428: Azure Cloud Shell command injection (CVSS 9.6)

CVE-2026-35428 is a command injection flaw in Azure Cloud Shell that allows unauthenticated remote attackers to perform spoofing over a network. It requires user interaction and carries high confidentiality, integrity, and availability impact. Microsoft remediated this server-side. Cloud Shell sessions are frequently used by privileged administrators, so if a session was open during the exposure window, treat the associated credential as potentially compromised and rotate it.

### CVE-2026-42823: Azure Logic Apps privilege escalation (CVSS 9.9)

CVE-2026-42823 is an improper access control vulnerability in Azure Logic Apps that allows an authorised attacker to elevate privileges over a network. Logic Apps are increasingly used to automate security workflows, data pipelines, and integration between SaaS platforms, which makes a privilege escalation path here a significant risk for organisations using them in regulated workloads. Microsoft patched this server-side. Your action is to review Logic App managed identity assignments and confirm they follow least-privilege.

<!-- INTERNAL_LINK: Azure Logic Apps security best practices | azure-logic-apps-security -->

---

## The "no customer action required" trap

A pattern has emerged across the cloud CVEs patched in 2026 that deserves its own section, because it is lulling teams into a false sense of security.

Microsoft resolved numerous critical cloud-native vulnerabilities, including CVE-2026-42826, CVE-2026-35428, CVE-2026-33109, and CVE-2026-33823, with the advisory note: "requires no customer action." For years, enterprise security teams built vulnerability programmes around assets they could see and remediate themselves: Windows servers, routers, laptops, applications. Cloud services increasingly break that model.

The NCSC's Cloud Security Principle 5 is clear on this point: vulnerability management, protective monitoring, incident management, and configuration and change management are all aspects your provider should have a process in place to address. But the NCSC equally makes clear that customers retain responsibility for their configurations, data classification, and access controls built on top of those services.

"No customer action required" means the vendor patched their infrastructure. It does not mean:

- Your data was not exposed during the vulnerability window
- Your access logs do not warrant review
- Your managed identities and RBAC assignments are correctly scoped
- Your secrets stored in that service are uncompromised

Run a log review. Validate your configurations. Rotate high-privilege credentials that were active during the exposure window. These actions are always warranted, regardless of what the advisory says.

---

## Detecting cloud CVE exposure with AWS Security Hub and CLI

For AWS environments, Security Hub's integration with Amazon Inspector provides your first line of automated CVE detection across EC2, Lambda, and container workloads. The following AWS CLI snippet queries Inspector v2 for critical findings on your EC2 fleet, scoped to findings with an EPSS score above 0.1. That threshold is a useful proxy for exploitation likelihood that supplements the now-degraded NVD enrichment:

```bash
# Query Amazon Inspector v2 for critical EC2 CVE findings with high EPSS scores
aws inspectorv2 list-findings \
  --filter-criteria '{
    "findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}],
    "severity": [{"comparison": "EQUALS", "value": "CRITICAL"}],
    "resourceType": [{"comparison": "EQUALS", "value": "AWS_EC2_INSTANCE"}],
    "epssScore": [{"lowerInclusive": 0.1, "upperInclusive": 1.0}]
  }' \
  --sort-criteria '{"field": "EPSS_SCORE", "sortOrder": "DESC"}' \
  --query 'findings[].{CVE:packageVulnerabilityDetails.vulnerabilityId,
                        EPSS:epss.score,
                        Instance:resources[0].id,
                        FixAvailable:fixAvailable}' \
  --output table
```

This query surfaces findings sorted by EPSS exploitation probability rather than raw CVSS base score, which is a materially better signal now that NVD enrichment is patchy. For Windows-specific CVEs like CVE-2026-41096 and CVE-2026-41089, filter further by `packageVulnerabilityDetails.vulnerablePackages[].name` for `Windows`.

For patch compliance posture across an EC2 fleet, AWS Systems Manager Patch Manager gives you a compliance summary per patch group:

```bash
# Check patch compliance summary for a specific patch group
aws ssm describe-patch-group-state \
  --patch-group "windows-production" \
  --query 'Instances | {
    Compliant: sum_by(@, &ComplianceStatus == `COMPLIANT`),
    NonCompliant: sum_by(@, &ComplianceStatus == `NON_COMPLIANT`),
    Missing: sum_by(@, &MissingCount > `0`)
  }'
```

<!-- INTERNAL_LINK: AWS Inspector v2 setup and tuning | aws-inspector-v2-configuration -->

---

## Common pitfalls in cloud CVE triage

This is where I see organisations of all sizes make avoidable mistakes.

Pitfall 1: sorting by CVSS base score and treating the result as a priority list. Too often, teams ingest CVE data into scanners, sort by CVSS base score, and start patching from the top down. That approach ignores the richer signals available and leads to misallocated effort: patching an unconfirmed theoretical issue while a slightly lower-scored but actively exploited vulnerability sits unaddressed. Use EPSS scores and CISA's KEV catalogue as your primary triage signals. CVSS is context, not a queue.

Pitfall 2: treating "no customer action required" as "nothing to do." Covered above, but it bears repeating. Cloud-patched CVEs still demand a log review and a configuration audit. Your blast radius is your problem, not Microsoft's or Amazon's.

Pitfall 3: ignoring the NVD enrichment gap. If your vulnerability scanner pulls from NVD alone, you are flying partially blind. Subscribe to vendor-direct advisories from Microsoft MSRC, AWS Security Bulletins, and CISA KEV alerts, and supplement with a commercial enrichment feed.

Pitfall 4: not separating cloud-service CVEs from OS-level CVEs in your patching workflow. Azure DevOps, Logic Apps, and Cloud Shell vulnerabilities resolve themselves. EC2 Windows instances with the Netlogon and DNS Client CVEs do not. Conflating these in your remediation workflow produces false compliance reporting.

Pitfall 5: assuming your cloud workloads are unaffected by Windows kernel CVEs. If you run Windows on EC2, which is common across UK financial services for .NET workloads, SQL Server, and Active Directory, every Windows CVE in a given Patch Tuesday is in scope for your cloud environment. Treat your cloud Windows fleet with the same urgency as on-premises.

Pitfall 6: underestimating how much AI has compressed the patch-to-exploit timeline. Security researcher Himanshu Anand made the point bluntly: "the 90-day disclosure policy is dead," because large language models compress disclosure and exploit timelines to near-zero. "When 10 unrelated researchers find the same bug in six weeks, and AI can turn a patch diff into a working exploit in 30 minutes, what exactly is the 90-day window protecting?" Your SLAs for critical patching need to reflect this. A 30-day window for CVSS 9.0+ vulnerabilities with network-level exploitability is no longer adequate.

<!-- INTERNAL_LINK: building a cloud vulnerability management programme | cloud-vulnerability-management-programme -->

---

## Keeping pace: a practical monitoring stack

Given the volume of recent cloud security CVEs, manual review does not scale. A minimal but effective monitoring stack for a UK enterprise running AWS and Azure hybrid should include:

- CISA KEV Catalogue: your authoritative "patch this now" signal. Subscribe via RSS or the CISA API.
- Microsoft MSRC Security Update Guide: do not wait for Patch Tuesday roundups. Set up email notifications for products in your scope.
- AWS Security Bulletins (aws.amazon.com/security/security-bulletins): covers AMI-level, SDK-level, and service-level advisories.
- Amazon Inspector v2: continuous CVE scanning across EC2, Lambda, and container images, with native integration into Security Hub.
- AWS Security Hub with the AWS Foundational Security Best Practices standard enabled: surfaces misconfigurations that increase your blast radius when a CVE lands.
- NCSC Early Warning: a free alerting service that maps CISA KEV and other threat intel to your registered IP ranges. Most UK organisations are not using it.

The NCSC's vulnerability management guidance puts the objective clearly: an effective vulnerability management process allows your organisation to understand, and validate on a regular basis, which vulnerabilities are present in your technical estate, where updates are failing, and to actively reduce the impact of both. It also allows you to react quickly when a critical vulnerability is disclosed, by helping you understand your organisation's exposure to it.

For FCA-regulated firms, this is not advisory; it is a control expectation under operational resilience requirements. Your ability to demonstrate a defensible response timeline to a critical CVE will be tested.

---

## Key takeaways

Stop triaging on CVSS base score alone. Use EPSS exploit probability and CISA KEV catalogue status as primary signals, particularly now that NVD enrichment is increasingly incomplete for non-federal, non-KEV CVEs.

"No customer action required" is not the end of your obligation. For cloud-native CVEs patched server-side, your job is to audit access logs, validate configurations, and rotate credentials that were active during the exposure window.

Windows on EC2 is in scope for every Windows Patch Tuesday. CVE-2026-41089 (Netlogon RCE, CVSS 9.8) and CVE-2026-41096 (DNS Client RCE, CVSS 9.8) are directly exploitable on AWS-hosted Windows workloads if unpatched. Use AWS Systems Manager Patch Manager to enforce compliance at scale.

Agentic adversaries have compressed patch-to-exploit timelines to hours, not weeks. Your critical CVE patching SLA needs to reflect this. Thirty days is no longer an acceptable window for CVSS 9.0+ vulnerabilities with network-level exploitability.

Supplement NVD with vendor-direct advisory feeds. As NIST moves to risk-based NVD enrichment, organisations relying solely on scanner-integrated NVD data will have significant coverage gaps. Subscribe directly to MSRC, AWS Security Bulletins, and CISA KEV.

The NCSC's vulnerability management guidance is the baseline, not the ceiling. For UK financial services and public sector organisations, demonstrating adherence to the NCSC's five vulnerability management principles is the minimum expected posture.