---
title: "Privileged Access Management in AWS: A Practitioner's Guide"
date: 2025-07-12
description: "A practical guide to privileged access management in AWS covering JIT access, SCPs, IAM Access Analyzer, root account controls, and common pitfalls."
tags: ["aws", "iam", "privileged-access-management", "cloud-security", "zero-trust"]
slug: "privileged-access-management-in-aws"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2149
draft: false
---

# Privileged Access management in AWS: a practitioner's guide

In my experience, privileged access is the single control domain where UK financial services firms and government clients accumulate the most critical risk, and they do it quietly, incrementally, and often invisibly until something breaks. An IAM key leaks. Root credentials sit cached on a developer laptop. A contractor leaves but their access persists for months.

The blast radius here is different from on-premises. A compromised AWS admin identity can reach compute, storage, networking, secrets, and billing simultaneously across multiple accounts and regions. That changes what good PAM looks like.

This guide gives you a concrete, implementable framework covering architecture, native AWS controls, JIT access patterns, detection, and the mistakes I see teams make repeatedly.

<!-- INTERNAL_LINK: what is zero trust architecture | what-is-zero-trust-architecture -->
<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->

---

## Why privileged access is a different problem in AWS

Traditional PAM thinking — vault the root password, rotate it quarterly, done — does not map cleanly onto AWS. You are dealing with account root users, shared users, local users, and federated users, all with varying levels of access depending on the roles and permission sets they hold or can assume. The attack surface is wider, and the consequences of getting it wrong are proportionally larger.

The NCSC is unambiguous on this point. Highly privileged access, particularly access to customer data, requires particularly careful management, including authorisation from multiple nominated personnel and phishing-resistant MFA. For FCA-regulated firms, that is not aspirational guidance. It maps directly onto your operational resilience and cyber frameworks.

<!-- INTERNAL_LINK: AWS compliance and governance | aws-compliance-and-governance -->
<!-- INTERNAL_LINK: what is CIEM | what-is-ciem-cloud-infrastructure-entitlement-management -->

---

## The four pillars of AWS PAM

### 1. Root account hardening

The AWS root user is the single most dangerous identity in any account. In a multi-account organisation, the individual or team controlling the root password should not also control the MFA token. Dual control is the baseline.

In June 2025, AWS extended its mandatory root MFA requirement to member accounts, completing a phased rollout that began with management and standalone accounts, and centralised root access management lets you remove long-lived root credentials from member accounts entirely. Use this feature. It is the strongest root account control AWS has shipped to date.

Root credentials should be stored in a vaulted PAM solution such as CyberArk or HashiCorp Vault, with dual-control access and mandatory audit logging on every retrieval. Access should only happen through a well-documented break-glass procedure, not as part of routine operations.

### 2. Eliminate standing privilege and adopt JIT access

Standing privilege is the enemy. Every identity with persistent `AdministratorAccess` or broad PowerUser rights attached is a liability. The model to work towards is just-in-time administration combined with just-enough administration: access granted for the minimum scope required, persisting only for the duration of the task.

In AWS, the primary native path for JIT elevated access is IAM Identity Center combined with time-bound permission set assignments. If you are running Microsoft Entra ID as your identity provider, which is common in UK enterprise and government, pairing IAM Identity Center with Entra PIM gives you a solid architecture. You map security groups in Entra to permission sets in IAM Identity Center, automate provisioning and deprovisioning through approval workflows, and get a clean audit trail of who had what access and when.

This is the architecture I would deploy first in most environments.

<!-- INTERNAL_LINK: AWS IAM Identity Center guide | aws-iam-identity-centre-guide -->

### 3. Enforce least privilege with SCPs and permissions boundaries

Least privilege is not a one-time policy configuration. It is an ongoing operational discipline. AWS gives you two complementary mechanisms for enforcing it at scale.

Service Control Policies (SCPs) operate at the AWS Organizations level and define the ceiling on what IAM users and roles in member accounts can do. If an SCP does not allow an action, it cannot be performed regardless of what the IAM policy says. That includes the root user of member accounts.

