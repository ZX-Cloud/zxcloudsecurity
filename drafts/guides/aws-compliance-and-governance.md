---
title: "AWS Compliance and Governance: A Practitioner's Guide for 2026"
date: 2026-06-27
description: "A practical guide to AWS compliance and governance for architects and engineers — covering SCPs, Config Rules, NCSC alignment, and common pitfalls."
tags: ["aws compliance and governance", "aws organizations", "service control policies", "aws config", "cloud security", "ncsc", "fedramp", "gdpr"]
slug: "aws-compliance-and-governance-guide"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2629
draft: false
---

# AWS compliance and governance: a practitioner's guide for 2026

If you are running workloads in AWS today, whether for a UK financial services firm, a central government department, or a regulated SaaS business, AWS compliance and governance is not a configuration task you complete once and forget. It is a continuous discipline that now spans AI models, agentic developer tooling, multi-account organisational structure, and real-time detective controls. The compliance surface keeps expanding, and the pace of AWS service releases means your governance posture can drift within weeks of a major deployment. This guide gives you a structured, opinionated approach based on what actually works in production.

---

## Why the stakes are higher than ever

Securing AWS in 2026 depends on continuous, risk-based governance rather than isolated tools or point-in-time checks. Most cloud security incidents stem from customer-side issues: identity misuse, misconfigurations, and exposed workloads.

With the AWS shared responsibility model placing identity, configuration, and workload protection squarely on customers, misconfigurations and permission creep now drive most incidents. That is the uncomfortable truth that too many organisations acknowledge in theory and ignore in practice.

For UK practitioners, the regulatory landscape compounds this. GDPR enforcement is active, the FCA's operational resilience rules have teeth, and the NCSC publishes actionable cloud security guidance that government and regulated-sector buyers are increasingly expected to evidence compliance against. Meanwhile, AWS itself is moving fast: just in the last few weeks of June 2026, OpenAI GPT, OpenAI GPT OSS, and NVIDIA Nemotron models received FedRAMP High and DoD IL-4/5 approval within Amazon Bedrock in the AWS GovCloud (US) regions, and Kiro, AWS's agentic IDE and CLI, achieved FedRAMP High and DoD CC SRG IL-4/5 authorisation in the same regions.

The compliance boundary is no longer just your VPCs and IAM policies. It now includes the AI and developer tooling your engineers reach for every day.

---

## Understanding the foundation: shared responsibility and the GRC model

Governance, Risk Management, and Compliance (GRC) helps organisations set the foundation for meeting security and compliance requirements and defines the overall policies your cloud environment should adhere to.

This model, underpinned by a clear understanding of your security responsibilities in the cloud, forms the basis for your organisation's GRC posture. Establishing that posture early means defining roles, risk-based requirements, and compliance obligations before you start building, not after.

Practically, this means defining a RACI before you write a single SCP. Who owns the security tooling account? Who approves new AWS services for production use? Who reviews the AWS Config conformance pack findings each sprint? If these questions do not have named answers in your organisation, your governance posture is fictional.

You also need to confirm which risk and compliance frameworks apply, and how your environment will meet those requirements on an ongoing basis. For UK organisations this typically means mapping to: NCSC 14 Cloud Security Principles, ISO 27001/27017, Cyber Essentials Plus, and, for financial services, FCA SYSC 8 and the DORA-adjacent operational resilience requirements.

<!-- INTERNAL_LINK: AWS Shared Responsibility Model explained | aws-shared-responsibility-model -->

---

## The AWS compliance programme: what AWS covers and what you do not

AWS supports 143 security standards and compliance certifications, including PCI-DSS, HIPAA/HITECH, FedRAMP, GDPR, FIPS 140-2, and NIST 800-171. The AWS Compliance Programme helps customers understand the controls in place at AWS and ties governance-focused, audit-friendly service features to applicable compliance standards.

None of that is a substitute for your own controls. Compliance certifications and attestations are assessed by a third-party, independent auditor and result in a certification, audit report, or attestation of compliance. AWS customers remain responsible for complying with applicable compliance laws, regulations, and privacy programmes.

Use AWS Artifact to pull down the reports you need for your own audit evidence packs: SOC 2 Type II, ISO 27001 certificates, PCI DSS Attestation of Compliance. These are the artefacts your auditors want to see as the AWS-side evidence. Your side of the ledger still needs Config rules, CloudTrail, GuardDuty findings, and IAM access reviews.

### NCSC cloud security principles and AWS

