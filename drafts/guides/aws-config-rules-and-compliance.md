---
title: "AWS Config Rules and Compliance: A Practitioner's Guide"
date: 2026-08-04
description: "A deep-dive practitioner's guide to AWS Config rules and compliance — covering managed rules, conformance packs, proactive evaluation, multi-account aggregation, and common pitfalls."
tags: ["aws-config", "cloud-compliance", "security", "aws-security", "devsecops"]
slug: "aws-config-rules-and-compliance"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2513
draft: false
---

# AWS Config rules and compliance: a practitioner's guide

If you are responsible for the security posture of an AWS environment, whether you are running workloads regulated by the FCA, handling personal data under GDPR, or simply trying to stop your engineers from opening port 22 to the world, then AWS Config rules and compliance belong at the centre of your detective controls strategy. AWS Config has been expanding rapidly throughout 2026: in March AWS announced an additional 75 managed rules covering security, durability, and operations, and in July a further 191 managed rules landed across Amazon Bedrock, SageMaker, ECS, EKS, RDS, Redshift, S3, and CloudTrail. If you set up Config two years ago and left it running, you likely have significant blind spots right now.

This guide is aimed at security architects and senior engineers who already understand the basics and want to implement Config rules properly, at scale, without blowing the budget or producing compliance theatre.

<!-- INTERNAL_LINK: AWS Security Hub integration with Config | aws-security-hub-guide -->

---

## What AWS Config actually does (and what it does not)

Before getting into rules, it is worth being precise about what the service records. CloudTrail tracks who performed an action. AWS Config tracks what changed and when. Together they give you a full audit trail, but do not conflate the two; they answer different questions. Config maintains a continuous inventory of your resource configurations and evaluates those configurations against rules you define.

The rules engine runs continuously and can detect non-compliant resources in near real time. A Config rule finding is a signal, not a block. Enforcement still requires coupling Config to remediation or preventive controls such as SCPs. That distinction matters enormously when you are presenting evidence to an auditor and they assume Config is doing more than it actually is.

<!-- INTERNAL_LINK: AWS IAM and preventive controls with SCPs | aws-iam-security-best-practices -->

---

## Managed rules vs. custom rules

### Managed rules

AWS provides over 300 managed rules that you can enable without writing any code. They cover the most common security checks: IAM configuration, encryption requirements, network exposure, audit trail verification. AWS maintains them and updates them as best practices evolve.

A sensible starting set for any UK financial services or government deployment would include:

- `ROOT_ACCOUNT_MFA_ENABLED` — root account protection
- `INCOMING_SSH_DISABLED` — open SSH detection
- `ENCRYPTED_VOLUMES` — EBS encryption at rest
- `S3_BUCKET_PUBLIC_READ_PROHIBITED` — public S3 access
- `RDS_STORAGE_ENCRYPTED` — RDS encryption
- `CLOUDTRAIL_ENABLED` — audit trail verification
- `IAM_PASSWORD_POLICY` — password hygiene

Do not enable all 300+ rules at once. Instrument your highest-risk controls first, address the non-compliant resources, and expand iteratively. This is not just good practice; it is cost management.

### Custom rules

Custom rules, backed by Lambda functions, are appropriate when you need to enforce internal standards with no managed equivalent: checking that every EC2 instance carries a mandatory cost-allocation tag, or that every IAM role has a specific permission boundary attached. The trade-off is real. Heavy or poorly optimised Lambda-backed rules drive up execution costs and slow down evaluation results.

The practical pattern is to combine the two: managed rules for general checks, Lambda-backed custom rules for specific internal policies.

<!-- INTERNAL_LINK: DevSecOps and shift-left policy enforcement | devsecops-shift-left-security -->

---

## Proactive evaluation: shift compliance left

For most of its existence, AWS Config was a purely detective control. It told you what was wrong after the fact. Proactive evaluation mode changed that. You can now evaluate resource configurations before they are created or updated, catching non-compliant settings before anything reaches production.

The mechanism is the `StartResourceEvaluation` API with `PROACTIVE` mode, combined with `GetResourceEvaluationSummary` to retrieve the result. One important caveat the AWS documentation is explicit about: proactive rules do not prevent a non-compliant resource from being deployed. You are still relying on your CI/CD pipeline or IaC tooling to act on the API response. Wire `StartResourceEvaluation` into your CloudFormation or Terraform pipeline and fail the build on a NON_COMPLIANT result. That is a meaningful shift-left without requiring a full CloudFormation Guard or OPA implementation.

