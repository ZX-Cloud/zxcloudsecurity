---
title: "HIPAA Compliance on AWS: A Practical Architect's Guide"
date: 2026-07-19
description: "Master HIPAA compliance on AWS: BAA setup, HIPAA-eligible services, encryption, IAM controls, audit logging, and the proposed 2026 Security Rule changes."
tags: ["hipaa", "aws-compliance", "healthcare-security", "data-protection", "cloud-security"]
slug: "hipaa-compliance-aws-guide"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2362
draft: false
---

# HIPAA compliance on AWS: what every cloud security architect actually needs to know

If you are building or auditing healthcare workloads on AWS in 2026, HIPAA compliance is a live architectural constraint with real enforcement teeth. The Office for Civil Rights (OCR) at HHS continues to pursue breach investigations, hacking and IT incidents are now the dominant cause of breached health records on the OCR portal, and a major proposed overhaul of the HIPAA Security Rule is working its way through the federal rulemaking process. Sorting out your HIPAA posture on AWS is urgent regardless of where that rulemaking lands. This guide covers the foundation: what the Business Associate Addendum (BAA) actually gives you, how to structure HIPAA-eligible service usage, the technical controls you must configure yourself, and the common mistakes that turn a compliant architecture on paper into a reportable breach in practice.

<!-- INTERNAL_LINK: AWS compliance and governance overview | aws-compliance-and-governance -->

---

## What the AWS BAA does and does not do

AWS is HIPAA eligible, not HIPAA compliant on its own. Amazon provides compliant building blocks; you are responsible for configuring them correctly.

Under HIPAA, cloud service providers such as AWS are considered business associates when they create, receive, maintain, or transmit ePHI on behalf of a covered entity or another business associate. AWS offers a standardised Business Associate Addendum for customers subject to HIPAA. Customers who execute an AWS BAA may use any AWS service in an account designated as a HIPAA account, but they may only process, store, and transmit ePHI using HIPAA eligible services.

Until the BAA is in place, putting PHI on AWS is a HIPAA violation, even if every technical control is correctly configured. You accept the BAA through AWS Artifact — it is self-service and takes minutes. The BAA applies to specific AWS accounts. In a multi-account architecture, accept the BAA in each account that will touch PHI: production, staging, analytics, backup. Sandbox and developer accounts not touching real PHI do not need to be covered.

A BAA commits the provider to safeguard the ePHI its platform handles and to report incidents on its side. It says nothing about whether you left a storage bucket public, attached an over-permissive role to a workload, or shipped logs containing PHI to an unmonitored sink. HHS guidance is blunt on this division: the customer remains responsible for implementing the safeguards on the services it configures. The misconfiguration is yours, and so is the violation.

---

## HIPAA-eligible services: the list that actually matters

AWS offers over 160 HIPAA eligible services, with new services added frequently. The list includes the core services most workloads depend on: EC2 for compute, S3 for storage, RDS and Aurora for databases, Lambda for functions, EBS for block storage, KMS for key management, and CloudTrail for logging.

A notable recent addition: AWS updated its HIPAA Eligible Services Reference on 10 February 2026, and the list now includes Amazon Bedrock and Amazon Bedrock AgentCore. The model providers (Anthropic, Meta, Mistral, Cohere, Amazon) do not see your prompts or completions — Bedrock isolates them. For teams building clinical AI pipelines, this is a material change, but eligibility is the starting line, not the finish line.

These services are eligible to create, receive, process, maintain, or transmit electronic protected health information. AWS has demonstrated its compliance with HIPAA requirements with respect to each service, subject to the shared responsibility model. Customers must still configure these services in line with HIPAA requirements.

You can also use services that are not on the eligible list within a HIPAA account, provided those services do not process or store ePHI. Always verify eligibility before routing any data flow. The list updates roughly monthly as new services and instance types become eligible.

<!-- INTERNAL_LINK: AWS Well-Architected Security pillar | aws-well-architected-security -->

