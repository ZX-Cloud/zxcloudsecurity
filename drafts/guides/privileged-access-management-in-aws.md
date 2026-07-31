---
title: "Privileged Access Management in AWS: A Practitioner's Guide"
date: 2025-07-31
description: "A practical guide to privileged access management in AWS covering JIT access, SCPs, IAM boundaries, monitoring, and common pitfalls for UK enterprises."
tags: ["aws", "iam", "privileged-access-management", "cloud-security", "zero-trust"]
slug: "privileged-access-management-in-aws"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2253
draft: false
---

# Privileged Access Management in AWS: A Practitioner's Guide

Credential abuse doesn't get the attention it deserves in architecture reviews. The 2025 Verizon Data Breach Investigations Report, which analysed over 22,000 security incidents including 12,195 confirmed data breaches, found that credential abuse accounted for 22% of all initial access vectors. That figure should inform every conversation you have about privileged access management in AWS. The cloud amplifies the blast radius of a compromised privileged identity: a single over-permissioned IAM role can open a path from a developer's stolen session token to a full account takeover. This guide walks through how to close those paths, practically and systematically, across IAM policies, Service Control Policies (SCPs), temporary credentials, and detective controls.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: AWS IAM Identity Centre setup guide | aws-iam-identity-centre-guide -->

---

## Why persistent privileged access is the wrong default

The traditional PAM model assumed a clean binary: privileged users versus regular users. Modern application access doesn't work that way. What's actually needed is individual access granted at the right level, for the right duration, through a just-in-time (JIT) approach.

The problem with persistent elevated access in AWS is structural. Infrastructure-as-code has made spinning up resources trivial, but access governance hasn't kept pace. Developers move fast, access gets provisioned for a sprint, and those permissions remain long after the work is done. That's the predictable outcome when access management depends on manual cleanup rather than built-in expiration.

From a UK regulatory standpoint, this matters beyond your security posture. The NCSC publishes 14 Cloud Security Principles to help UK organisations evaluate whether a cloud provider's security posture aligns with their risk appetite and regulatory obligations. Principle 9 addresses identity and access management directly: your provider should make tools available for you to securely manage your use of the service, covering identity and access management, MFA, role-based access controls, and privileged access management. For FCA-regulated firms, the same principles underpin your ability to demonstrate access control adequacy during supervisory reviews.

---

## The four controls that form a PAM foundation in AWS

### 1. Enforce least privilege at the IAM layer

Least privilege means users only have the minimum access necessary to do their job. In practice that means no wildcard actions or resources in IAM policies, and using IAM Access Analyzer to surface what access is actually being used.

Achieving least privilege is a continuous process, not a one-time configuration. IAM Access Analyzer guides you toward it by providing capabilities to set, verify, and refine permissions, using provable security to identify external, internal, and unused access across your AWS resources.

A workflow that holds up in production: start a new role with a broad AWS-managed policy, observe it under real workload conditions for 30 to 90 days via CloudTrail, then use Access Analyzer's policy generation feature. That feature reads CloudTrail logs and produces a scoped policy matching only the actions and resources actually invoked. It's genuinely useful and consistently underused.

<!-- INTERNAL_LINK: AWS Well-Architected Security pillar | aws-well-architected-security -->

### 2. Replace standing access with temporary credentials

Temporary credentials are one of the most powerful mechanisms in AWS, and one of the most misunderstood. They enable short-lived, tightly scoped access without the long-term risk of static IAM user credentials.

AWS issues temporary credentials via the Security Token Service (STS), granting access to resources for a limited duration. These credentials are typically assumed via IAM roles, either directly through `sts:AssumeRole` or through identity federation using AWS IAM Identity Centre.

For privileged human access, the principle is straightforward: preventing direct human interaction with services and systems through automation is the primary means of controlling privileged access. Where automation isn't yet in place, providing a secure method for temporary elevated access is the next best option.

A sound PAM solution needs three things: an eligibility process for granting access, an approval process for granting access, and auditing of the access grants and the activities taken under them.

<!-- INTERNAL_LINK: AWS IAM Identity Centre | aws-iam-identity-centre -->

