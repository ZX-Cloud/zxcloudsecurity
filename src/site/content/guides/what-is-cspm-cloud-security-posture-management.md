+++
title = "What is CSPM (Cloud Security Posture Management)?"
date = "2026-06-07T13:47:34Z"
slug = "what-is-cspm-cloud-security-posture-management"
description = "What is CSPM (Cloud Security Posture Management)? — a practical guide for cloud security architects."
keywords = ["CSPM", "cloud security posture management", "misconfiguration", "compliance"]
type = "guides"
draft = false
+++

Cloud Security Posture Management (CSPM) is a category of security tooling that continuously monitors cloud infrastructure for misconfigurations, compliance violations, and risks that expose organisations to breach or data loss. Unlike perimeter-based controls, CSPM focuses on the configuration layer — the settings, policies, and permissions that define how cloud resources behave. It has become a foundational discipline for any organisation running workloads in AWS, Azure, Google Cloud, or across multiple providers simultaneously.

## Why Misconfiguration Is the Defining Cloud Security Problem

The cloud operates on a shared responsibility model. Your provider secures the underlying infrastructure; you're responsible for everything you deploy on top of it. That boundary is where most breaches actually happen.

Misconfiguration consistently ranks as the leading cause of cloud security incidents, and the reasons are structural rather than accidental. Cloud environments are dynamic by design — teams spin up resources via Infrastructure as Code, CI/CD pipelines, and self-service portals at a pace that's impossible to audit manually. A single misconfigured S3 bucket, an overly permissive IAM role, or a publicly exposed storage account in Azure can sit undetected for months.

Several high-profile breaches have followed exactly this pattern. The 2019 Capital One incident, which exposed over 100 million customer records, stemmed from a misconfigured Web Application Firewall combined with an IAM role that granted excessive permissions to an EC2 instance. The attacker didn't exploit a zero-day vulnerability — they exploited a configuration error that should have been caught during posture review.

Misconfiguration risks compound in multi-cloud environments. Each provider has its own identity model, networking primitives, and default settings — and defaults are frequently insecure. Azure Storage accounts historically defaulted to allowing public blob access. AWS S3 buckets can be made public at the bucket or object level through multiple overlapping mechanisms. GCP service accounts can be granted project-level owner permissions with a few clicks. Without automated, continuous monitoring, these risks accumulate faster than any security team can track.

## What CSPM Tools Actually Do

CSPM platforms sit above the control plane of your cloud environment, using read-only API access to continuously interrogate resource configurations. At their core, they perform four functions:

**Continuous configuration assessment.** The tool inventories all resources across your cloud accounts — compute instances, storage buckets, databases, network security groups, IAM policies, serverless functions — and evaluates each against a library of security rules. These rules encode best practices from benchmarks such as CIS (Centre for Internet Security), NIST 800-53, and cloud-provider-specific frameworks.

**Compliance mapping.** CSPM tools map findings to specific regulatory frameworks — PCI DSS, ISO 27001, SOC 2, GDPR, Cyber Essentials, and others. This makes them particularly valuable for organisations subject to audit, as they provide continuous evidence of control effectiveness rather than a point-in-time snapshot.

**Risk prioritisation.** Not all misconfigurations carry equal risk. A security group allowing inbound SSH from 0.0.0.0/0 on a public-facing instance is categorically more dangerous than the same rule on an isolated development account. Better CSPM platforms apply contextual analysis — considering network exposure, data sensitivity, and blast radius — to surface the findings that matter most.

**Drift detection and alerting.** Cloud configurations change constantly. CSPM tools detect when a resource drifts from its known-good state or from an established baseline, alerting security teams in near-real time. Some platforms support automated remediation, either through direct API calls or by triggering Infrastructure as Code pipelines to restore the intended state.

### Leading CSPM Platforms

The market includes both specialist tools and capabilities embedded within broader platforms:

