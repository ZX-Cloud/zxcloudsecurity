---
title: "AWS KMS Key Management Best Practices: A Production-Grade Guide"
date: 2026-06-18
description: "Master AWS KMS key management best practices with real policy examples, rotation strategy, audit controls, and pitfalls that cost teams dearly in production."
tags: ["aws-kms", "encryption", "cloud-security", "iam", "key-management"]
slug: "aws-kms-key-management-best-practices"
author: "Steve Harrison - Principal Security Architect"
word_count: 2472
draft: false
---

# AWS KMS key management best practices: a production-grade guide

If you are running regulated workloads in AWS — whether that is FCA-supervised financial services, NHS data, or any system handling UK GDPR-classified personal data — your encryption story is only as strong as your key management posture. KMS key management is not optional configuration hygiene. It is the difference between a defensible audit trail and an irrecoverable data loss event.

Every encrypted S3 object, EBS volume, RDS database, and secret in Secrets Manager depends on KMS keys. Misconfigure them and an attacker can decrypt your most sensitive data, or render it permanently inaccessible by scheduling key deletion. The January 2025 Codefinger ransomware campaign made that threat concrete. This guide covers the practices that matter most in production, with real policy syntax and honest trade-offs.

<!-- INTERNAL_LINK: AWS IAM least privilege guide | aws-iam-least-privilege-best-practices -->

---

## Understand the key hierarchy before you design anything

KMS keys are logical representations of a cryptographic key. There are three types: customer managed keys that you create, AWS managed keys that AWS services create in your account on your behalf, and AWS owned keys that an AWS service owns and manages across multiple accounts.

The distinction matters in practice. Customer managed keys give you full control over lifecycle and usage. AWS managed keys give you CloudTrail visibility but hand control to the service. AWS owned keys give you neither. They are appropriate only for low-sensitivity workloads where you accept the shared responsibility trade-off.

The NCSC's cloud security guidance puts it plainly: good data encryption is undermined by poor key management. Getting this right is difficult because key management is a complex and subtle topic. That framing is accurate. I have reviewed configurations where teams assumed AWS managed keys were sufficient for regulated data, and the audit conversation did not go well.

For most organisations, the right starting point is one customer managed key per application, per environment, per data classification level. This gives you clean separation of duties, granular CloudTrail attribution, and the ability to perform crypto-shredding at the data tier without touching adjacent systems.

---

## Design key policies with separation of duties in mind

A key policy is a resource policy for a KMS key and the primary way to control access to it. Every KMS key must have exactly one key policy, and the statements in that policy determine who can use the key and how.

Here is the principle that trips up most teams: no AWS principal has any permissions to a KMS key unless those permissions are explicitly allowed in a key policy, an IAM policy, or a grant. Without a key policy grant, IAM policies that allow KMS permissions have no effect. The key policy is the outer gate.

Separation of duties means administrator roles that create and delete keys must not have the ability to use the key cryptographically. Some services may only need to encrypt data and should not be granted decrypt permissions. This is not a theoretical control. It directly limits the blast radius of a compromised admin credential.

