+++
title = "What is CSPM (Cloud Security Posture Management)?"
date = "2026-06-08T09:24:46Z"
slug = "what-is-cspm-cloud-security-posture-management"
description = "What is CSPM (Cloud Security Posture Management)? — a practical guide for cloud security architects."
keywords = ["CSPM", "cloud security posture management", "misconfiguration", "compliance"]
type = "guides"
draft = false
+++

Cloud Security Posture Management (CSPM) is a category of security tooling that continuously monitors cloud environments for misconfigurations, policy violations, and compliance drift. CSPM tools provide automated assessment and remediation of security risks across IaaS, PaaS, and SaaS environments. In an era where the shared responsibility model places configuration squarely in the customer's hands, CSPM has become foundational infrastructure for any serious cloud security programme.

---

## Why Misconfiguration Is the Primary Threat Vector

The cloud doesn't get breached the way data centres traditionally did. Sophisticated zero-days and nation-state exploits make headlines, but the overwhelming majority of cloud security incidents trace back to something far more mundane: a storage bucket left publicly accessible, an overly permissive IAM policy, a security group open to 0.0.0.0/0, or logging quietly disabled on a critical service.

Gartner has consistently projected that through the mid-2020s, nearly all cloud security failures will be the customer's fault — not the provider's. This isn't a criticism; it's a structural consequence of how cloud platforms work. When an engineer provisions an S3 bucket, spins up an RDS instance, or deploys a Kubernetes cluster via Terraform, they make dozens of configuration decisions. At scale, across hundreds of engineers and thousands of resources, the probability of misconfiguration approaches certainty.

Several factors compound the problem:

- **Velocity**: Development teams move fast. Security reviews that once happened at deployment gates now need to happen continuously.
- **Sprawl**: Multi-cloud and multi-account architectures mean security teams may have limited visibility into what's actually running.
- **Ephemeral infrastructure**: Resources spun up for testing often persist. Temporary permissions become permanent.
- **Drift**: A resource correctly configured at deployment can drift out of compliance as policies, services, and threat landscapes evolve.

The 2019 Capital One breach — caused by a misconfigured WAF and overly permissive EC2 role — remains the canonical example. More recently, exposed Azure Blob containers and misconfigured Elasticsearch clusters have leaked hundreds of millions of records. The pattern is consistent.

---

## What CSPM Tools Actually Do

At their core, CSPM platforms perform continuous, automated assessment of your cloud configuration against security baselines and compliance frameworks. The core capabilities break down into several distinct functions.

### Inventory and Visibility

Before you can secure what you have, you need to know what you have. CSPM tools continuously discover resources across accounts, subscriptions, and projects — mapping relationships between services, identities, network paths, and data stores. This asset inventory is the foundation everything else builds on. Tools like Wiz, Orca Security, and Prisma Cloud build rich cloud asset graphs that let you ask questions like "which compute instances have access to S3 buckets containing PII and are reachable from the internet?"

### Configuration Assessment

CSPM platforms compare your actual configuration state against security benchmarks — typically the CIS Foundations Benchmarks for AWS, Azure, and GCP, NIST CSF, or provider-native frameworks like AWS Security Hub's FSBP. Every deviation from the baseline generates a finding, categorised by severity. This is where CSPM earns its keep: instead of manual audits against a 400-point checklist, you get a continuous, automated feed of configuration gaps.

### Compliance Mapping

Most organisations operate under multiple regulatory regimes simultaneously — PCI DSS, ISO 27001, SOC 2, GDPR, and for UK organisations increasingly Cyber Essentials Plus. CSPM tools map configuration findings to specific control requirements, giving you audit-ready reports that demonstrate compliance posture at a point in time and track it over time. This matters enormously when a QSA or external auditor asks for evidence.

### Threat Detection and Contextual Risk

Modern CSPM platforms go beyond static configuration checks. They correlate configuration state with runtime signals — CloudTrail events, VPC Flow Logs, Azure Activity Logs — to detect anomalous behaviour in context. Wiz's Security Graph, for example, can identify a critical risk path: an internet-exposed VM with a known CVE, running with an overprivileged role, with network access to a database containing sensitive data. This contextual risk scoring prevents alert fatigue by surfacing the issues that actually matter.

### Remediation

CSPM tools offer remediation guidance ranging from human-readable descriptions of what's wrong and how to fix it, through to one-click automated remediation and Infrastructure as Code fixes that can be submitted as pull requests. The degree of automated remediation you enable should be calibrated carefully — automated changes in production carry their own risks.