- **Wiz** — widely adopted for its graph-based approach, which models how misconfigurations chain together to create exploitable attack paths rather than surfacing issues in isolation
- **Orca Security** — uses agentless side-scanning to assess configurations and workloads without requiring agents on instances
- **Prisma Cloud (Palo Alto Networks)** — a full-lifecycle platform with strong CSPM capabilities alongside CWPP and code security
- **Microsoft Defender for Cloud** — deeply integrated with Azure, with multi-cloud support for AWS and GCP; a pragmatic choice for Azure-heavy organisations
- **AWS Security Hub** — native to AWS, aggregates findings from AWS Config, GuardDuty, and third-party tools; strong for AWS-only environments
- **Lacework** — combines CSPM with behavioural anomaly detection using machine learning

## Posture Management in Multi-Cloud Environments

Running workloads across multiple cloud providers introduces posture management complexity that single-cloud tools can't adequately address. Each provider has distinct configuration models, and a finding in AWS doesn't always have a direct equivalent in GCP or Azure. This creates gaps when teams rely on native tooling alone.

Multi-cloud CSPM requires a unified data model that normalises findings across providers into a consistent taxonomy. Wiz, Orca, and Prisma Cloud handle this well; native tools generally do not. When evaluating platforms for multi-cloud coverage, prioritise those that provide a single inventory view, consistent severity scoring, and unified compliance reporting across all providers.

Equally important is IAM posture management, sometimes called Cloud Infrastructure Entitlement Management (CIEM) — a discipline closely related to CSPM. Excessive permissions are a misconfiguration class in their own right. A CSPM tool that can identify over-privileged service accounts, unused IAM roles, and cross-account trust relationships is significantly more valuable than one that only assesses resource-level settings.

## What Architects Should Do: Practical Guidance

**Establish a baseline before you alert.** Deploying CSPM into a mature environment often surfaces thousands of findings immediately. Prioritise ruthlessly: start with high-severity, internet-exposed resources and work inward. Trying to remediate everything at once leads to alert fatigue and abandonment.

**Integrate CSPM into your CI/CD pipeline.** Posture management works best when it starts at the code layer. Use tools like Checkov, Terrascan, or the IaC scanning capabilities within your CSPM platform to catch misconfigurations before they reach production. Shift-left reduces the cost and urgency of runtime findings.

**Define ownership for findings.** Security teams can identify misconfigurations, but remediation often sits with platform engineering or application teams. Build a workflow that routes findings to the right owner with context — ideally integrated into your ticketing system (Jira, ServiceNow) so remediation is tracked to closure.

**Treat compliance frameworks as a floor, not a ceiling.** CIS benchmarks and regulatory mappings are useful starting points, but they don't capture your organisation's specific threat model. Supplement with custom policies that reflect your architecture — for example, rules that enforce tagging standards, require encryption for specific data classifications, or flag deployments outside approved regions.

**Measure posture over time.** Track your posture score as a metric, but be cautious about treating it as a single KPI. A rising score can mask new high-severity findings if remediation is focused on volume rather than risk. Report on critical-severity open findings and mean time to remediate as more meaningful signals.

**Review default settings when adopting new services.** Cloud providers introduce new services continuously, each with their own default configurations — not all of them secure. Make reviewing default settings part of your service adoption process, before workloads are deployed at scale.

## Key Takeaways

- CSPM provides continuous, automated monitoring of cloud resource configurations against security best practices and compliance frameworks.
- Misconfiguration — not vulnerabilities or malware — is the primary cause of cloud breaches, driven by the speed and scale of cloud adoption.
- Effective CSPM goes beyond rule-matching: contextual risk prioritisation, attack path analysis, and IAM posture visibility are now table stakes for mature implementations.
- Multi-cloud environments demand platforms with a unified data model; native tools from individual providers leave significant gaps.
- Posture management is most effective when integrated across the full delivery lifecycle — from IaC scanning in pipelines through to continuous runtime monitoring and structured remediation workflows.