The following is a hardened key policy skeleton that enforces this separation. It names administrator and user roles explicitly rather than delegating broadly to the account root.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnableRootAccountForBreakGlass",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:root"
      },
      "Action": "kms:*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:PrincipalType": "Account"
        }
      }
    },
    {
      "Sid": "AllowKeyAdministration",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:role/kms-admin-role"
      },
      "Action": [
        "kms:Create*",
        "kms:Describe*",
        "kms:Enable*",
        "kms:List*",
        "kms:Put*",
        "kms:Update*",
        "kms:Revoke*",
        "kms:Disable*",
        "kms:Get*",
        "kms:Delete*",
        "kms:TagResource",
        "kms:UntagResource",
        "kms:ScheduleKeyDeletion",
        "kms:CancelKeyDeletion"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowEncryptOnly",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:role/app-ingest-role"
      },
      "Action": [
        "kms:GenerateDataKey",
        "kms:Encrypt"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "kms:ViaService": "s3.eu-west-2.amazonaws.com"
        }
      }
    },
    {
      "Sid": "AllowDecryptForReadRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:role/app-reader-role"
      },
      "Action": [
        "kms:Decrypt",
        "kms:DescribeKey"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "kms:ViaService": "s3.eu-west-2.amazonaws.com"
        }
      }
    }
  ]
}
```

A few things worth noting in this policy. The `kms:ViaService` condition ties key usage to a specific AWS service in a specific region. Restricting KMS key usage this way limits an attacker's ability to use your keys for unauthorised encryption or decryption via direct API calls. The ingest role can encrypt but not decrypt, which is a useful control for write-only pipelines. The admin role has no cryptographic permissions at all. That is separation of duties enforced at the policy layer, not just in documentation.

Do not use `kms:*` for actions in IAM or key policies. It grants a principal permissions to both administer and use the key simultaneously.

<!-- INTERNAL_LINK: AWS SCP guardrails for production accounts | aws-service-control-policies-guide -->

---

## Enable and enforce automatic key rotation

When a KMS key is rotated, only the current key material changes. AWS KMS retains all previous key material versions and automatically uses the correct one when decrypting existing ciphertext. Consuming applications see none of this. No code changes are required.

This is one of the genuinely well-designed features of KMS. Rotation is operationally transparent, which removes the usual excuse for not enabling it.

Enable automatic rotation on every customer managed symmetric key you provision. You can also trigger on-demand rotation using the `RotateKeyOnDemand` API, which is worth knowing about when responding to a suspected credential exposure.

On pricing: each key incurs a base cost, and the first two rotations add $1 per month (prorated hourly) in additional charges. Subsequent rotations beyond the second are not billed separately. The capped pricing makes frequent rotation economically straightforward to justify to finance teams.

Enforce rotation at scale using AWS Config's `cmk-backing-key-rotation-enabled` managed rule, or the equivalent Security Hub control. Both will flag non-compliant keys automatically.

---

## Lock down key deletion with SCPs and condition keys

Accidental key deletion is one of the few truly irreversible mistakes you can make in AWS. When a KMS key is scheduled for deletion it enters a `PendingDeletion` state for a mandatory waiting period of 7 to 30 days. During this window the key is unusable for encryption or decryption. If the waiting period expires, the key material is destroyed and any data encrypted by that key is permanently unrecoverable. That is cryptographic erasure. There is no recovery path.

Implement two layers of protection. First, an SCP at the AWS Organisations level:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyKMSKeyDeletion",
      "Effect": "Deny",
      "Action": "kms:ScheduleKeyDeletion",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalArn": "arn:aws:iam::*:role/BreakGlassKMSAdmin"
        }
      }
    }
  ]
}
```

SCPs set permission guardrails that apply to all accounts within an AWS Organisation. This one ensures that only a named break-glass role can schedule key deletion across your entire estate.

Second, use the `kms:TrailingDaysWithoutKeyUsage` condition key in the key policy itself. This lets you automatically block deletion or disabling of recently used keys, which is a useful data-driven safety net on top of the SCP. Pair it with a CloudWatch alarm that fires if anything attempts to use a key during its pending deletion window. Teams schedule key deletion, forget about it, and find out three weeks later that their backup restore job has been silently broken.

For any temporary deactivation, prefer disabling a key over scheduling its deletion. Disabled keys preserve key material. Deleted keys do not.

---

## Audit every KMS action with CloudTrail

CloudTrail logs all AWS KMS operations: read-only operations such as `ListAliases` and `GetKeyRotationStatus`, management operations such as `CreateKey` and `PutKeyPolicy`, cryptographic operations such as `GenerateDataKey` and `Decrypt`, and internal operations that AWS KMS performs on your behalf such as `RotateKey` and `DeleteExpiredKeyMaterial`.

Default CloudTrail event history covers 90 days. For anything beyond that, create a trail and write it to S3. If you manage an AWS Organisation, create an organisation trail that covers all member accounts in a single configuration.

Amazon EventBridge is worth setting up alongside CloudTrail. It receives events from CloudTrail and Security Hub in near real time and lets you create rules that trigger on specific KMS operations. For the operations that matter most, including `DisableKey`, `ScheduleKeyDeletion`, `PutKeyPolicy`, and `DeleteAlias`, you want alerting, not just logging.

For FCA-regulated firms and public sector organisations operating under NCSC Cloud Security Principles, KMS integration with CloudTrail is audit evidence. Write those logs to a separate, locked-down security account. Never store them in the same account as the workload keys.

AWS recently launched the `GetKeyLastUsage` API, which lets you quickly determine when a key was last used for a cryptographic operation. This is particularly useful during key cleanup exercises and before scheduling any deletion.

<!-- INTERNAL_LINK: AWS CloudTrail centralised logging architecture | aws-cloudtrail-centralised-logging -->

