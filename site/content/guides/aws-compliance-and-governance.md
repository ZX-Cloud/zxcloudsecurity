---
title: "AWS Compliance and Governance: A Practitioner's Guide for 2026"
date: 2026-06-20
description: "Master AWS compliance and governance with SCPs, Control Tower, NCSC alignment, and real-world guardrails. Practical guidance for UK regulated environments."
tags: ["aws-compliance", "aws-governance", "service-control-policies", "aws-security", "ncsc", "fca", "cloud-security"]
slug: "aws-compliance-and-governance"
author: "Steve Harrison, Principal Security Architect"
word_count: 2288
draft: false
---

# AWS compliance and governance: a practitioner's guide for 2026

If you run workloads in AWS for a UK-regulated organisation -- FCA-supervised financial services, NHS, central government, or any data-intensive enterprise -- then AWS compliance and governance is not a project you complete once and file away. It is a continuous operational discipline. Most incidents I see investigated stem from the customer side: identity misuse, misconfiguration, exposed workloads. Not platform failures. That matters because it means the controls are largely in your hands.

This guide covers the architectural decisions, policy primitives, and operational habits that actually hold up under audit.

<!-- INTERNAL_LINK: AWS IAM least privilege guide | aws-iam-least-privilege -->

---

## What AWS governance actually means in practice

Before getting into tooling, it helps to be precise about what governance covers. The definition you'll find in most documentation -- managing your AWS environment to ensure security, compliance, and cost-efficiency -- is fine as far as it goes. In practice it breaks into three distinct layers:

1. Preventive controls: policies that make non-compliant actions impossible before resources are provisioned
2. Detective controls: rules and findings that surface misconfiguration after the fact
3. Responsive controls: automation that remediates or notifies when a detective control fires

Most organisations I encounter lean heavily on detective controls because they're easier to retrofit. The problem is that by the time a Config rule fires on an unencrypted S3 bucket in production, the audit trail exists, the data is potentially exposed, and the remediation is disruptive. Shift left. Invest in preventive controls first.

<!-- INTERNAL_LINK: AWS Security Hub setup and configuration | aws-security-hub-setup -->

---

## Building your governance foundation with AWS Organizations and SCPs

AWS Organizations is free and gives you a hierarchical structure of Organisational Units (OUs), centralised billing, and Service Control Policies that set permission guardrails across all member accounts.

SCPs are the top-level security guardrails in AWS. They set the maximum permissions for every identity in an account, including the root user. Unlike IAM policies, SCPs only restrict -- they do not grant. That distinction matters: an account administrator cannot grant themselves permissions that an SCP denies, regardless of what their IAM policies say. You can also use SCPs with the full fine-grained control supported in the IAM policy language, so there is no reason to keep them coarse.

### A foundational SCP for UK-regulated workloads