For UK public sector and regulated-sector organisations, the NCSC's 14 Cloud Security Principles remain the most relevant framework. AWS has designed and manages its infrastructure in alignment with best security practices and IT security standards that map to these principles, and publishes a companion whitepaper, "Using AWS in the Context of NCSC UK's Cloud Security Principles", which is worth reading before your next audit conversation.

AWS provides conformance packs through AWS Config that map to the NCSC Cloud Security Principles, which gives you immediate visibility of gaps against Principles 1 through 14. Deploy the `Operational-Best-Practices-for-NCSC` conformance pack as your starting point.

AWS has also collaborated with the NCSC to tailor advice on how UK public sector customers can use the Landing Zone Accelerator on AWS (LZA) to meet the NCSC's guidance on using cloud services securely. If you are standing up a new environment for a government or regulated client, the LZA is worth evaluating seriously as a baseline. It compresses months of foundational work.

<!-- INTERNAL_LINK: AWS Landing Zone Accelerator for UK Public Sector | aws-landing-zone-accelerator-uk -->

---

## Preventive controls: service control policies and resource control policies

SCPs are the single most powerful preventive governance tool in AWS. Service control policies offer central control over the maximum available permissions for IAM users and roles in an organisation. They are your hard guardrails: the things that simply cannot happen regardless of what an individual account's IAM policies permit.

Resource Control Policies (RCPs) are a sibling policy type introduced by AWS in November 2024. They cover resource-side governance use cases that SCPs cannot fully handle, particularly for services like S3, STS, KMS, Secrets Manager, and SQS. An RCP can enforce that an S3 bucket may only be accessed by principals from within your organisation, regardless of how the bucket's own resource policy is configured.

If you are designing org-wide guardrails in 2026, understand both. SCPs handle the "who can do what" question. RCPs handle the "who can touch this resource" question. Used together, they close gaps that neither could close alone.

### Data residency SCP: locking workloads to `eu-west-2`

The most common first SCP I deploy for UK clients is a region restriction. Restricting resource creation to your approved operational regions only enforces data residency requirements and limits the blast radius during security incidents.

For a UK-only estate, adapt as follows:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonUKRegions",
      "Effect": "Deny",
      "NotAction": [
        "iam:*",
        "organizations:*",
        "route53:*",
        "budgets:*",
        "waf:*",
        "cloudfront:*",
        "sts:*",
        "support:*",
        "account:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "eu-west-2"
          ]
        }
      }
    }
  ]
}
```

The `NotAction` block is critical. Global services, IAM, Route 53, CloudFront, STS, operate outside regions. If you forget to exempt them, you will break IAM role creation and your Route 53 hosted zones immediately. Test this in a sandbox OU first, every time.

A second SCP every UK organisation should have from day one prevents CloudTrail from being disabled or tampered with:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ProtectCloudTrail",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:DeleteTrail",
        "cloudtrail:StopLogging",
        "cloudtrail:UpdateTrail",
        "cloudtrail:PutEventSelectors"
      ],
      "Resource": "*"
    }
  ]
}
```

This SCP prevents users or roles in any affected account from disabling a CloudTrail log, whether directly via CLI or through the console. For regulated industries, immutable audit logs are non-negotiable. This SCP enforces that at the organisational level rather than leaving it as an afterthought in individual accounts.

<!-- INTERNAL_LINK: AWS Organizations multi-account strategy | aws-organizations-multi-account-strategy -->

---

## Detective controls: AWS Config, Security Hub, and continuous compliance

Preventive controls stop the bad thing. Detective controls tell you when the bad thing has already happened, or is happening. The pairing of AWS Config and AWS Security Hub is the standard approach, and it works well when configured correctly.

AWS CloudTrail logs, monitors, and retains AWS API activity, giving you visibility into actions taken within your accounts and supporting compliance analysis. AWS Config assesses, audits, and evaluates the configurations of your AWS resources, which is how you track drift against your security policies.

AWS Control Tower sits above both and provides a centralised framework for managing multiple AWS accounts, enforcing security policies, and configuring preventive and detective guardrails. In practice, I use Config conformance packs mapped to the frameworks that matter to the client: the NCSC pack for UK government work, the PCI DSS pack for financial services, or the CIS AWS Foundations Benchmark as a general-purpose baseline.

The Config Aggregator in your security or audit account is where everything surfaces. Reviewing compliance findings account-by-account will burn out your team and cause things to be missed. Get everything into the aggregator and set up alerting that routes to someone who will actually act on it.

---

## AI services, FedRAMP, and what it means for UK architects

You might be wondering why a guide on AWS compliance and governance is discussing FedRAMP. Because the compliance posture of the AI services your teams are reaching for directly affects your own GRC position, and because the US public sector compliance regime is increasingly the leading indicator for what regulated enterprises globally demand.