A minimal CLI invocation to check a resource pre-deployment looks like:

```bash
# Evaluate a resource configuration before provisioning
aws configservice start-resource-evaluation \
  --evaluation-mode PROACTIVE \
  --resource-details '{
    "ResourceId": "my-new-s3-bucket",
    "ResourceType": "AWS::S3::Bucket",
    "ResourceConfiguration": "{\"BucketName\":\"my-new-s3-bucket\",\"VersioningConfiguration\":{\"Status\":\"Enabled\"}}",
    "ResourceConfigurationSchemaType": "CFN_RESOURCE_SCHEMA"
  }'

# Retrieve the evaluation result using the returned ResourceEvaluationId
aws configservice get-resource-evaluation-summary \
  --resource-evaluation-id <ResourceEvaluationId>
```

<!-- INTERNAL_LINK: Cloud security vulnerability management and shift-left | cloud-security-vulnerability-management -->

---

## Conformance packs: compliance frameworks at scale

Once you move beyond a handful of rules, managing them individually becomes untenable. A conformance pack is a collection of Config rules and remediation actions deployed as a single unit, either into a single account and region or across an entire AWS organisation.

When you need to implement a full compliance framework, CIS Benchmarks, PCI DSS, HIPAA, or NIST, you are typically looking at dozens of rules. Adding them individually is error-prone and hard to audit. Conformance packs solve that by treating the framework as a deployable package.

AWS provides sample templates for the most common frameworks. The CIS AWS Foundations Benchmark v1.4 pack is the natural starting point for most UK organisations; it maps directly to many NCSC Cloud Security Principles and to the FCA's operational resilience expectations. AWS publishes a sample mapping between the CIS Amazon Web Services Foundation v1.4 Level 1 controls and the specific managed Config rules that correspond to each control. For payment card environments, AWS Config rules satisfy PCI DSS Requirements 2.2.1 and 2.2.6 for configuration standards consistent with industry-accepted hardening guidelines.

A critical caveat that auditors frequently misunderstand: AWS is explicit that conformance pack sample templates are not designed to fully ensure compliance with a specific governance or compliance standard. You are responsible for making your own assessment of whether your use of the services meets applicable legal and regulatory requirements. Config gives you evidence of technical control states. It does not replace the broader governance, policy, and process requirements of FCA SYSC or GDPR Article 32.

<!-- INTERNAL_LINK: Cloud compliance frameworks overview | cloud-compliance-frameworks -->

---

## Auto-remediation: closing the loop

Detection without remediation is a compliance report nobody reads. AWS Config applies remediation using AWS Systems Manager Automation documents, which define the actions to be performed on non-compliant resources. AWS provides a set of managed automation documents for common fixes, and you can create custom ones where needed.

The following CloudFormation snippet attaches automatic remediation to the `s3-bucket-server-side-encryption-enabled` rule using the AWS-managed SSM document:

```yaml
# CloudFormation: Auto-remediation for unencrypted S3 buckets
Resources:
  S3EncryptionRemediationConfig:
    Type: AWS::Config::RemediationConfiguration
    Properties:
      ConfigRuleName: s3-bucket-server-side-encryption-enabled
      TargetId: AWS-EnableS3BucketEncryption
      TargetType: SSM_DOCUMENT
      TargetVersion: "1"
      Automatic: true
      MaximumAutomaticAttempts: 3
      RetryAttemptSeconds: 60
      Parameters:
        BucketName:
          ResourceValue:
            Value: RESOURCE_ID
        SSEAlgorithm:
          StaticValue:
            Values:
              - "aws:kms"
        AutomationAssumeRole:
          StaticValue:
            Values:
              - !GetAtt ConfigRemediationRole.Arn
      ResourceType: AWS::S3::Bucket
```

Be deliberate about what you automate. Enabling KMS encryption on an S3 bucket automatically is generally safe. Automatically revoking IAM access or terminating an EC2 instance is not. Use automatic remediation for low-blast-radius fixes and keep manual remediation, a single click in the console, for anything that could cause an outage.

<!-- INTERNAL_LINK: AWS KMS key management and encryption best practices | aws-kms-key-management-best-practices -->

---

## Multi-account aggregation: the enterprise view

Per-account Config dashboards are not a compliance posture for any organisation running more than one AWS account. You need a centralised view.