---

## Technical safeguards: the controls you must configure yourself

This is where most teams underestimate the work. HIPAA's Security Rule technical safeguards (45 CFR §164.312) map directly to concrete AWS configuration decisions. AWS provides the services; you provide the settings.

### Encryption at rest

HIPAA requires encryption for all protected health information at rest. For RDS, enable encryption at rest when creating the instance — it cannot be added later without a snapshot/restore cycle. Use AWS KMS for key management.

For S3, use server-side encryption with AWS KMS (SSE-KMS) rather than SSE-S3. KMS gives you better key management controls and a cleaner audit trail. Create customer-managed keys (CMKs) for ePHI workloads rather than relying on AWS-managed keys. CMKs give you control over key policies and rotation schedules that AWS-managed keys do not.

Here is a working CloudFormation snippet for a HIPAA-scoped S3 bucket with CMK encryption, versioning, and public access blocking:

```yaml
Resources:
  PhiKmsKey:
    Type: AWS::KMS::Key
    Properties:
      Description: "CMK for ePHI bucket encryption"
      EnableKeyRotation: true
      KeyPolicy:
        Version: "2012-10-17"
        Statement:
          - Sid: EnableIAMPolicies
            Effect: Allow
            Principal:
              AWS: !Sub "arn:aws:iam::${AWS::AccountId}:root"
            Action: "kms:*"
            Resource: "*"
            Condition:
              StringEquals:
                "kms:ViaService": !Sub "s3.${AWS::Region}.amazonaws.com"

  PhiKmsKeyAlias:
    Type: AWS::KMS::Alias
    Properties:
      AliasName: alias/hipaa-phi-key
      TargetKeyId: !Ref PhiKmsKey

  PhiBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyID: !Ref PhiKmsKey
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: ArchivePhiDataAfter90Days
            Status: Enabled
            Transitions:
              - TransitionInDays: 90
                StorageClass: GLACIER_IR

  PhiBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref PhiBucket
      PolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Sid: DenyNonTLS
            Effect: Deny
            Principal: "*"
            Action: "s3:*"
            Resource:
              - !GetAtt PhiBucket.Arn
              - !Sub "${PhiBucket.Arn}/*"
            Condition:
              Bool:
                "aws:SecureTransport": "false"
```

### Encryption in transit

Mandate TLS 1.2 or higher for all client and service communications; prefer TLS 1.3 where it is supported. Terminate TLS at Application Load Balancers or API Gateway with strong ciphers, and re-encrypt traffic to downstream services.

Use VPC endpoints (gateway endpoints for S3 and DynamoDB, interface endpoints for other services) to access AWS services without sending traffic over the public internet. This reduces exposure and keeps ePHI traffic within the AWS network, which simplifies your compliance documentation considerably.

### Identity and access management

Use IAM roles with least privilege. Enforce MFA on the root account and on all privileged users. Use AWS Organisations Service Control Policies (SCPs) to prevent disabling logging or encryption.

