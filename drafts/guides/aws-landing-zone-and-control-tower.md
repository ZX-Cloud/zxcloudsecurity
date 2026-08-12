---
title: "AWS Landing Zone and Control Tower: A Practitioner's Security Guide"
date: 2026-08-12
description: "Master AWS landing zone and Control Tower architecture, guardrails, AFT account vending, and compliance mapping for regulated UK cloud environments."
tags: ["aws", "landing-zone", "control-tower", "cloud-security", "compliance", "multi-account"]
slug: "aws-landing-zone-and-control-tower"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 1964
draft: false
---

# AWS Landing Zone and Control Tower: A Practitioner's Security Guide

If you are building a cloud programme for a UK financial services firm, a public sector department, or any enterprise with serious compliance obligations, getting the foundation right is non-negotiable. AWS landing zone and Control Tower are the two most important architectural decisions you will make before a single workload ever runs in production. Get them wrong and you will spend years paying down governance debt: unpicking ad-hoc account structures, hunting for who deleted that SCP, and failing FCA or NCSC assurance reviews. Get them right and every team that follows you inherits a secure, auditable baseline on day one.

<!-- INTERNAL_LINK: AWS Well-Architected Security pillar overview | aws-well-architected-security -->

## What is a landing zone (and why it is not just Control Tower)

A landing zone is a well-architected, multi-account AWS environment that is scalable and secure. It provides the central architecture and guardrails in a foundational cloud environment: a starting point from which an organisation can launch and deploy workloads with confidence in its security and infrastructure.

Control Tower is the orchestration engine that builds and governs that environment. It orchestrates AWS Organizations, AWS Config, IAM Identity Center, and other services to provide a prescriptive approach to building and managing a secure multi-account environment.

The two concepts are often conflated, but the distinction matters operationally. Control Tower is a service; the landing zone is the outcome. You can have a poorly governed landing zone even with Control Tower enabled, if you neglect drift management and guardrail hygiene. Equally, you can extend Control Tower significantly using the Landing Zone Accelerator (LZA), but more on that shortly.

## The core account structure

The canonical Control Tower account structure includes:

- Management account: root of the organisation; no workloads should run here
- Log Archive account: immutable CloudTrail and Config logs
- Audit account: Security Hub aggregation, GuardDuty delegated admin, cross-account read access for your security team
- Workload accounts: isolated per environment (`dev`, `staging`, `prod`) and per team or service

If you are hosting more than a handful of accounts, you need an orchestration layer that handles account deployment and governance. Control Tower is the right choice for that.

The Organisational Unit (OU) hierarchy is where most architects get into trouble. Keep it shallow. Deeply nested OUs make SCP inheritance difficult to reason about and create opportunities for guardrail gaps. A practical structure for a mid-size regulated organisation looks like:

```
Root
├── Security OU
│   ├── Log Archive account
│   └── Audit account
├── Infrastructure OU
│   ├── Network account (Transit Gateway, shared VPCs)
│   └── Shared Services account
├── Workloads OU
│   ├── Production OU
│   └── Non-Production OU
└── Sandbox OU
```

The Sandbox OU should have more permissive guardrails to allow experimentation, but must be denied access to any production data sources via SCP.

<!-- INTERNAL_LINK: Cloud identity and access management foundations | cloud-identity-and-access-management -->

## Guardrails: preventive, detective, and declarative

There are three guardrail types worth understanding properly, because the distinction shapes how you design your control environment.

Preventive guardrails use SCPs to block non-compliant actions before they happen. A well-scoped preventive guardrail will block IAM actions that allow privilege escalation, such as attaching administrator policies to roles or creating overly permissive IAM users. Because SCPs operate at the organisation level, individual account administrators cannot bypass them. That is the point.

Detective guardrails use AWS Config rules to surface non-compliance after the fact. They do not stop anything; they tell you something happened. Treat them as your visibility layer, not your enforcement layer.

Declarative guardrails are the newest addition, reaching general availability in December 2024. These policies enforce a desired service configuration and, critically, remain in effect regardless of new APIs or new principals being added to the account. That last behaviour closes a real gap. SCPs alone cannot fully plug every privilege path when AWS releases new service features. Declarative policies can.