Config's multi-account, multi-region aggregator pulls data from multiple accounts and regions into a single account. It is a read-only view: the aggregator replicates data from source accounts but cannot deploy rules or modify resources in those accounts. Aggregators do not incur additional costs, which removes the usual objection.

If you are using AWS Organizations, set up an organisation-based aggregator in your security tooling account. It automatically collects Config data from all accounts in the organisation where Config is enabled, without requiring individual per-account authorisation. For environments not using Organizations, you need explicit authorisation from each source account.

<!-- INTERNAL_LINK: AWS IAM Identity Centre for multi-account access | aws-iam-identity-centre-guide -->

---

## Common pitfalls

These are the mistakes I see repeatedly in production environments. Avoiding them will save you money and embarrassment during audits.

### 1. Recording everything in every region

Enabling Config in all regions without filtering resource types is a primary driver of unexpected cost. Only enable recording for resource types that need monitoring. It reduces costs and storage requirements, and keeps your evaluation results focused on what matters.

### 2. Enabling 300+ rules on day one

A flood of NON_COMPLIANT findings across hundreds of rules on day one guarantees alert fatigue and zero remediation. Prioritise by risk, not by coverage percentage.

### 3. Assuming conformance packs equal full compliance

This is the most dangerous misconception. Deploying the PCI DSS conformance pack does not make you PCI compliant. It gives you evidence about a subset of technical controls. The broader governance, policy, and process requirements still need to be addressed separately.

### 4. Neglecting the cost of deleting rules

This one bites teams who are tidying up. Deleting rules creates configuration items for `AWS::Config::ResourceCompliance` that affect your configuration recorder costs. If you are deleting rules that evaluate a large number of resource types, you can see a significant spike in recorded items. To avoid it, disable recording for `AWS::Config::ResourceCompliance` before deleting the rules, then re-enable it afterwards.

### 5. Leaving conformance packs with redundant rules

Conformance packs with redundant rules cause double evaluations, which silently inflates Config costs. Before deploying a pack, audit it for overlap with individually deployed rules and remove duplicates.

### 6. Not accounting for new resource types

If you have opted to record only specific resource types, which is sensible for cost management, you must actively review new Config resource type announcements and update your recording configuration. AWS has been adding dozens of new types per quarter throughout 2025 and 2026. Your coverage will degrade silently as new services are adopted if you are not paying attention.

### 7. Custom rule Lambda functions without deleted-resource logic

When creating custom Lambda-backed rules, add logic to handle the evaluation of deleted resources. When evaluation results are marked as `NOT_APPLICABLE`, they are marked for deletion and cleaned up. Without this logic, your custom rules will error on resource deletion events and produce misleading compliance states.

---

## What's new in 2026: coverage expansion you should act on

The July 2026 expansion added 191 managed rules across Bedrock, SageMaker, ECS, EKS, RDS, Redshift, S3, and CloudTrail. The new rules cover encryption, logging, public access, network security, and data protection for these services.

If your organisation is deploying generative AI workloads, Bedrock agents, SageMaker endpoints, or Bedrock AgentCore, you now have Config resource type coverage that did not exist a few months ago. Review your recording configuration and conformance packs to make sure those workloads are actually being evaluated.

<!-- INTERNAL_LINK: AI security and cloud guide | ai-security-cloud-guide -->
<!-- INTERNAL_LINK: Shared responsibility model in cloud security | shared-responsibility-model-cloud-security -->

---

## Key takeaways

Start narrow and expand deliberately. Enable your highest-risk managed rules first, get to a clean baseline, then broaden coverage.

Use conformance packs for framework alignment, not as compliance proof. The CIS v1.4 and PCI DSS packs produce useful evidence artefacts, but AWS is explicit that they are not designed to fully ensure compliance with a specific governance or compliance standard.

Enable proactive evaluation in your IaC pipelines. Using `StartResourceEvaluation` in PROACTIVE mode before deploying resources shifts compliance left without requiring platform-level blocking.

Deploy an organisation aggregator in your security account. It costs nothing extra and gives you a single view across every account and region.

Pair Config findings with SSM auto-remediation carefully. Automate low-blast-radius fixes such as enabling encryption or enforcing tags. Keep manual remediation for anything that could affect availability.

Audit your recording configuration quarterly. AWS is adding new resource types at pace in 2026. If you record only specific types, your coverage will silently degrade as new services are adopted across your estate.