An SCP that prevents disabling CloudTrail across the organisation:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyCloudTrailDisable",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail",
        "cloudtrail:UpdateTrail"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyKMSKeyDisable",
      "Effect": "Deny",
      "Action": [
        "kms:DisableKey",
        "kms:ScheduleKeyDeletion"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/hipaa-scope": "true"
        }
      }
    }
  ]
}
```

### Audit controls and logging

HIPAA requires audit controls that record and examine activity in systems containing PHI. AWS CloudTrail logs every API call in your account. Configure it to run in all regions (not just your primary region), enable log file validation to detect tampering, deliver logs to an S3 bucket owned by a separate AWS account where possible, and enable CloudWatch Logs integration for real-time alerting.

Retain CloudTrail logs for at least six years — HIPAA requires six years for documentation of required activities. S3 lifecycle policies can move logs to Glacier Instant Retrieval after 90 days to cut storage costs while meeting retention requirements.

Use Amazon Macie to scan S3 buckets for PII and ePHI. PHI has a habit of drifting into places where it was never intended to land: log buckets, test environments, analytics pipelines. Macie catches that drift before it becomes a reportable incident.

<!-- INTERNAL_LINK: AWS CloudTrail configuration best practices | aws-cloudtrail-configuration-best-practices -->
<!-- INTERNAL_LINK: Cloud compliance frameworks | cloud-compliance-frameworks -->

---

## Generative AI and ePHI: the new frontier

AWS has developed its generative AI services, including Amazon SageMaker AI, Amazon Bedrock, and Amazon Q Business, so customers can deploy applications in conformance with HIPAA requirements. AWS HealthLake is a HIPAA-eligible service that stores and analyses healthcare data in the FHIR R4 format, automatically standardising medical terminologies including SNOMED CT, ICD-10-CM, RxNorm, and LOINC.

When using Bedrock with PHI, the architectural discipline is straightforward: use Guardrails to redact PII and PHI and constrain the agent at both input and output. Bedrock does not train on your data. Add encryption, scoped accounts, and audit logs to make the architecture defensible under scrutiny.

If your solution involves training a custom model using SageMaker AI, think carefully about whether ePHI can appear in the training data and what controls that requires. In many cases the right answer is to remove PII and ePHI from training data so the model cannot return restricted data in a response — not as a technical limitation, but as a deliberate design choice.

<!-- INTERNAL_LINK: Securing AI agents on cloud infrastructure | securing-ai-agents-cloud-infrastructure -->

---

## The proposed HIPAA Security Rule update: what is actually happening

Much has been written about imminent HIPAA changes. Here is the accurate picture as of July 2026.

The proposed HIPAA Security Rule update is not yet final. OCR issued the NPRM in late December 2024, and it was formally published in the Federal Register on 6 January 2025. HHS's Fall 2026 Unified Agenda lists July 2027 as the anticipated timeframe for the Office of Management and Budget to complete final action. The NPRM would introduce mandatory encryption of ePHI at rest and in transit (removing the "addressable" designation), required multi-factor authentication for all systems accessing ePHI, a 72-hour requirement to restore critical relevant electronic information systems and data following a loss, annual penetration testing, and enhanced business associate oversight obligations. These would represent the most substantial update to HIPAA security requirements since the original rule. As of mid-2026, they remain proposed.

The practical implication is this: OCR is holding organisations to a functioning risk management programme under the rules that exist today. The extra runway before any final rule is time to build that programme, not time to wait.

The revisions introduce stricter audit requirements, set intervals for technical testing, mandate network segmentation, and expand incident response obligations. Encryption and MFA move from "addressable" to required controls.

If you are already running KMS encryption across all ePHI services and enforcing MFA on all IAM principals with six-year CloudTrail retention, the proposed rule changes very little about your day-to-day posture. If you are not, you have a gap that is both a present compliance risk and a future regulatory certainty.

---

## Common pitfalls: where HIPAA compliance actually breaks on AWS

Healthcare data breaches on AWS are increasingly caused not by sophisticated attacks, but by misconfigured services, missing agreements, and misunderstood responsibility boundaries. The patterns I see most often are:

1. Treating the BAA as the finish line. Even with a signed Business Associate Agreement, your organisation can still violate HIPAA through misconfigured services, over-permissive access controls, unencrypted storage, or inadequate logging. The BAA covers what AWS does. Everything you configure is still your problem.

2. Routing ePHI through non-eligible services. Using a non-eligible service to process, store, or transmit PHI violates your BAA and creates an unmitigated compliance exposure. AWS will not prevent you from sending PHI to a non-eligible service. Teams building event-driven architectures are particularly susceptible: a Lambda function (eligible) that fans out to a non-eligible service is a compliance break at the fan-out point.

3. Failing to encrypt EBS volumes at instance creation. Encryption must be enabled at creation time for both EBS and RDS, because you cannot encrypt an existing unencrypted volume in place. I find this in roughly half the heritage environments I review. The fix requires a snapshot/restore cycle and planned downtime.

4. PHI leaking into Lambda logs. Every Lambda function touching PHI logs to CloudWatch by default, and those logs must be encrypted and retention-bounded. Lambda environment variables containing PHI or BAA-scoped secrets must be encrypted via KMS, not stored as plaintext.

5. BAA not covering all PHI-holding accounts. If your organisation consolidates accounts, brings in a new managed service provider, or migrates to AWS Control Tower, re-verify that the BAA covers every account holding PHI. Account creation does not automatically inherit the BAA — it must be accepted in each new account.

6. Skipping the Security Risk Analysis for cloud infrastructure. Your Security Risk Analysis must cover your cloud environment, not just your on-premises systems. That means evaluating risks specific to cloud deployments: data residency, multi-tenancy, API security, third-party integrations, and disaster recovery. Many organisations conduct their SRA only for on-premises infrastructure and miss their cloud footprint entirely.

7. Assuming dedicated EC2 tenancy is required. AWS's own HIPAA compliance programme required Dedicated Instances or Dedicated Hosts for PHI-processing EC2 and EMR workloads until AWS removed that requirement in January 2017. Shared-tenancy EC2 instances have been fully eligible ever since. The lingering belief that dedicated tenancy is required adds material cost to migrations for no compliance benefit.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: What is CSPM | what-is-cspm-cloud-security-posture-management -->

---

## Continuous compliance: AWS Config and conformance packs

Point-in-time hardening is not enough. Static checks decay as infrastructure changes. Watch for new public buckets, widened permissions, and disabled logging as they happen, not in the next quarterly review.

Enable AWS Config to track resource configurations over time and evaluate them against compliance rules. AWS provides managed rules that align with HIPAA requirements, and you can add custom rules for organisation-specific policies. Config gives you the evidence trail that demonstrates continuous compliance rather than point-in-time assessments.

The `Operational Best Practices for HIPAA Security` conformance pack maps HIPAA Security Rule controls to managed AWS Config rules. Deploy it into every account holding ePHI and treat any `NON_COMPLIANT` finding as a P1 remediation item.

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->
<!-- INTERNAL_LINK: Cloud threat detection | cloud-threat-detection -->

---

## Key takeaways

The BAA is necessary but not sufficient. Customers do not automatically inherit HIPAA compliance by using HIPAA eligible services. Sign the BAA via AWS Artifact first, then do the configuration work.

Over 160 HIPAA-eligible services are now available, including Amazon Bedrock and Bedrock AgentCore as of February 2026. Confirm a service is on the current AWS HIPAA Eligible Services Reference before placing PHI on it, and make sure your BAA is active in AWS Artifact. The list changes monthly.

Encrypt everything at rest with KMS CMKs. Every storage resource touching PHI needs KMS encryption: S3 buckets, EBS volumes, RDS instances, DynamoDB tables. EBS and RDS encryption must be set at creation time and cannot be retrofitted without a rebuild.

CloudTrail with six-year retention is non-negotiable. Enable it in all regions, deliver to a cross-account log archive, enable log file validation, and enforce MFA delete on the destination bucket. This is your audit trail for breach investigations and OCR inquiries.

The proposed HIPAA Security Rule update is not yet final; HHS's Fall 2026 Unified Agenda lists July 2027 as OMB's anticipated timeframe for final action. Encryption and MFA are moving from "addressable" to mandatory. If you are not already doing both, close that gap now — not because of what is coming, but because current OCR investigations routinely cite exactly these deficiencies.

Automate compliance monitoring with AWS Config conformance packs. Deploy the HIPAA Security operational best-practices pack, integrate findings into AWS Security Hub, and treat `NON_COMPLIANT` results as live defects. Compliance is continuous or it is not compliance at all.