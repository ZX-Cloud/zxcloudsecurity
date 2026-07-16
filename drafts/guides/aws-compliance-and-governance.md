---
title: "AWS Compliance and Governance: A Practitioner's Guide for 2026"
date: 2026-07-16
description: "A practical guide to AWS compliance and governance covering SCPs, RCPs, Config conformance packs, NCSC alignment, and common pitfalls to avoid."
tags: ["aws compliance and governance", "service control policies", "aws config", "aws organizations", "cloud compliance", "security guardrails"]
slug: "aws-compliance-and-governance-guide"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2265
draft: false
---

# AWS compliance and governance: a practitioner's guide for 2026

If you're running workloads in AWS for UK financial services, government, or any enterprise that faces a regulator, AWS compliance and governance is no longer a project you do before an audit. It is continuous, automated, and woven into your account structure from day one. Most breaches now originate from identity misuse, configuration drift, and exposed services rather than flaws in the underlying infrastructure. The implication is that cloud security has to shift from periodic validation to real-time governance, with risk-driven insight taking priority over blanket control compliance. This guide gives you a working architecture for governance at scale: organisational guardrails, continuous compliance monitoring, evidence automation, and the mistakes that quietly erode your security posture between audits.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->

---

## Why governance matters more than certifications

There is a persistent confusion between AWS being compliant and your workloads being compliant. The AWS Shared Responsibility Model is a contract, not a safety net. AWS is accountable for securing the cloud itself: physical facilities, hardware, networking, and the virtualisation layer. You are accountable for everything built on top: operating systems, network exposure, identities, access policies, applications, data, and compliance controls.

AWS maintains a broad portfolio of security standards and compliance certifications, including PCI-DSS, HIPAA/HITECH, FedRAMP, and GDPR, alongside FIPS 140-2/140-3 validation for specific cryptographic modules and endpoints and a NIST 800-171 compliance mapping. That breadth is genuinely useful when an auditor asks for platform-level evidence. But none of those certifications prevent you from creating an unencrypted S3 bucket, attaching an overly permissive IAM policy, or leaving GuardDuty disabled in a region you forgot you provisioned resources into.

For UK practitioners there is an additional layer. AWS EMEA Sarl has been designated as a critical third party (CTP) to the UK financial sector by HM Treasury. That designation means your FCA-regulated firm's reliance on AWS now sits under the UK's own critical third-party oversight regime, run by HM Treasury, the PRA, the FCA, and the Bank of England under powers introduced by the Financial Services and Markets Act 2023. It is only thematically similar to the EU's DORA, not legally connected to it. You need contractual controls, exit plans, and continuous visibility into the security posture of your own workloads. AWS provides the tools; the responsibility for using them lands squarely with you.

<!-- INTERNAL_LINK: cloud compliance frameworks overview | cloud-compliance-frameworks -->

---

## The governance control plane: AWS Organizations, SCPs, and RCPs

### Service control policies

Service control policies (SCPs) give you central control over the maximum available permissions for IAM users and roles across an organisation. An SCP does not grant permissions. It defines a guardrail, setting limits on what IAM principals in your organisation can do.

`NotAction` specifies what is not covered by the policy and is useful for broad permissions with specific exceptions; it has long been usable in Deny statements. In September 2025, AWS Organizations extended SCPs to support the full IAM policy language, adding conditions, individual resource ARNs, wildcards at the beginning, middle, or end of the Action string, and the ability to use `NotAction` in Allow statements as well. Treat that Allow-plus-NotAction capability with caution: an Allow-effect SCP using `NotAction` still cannot grant anything beyond what IAM already permits, and mixing Allow/NotAction statements with Deny baselines in the same policy set is a common source of confusing, hard-to-reason-about evaluation outcomes. Scope any Allow-list SCP narrowly and test it in isolation before combining it with your Deny baselines.