---

## Centralised vs. decentralised key management

When designing your KMS architecture you need to decide whether to manage keys centrally in one or a few designated accounts, or distribute key management to individual workload accounts.

The centralised model keeps all keys in a shared account. Other accounts are permitted only to use those keys for cryptographic operations. Lifecycle management and policy changes all happen from one place. This reduces the risk of unintended deletion or privilege escalation by delegated administrators in workload accounts.

AWS generally recommends starting with a decentralised approach unless you have a specific reason to centralise. That is reasonable default guidance. That said, regulated environments often have compliance drivers that push towards centralisation, and I have seen both models work well when the access boundaries are clearly defined.

For multi-account environments managed via AWS Control Tower or Landing Zone Accelerator, I usually recommend a hybrid: a centralised key management account for shared platform services such as logging, backup, and audit, with decentralised customer managed keys per workload account for application data.

On BYOK: the NCSC's position is clear. When keys are generated externally and imported into a KMS, you are introducing more opportunities for the key to be lost or stolen. The NCSC recommends avoiding HYOK and BYOK where possible. Unless a specific regulatory requirement mandates external key material (which is rare and is usually a misreading of the requirement), keep key generation inside the AWS KMS HSM boundary.

---

## Common pitfalls in production environments

These are the mistakes I find most frequently when reviewing KMS configurations for UK financial services and government clients.

Using `kms:*` in key or IAM policies grants a principal both administrative and cryptographic permissions simultaneously. If that principal is compromised, the attacker has everything. Least privilege means separating those permission sets explicitly.

Setting `"Resource": "*"` in IAM policies for cryptographic operations is equally problematic. A wildcard in the Resource element applies the permissions to all KMS keys in all accounts the principal has access to, potentially including keys in other accounts. Scope by key ARN.

Setting `"Principal": "*"` in a key policy without a tightly scoped condition gives every identity in every AWS account permission to use the key. This comes up more often than it should, usually in keys created by developers testing something quickly.

Adding IAM users directly to key policies creates a maintenance problem. Every time the authorised user list changes, the key policy needs updating. Use IAM roles.

Relying on AWS managed keys for sensitive data workloads is a common assumption that does not hold up under scrutiny. AWS managed keys offer no ability to restrict cross-service usage, set custom rotation schedules, or enforce encryption context conditions. For anything classified as sensitive or restricted under UK GDPR Article 4, use a customer managed key.

Key policies are regional. Unlike IAM policies, a key policy controls access only to a KMS key in the same region. Multi-region deployments require careful per-region policy management. Teams running active-active or DR setups sometimes discover this gap late.

Finally: set the CloudWatch alarm for pending deletion. This is the simplest control on this list and the one most frequently skipped.

---

## Key takeaways

Separate administrators from users at the key policy level. Admin roles must not have `kms:Encrypt` or `kms:Decrypt`. Cryptographic roles must not have `kms:PutKeyPolicy` or `kms:ScheduleKeyDeletion`. This is the single most impactful control you can implement.

Enable automatic key rotation on every customer managed key. It is operationally transparent, now affordable due to capped pricing beyond two rotations, and expected by every compliance framework from CIS AWS Foundations through to NCSC Cloud Security Principles.

Deny `kms:ScheduleKeyDeletion` via SCP at the organisation level and limit it to a named break-glass role. Pair this with the `kms:TrailingDaysWithoutKeyUsage` condition key in the key policy for defence in depth. Key deletion is irreversible.

Write CloudTrail to a locked security account and configure EventBridge rules for high-risk operations including `DisableKey`, `ScheduleKeyDeletion`, `PutKeyPolicy`, and `DeleteAlias`. For FCA or NCSC-regulated environments, this log stream is audit evidence.

Avoid BYOK and HYOK unless a specific, audited regulatory requirement mandates it. The NCSC explicitly recommends against both, and the operational complexity rarely delivers meaningful security uplift when AWS KMS generates keys inside FIPS-validated HSMs.

Enforce `kms:ViaService` conditions on application keys to restrict usage to the specific AWS service and region your workload requires. This is one of the most underused controls in KMS and directly limits the blast radius of a compromised IAM credential.

<!-- INTERNAL_LINK: AWS Security Hub baseline configuration | aws-security-hub-baseline-guide -->
<!-- INTERNAL_LINK: Envelope encryption patterns on AWS | aws-envelope-encryption-patterns -->