A practical example of a preventive SCP that denies actions outside your governed regions, deployable at the Root or Workloads OU level:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonEURegions",
      "Effect": "Deny",
      "NotAction": [
        "acm:*",
        "iam:*",
        "cloudfront:*",
        "route53:*",
        "sts:*",
        "support:*",
        "trustedadvisor:*",
        "waf:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "eu-west-1",
            "eu-west-2",
            "eu-central-1"
          ]
        }
      }
    }
  ]
}
```

Global services (IAM, CloudFront, Route 53, STS) are explicitly excluded via `NotAction`. Failing to do this is a common cause of lockouts. Apply this at the Workloads OU level rather than Root to avoid breaking Control Tower's own management operations.

<!-- INTERNAL_LINK: AWS IAM best practices and least privilege | aws-iam-best-practices -->

## Account Factory for Terraform (AFT): industrialising account vending

Manually clicking through the Control Tower console to create accounts is fine for your first five. Beyond that, it becomes a bottleneck and an audit headache.

AFT adopts a GitOps model that automates account provisioning and updating in Control Tower. You create an account request Terraform file, which triggers the AFT workflow. Once provisioning completes, the workflow continues through the AFT account provisioning framework and into account customisations. For organisations already using Terraform for infrastructure, this keeps account requests in the same workflow as everything else and makes per-account customisations straightforward.

A minimal AFT account request looks like this:

```hcl
module "my_workload_prod" {
  source = "./modules/aft-account-request"

  control_tower_parameters = {
    AccountEmail              = "aws-prod-payments@example.co.uk"
    AccountName               = "payments-prod"
    ManagedOrganizationalUnit = "Workloads/Production"
    SSOUserEmail              = "platform-team@example.co.uk"
    SSOUserFirstName          = "Platform"
    SSOUserLastName           = "Team"
  }

  account_tags = {
    Environment  = "prod"
    CostCentre   = "PAYMENTS"
    DataClass    = "CONFIDENTIAL"
    Owner        = "payments-team@example.co.uk"
  }

  change_management_parameters = {
    change_requested_by = "Steve Harrison"
    change_reason       = "New production account for payments service"
  }