OpenAI GPT, OpenAI GPT OSS, and NVIDIA Nemotron models are now FedRAMP High and DoD CC SRG Impact Level 4 and 5 approved within Amazon Bedrock in the AWS GovCloud (US) regions. Federal agencies, public sector organisations, and enterprises with those compliance requirements can now use these models to build generative AI applications with confidence they meet the required security standards.

Kiro is now FedRAMP High and DoD CC SRG IL-4/5 authorised in the same regions, meaning it can be used as an agentic engineering environment where those compliance requirements apply.

For UK architects, the practical implication is straightforward. If your engineers are using Bedrock-powered AI services or agentic tooling like Kiro, you need to understand the data classification of the prompts and generated artefacts those tools process. Content collection for service improvement, including prompts, responses, and generated code, is disabled by default in the AWS GovCloud (US) regions. UK deployments typically require contractual GDPR Article 28 processor agreements and data residency assurance. Check the current AWS Data Processing Addendum and the model-specific data handling documentation carefully before your teams start using these services at scale.

<!-- INTERNAL_LINK: Securing Amazon Bedrock for enterprise workloads | securing-amazon-bedrock-enterprise -->

---

## Common governance pitfalls to avoid

These are the mistakes I see repeatedly in production AWS environments, usually discovered during an audit or an incident.

### 1. SCPs not applied to the management account

SCPs do not affect users or roles in the management account. They apply only to member accounts in your organisation. This means your management account is ungoverned by SCPs, and it is the account attackers most want access to. Lock it down with strict IAM policies, enable MFA on the root user, and use it only for billing and organisational management. Never deploy workloads there.

### 2. Treating Config as optional

Teams often enable Config in their primary region and forget about it everywhere else. Config must be enabled in every active region, in every account, with multi-region trails. Add an SCP that prevents anyone from disabling Config or altering its rules. Then verify Config is actually running before you rely on its findings.

### 3. Conflating AWS's compliance certifications with your own

Most security failures in AWS occur not because the shared responsibility model is unclear, but because it is underestimated. A secure AWS platform does not automatically result in a secure AWS environment. AWS's ISO 27001 certificate covers the infrastructure, not your application code, your S3 bucket permissions, or your Lambda execution roles.

### 4. Deploying SCPs without testing

AWS recommends you do not attach SCPs to the root of your organisation without thoroughly testing the impact first. Create an OU, move accounts into it one at a time, and verify behaviour before you go wider. I have seen region-restriction SCPs break CI/CD pipelines because the IAM role for the build agent was not explicitly exempted. Test in a sandbox OU, then an isolated dev OU, before touching prod.

### 5. No tagging strategy at governance inception

Tagging enables you to group resources by assigning metadata for access control (ABAC), cost reporting, and automation. If you do not enforce mandatory tags via Config rules or AWS Tag Policies from the start, you will spend the next two years trying to retroactively tag 10,000 resources before your next FCA audit. Enforce tags at resource creation.

### 6. Forgetting that SCPs do not grant permissions

SCPs do not grant permissions to the IAM users and roles in your organisation. An SCP defines a permission guardrail, or sets a ceiling, on the actions that users and roles can perform. A common mistake is trying to use an SCP as an allow-list in isolation. You still need IAM policies. SCPs are the ceiling, not the floor.

---

## Key takeaways

- Governance is a continuous process, not a project. Automate your detective controls and set up alerting that someone actually reviews on a regular cadence.

- Deploy SCPs and RCPs as a pair. SCPs control what principals can do; RCPs control what can be done to resources. Both are necessary for a complete data perimeter in 2026.

- Map to NCSC 14 Principles for UK work. Use the AWS Config NCSC conformance pack to get baseline detective coverage aligned to the framework your clients and auditors actually reference. Supplement with the Landing Zone Accelerator for new environments.

- AI and agentic tooling are now in scope for governance. The FedRAMP High authorisation of Bedrock models and Kiro sets the bar globally. Before your developers adopt any Bedrock-powered service, verify the data handling terms, check GDPR Article 28 compliance, and confirm data residency within `eu-west-2` where applicable.

- Test SCPs destructively before promoting. A misconfigured SCP can silence an entire OU. Use sandbox OUs, the IAM Policy Simulator, and CloudTrail to validate behaviour before wider rollout.

- Your organisation's certifications live in AWS Artifact. Pull these as standard practice for audit evidence packs. They cover AWS's half of the shared responsibility model. Your Config findings, CloudTrail logs, and IAM access reviews cover yours.