---

## Native Tooling vs. Third-Party CSPM

Every major cloud provider offers native posture management capabilities: AWS Security Hub with Config Rules, Microsoft Defender for Cloud, and Google Security Command Center. These are worth enabling regardless of what else you deploy — they're deeply integrated, reasonably priced, and often a licensing requirement for certain compliance frameworks.

The case for third-party CSPM platforms rests primarily on multi-cloud normalisation and depth. If you operate across AWS and Azure — or AWS and GCP — you'll want a single pane of glass with consistent severity scoring, unified compliance reporting, and a single workflow for triage and remediation. Native tools don't provide this cross-cloud visibility. Third-party platforms also tend to offer richer contextual analysis, better integration with developer workflows, and more sophisticated attack path modelling.

The practical answer for most mature organisations is both: native tooling for deep integration and baseline coverage, a third-party CSPM platform for cross-cloud visibility, enriched context, and developer-facing workflows.

---

## What Architects Should Do: Practical Guidance

Getting CSPM right requires more than licensing a tool. Here's what effective implementation looks like in practice.

- **Start with a benchmark, not a blank slate.** Pick a well-understood framework — CIS Benchmarks are a sensible default — and configure your CSPM platform against it from day one. Customise later once you understand your noise profile.

- **Integrate CSPM into your CI/CD pipeline.** Shift posture checks left. Tools like Checkov, tfsec, or Snyk Infrastructure as Code can catch misconfigurations in Terraform and CloudFormation before they reach production. CSPM in production is your safety net, not your first line of defence.

- **Normalise findings across clouds.** If your CSPM platform can't give you a consistent severity score for the same misconfiguration in AWS and Azure, you'll struggle to prioritise. Insist on normalised, cross-cloud risk scoring when evaluating platforms.

- **Map findings to business risk, not just technical severity.** A critical finding on a non-production, air-gapped environment is less urgent than a medium finding on a payment-processing account. Build asset classification into your CSPM configuration so severity is contextualised.

- **Establish clear ownership and SLAs for remediation.** CSPM generates findings; humans fix them. Without clear ownership — mapped to cloud accounts, teams, or resource tags — findings age indefinitely. Define escalation paths and track mean-time-to-remediation as a security metric.

- **Review suppressed and accepted findings regularly.** Risk acceptances accumulate. Build a quarterly review cadence to reassess whether exceptions still apply.

- **Include CSPM coverage in your cloud landing zone design.** Accounts, subscriptions, or projects should be enrolled in CSPM tooling automatically as part of provisioning — not as an afterthought.

---

## Key Takeaways

- **CSPM addresses the leading cause of cloud breaches**: misconfiguration, which is a customer responsibility under the shared responsibility model.
- **Core capabilities** include continuous asset discovery, configuration assessment against benchmarks, compliance mapping, contextual risk scoring, and remediation guidance.
- **Native and third-party tools serve different purposes** — use both in mature environments, particularly when operating across multiple cloud providers.
- **CSPM is not a product you deploy; it's a programme you run.** Tooling without defined ownership, remediation SLAs, and integration into developer workflows generates noise rather than security improvement.
- **Shift left wherever possible** — catching misconfigurations in code review or CI/CD is faster and cheaper than remediating them in production.


## Related Guides

- [Zero Trust Architecture](/guides/what-is-zero-trust-architecture/) — CSPM provides the continuous verification layer that underpins a Zero Trust posture in cloud environments.
- [Data Security Posture Management (DSPM)](/guides/what-is-dspm-data-security-posture-management/) — Where CSPM focuses on infrastructure configuration, DSPM focuses on data risk. The two disciplines are increasingly deployed together.
- [Cloud Infrastructure Entitlement Management (CIEM)](/guides/what-is-ciem-cloud-infrastructure-entitlement-management/) — CIEM extends CSPM into the identity layer, surfacing over-privileged roles and toxic permission combinations that CSPM alone may miss.
- [AWS IAM Security Best Practices](/guides/aws-iam-security-best-practices/) — The IAM misconfigurations that CSPM tools most frequently flag, and how to remediate them.
- [The Shared Responsibility Model in Cloud Security](/guides/shared-responsibility-model-cloud-security/) — Understanding which posture controls are your responsibility versus the cloud provider's.
- [Cross-Cloud Security Services Comparison](/guides/cross-cloud-security-services-comparison/) — Compare AWS Security Hub, Microsoft Defender for Cloud, and Google Security Command Center as native CSPM solutions.