Below is a production-grade SCP combining several high-value privileged access controls: denying root API usage in member accounts, preventing CloudTrail from being disabled, and requiring MFA for sensitive IAM actions.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyRootAccountAPIAccess",
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
      "Sid": "ProtectCloudTrailFromDisabling",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail",
        "cloudtrail:UpdateTrail",
        "cloudtrail:PutEventSelectors"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyHighRiskIAMWithoutMFA",
      "Effect": "Deny",
      "Action": [
        "iam:CreateUser",
        "iam:AttachUserPolicy",
        "iam:CreateAccessKey",
        "iam:DeleteRolePolicy"
      ],
      "Resource": "*",
      "Condition": {
        "BoolIfExists": {
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    },
    {
      "Sid": "PreventGuardDutyDisabling",
      "Effect": "Deny",
      "Action": [
        "guardduty:DeleteDetector",
        "guardduty:DisassociateFromAdministratorAccount",
        "guardduty:StopMonitoringMembers"
      ],
      "Resource": "*"
    }
  ]
}
```

> Do not attach SCPs without thoroughly testing the impact on target accounts first. Test in a separate organisation or OU, then deploy to more specific OUs and broaden incrementally. Be aware that the unconditional deny on `cloudtrail:UpdateTrail` also blocks legitimate trail changes, such as attaching a KMS key or moving the destination S3 bucket, so you will need a controlled exception process (for example, a temporary SCP change under change control) for approved trail modifications.

Permissions boundaries are the second mechanism. They cap the maximum effective permissions any IAM role or user can exercise, even if a developer later attaches a broader policy. This is the right tool for delegating IAM management to application teams without losing central governance.

### 4. Continuous least-privilege refinement via IAM Access Analyzer

IAM Access Analyzer gives you tools to set, verify, and refine permissions across your accounts. The feature I find most useful in practice is policy generation from CloudTrail activity: you deploy a role with broader permissions during development, let the workload run for two to four weeks, then ask Access Analyzer to generate a tightened policy based on what was actually called.

Feed that generated policy through your CI/CD pipeline using the `ValidatePolicy` API before promoting to production. Bear in mind what that check actually does: it validates policy syntax and flags deviations from IAM best practice, but it does not confirm the generated policy is functionally complete for your workload, so test the tightened policy in a non-production environment before cutover. It will not catch every edge case, but it removes the guesswork from least-privilege refinement and gives you an evidence base for your access reviews.

<!-- INTERNAL_LINK: AWS CloudTrail configuration best practices | aws-cloudtrail-configuration-best-practices -->
<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->

---

## Privileged access workstations and the NCSC's March 2025 guidance

The NCSC published updated principles on privileged access workstations (PAWs) in March 2025. The core argument is straightforward: a dedicated PAW is one of the most effective controls for defending administrators against credential theft and malware infection. When designed properly, PAWs address real-world attack paths that technical controls in AWS cannot reach.

For AWS console access, this means privileged administrators should only authenticate from hardened, managed devices, not from the same laptop they use for day-to-day work and email. Enforce this via IAM Identity Center's attribute-based access controls combined with an MDM policy assertion. Where your organisation uses Entra ID, Conditional Access policies can restrict AWS console authentication to compliant devices registered in Intune.

On MFA: the NCSC recommends phishing-resistant MFA for administrative access, specifically FIDO2 security keys or passkeys. For your highest-privilege roles, anything with `iam:*` or cross-account assume-role rights, hardware FIDO2 keys are the correct choice. Software TOTP is not sufficient for production admin access to sensitive workloads.

---

## Session monitoring and audit logging

PAM in AWS is incomplete without immutable, queryable audit trails. Privileged session logging tells you who accessed what, what actions they performed, and when. That matters both for forensic analysis after an incident and for demonstrating compliance to your auditors.

Your core audit stack should cover:

- AWS CloudTrail for management events and data events on sensitive services (S3, KMS, Secrets Manager). Enable CloudTrail Lake for long-term queryable storage.
- AWS GuardDuty for anomalous usage of powerful IAM credentials, including credential exfiltration and unusual cross-region role assumption patterns.
- AWS Config for continuous recording of IAM resource configuration changes, with managed rules for detecting overly permissive policies.
- VPC Flow Logs and CloudWatch Logs Insights to correlate network behaviour with identity activity during incident investigation.

For FCA-regulated firms, your audit log retention must satisfy both internal audit requirements and ICO expectations under GDPR Article 5(2). My baseline recommendation is 12 months hot and 36 months archived.

<!-- INTERNAL_LINK: cloud incident response | cloud-incident-response -->

---

## Third-party PAM tools: when native controls are not enough

AWS IAM covers MFA, RBAC, and policy-based access controls well. What it does not give you out of the box is privileged session recording with keystroke logging, credential vaulting for service accounts, or structured access request workflows with approval routing and justification capture.

For organisations subject to PCI DSS, DORA, or FCA operational resilience requirements, those gaps can matter at audit time. CyberArk, Teleport, and BeyondTrust all address them, and each integrates with AWS through different mechanisms. If your organisation already has CyberArk on-premises, extending it to cover AWS is usually the lowest-friction path to covering privileged session recording for EC2 instances.

The decision to add a third-party PAM tool should be driven by specific compliance requirements, not by a general sense that more tooling equals more security. Native AWS controls, properly configured, are adequate for many organisations. Know what your auditors actually need before you invest.

<!-- INTERNAL_LINK: cross-cloud security services comparison | cross-cloud-security-services-comparison -->

---

## Common pitfalls in AWS privileged access management

After reviewing dozens of AWS environments across financial services, central government, and NHS organisations, these are the patterns I see fail most often.

### Treating the management account as just another account

The AWS Organizations management account is exempt from SCPs. SCPs apply only to member accounts and have no effect on users or roles in the management account. Teams frequently deploy workloads, pipelines, and human users into the management account, then wonder why their guardrails do not apply. Keep the management account empty except for AWS Organizations administration.

### Long-lived IAM access keys left in rotation

I still find production environments where applications are authenticating with access keys created in 2019. There is no legitimate use case for long-lived keys in a modern workload. Use IAM roles for EC2, Lambda, ECS, and EKS. Use OIDC federation for CI/CD pipelines. Prohibit static credentials by policy and enforce it with an SCP.

### Neglecting machine identity in PAM scope

PAM in AWS is not just a human identity problem. Service accounts, Lambda execution roles, EC2 instance profiles, and CI/CD pipeline roles often carry excessive permissions that are never reviewed. Roles get created in a rush, permissions are copied from other roles, and nobody circles back to audit them. Over time, permissions accumulate and your exposure grows without anyone noticing.

### Not testing SCPs before broad deployment

An SCP applied at the organisational root with a missing Allow statement can lock every member account out of services simultaneously. Always test in a sandbox OU, use the IAM Policy Simulator, and roll out incrementally. Missing an Allow at the root level is not a minor misconfiguration. It will effectively block all access to AWS services for every member account in your organisation.

### Ignoring the break-glass process

Every organisation needs a documented, tested emergency access procedure. If your JIT system goes down, can your team still respond to a production incident? The break-glass role should exist in every account, with access tightly restricted, MFA enforced, and every use generating an alert to your SOC. Document it, test it at least annually, and make sure the people who need it can find the credentials under pressure.

### Skipping access reviews

IAM provides last-accessed information specifically to help you identify users, roles, policies, and credentials you no longer need. Use it. Quarterly access reviews are the minimum for regulated environments. Automate the data collection so the human review is tractable rather than a week-long manual exercise.

<!-- INTERNAL_LINK: cloud security vulnerability management | cloud-security-vulnerability-management -->
<!-- INTERNAL_LINK: what is CSPM | what-is-cspm-cloud-security-posture-management -->

---

## Key takeaways

Eliminate standing privilege first. JIT access via IAM Identity Center with time-bound permission sets is the highest-leverage change most AWS environments can make today. Access granted only when needed and for a limited time removes a large class of risk without requiring third-party tooling.

Lock down root accounts at the organisational level. Enforce root MFA across all AWS Organizations member accounts, remove root credentials from member accounts using centralised root access management, and maintain a tested break-glass procedure.

Use SCPs as your permission ceiling, not your only control. SCPs define what is possible in member accounts. You still need IAM policies, permissions boundaries, and Access Analyzer to achieve genuine least privilege within that ceiling.

Make audit logs immutable and queryable. CloudTrail is table stakes. CloudTrail Lake, GuardDuty anomaly detection, and centralised SIEM integration are the production standard for organisations with real compliance obligations.

Treat static access keys as a critical finding. Prohibit long-lived IAM credentials by policy and SCP, enforce rotation via Config rules, and use IAM Access Analyzer to surface unused credentials automatically.

Extend PAM to machine identities. Every Lambda role, EC2 instance profile, and CI/CD pipeline identity is in scope, not just the humans with console access.