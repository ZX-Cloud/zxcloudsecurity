---
title: "AWS Compliance and Governance: A Practitioner's Guide for 2026"
date: 2026-08-06
description: "A practical guide to AWS compliance and governance for UK architects: SCPs, Config, Security Hub, PCI DSS, GDPR, and the pitfalls that sink audit programmes."
tags: ["aws compliance and governance", "aws config", "service control policies", "aws security hub", "pci dss", "gdpr", "aws control tower", "cloud governance"]
slug: "aws-compliance-and-governance"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2196
draft: false
---

# AWS Compliance and Governance: A practitioner's guide for 2026

AWS compliance and governance is not a once-a-year audit exercise. It is a continuous engineering discipline. Regulatory pressure on UK cloud deployments has never been higher: the FCA's operational resilience rules, UK GDPR obligations post-Brexit, and the sector-agnostic expectations of the NCSC's Cloud Security Principles all require demonstrable, evidence-backed controls rather than a PDF attestation that gathers dust between audits. If you are running regulated workloads on AWS and your governance posture still relies on manual reviews and spreadsheet checklists, this guide is a direct challenge to that approach.

<!-- INTERNAL_LINK: Understanding the shared responsibility model | shared-responsibility-model-cloud-security -->

## Why governance architecture matters more than certification

There is a misunderstanding I encounter repeatedly on client engagements: the belief that because AWS holds a particular certification, your workload inherits it automatically. That is wrong, and it is precisely the misunderstanding that trips up FCA-regulated firms at audit time.

AWS maintains PCI DSS Level 1 Service Provider certification, the highest level available. This covers AWS's physical infrastructure, hypervisors, and managed service security. It does not make your workloads PCI compliant. The same logic applies to every certification in the portfolio. Your job as a cloud architect is to implement the customer-side controls that complete the picture.

Most cloud security incidents stem from customer-side issues: identity misuse, misconfigurations, and exposed workloads. Governance architecture is the mechanism by which you prevent those incidents and prove to regulators that you are preventing them.

<!-- INTERNAL_LINK: AWS Well-Architected security pillar | aws-well-architected-security -->

## The governance toolchain: what each service actually does

Understanding which AWS service solves which governance problem saves you from over-engineering, and from the opposite failure mode of assuming one tool covers everything.

### AWS Organisations and Service Control Policies (SCPs)

A service control policy is a set of controls at the organisational unit level that restricts the maximum permissions that users, roles, and root users in AWS accounts can hold. SCPs are your outermost guardrail layer. Because they apply at the AWS Organisation level, you validate a few centralised controls rather than reviewing hundreds of IAM policies. That reduces audit scope and gives you assurance that critical rules apply consistently, not just by convention.

In September 2025, AWS added full IAM policy language support to SCPs. You can now use `NotAction` and conditions in Allow statements, individual resource ARNs, and the `NotResource` element in both Allow and Deny statements.

