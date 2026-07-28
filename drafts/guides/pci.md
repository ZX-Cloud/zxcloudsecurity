---
title: "PCI DSS 4.0 on AWS: A Practitioner's Guide to Cloud Compliance"
date: 2026-07-28
description: "A practical guide to achieving PCI DSS 4.0 compliance on AWS — covering scope, segmentation, MFA, WAF, logging, and the most common pitfalls."
tags: ["pci", "pci-dss", "aws", "cloud-compliance", "financial-services", "security"]
slug: "pci-dss-aws-compliance-guide"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 1770
draft: false
---

# PCI DSS 4.0 on AWS: a practitioner's guide to cloud compliance

If your organisation stores, processes, or transmits payment card data on AWS, PCI compliance is no longer something you can treat as a periodic audit exercise. As of 31 March 2025, all requirements of PCI DSS 4.0 are mandatory. This isn't just another version increment — it represents a genuine change in how payment security is assessed, particularly in cloud environments.

The 64 requirements that organisations could previously treat as best practices are now fully enforceable, and assessors are scrutinising every control. For teams running payment workloads on AWS, the platform offers genuinely strong tooling for PCI compliance. The problem is that most of the failure modes I see in the field are self-inflicted: misconfigured services, scope creep, and a fundamental misreading of what AWS actually takes responsibility for.

This guide is aimed at cloud security architects and senior engineers who need a technically grounded picture of how to approach PCI on AWS right now.

<!-- INTERNAL_LINK: shared responsibility model primer | shared-responsibility-model-cloud-security -->

## Understanding what AWS actually covers

Before touching a single control, you need to internalise the shared responsibility boundary. AWS holds PCI DSS Level 1 Service Provider certification, the highest level of assessment available. That sounds reassuring. It is not a free pass.

The physical data centres, hypervisor, and managed service endpoints are AWS's responsibility. Everything you deploy on top of that — IAM policies, S3 bucket ACLs, security group rules, encryption key management, application code — is yours.

The most common mistake I see is a misreading of this model. Teams assume that because their cloud provider is compliant, they are compliant by extension. That assumption leads to neglecting their own responsibilities for data encryption, access control, and vulnerability management, which is precisely where most cloud breaches occur.

If you leave an S3 bucket public, you are non-compliant. Not Amazon. And yes, that still happens in production environments I review.

<!-- INTERNAL_LINK: cloud compliance frameworks overview | cloud-compliance-frameworks -->

## Scope reduction: the most valuable architectural decision you will make

Network segmentation is the single most consequential decision in a PCI DSS programme, because it determines how much of your environment the assessor has to examine.

PCI DSS 4.0 does not mandate network segmentation, but segmentation is the practical mechanism for reducing the scope of your cardholder data environment (CDE). When segmentation isolates the CDE, only the segmented systems fall in scope.

In practice on AWS, this means isolating CDE components at the account level, not just the VPC level. A dedicated AWS account for payment processing isolates CDE resources from every other part of your estate. Cross-account access is then explicit and auditable. This is architecturally cleaner than trying to enforce segmentation purely through security groups within a shared account, and it maps directly to how AWS Control Tower's guardrails are designed to work.

A multi-account structure using AWS Organizations, aligned with organisational units (OUs), provides the right segmentation model. Your CDE OU should have Service Control Policies (SCPs) that prohibit the creation of internet-facing resources, restrict which AWS services can be provisioned, and enforce mandatory tagging for compliance tracking.