  account_customizations_name = "payments-prod-customizations"
}
```

AFT uses a layered customisation model. Account provisioning customisations run before global customisations. Global customisations apply to every account AFT manages. Account customisations apply only to specific accounts. In practice this means you can enforce organisation-wide baselines (Security Hub standards, GuardDuty enablement, centralised logging subscription filters) while still allowing team-specific resources to be provisioned automatically at account creation.

<!-- INTERNAL_LINK: DevsSecOps and shift-left security pipelines | devsecops-shift-left-security -->

## Landing Zone Accelerator: going beyond Control Tower defaults

For highly regulated workloads, Control Tower's out-of-the-box configuration is a starting point, not a finish line. The Landing Zone Accelerator on AWS (LZA) fills the gap.

AWS recommends deploying Control Tower as the foundational landing zone and then extending it with LZA. Together they cover 35+ AWS services and are designed to support organisations with complex compliance requirements. LZA is delivered as an open-source project built with the AWS Cloud Development Kit (CDK), installed directly into your environment so you have full access to the underlying infrastructure as code.

For UK practitioners, the NCSC alignment is particularly relevant. AWS worked with the NCSC to tailor guidance on how UK public sector customers can use LZA to meet the NCSC's "using cloud services securely" guidance. The LZA documentation covers all 14 NCSC Cloud Security Principles, from data in transit protection and asset protection through to audit information and alerting.

The LZA Universal Configuration, released in November 2025, is worth noting separately. It is the first sample configuration accompanied by the LZA Compliance Workbook, available on AWS Artifact. The workbook includes detailed control mappings for NIST 800-53 Rev5, CMMC/NIST 800-171, ISO-27001, HIPAA, C5:2020, NATO D-32 (Appendix B), and DoD CCI. For organisations going through formal assessment and authorisation cycles, having pre-mapped evidence can reduce timelines materially.

One caveat worth being direct about: LZA will not make you compliant. It provides the foundational infrastructure from which additional solutions can be integrated. Think of it as an accelerant, not a certification.

<!-- INTERNAL_LINK: Cloud compliance frameworks overview | cloud-compliance-frameworks -->
<!-- INTERNAL_LINK: AWS KMS key management best practices | aws-kms-key-management-best-practices -->

## Landing Zone 4.0: what changed and why it matters

AWS made Landing Zone 4.0 generally available in November 2025, introducing a significant architectural overhaul. The main change is a move to dedicated resources per service, rather than shared ones. AWS Config, CloudTrail, SecurityRoles, and AWS Backup integrations can now be selectively enabled, and each gets its own dedicated resources rather than sharing infrastructure. This improves isolation and reduces the risk of one component's configuration affecting another.

The version also removes previous constraints on the control catalogue, giving you access to over 750 controls from AWS Control Catalog without restructuring your existing organisation.

If you are upgrading from 3.x, be clear on one hard constraint: there is no rollback. Once you upgrade to Landing Zone 4.0, you cannot revert to version 3.x. Test the upgrade in a non-production environment first, and take comprehensive backups before you start.

Running on 3.x indefinitely will limit your access to new controls and the improved isolation model. Plan the upgrade, but do not do it on a Friday afternoon.

<!-- INTERNAL_LINK: Cloud threat detection and Security Hub | cloud-threat-detection -->

## Common pitfalls

These are the failure modes I see repeatedly across client engagements. Most are avoidable with disciplined process.

### 1. Making changes outside Control Tower

If you change accounts, OUs, or Control Tower-managed SCPs directly in the AWS Organizations console, you will cause drift. Control Tower detects drift automatically, but detecting it is not the same as fixing it. Treat drift as an incident, not a maintenance task. Review your landing zone regularly and remediate promptly.

### 2. Granting broad access to the management account

Almost all routes that lead to Control Tower drift run through the management account, where Control Tower lives alongside AWS Organizations and the services that vend accounts. The management account should have break-glass access only. Your platform team's day-to-day operations should happen from the Audit account or a dedicated tooling account, with IAM constrained to only what each role genuinely needs.

### 3. Overly broad preventive guardrails

Preventive guardrails that are too broadly scoped will block legitimate workflows and cause operational disruption. I have seen teams lock themselves out of entire service categories by applying a region-restriction SCP at Root without accounting for global services. Always test new SCPs in a Sandbox OU before applying them to production workload OUs.

### 4. Neglecting KMS encryption for the logging account

AWS strongly recommends creating a KMS customer managed key before deploying your landing zone. This key is used to encrypt sensitive log files managed by Control Tower. Beyond initial setup, landing zone upgrades can fail because of KMS key policy misconfigurations. This is one of the most common support escalations I see from clients upgrading between landing zone versions.

<!-- INTERNAL_LINK: AWS KMS key management best practices | aws-kms-key-management-best-practices -->

### 5. Treating LZA as a compliance silver bullet

The compliance workbook maps controls to frameworks; it does not operate them for you. Shared responsibility still applies. Your security team must maintain detective controls, triage Security Hub findings, and conduct regular access reviews. None of that is automated by the landing zone itself.

<!-- INTERNAL_LINK: Cloud security vulnerability management | cloud-security-vulnerability-management -->
<!-- INTERNAL_LINK: Cloud incident response planning | cloud-incident-response -->

### 6. Skipping the upgrade to Landing Zone 4.0 indefinitely

Running on 3.x keeps you away from the improved isolation model and limits your access to the full control catalogue. The upgrade has a cost in planning and testing time, but the longer you leave it, the larger the delta becomes. Plan it properly; just do not keep deferring it.

## Key takeaways

- Control Tower is the orchestration engine; the landing zone is the multi-account environment it produces. Treat the outcome, not the console, as your success metric.
- Preventive SCPs, detective Config rules, and declarative policies each do different things. Use all three rather than relying on any one type. Together they give you hard blocks, visibility, and future-proof enforcement.
- AFT is the right account vending mechanism for Terraform-first teams. Its GitOps model removes the manual touchpoints that create inconsistency and audit gaps.
- The LZA Universal Configuration and Compliance Workbook are material for regulated industries. Available from AWS Artifact, the workbook provides auditable control mappings across ISO-27001, C5:2020, NIST 800-53 Rev5, and other major frameworks.
- Drift is your biggest operational risk post-deployment. Never change Control Tower-managed resources outside the Control Tower console, lock down management account access, and treat any drift notification as requiring same-day resolution.
- For UK public sector and regulated financial services, LZA's NCSC alignment across all 14 Cloud Security Principles makes it the most coherent starting point for organisations subject to G-Cloud procurement or FCA operational resilience requirements. It does not replace your own risk assessment or ongoing security operations.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: What is CSPM cloud security posture management | what-is-cspm-cloud-security-posture-management -->