A foundational SCP that every UK-regulated environment should have is a region lock. Here is a working example that restricts all API calls to `eu-west-2` (London) and `eu-west-1` (Ireland) for resilience, with a carve-out for global services that must operate from `us-east-1`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonApprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "iam:*",
        "sts:*",
        "route53:*",
        "cloudfront:*",
        "wafv2:*",
        "budgets:*",
        "ce:*",
        "support:*",
        "trustedadvisor:*",
        "organizations:*",
        "account:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "eu-west-2",
            "eu-west-1"
          ]
        }
      }
    },
    {
      "Sid": "DenyRootCredentialUsage",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "aws:PrincipalArn": "arn:aws:iam::*:root"
        }
      }
    },
    {
      "Sid": "ProtectSecurityServices",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:DeleteTrail",
        "cloudtrail:StopLogging",
        "guardduty:DeleteDetector",
        "config:DeleteConfigurationRecorder",
        "config:StopConfigurationRecorder",
        "securityhub:DisableSecurityHub"
      ],
      "Resource": "*"
    }
  ]
}
```

The `ProtectSecurityServices` statement above prevents member accounts from disabling the tools you rely on for operational and risk auditing. That matters because without it, any account with sufficient IAM permissions can quietly turn off GuardDuty or stop a Config recorder, and you may not notice until an auditor asks for six months of findings.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: AWS IAM Identity Centre guide | aws-iam-identity-centre-guide -->

### AWS Control Tower

Control Tower automates landing zone creation for multi-account environments, applying pre-configured blueprints and guardrails that enforce baseline security from the start. It handles identity, federated access, logging, and account setup standardisation. The guardrails themselves are a mix of SCPs (preventive) and AWS Config rules (detective), and the distinction matters: an SCP blocks the action; a Config rule tells you after the fact that something is wrong.

### AWS Config and conformance packs

AWS Config is your continuous configuration monitoring layer. A conformance pack is a collection of Config rules and remediation actions deployed as a single entity, either into a single account and region or across an entire organisation. AWS ships ready-made conformance packs aligned to PCI DSS, CIS Benchmarks, and NIST CSF, so you are not authoring individual Config rules from scratch for common frameworks.

### AWS Security Hub CSPM

Security Hub continuously evaluates your resources against compliance standards and produces a compliance score that updates as findings change. Each standard contains controls, which are automated checks against specific aspects of your AWS configuration. When a control fails, Security Hub generates a finding that identifies what is wrong and how to fix it.

<!-- INTERNAL_LINK: Full Security Hub deployment guide | aws-security-hub-guide -->

In June 2026, AWS added the AI Security Best Practices standard to Security Hub: 31 automated controls that detect when deployed AI resources do not meet security best practices. The standard covers Amazon Bedrock, Amazon Bedrock AgentCore, and Amazon SageMaker, and does not require manual assessments or custom rule authoring. If you are building AI workloads and have not enabled this standard, you have a gap in your posture management that no other Security Hub standard currently fills.

<!-- INTERNAL_LINK: AI security in the cloud | ai-security-cloud-guide -->

## What AWS's recent certification renewals mean for your programme

AWS publishes compliance package updates regularly, and you should be reading them. Not because the announcements are interesting in themselves, but because scope changes directly affect what you can build on without acquiring additional controls yourself.

### Spring 2026 PCI DSS and PCI 3DS renewal

AWS completed its PCI DSS and PCI 3DS certification renewal in Spring 2026, expanding scope to include three additional services and one additional region. The newly added services are Amazon Bedrock AgentCore, AWS Parallel Computing Service, and AWS Skill Builder. The Asia Pacific (New Zealand) region was also added. For UK financial services teams building agentic AI workflows on top of payment infrastructure, the Bedrock AgentCore addition is directly relevant.

Each certification package includes two components: an Attestation of Compliance (AOC) demonstrating AWS was successfully validated against the standards, and an AWS Responsibility Summary that describes what customers are responsible for when handling payment card data. AWS was evaluated by Coalfire, a third-party Qualified Security Assessor. Both packages are available through AWS Artifact.

### Spring 2026 SOC reports and OSCAL format

The Spring 2026 SOC 1, 2, and 3 reports cover 188 services over the 12-month period from April 2025 to March 2026.

The OSCAL format release is worth paying attention to separately. As of June 2026, AWS is the first major cloud provider to offer compliance reports in NIST's Open Security Controls Assessment Language, a machine-readable JSON format. The SOC 1 and SOC 2 packages in OSCAL format are available as a distinct package in AWS Artifact.

In practical terms, this means you can ingest AWS's own control evidence as structured JSON rather than parsing a PDF. If you are building an automated evidence pipeline, and every serious compliance programme should be, this is material. You can now automate the ingestion of AWS control evidence directly into your compliance tooling without manual reformatting.

<!-- INTERNAL_LINK: Cloud compliance frameworks overview | cloud-compliance-frameworks -->

## UK-specific considerations: GDPR, FCA operational resilience, and sovereign cloud

For UK practitioners, three regulatory obligations shape governance architecture decisions in ways that differ from purely US-centric guidance.

UK GDPR and data residency: the region-lock SCP shown above is a starting point, but it needs to be paired with a data classification policy that identifies what constitutes personal data, where it flows, and which services process it. AWS Config rules for S3 public access blocks, RDS encryption, and CloudTrail logging are the detective layer; the SCP is the preventive layer.

FCA operational resilience (PS21/3): financial institutions in the UK are permitted to use cloud services, provided they comply with applicable legal and regulatory requirements. The practical implication for governance architecture is that you need to map your important business services to their underlying AWS dependencies and demonstrate you can remain within your impact tolerances during disruption. That is not a Security Hub problem; it is an architecture and business continuity problem that your governance programme needs to address alongside the technical controls.

AWS European Sovereign Cloud: this is now generally available, but it is not a UK solution. On 15 January 2026, AWS opened the European Sovereign Cloud as a physically and logically separate partition, with the first region in Brandenburg, Germany. The UK is not on the map, and AWS has said nothing to suggest it will be. UK-regulated firms should not be waiting for a UK sovereign cloud offering. The governance controls available in `eu-west-2` are mature and well-evidenced, and they are what your auditors will be assessing you against.

<!-- INTERNAL_LINK: Cross-cloud security services comparison | cross-cloud-security-services-comparison -->

## Common pitfalls in AWS compliance and governance programmes

These are the failure modes I see most frequently on real engagements. Some cost organisations weeks of rework at the worst possible time, just before an audit.

Treating Security Hub as your compliance pipeline: Security Hub detects control failures. It is not a compliance pipeline, and treating it as one is why teams still scramble for evidence at audit time. Security Hub tells you what is failing now. It does not automatically collect the historical evidence a QSA needs to see across an audit period.

Building controls before building evidence management: AWS offers substantial compliance material, but your implementation only becomes useful when someone can answer three questions for each control: what is the rule, how is it checked, and who handles exceptions? Teams routinely build controls before they build evidence management. That is the wrong order if audit readiness is your goal.

Assuming AWS certification scope equals your scope: AWS's PCI Level 1 certification covers the infrastructure layer. Your application's handling of cardholder data is entirely your responsibility to design, implement, and evidence.

Deploying SCPs without testing in non-production first: a badly scoped SCP that blocks a global service API call can break deployments across your entire organisation simultaneously. Test every SCP in a development or test account before attaching it at the Organisation root.

Ignoring new services entering compliance scope: every time AWS expands its PCI or SOC scope, as it did in Spring 2026 with Bedrock AgentCore, it may mean a service you have already deployed can now be brought within your compliance boundary with reduced overhead. Failing to monitor these announcements means leaving audit efficiency on the table.

Relying on a single compliance standard in Security Hub: there is significant overlap between standards. A resource that fails the CIS 3.1 control for CloudTrail will likely also fail the equivalent Foundational Security Best Practices and PCI checks. Security Hub handles deduplication, so enabling multiple standards does not create double-counting in your scoring, but it does give you broader coverage signals. Enable them all.

<!-- INTERNAL_LINK: Cloud threat detection guide | cloud-threat-detection -->
<!-- INTERNAL_LINK: DevSecOps and shift-left security | devsecops-shift-left-security -->

## Building a continuous compliance pipeline

The architecture that works in production for regulated clients combines the following layers:

1. Preventive controls: SCPs at the Organisation root and OU level block non-compliant actions before they land.
2. Detective controls: AWS Config rules and conformance packs continuously evaluate resource state; findings flow to Security Hub via native integration.
3. Alerting: Security Hub findings routed via EventBridge to your SIEM or ticketing system for triage SLAs.
4. Evidence collection: Config snapshots, CloudTrail logs, and Security Hub compliance status exports stored immutably in a dedicated audit S3 bucket in your Log Archive account, KMS-encrypted with object lock enabled.
5. Reporting: automated generation of compliance posture reports against your chosen standards, exportable for auditor consumption without a five-person fire drill.

<!-- INTERNAL_LINK: AWS KMS key management best practices | aws-kms-key-management-best-practices -->
<!-- INTERNAL_LINK: Cloud incident response | cloud-incident-response -->

The honest caveat: PCI QSAs ask for control evidence across the audit period, not screenshots taken the week before. Deploy organisation-wide Config conformance packs aligned to PCI, export compliance state continuously, and pair that with Security Hub standards checks. Start building this pipeline on day one, not the quarter before your assessment.

## Key takeaways

- AWS compliance and governance is a continuous engineering discipline, not an annual audit event. Preventive SCPs, detective Config rules, and Security Hub CSPM working together give you the automated posture management that regulators increasingly expect.
- AWS's Spring 2026 PCI DSS renewal added Amazon Bedrock AgentCore to scope, meaning teams building agentic AI workloads on payment infrastructure can now operate within the PCI compliance boundary. All reports are accessible via AWS Artifact.
- AWS is the first major cloud provider to offer SOC 1 and 2 reports in machine-readable OSCAL format, covering 188 services. Use this to automate evidence ingestion into your compliance pipeline rather than manually processing PDF attestations.
- UK practitioners must not conflate the AWS European Sovereign Cloud with a UK compliance solution. The ESC is EU-only. Governance controls in `eu-west-2` remain the correct foundation for UK-regulated workloads.
- The most common programme failure is building controls without a parallel evidence management strategy. A maintained control register and a continuous Config export pipeline are more valuable at audit time than a sophisticated compliance dashboard with no evidence trail.
- Test SCPs in non-production before attaching them at the Organisation root. A single misconfigured SCP that blocks a global IAM or STS endpoint can break every account in your estate simultaneously.