### 3. Use SCPs as org-wide privilege guardrails

Service Control Policies operate at the AWS Organisations level and are one of the most effective tools for preventing privilege escalation at scale. When attached to an organisation, organisational unit, or account, an SCP defines the maximum available permissions for all accounts in scope. Nothing inside that boundary can exceed it.

Privilege escalation is the ability of a bad actor to use stealthy permissions to elevate privilege levels and compromise security. SCPs are the right place to prevent this: restrict administrative IAM actions to delegated IAM admins, and deny those actions to everyone else, except from approved roles.

A minimal SCP to require MFA for sensitive IAM operations, the kind that should be applied broadly across your production and security OUs, looks like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyIAMPrivEscWithoutMFA",
      "Effect": "Deny",
      "Action": [
        "iam:CreateUser",
        "iam:AttachUserPolicy",
        "iam:AttachRolePolicy",
        "iam:PutUserPolicy",
        "iam:PutRolePolicy",
        "iam:CreateAccessKey",
        "iam:UpdateAssumeRolePolicy",
        "iam:PassRole"
      ],
      "Resource": "*",
      "Condition": {
        "BoolIfExists": {
          "aws:MultiFactorAuthPresent": "false"
        },
        "ArnNotLike": {
          "aws:PrincipalArn": [
            "arn:aws:iam::*:role/BreakGlassAdmin",
            "arn:aws:iam::*:role/PipelineDeployRole"
          ]
        }
      }
    }
  ]
}
```

This SCP blocks the IAM operations most likely to result in privilege escalation: creating users, attaching policies, and creating access keys. Requiring MFA for these actions forces deliberate human involvement and stops automated attacks using stolen credentials cold.

CI/CD pipeline roles are exempted via the `ArnNotLike` condition. Those roles use their own role-assumption authentication chain and would break if MFA was enforced against them. That's an intentional design decision, not a gap, but it needs to be documented and reviewed periodically.

### 4. Apply permissions boundaries for delegated IAM management

SCPs set organisation-wide limits; permissions boundaries provide fine-grained control at the individual principal level. A permissions boundary defines the maximum permissions a role or user can be granted, regardless of what their attached IAM policy says. It's a ceiling, not a grant.

If you allow developers or team leads to create IAM roles (for Lambda functions, say), set a permissions boundary that caps what those created roles can do. Without this, a developer can create a role with `AdministratorAccess`, which is a straightforward privilege escalation path.

The layering to aim for: SCPs at the org level set hard limits no account can break; permissions boundaries at the user and role level prevent privilege escalation by individual principals; resource policies protect specific resources. A denial in any one layer is final.

<!-- INTERNAL_LINK: Shared responsibility model | shared-responsibility-model-cloud-security -->

---

## Implementing just-in-time access with IAM Identity Centre

JIT access removes standing privilege entirely. Time-bound, approval-based permissions that automatically revoke when the window expires are the core mechanism for addressing permission sprawl.

AWS IAM Identity Centre and STS-issued temporary credentials are the natural implementation path. For organisations already using Microsoft Entra, AWS published guidance in 2025 on integrating Entra Privileged Identity Management (PIM) directly with IAM Identity Centre. The approach allows users to request temporary elevated access with justification and approval, with automated provisioning and deprovisioning based on predefined policies.

Every JIT request, whether approved or denied, must be logged and monitored. That audit trail is what makes security forensics and compliance reporting possible after the fact.

The NCSC's March 2025 guidance on Privileged Access Workstations reinforces the automation-first principle: where possible, use automation to replace manual administrative processes, including Infrastructure as Code and a secure CI/CD mechanism.

<!-- INTERNAL_LINK: Cloud incident response | cloud-incident-response -->

---

## Detective controls: monitoring privileged activity

Preventive controls fail. Your detective layer is what limits blast radius when they do.

At minimum, alerting should cover changes to CloudTrail logging, IAM privileges, root activity, security group exposure, KMS deletion scheduling, and S3 bucket policy changes.

Configure CloudTrail across all AWS accounts and regions. This ensures every event is logged regardless of where it occurred, including activity in otherwise unused regions where unusual behaviour is easy to miss.

For IAM-specific alerting, send CloudTrail logs to CloudWatch and create metric filters and alarms that fire when specific events or anomalies in the type or volume of IAM API calls are detected.

The root account has full permissions to create accounts, delete accounts, alter billing, and take down your entire infrastructure. It should almost never be used. If it is used, your security team needs to know immediately.

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->
<!-- INTERNAL_LINK: Cloud threat detection | cloud-threat-detection -->
<!-- INTERNAL_LINK: AWS KMS key management best practices | aws-kms-key-management-best-practices -->

The CIS AWS Foundations Benchmark remains the most practical baseline to automate against. AWS Security Hub supports CIS AWS Foundations Benchmark versions 5.0.0, 3.0.0, 1.4.0, and 1.2.0. AWS recommends v5.0.0. Security Hub automates continuous compliance scanning against it, so deviations surface without requiring manual audits.

---

## Common pitfalls in AWS privileged access management

These are the mistakes I see consistently across AWS estates, including ones that have passed internal audits.

Treating SCPs as the sole control. SCPs are coarse-grained guardrails, and they don't grant access. You still need identity-based or resource-based policies to actually permit anything. SCPs define the ceiling; they don't do the floor work.

Ignoring policy evaluation order. A common mistake is assuming permissions boundaries override or conflict with resource policies or SCPs. They don't: each acts as an independent constraint, and a denial in any one layer is final. Engineers waste hours broadening identity policies when the blocker is actually an SCP or a boundary condition elsewhere.

Using AWS-managed policies as permanent fixtures. AWS-managed policies are continuously updated by AWS. The permissions they grant will likely grow over time as AWS adds new services and features. What passed your last access review may be significantly broader six months later.

Treating access reviews as annual events. An annual IAM review is a checkbox exercise. Run IAM Access Analyzer continuously to detect external and unused access, monitor for anomalous IAM API calls via CloudTrail and GuardDuty, and use AWS Config rules to flag non-compliant IAM configurations automatically.

Keeping long-lived access keys for human users. IAM user keys being exposed is one of the biggest causes of breaches over the past decade. They don't expire, they frequently carry too many privileges, and they're easy to identify in the wild due to their distinctive `AKIA` prefix. There is no acceptable use case for human users authenticating via long-lived access keys in 2025. If you have them, you have a liability.

Ignoring the root account as an attack surface. The root account is the most privileged identity in AWS. Minimise its use, adopt least privilege for everything else, and lock it down with hardware MFA. Alert on every single usage without exception.

Not exempting CI/CD roles thoughtfully. Break-glass and pipeline role exemptions in SCPs need to be documented, version-controlled, and reviewed periodically. An unreviewed exemption list becomes a map of your privilege escalation paths.

<!-- INTERNAL_LINK: DevSecOps shift-left security | devsecops-shift-left-security -->

---

## Key takeaways

Credential abuse accounted for 22% of all confirmed breaches in the 2025 Verizon DBIR. Privileged access management in AWS is a first-order security priority, not a compliance afterthought.

Eliminate standing privilege wherever possible. JIT access via IAM Identity Centre and STS-issued temporary credentials is the architectural target. Temporary, scoped access by default is what makes least privilege operational in practice.

Layer your controls. SCPs set the organisational ceiling, permissions boundaries cap individual principals, and IAM policies define actual grants. A denial in any layer is final. Design with that in mind, and test all three layers when access breaks unexpectedly.

The CIS AWS Foundations Benchmark is your baseline, not your ceiling. CIS AWS Foundations Benchmark v5.0.0 covers 60+ controls across IAM, storage, logging, monitoring, and networking. Automate enforcement via Security Hub and treat deviations as incidents, not observations.

Detective controls are non-negotiable. CloudTrail, CloudWatch metric filters for IAM privilege changes, GuardDuty, and IAM Access Analyzer running continuously are the minimum viable setup. Alert on root usage, IAM policy changes, and CloudTrail disablement as high-severity events requiring immediate investigation.

Phishing-resistant MFA is required for all privileged accounts. The NCSC recommends FIDO2 security keys or passkeys for administrative access. TOTP apps are an acceptable stepping stone; they are not the destination.