A baseline SCP that every production OU should carry is a hard deny on disabling your core security services. Here is a production-ready example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyDisableSecurityServices",
      "Effect": "Deny",
      "Action": [
        "guardduty:DeleteDetector",
        "guardduty:DisassociateFromAdministratorAccount",
        "securityhub:DisableSecurityHub",
        "config:DeleteConfigurationRecorder",
        "config:StopConfigurationRecorder",
        "cloudtrail:DeleteTrail",
        "cloudtrail:StopLogging"
      ],
      "Resource": "*",
      "Condition": {
        "ArnNotLike": {
          "aws:PrincipalARN": [
            "arn:aws:iam::*:role/SecurityBreakGlassRole"
          ]
        }
      }
    },
    {
      "Sid": "DenyLeaveOrganisation",
      "Effect": "Deny",
      "Action": "organizations:LeaveOrganization",
      "Resource": "*"
    },
    {
      "Sid": "DenyUnencryptedS3Objects",
      "Effect": "Deny",
      "Action": "s3:PutObject",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedRDSInstances",
      "Effect": "Deny",
      "Action": "rds:CreateDBInstance",
      "Resource": "*",
      "Condition": {
        "Bool": {
          "rds:StorageEncrypted": "false"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedEBSVolumes",
      "Effect": "Deny",
      "Action": "ec2:CreateVolume",
      "Resource": "*",
      "Condition": {
        "Bool": {
          "ec2:Encrypted": "false"
        }
      }
    }
  ]
}
```

If an attacker gains control of an account, they should not be able to remove it from the organisation, which would strip away all SCP restrictions. The `DenyLeaveOrganisation` statement is non-negotiable. Notice also the `SecurityBreakGlassRole` exception. Without a surgical carve-out like this, your own security team cannot remediate a compromised GuardDuty configuration during an incident.

Notice, too, that each encryption deny statement uses a condition key that is actually evaluated for that service's API call. `s3:x-amz-server-side-encryption` only applies to S3 object-level requests such as `s3:PutObject`, so it belongs on that action rather than on `s3:CreateBucket`, which carries no such header. Bucket-level default encryption is better enforced through a bucket policy or an AWS Config rule. RDS and EBS have their own service-specific condition keys, `rds:StorageEncrypted` and `ec2:Encrypted`, and an SCP that reuses the S3 condition key against those services will simply never evaluate to true, silently failing to enforce anything.

One operational detail that catches teams out: SCPs do not apply to the management account. Never run workloads there, and test all SCPs against member accounts only.

<!-- INTERNAL_LINK: AWS CloudTrail configuration best practices | aws-cloudtrail-configuration-best-practices -->

### Resource control policies: the data perimeter layer

Resource control policies (RCPs) are an authorisation policy type managed in AWS Organizations that set the maximum available permissions on resources across your entire organisation. Where SCPs constrain what IAM principals can do, RCPs constrain who can access a given resource regardless of what that resource's own policy says.

The practical difference matters. An RCP can enforce the invariant that no S3 bucket in your organisation can ever be accessed by a principal outside the organisation, even if a developer writes a permissive bucket policy. That kind of hard guarantee is exactly what the FCA's operational resilience rules and the NCSC's data security principles both point toward. SCPs and RCPs are complementary controls, not alternatives. Deploy both.

<!-- INTERNAL_LINK: what is CIEM | what-is-ciem-cloud-infrastructure-entitlement-management -->

---

## Continuous compliance with AWS Config and conformance packs

A conformance pack is a collection of AWS Config rules and remediation actions deployed as a single entity, either into an individual account and region or across an organisation via AWS Organizations. You author them as YAML templates listing the Config managed or custom rules you want to enforce.

For UK practitioners, AWS provides a sample mapping between the NCSC Cloud Security Principles and AWS managed Config rules, and a separate mapping covering the NCSC Cyber Assessment Framework (CAF). Each Config rule maps to one or more NCSC controls, and a single NCSC control can map to multiple Config rules. This is the kind of pre-built alignment that saves weeks of manual mapping work before an audit.

Deploy your NCSC CAF conformance pack via the AWS CLI as part of a pipeline step:

```bash
# Deploy the NCSC CAF conformance pack across your organisation
aws configservice put-organization-conformance-pack \
  --organization-conformance-pack-name "NCSC-CAF-Baseline" \
  --template-s3-uri "s3://your-governance-bucket/ncsc-caf-conformance-pack.yaml" \
  --delivery-s3-bucket "your-config-delivery-bucket" \
  --excluded-accounts "111122223333"   # Exclude management account

# Check pack status across member accounts
aws configservice describe-organization-conformance-pack-statuses \
  --organization-conformance-pack-names "NCSC-CAF-Baseline"