Here's a minimal SCP example that prevents direct internet egress from a CDE account:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyDirectInternetGatewayAttachment",
      "Effect": "Deny",
      "Action": [
        "ec2:AttachInternetGateway",
        "ec2:CreateInternetGateway"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyPublicS3Buckets",
      "Effect": "Deny",
      "Action": [
        "s3:PutBucketPublicAccessBlock",
        "s3:DeletePublicAccessBlock"
      ],
      "Resource": "*"
    },
    {
      "Sid": "EnforceEncryptionAtRest",
      "Effect": "Deny",
      "Action": "s3:PutObject",
      "Resource": "*",
      "Condition": {
        "StringNotEqualsIfExists": {
          "s3:x-amz-server-side-encryption": [
            "AES256",
            "aws:kms"
          ]
        }
      }
    }
  ]
}
```

Also consider scope reduction at the data level. Point-to-Point Encryption (P2PE) solutions and hosted payment pages can reduce scope further by ensuring card data is encrypted before it enters your network and never reaches your application servers. If you're building a new payment flow, the cheapest PCI control is the one you never have to implement because the card data never touches your infrastructure.

<!-- INTERNAL_LINK: AWS KMS and encryption key management | aws-kms-key-management-best-practices -->

## MFA, identity, and access control

MFA requirements expanded significantly in v4.0. Requirement 8.4.2 now mandates MFA for all access to the cardholder data environment, not just remote access. This catches out organisations that previously only enforced MFA on VPN connections. If a developer can SSH to a CDE instance via IAM credentials without a second factor, you have a finding.

Password minimums also jumped from 7 to 12 characters. AWS IAM combined with AWS Organizations provides the foundation for meeting these requirements at scale.

In practice, you should enforce MFA through AWS IAM Identity Centre with hardware tokens or authenticator apps for all human access, and use role-based access with clearly scoped permissions for workload identities. Service accounts and application IAM roles should have no console access and should be denied `iam:CreateAccessKey` via SCP.

The standard also requires that all human account privileges are reviewed every six months. The review frequency for application and system accounts can be set through a targeted risk analysis, but it needs to be documented and defensible to your QSA.

<!-- INTERNAL_LINK: AWS IAM Identity Centre configuration guide | aws-iam-identity-centre-guide -->
<!-- INTERNAL_LINK: IAM security best practices | aws-iam-security-best-practices -->

## Logging, monitoring, and continuous compliance

Requirement 10 is explicit about logging scope and retention. All access to system components and cardholder data must be logged. AWS CloudTrail captures API calls; VPC Flow Logs track network traffic. Logs must be retained for at least 12 months, with 3 months immediately available.

For automated compliance checking, AWS Security Hub's PCI DSS v4.0.1 standard includes 144 automated security controls, available across all public AWS Regions and AWS GovCloud (US) Regions. Enable it via central configuration in a delegated Security Hub administrator account so findings aggregate across the entire organisation rather than sitting siloed per account.

AWS Audit Manager supports PCI DSS v4.0 with a prebuilt collection of controls and automated evidence sources. Wire it to Security Hub's consolidated control findings so your evidence packages are continuously updated rather than assembled in a panic the week before your QSA arrives.

One caveat worth stating plainly: passing all Security Hub PCI checks does not mean you are PCI DSS compliant. The standard has many requirements — physical security and process controls among them — that no automated tool can verify. Security Hub is a floor, not a ceiling.

<!-- INTERNAL_LINK: AWS Security Hub full guide | aws-security-hub-guide -->

## Web application security: requirements 6.4.2, 6.4.3, and 11.6.1

These three requirements generated the most remediation work in client engagements in early 2025, and they remain a source of confusion.

Requirement 6.4.2 mandates that a solution is deployed that continually detects and prevents web-based attacks against public-facing web applications. In practice, that means a WAF installed in front of those applications checking all traffic.

AWS WAF supports PCI DSS 4.0 compliance protection with partner solutions, which matters for Requirement 6.4.2. But don't stop there.

Requirements 6.4.3 and 11.6.1 became mandatory alongside the rest of the future-dated requirements on 31 March 2025, and they are still catching organisations off-guard. Requirement 6.4.3 addresses the integrity of payment page scripts executed in the consumer's browser, including those sourced from third-party sites. This is a direct response to Magecart-style skimming attacks. You need a documented inventory of all payment page scripts, authorisation records, and a mechanism to detect tampering. That mechanism needs to run continuously, not just at point-in-time assessments.

Requirement 11.6.1 requires detection of unauthorised changes to payment pages. Together, these two requirements demand stronger client-side visibility than most teams had in place before the deadline.

<!-- INTERNAL_LINK: AWS WAF configuration guide | aws-waf-configuration -->

## Penetration testing and segmentation validation

PCI DSS 4.0 is explicit that segmentation is not just architected — it must be proven to work. Requirement 11.4.1 requires penetration testing to verify segmentation effectiveness at least annually. For service providers, the frequency is every six months. Testing must also be performed after any significant change to the segmentation controls.

If you are using AWS Transit Gateway to route between accounts, or if your CDE account has any cross-account IAM trust relationships, each of those paths needs to be in scope for your pentest. Testers who only scan within the CDE account without validating lateral movement paths from out-of-scope accounts are giving you an incomplete picture.

<!-- INTERNAL_LINK: cloud vulnerability management programme | cloud-security-vulnerability-management -->

## Common pitfalls

Based on assessments with UK financial services clients, these are the mistakes that cost teams time and money.

Treating AWS's PCI certification as inherited compliance. You inherit the physical security compliance of the data centre. You are fully liable for how you configure your servers, encrypt your data, and manage user access. Those are separate things.

Scope creep through uncontrolled resource provisioning. Cloud environments make spinning up resources easy, but each resource touching cardholder data expands compliance scope. A developer standing up a test Lambda that receives raw card data has just created a new CDE system component. Enforce guardrails via SCPs and AWS Config rules before that happens.

Serverless blind spots. If a Lambda function processes credit card data, the underlying code and the IAM role invoking it are in scope. You escape physical server management, but you increase the burden on application security under Requirement 6.

Ignoring client-side requirements. An inventory of third-party JavaScript on your payment pages is not optional. Requirements 6.4.3 and 11.6.1 make it a mandatory, continuously maintained artefact.

Assuming Security Hub findings equal a compliance pass. Security Hub is a useful drift-detection tool, but it does not assess your policies, procedures, staff training, or physical access controls. Your QSA will ask about all of those.

Under-logging VPC traffic. Many teams enable CloudTrail but skip VPC Flow Logs, particularly on non-production accounts that still touch CDE data. Requirement 10 applies to all in-scope systems.

<!-- INTERNAL_LINK: cloud threat detection and monitoring | cloud-threat-detection -->

## Key takeaways

All PCI DSS 4.0 requirements have been mandatory since 31 March 2025. If you have not completed your v4.0 gap assessment, that needs to be your next sprint.

AWS holds Level 1 PCI certification for its infrastructure. Your organisation is fully responsible for configuration and operation within that environment. The compliance boundary runs through your IAM policies, not AWS's.

Scope reduction via dedicated CDE AWS accounts, enforced through AWS Organizations SCPs and Control Tower guardrails, is the highest-return architectural investment you can make before your assessment.

Requirement 8.4.2 mandates MFA for all access to the CDE. Enforce this through IAM Identity Centre and deny static credentials in CDE accounts via SCP.

Requirements 6.4.3 and 11.6.1 require script inventory and integrity monitoring on payment pages. AWS WAF partner integrations via the AWS Marketplace are the most pragmatic path to meeting these controls at scale.

AWS Security Hub's 144 automated PCI DSS v4.0.1 controls give you continuous compliance drift detection. They are a baseline diagnostic tool, not a substitute for a Qualified Security Assessor assessment.