The following SCP enforces region restriction (keeping data in `eu-west-2` and `eu-west-1`), prevents CloudTrail from being disabled, and blocks creation of unencrypted S3 buckets. Apply it at the root OU level, then create targeted exceptions in child OUs where needed.

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
        "sts:AssumeRole",
        "support:*",
        "trustedadvisor:*"
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
      "Sid": "DenyDisableCloudTrail",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:DeleteTrail",
        "cloudtrail:StopLogging",
        "cloudtrail:UpdateTrail"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyUnencryptedS3BucketCreation",
      "Effect": "Deny",
      "Action": "s3:CreateBucket",
      "Resource": "*",
      "Condition": {
        "Null": {
          "s3:x-amz-server-side-encryption": "true"
        }
      }
    },
    {
      "Sid": "DenyLeavingOrganisation",
      "Effect": "Deny",
      "Action": "organizations:LeaveOrganization",
      "Resource": "*"
    }
  ]
}
```

> Honest trade-off: region-restriction SCPs using `NotAction` are broad by design. You will inevitably need to expand the `NotAction` list as you adopt global services like CloudFront, IAM, and Route 53. Keep that list in version control and review it quarterly. I've seen `NotAction` lists so large they rendered the region restriction meaningless -- do not let it grow unchecked.

### Resource Control Policies: the missing piece

RCPs are a sibling policy type to SCPs, introduced by AWS in November 2024. They cover resource-side governance use cases that SCPs cannot fully handle, particularly for S3, STS, KMS, Secrets Manager, and SQS. SCPs constrain what identities in your accounts can do. RCPs constrain what external principals can do to your resources, even if those principals have valid IAM permissions in their own account. If you are not using RCPs yet, that is the gap in your governance stack that attackers look for.

<!-- INTERNAL_LINK: AWS Resource Control Policies explained | aws-resource-control-policies -->

---

## AWS Control Tower and automated compliance at scale

Beyond roughly five accounts, hand-rolling SCPs and account vending becomes error-prone. Control Tower handles account provisioning, guardrail application, and OU structure consistently. Its guardrails map directly onto NCSC Cloud Security Principles and FCA PS21/3 cloud outsourcing requirements.

Enable all mandatory guardrails as a minimum, then layer strongly-recommended guardrails based on your risk classification. For FCA-regulated workloads, I treat "strongly recommended" as mandatory.

Control Tower's Audit account is the right place to centralise your AWS Config aggregator, Security Hub cross-account findings, and CloudTrail organisation-wide logs. All of these will appear in FCA operational resilience submissions, so get the architecture right early rather than retrofitting it during an audit.

<!-- INTERNAL_LINK: AWS Control Tower landing zone setup for UK enterprises | aws-control-tower-landing-zone -->

---

## Aligning with the NCSC's 14 cloud security principles

The NCSC's cloud security principles help you choose a provider that meets your security needs. That is the easy part. The harder part -- and where most UK organisations fall short -- is configuring your cloud services securely once you are there.

AWS publishes a whitepaper mapping its platform controls to the NCSC principles, but the customer-side configuration work still falls on you. AWS also provides a sample mapping between the NCSC Cloud Security Principles and AWS managed Config rules, where each Config rule applies to a specific resource type and relates to one or more principle controls.

Deploy the NCSC conformance pack in AWS Config (`Operational-Best-Practices-for-NCSC`) as a baseline. It will not cover everything, but it gives you a defensible starting point for accreditation conversations. For G-Cloud procurement, AWS has worked with the NCSC to tailor guidance on how UK public sector customers can use the Landing Zone Accelerator to meet NCSC requirements for using cloud services securely.

<!-- INTERNAL_LINK: NCSC cloud security principles mapped to AWS Config rules | ncsc-aws-config-conformance-pack -->

---

## AI governance: an emerging gap in most frameworks

GenAI workloads introduce governance challenges that traditional cloud security frameworks were not built for: model drift, prompt injection, data exfiltration through inference endpoints, and opaque decision-making that conflicts with GDPR Article 22 on automated processing.

Amazon SageMaker Role Manager lets administrators define minimum permissions for ML-related roles in minutes rather than hand-crafting policies. SageMaker Model Cards give you a consistent place to capture intended uses, risk ratings, and training details from inception through to deployment. SageMaker Model Dashboard then monitors model behaviour in production in one view. These are not optional governance extras for FCA-regulated AI deployments -- PS7/23 on model risk management is explicit about evidencing model monitoring and governance.

SageMaker HyperPod now supports data capture for inference workloads, recording inference request and response payloads from production endpoints to S3. That audit trail feeds evaluation pipelines, fine-tuning jobs, and compliance evidence in a single mechanism.

Amazon SageMaker Unified Studio provides a single permission model with fine-grained access controls for consistent policy enforcement across your AI workloads. Pair this with Amazon Bedrock Guardrails if you are using foundation models -- Bedrock Guardrails can be applied directly to SageMaker-served models to filter outputs and enforce responsible use policies.

<!-- INTERNAL_LINK: Governing AI workloads on AWS for FCA-regulated firms | aws-ai-governance-fca -->

---

## Network governance: keeping traffic private

The shared responsibility model places identity, configuration, and workload protection squarely on customers. Nowhere is this more visible than in network architecture. Two recent AWS releases are directly relevant.

EKS cluster governance via IAM condition keys: teams managing multi-account environments have historically had to rely on manual processes or post-deployment checks to enforce cluster configuration standards. The expansion of EKS IAM condition keys changes that. You can now enforce private-only API endpoints, require customer-managed KMS keys for secrets encryption, restrict clusters to approved Kubernetes versions, and mandate deletion protection for production workloads -- all at the SCP level. Misconfigured EKS clusters become impossible to provision rather than detectable after the fact.

AWS Management Console Private Access: this allows customers to access the AWS Console from VPCs without any internet connectivity. For environments where your security policy prohibits internet access from workstation VPCs -- common in financial services and government -- this removes a significant architectural compromise that teams previously had to accept.

For messaging infrastructure, Amazon MQ encrypts messages at rest and in transit, restricts broker connections to a private endpoint within your VPC, and now supports AWS PrivateLink for the Amazon MQ API itself. Communication between your VPC and the Amazon MQ API stays entirely within the AWS network.

<!-- INTERNAL_LINK: AWS VPC design patterns for regulated workloads | aws-vpc-design-regulated -->

---

## Common governance pitfalls

These are the mistakes I see repeatedly across UK enterprise and public sector engagements.

### 1. Treating AWS Config as your only compliance tool

Config rules are detective controls. They tell you something broke -- they do not stop it from breaking. If your entire governance posture is "we have Config rules and Security Hub," you are running reactive governance. Add SCPs and RCPs to shift detection to prevention.

### 2. Not version-controlling your SCPs

I have seen production SCPs modified directly in the AWS console with no change history and no review process. Your SCPs are as critical as your application code. Store them in Git, run them through a CI/CD pipeline with policy-as-code validation (AWS CloudFormation Guard or OPA/Rego), and require peer review before merging.

### 3. Ignoring the FullAWSAccess SCP problem

By default, AWS attaches the `FullAWSAccess` managed SCP to every OU and account. Many teams assume this is a permissive policy and leave it alongside their deny-list SCPs. SCPs do not grant permissions -- they define the outer boundary of what IAM users and roles in your organisation can do. `FullAWSAccess` is simply the absence of restrictions. You still need meaningful identity-based or resource-based policies.

### 4. Overlooking data residency for AI inference

GDPR and UK GDPR require you to know where personal data is processed. If your SageMaker inference endpoints are deployed outside `eu-west-2` or `eu-west-1`, personal data in inference requests may be leaving UK/EEA jurisdiction. SageMaker inference recommendations are currently available in seven regions including Europe (Ireland) and Europe (Frankfurt) -- note that `eu-west-2` (London) is not currently included. Check region availability before deploying regulated inference workloads, and enforce region restrictions at the SCP level.

### 5. Miscounting your compliance boundary

AWS holds SOC 1/ISAE 3402, SOC 2, SOC 3, PCI DSS Level 1, ISO 27001, ISO 27017, and ISO 27018 certifications -- but these cover the platform, not your workload. AWS manages security of the cloud; you are responsible for security in the cloud, retaining control of the security you choose to implement to protect your own content, applications, systems, and networks. Auditors will ask about your controls, not AWS's certifications.

### 6. Neglecting the Audit account

Control Tower creates a dedicated Audit account for a reason. I regularly find organisations that have deployed workloads into it or given developers direct access to it. The Audit account should have read-only cross-account roles for security tooling and nothing else. Lock it down with SCPs that deny any resource creation outside the security tooling namespace.

---

## Key takeaways

Effective AWS compliance and governance is an architecture problem, not a checkbox exercise. Here is what to act on:

- Preventive before detective: SCPs and RCPs stop misconfigurations before they happen. Do not rely solely on Config rules and Security Hub findings. Invest in policy-as-code validation in your CI/CD pipeline.
- NCSC alignment is automatable: deploy the `Operational-Best-Practices-for-NCSC` conformance pack in AWS Config as a baseline and cross-reference AWS's NCSC whitepaper for the platform controls you inherit.
- AI governance needs explicit tooling: use SageMaker Role Manager, Model Cards, and Model Dashboard alongside Bedrock Guardrails. Data capture for inference workloads provides the audit trail GDPR and FCA model risk guidance require.
- Network isolation is a governance control: EKS IAM condition keys, Amazon MQ PrivateLink, and AWS Management Console Private Access all reduce your attack surface while satisfying NCSC Principle 1 (data in transit protection) and Principle 11 (external interface protection).
- Version-control everything: SCPs, RCPs, Config rules, and Control Tower customisations belong in Git with peer review and automated testing. Treat them as production code, because that is exactly what they are.
- Region restrictions require ongoing maintenance: encode permitted regions in your root OU SCP and review the `NotAction` list quarterly. Validate that AI inference services you adopt are available in your approved regions before deploying regulated workloads.