```

Conformance packs can be deployed across multiple accounts via AWS Organizations, giving you consistency across your estate. Once deployed, they generate compliance reports showing which rules are passing or failing. Treat that score as a leading indicator, not a compliance certificate. AWS is explicit that conformance packs are not designed to fully ensure compliance with any specific regulatory standard. The assessment of whether your use of AWS meets applicable legal requirements remains your responsibility.

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->

---

## Operationalising governance: from tools to security operations

Enabling the tooling is the easy part. Getting to the point where findings drive decisions, response times are measurable, and your posture actually improves week over week is where most organisations struggle.

AWS Security Blog guidance for organisations that have already enabled AWS Security Hub and Amazon GuardDuty sets out a phased maturity path covering tuning, notifications, automated remediation, and operational cadence. The core message matches what I see consistently across regulated UK engagements: a tuned environment with working notifications and a weekly review cadence outperforms a fully featured but neglected deployment by a significant margin.

For AWS compliance and governance to function as an operational discipline rather than an audit artefact, you need three things. First, a delegated administrator account for Security Hub and Config that is separate from the management account and from your workload accounts. Second, weekly findings triage with clear SLA ownership: critical findings resolved within 24 hours, high severity within 72 hours. Third, a quarterly capability review. AWS releases new detection and compliance capabilities on a regular basis. If you are not reviewing them quarterly, you are accumulating blind spots.

### Evidence automation with OSCAL

AWS has begun releasing SOC 1 and SOC 2 reports in machine-readable OSCAL format alongside the PDF version. AWS is the first major cloud provider to offer compliance reports to customers in NIST's Open Security Controls Assessment Language. The SOC report package in OSCAL format is available as a distinct package in AWS Artifact; check Artifact directly for the current report period and scope of services covered.

For FCA-regulated firms with Compliance as Code ambitions, this is worth paying attention to. The machine-readable SOC package means you can ingest AWS's own platform-level evidence programmatically into GRC platforms, audit workflows, or custom control dashboards. That removes a meaningful chunk of manual evidence-gathering work. Build this pipeline before your next audit cycle, not during it.

<!-- INTERNAL_LINK: cloud compliance frameworks | cloud-compliance-frameworks -->

---

## AI and the evolving governance surface

Governance does not stop at infrastructure. AWS has published guidance on Governance, Risk, and Compliance for Responsible AI Adoption aimed at FSI customers, covering governance, risk management, compliance, data management, model management, and AI agent management.

If your teams are using Amazon Bedrock, Amazon Q Developer, or third-party AI tooling integrated with AWS services, your governance framework needs to account for data residency of model inputs, least-privilege for AI agent IAM roles, and audit trails of agentic actions. This area is moving quickly. The NCSC's guidance on AI security and the FCA's emerging AI governance expectations will increasingly converge with your existing AWS governance controls. Do not treat AI workloads as out of scope for your current framework.

<!-- INTERNAL_LINK: securing AI agents in cloud infrastructure | securing-ai-agents-cloud-infrastructure -->

---

## Common pitfalls in AWS compliance and governance

These are the mistakes I see repeatedly in regulated environments. Every one of them has produced a real audit finding or a real incident.

### 1. Conflating AWS compliance with workload compliance

AWS's SOC 2 or ISO 27001 certification does not extend to your application tier. Most security failures in AWS occur not because the shared responsibility model is unclear, but because it is underestimated. A secure AWS platform does not automatically result in a secure AWS environment.

### 2. Running workloads in the management account

SCPs do not apply to the management account. Any workload running there operates outside your organisational guardrails. Keep it empty: billing, organisation management, and nothing else.

### 3. Building controls before building evidence management

Teams often build controls before they build evidence management. That is backwards for audit readiness. If you cannot demonstrate that a control exists and is continuously evaluated, an auditor will treat it as absent.

### 4. Config not enabled before Security Hub

Security Hub controls depend on AWS Config for resource evaluation. If Config is not enabled or is not recording all resource types, controls show NOT_AVAILABLE status and your security score is inaccurate. Verify Config is active and recording before enabling Security Hub standards.

### 5. Leaving regions unmonitored

Attackers target regions where monitoring is absent. Use central configuration with `ALL_REGIONS` to ensure coverage, including regions you do not actively use for workloads. This is a consistent pattern in AWS CIRT incident response engagements: attackers provision compute in quiet regions precisely because nobody is watching.

### 6. Not testing SCPs before broad rollout

AWS strongly recommends not attaching SCPs to the root of your organisation without thoroughly testing the impact on accounts first. Create an OU, move accounts into it one at a time, and verify behaviour before applying any SCP more broadly. Locking users out of services they depend on is an entirely avoidable incident.

### 7. Ignoring the threat technique catalog

The AWS Threat Technique Catalog covers areas such as container security, organisation-level trust abuse, and compute hijacking. Each entry reflects something the AWS CIRT has encountered in production, and each provides concrete mitigation steps. Running governance controls without feeding current threat intelligence into your detection rules is security theatre.

<!-- INTERNAL_LINK: cloud threat detection | cloud-threat-detection -->

---

## Key takeaways

AWS compliance and governance is continuous, not periodic. An annual audit posture is not a security posture.

SCPs and RCPs are complementary controls. Use SCPs to constrain what IAM principals can do; use RCPs to constrain how your resources can be accessed. Deployed together, they give you a genuine data perimeter, which is a hard requirement for UK financial services data handling.

Map your Config conformance packs to NCSC CAF controls. AWS provides the mapping templates. Deploy them via your organisation pipeline so every new account inherits the same baseline from day one.

Evidence automation is now viable. With AWS SOC reports available in OSCAL format via AWS Artifact, you can programmatically ingest platform-level evidence into your GRC workflows. Build this before your next audit cycle.

Operationalise your security tooling. Enabling GuardDuty and Security Hub is the starting point. The goal is to move from "these services are active" to "these services are driving our security operations." That requires documented cadence, ownership, and SLAs, not just activated dashboards.

Keep your governance scope current. AI workloads, new regions, and novel attack techniques such as organisation-level trust abuse and container workload modification all expand the governance surface. Quarterly reviews of new AWS capabilities and the AWS Threat Technique Catalog are not optional if you operate in a regulated sector.

<!-- INTERNAL_LINK: AWS Well-Architected security pillar | aws-well-architected-security -->
<!-- INTERNAL_LINK: what is CSPM | what-is-cspm-cloud-security-posture-management -->
<!-- INTERNAL_LINK: cloud identity and access management | cloud-identity-and-access-management -->