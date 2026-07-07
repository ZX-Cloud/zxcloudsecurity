---
title: "AWS IAM Best Practices: A Practitioner's Guide for 2026"
date: 2026-07-07
description: "A technical guide to AWS IAM best practices covering least privilege, SCPs, federation, Access Analyzer, and the most common IAM mistakes to avoid."
tags: ["aws", "iam", "cloud-security", "identity", "least-privilege"]
slug: "aws-iam-best-practices"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2291
draft: false
---

# AWS IAM best practices: a practitioner's guide for 2026

Identity is the perimeter. If you've spent any time reviewing AWS breach post-mortems, you'll already know the pattern: it's almost never an exotic zero-day. Over 80% of AWS breaches trace back to IAM misconfiguration, not novel attacks, just people leaving the door open. Getting IAM right is therefore the single highest-leverage security investment you can make in any AWS environment. This guide covers what that looks like in production: the controls, policy patterns, and guardrails I reach for on every engagement. If you're working in a regulated UK sector such as FCA-supervised financial services, central government, or NHS, most of this maps directly to the NCSC's Cloud Security Principles and the CIS AWS Foundations Benchmark.

<!-- INTERNAL_LINK: What is Zero Trust Architecture | what-is-zero-trust-architecture -->

---

## Why IAM remains the highest-priority attack surface

The AWS shared responsibility model places identity, configuration, and workload protection squarely on customers. That means misconfigurations and permission creep drive most incidents.

A developer requests extra access "just for a day." An old EC2 role hasn't been touched in years. A contractor key is still active. Your CI pipeline somehow has more privileges than production engineers. Individually, none of those look dangerous. Together, they represent a systemic failure of access governance.

Sound IAM controls also give you defensible evidence for SOC 2 CC6.x (Logical Access), PCI DSS Req. 7/8 (Restrict Access), and ISO 27001 A.9 (Access Control). For UK public sector organisations, AWS provides a conformance pack mapping IAM controls directly to NCSC Cloud Security Principles, which is useful evidence for G-Cloud procurement and Crown Commercial Service assurance processes.

<!-- INTERNAL_LINK: AWS Compliance and Governance | aws-compliance-and-governance -->

---

## 1. Kill the root account for day-to-day use

The root account has unrestricted access to all resources and cannot be constrained by IAM policies. Use it only for account-level tasks that specifically require root credentials, such as changing account settings or closing the account.

In practice: create your root account, immediately enable MFA, remove any access keys, and then never use it again. Use a hardware MFA device for root, not a virtual authenticator that could be compromised alongside other credentials. The NCSC explicitly recommends phishing-resistant MFA (FIDO2 security keys or passkeys) for administrative access.

If you're running AWS Organizations, enforce this at scale with an SCP:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyRootUserActions",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "aws:PrincipalArn": "arn:aws:iam::*:root"
        }
      }
    }
  ]
}
```

The root user bypasses all IAM policies and has unrestricted access to every resource, all billing information, and account closure. This SCP prevents accidental or malicious root usage and enforces the use of IAM roles with proper audit trails and scoped permissions.

---

## 2. Eliminate long-lived IAM user credentials

Handing a developer an access key pair and calling it done is no longer acceptable. Require human users to access AWS through temporary credentials. Federate through an identity provider so users assume roles, which provide short-lived credentials that expire automatically.

For centralised access management, AWS recommends IAM Identity Center to manage access across accounts and permissions within them. Federate that into your existing corporate IdP (Entra ID, Okta, Google Workspace) and your joiners/movers/leavers process flows through to AWS automatically. When someone leaves, disabling their IdP account revokes access to all connected systems immediately.

The same principle applies to workloads. When you're running on EC2 or Lambda, AWS delivers temporary credentials from an IAM role directly to the compute resource. Applications built with an AWS SDK will discover and use those credentials automatically, so there's no need to distribute long-lived credentials to anything running on AWS.

For CI/CD pipelines running outside AWS, use OIDC federation. GitHub Actions, GitLab CI, and CircleCI all support it natively. The migration path is straightforward: IAM Identity Center for humans, IAM Roles Anywhere for on-premises workloads, and OIDC federation for CI/CD pipelines.

<!-- INTERNAL_LINK: AWS IAM Identity Centre Guide | aws-iam-identity-centre-guide -->

---

## 3. Enforce least privilege, and automate it

Least privilege means granting only the specific permissions required to perform specific tasks. In theory, everyone agrees with this. In practice, teams default to broad permissions because it's faster, and then never come back to tighten them.

The honest way to achieve least privilege at scale is to use data, not guesswork. IAM Access Analyzer can analyse the services and actions your IAM roles actually use, then generate a fine-grained policy based on that observed activity in CloudTrail. That's a much more reliable starting point than trying to reason from first principles about what a role might need.

The flow I use for new workloads:

1. Deploy the role with a deliberately broad policy in a non-production account
2. Run a representative workload for 7-14 days (enough to cover all code paths)
3. Use Access Analyzer's policy generation to produce a tightened policy based on observed CloudTrail activity
4. Human review, then promote to production

Two caveats worth knowing. CloudTrail doesn't capture everything: data-plane calls on S3 and KMS need explicit configuration, otherwise they won't appear in the activity log. Generated policies also tend to be over-specific, referencing literal resource ARNs from your test environment, so they need parameterising before they're production-ready. Treat the output as a draft, not a finished deliverable.

For existing roles, check the "Last accessed" column in the IAM console for each service. If a permission hasn't been used in 90 days, it's probably safe to remove.

### Using conditions to add context

You can specify conditions under which a permission applies. For sensitive operations such as IAM changes or KMS key deletion, enforcing MFA as a condition is worth the overhead:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireMFAForDestructiveActions",
      "Effect": "Deny",
      "Action": [
        "iam:DeleteRole",
        "iam:DeleteUser",
        "kms:ScheduleKeyDeletion",
        "s3:DeleteBucket"
      ],
      "Resource": "*",
      "Condition": {
        "BoolIfExists": {
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    }
  ]
}
```

---

## 4. Use SCPs as organisation-wide guardrails

Service control policies (SCPs) give you central control over the maximum available permissions for IAM users and roles across an organisation. An SCP defines a permission guardrail; it sets the ceiling on what principals in your organisation can do. Critically, SCPs don't grant permissions. They only restrict them.

A significant update landed in September 2025 that expanded what's possible: AWS Organizations now supports full IAM policy language in SCPs, including conditions, individual resource ARNs, and the `NotAction` element with Allow statements. That brings SCP authoring much closer to standard IAM policy writing.

For UK-based organisations with GDPR or data residency obligations, a region-restriction SCP is non-negotiable. Deny all regions except those you actively operate in (typically `eu-west-1` and `eu-west-2`). This enforces data residency requirements, concentrates your security monitoring, and means an attacker who compromises credentials can't quietly spin up resources in regions you've never looked at.

<!-- INTERNAL_LINK: What is CIEM | what-is-ciem-cloud-infrastructure-entitlement-management -->

One practical caution: keep a break-glass IAM role in the management account. SCPs apply to every account in your organisation except the management account itself, which means a misconfigured SCP can lock your team out of member accounts. I've seen it happen.

---

## 5. Use permissions boundaries for delegated IAM

When you need to give teams the ability to create their own IAM roles (common in product teams working autonomously), permissions boundaries are the right mechanism. A managed policy attached as a permissions boundary defines the maximum permissions that identity-based policies can grant to an entity, without itself granting any permissions.

The practical use case: you want a development team to create IAM roles for their applications, but you don't want those roles to exceed the team's own permissions. Attach a permissions boundary to any role the team creates, capping what that role can actually do. Even if the team attaches `AdministratorAccess` to a role they create, the permissions boundary limits what that role can actually perform.

<!-- INTERNAL_LINK: AWS Well-Architected Security | aws-well-architected-security -->

---

## 6. Define all IAM in infrastructure as code

IAM policies created through the console are hard to audit, difficult to review, and impossible to track changes on. Every IAM role, policy, and trust relationship should live in version-controlled Terraform or CloudFormation. IAM policy checks can now run directly inside DevOps pipelines, scanning Terraform plans and policy JSON before deployment.

Integrate `aws iam validate-policy` into your CI pipeline. Enable IAM Access Analyzer's custom policy checks as a build gate. Any policy that grants `*:*` or creates a privilege escalation path should fail the build, not reach production.

<!-- INTERNAL_LINK: AWS CloudTrail Configuration Best Practices | aws-cloudtrail-configuration-best-practices -->

---

## 7. Monitor IAM continuously

IAM Access Analyzer covers a lot of ground: findings for external, internal, and unused access; basic and custom policy checks; and policy generation from observed activity. Run an organisation-scoped analyser rather than per-account analysers. The organisation scope surfaces cross-account access paths that per-account analysers miss entirely.

Enable GuardDuty's IAM threat detection. It will surface credential exfiltration, anomalous API calls from unusual geographies, and potential instance-metadata-based key theft. Feed findings into Security Hub for a unified compliance view.

<!-- INTERNAL_LINK: AWS Security Hub Guide | aws-security-hub-guide -->

AWS recommends CIS AWS Foundations Benchmark v5.0.0 as the current baseline. In regulated industries (finance, healthcare, government), alignment with CIS AWS Foundations is often an explicit requirement rather than just a recommendation.

---

## Common IAM pitfalls (and how to avoid them)

These are the mistakes I see on almost every first engagement. Mundane, avoidable, and consistently dangerous.

### 1. Wildcard policies that never get cleaned up

Overly broad permissions often begin as a temporary measure during an incident or a migration, and remain in place indefinitely because nobody schedules the follow-up review. Audit and compliance teams will flag this immediately during SOC 2 or ISO assessments. With broad permissions in place, lateral movement during a breach becomes straightforward.

### 2. Misconfigured trust policies

Allowing untrusted or overly broad principals to assume a role (such as an entire AWS account or a public service) opens the door for unauthorised access. Always scope the `Principal` in a trust policy to the specific role, service, or account ARN. Never use `"Principal": "*"`.

### 3. Privilege escalation via `iam:PassRole`

An IAM user or role with `iam:PassRole` permission can pass a highly privileged role to an AWS service. That service then acts on the user's behalf, using the passed role's permissions. If `iam:PassRole` is scoped to `*`, an attacker who compromises that principal can effectively grant themselves any permission in the account. Always scope `iam:PassRole` to specific role ARNs.

### 4. Forgetting service-linked roles

Service-linked roles are managed by AWS, but their permissions can still surprise you, particularly when a service updates them without notice. Audit them quarterly.

### 5. Stale credentials and zombie roles

Forgotten roles that are no longer needed but remain active are an unnecessary risk and a consistent target for attackers. Generate an IAM credential report monthly (`aws iam generate-credential-report`) and revoke or delete anything that hasn't been used in 90 days. The CIS AWS Foundations Benchmark requires access key rotation every 90 days or less.

### 6. Treating SCPs as a replacement for IAM policies

SCPs define the ceiling; they don't grant anything. You still need identity-based or resource-based policies attached to IAM principals or resources to actually grant permissions. Teams that deploy restrictive SCPs without the corresponding IAM grants end up locked out and then blame the SCP. I've seen this cause real incidents.

<!-- INTERNAL_LINK: Cloud Incident Response | cloud-incident-response -->

---

## Key takeaways

IAM best practices aren't a one-time configuration exercise. They're an ongoing operational discipline. Here's what I prioritise on every environment I review:

- Replace IAM user access keys with federated access via IAM Identity Center for humans, and IAM roles or OIDC federation for all workloads. There's no valid justification for a static access key in a greenfield AWS account in 2026.
- Use IAM Access Analyzer's policy generation against real CloudTrail activity to right-size role permissions. Treat the output as a starting point for human review, not a finished deliverable.
- Deploy SCPs as preventive guardrails. Lock down root account usage, restrict to approved AWS regions (critical for GDPR data residency), and consider an SCP that denies `iam:CreateAccessKey` to force the migration away from long-lived credentials.
- Use permissions boundaries when delegating IAM creation to product teams. They're the correct mechanism for self-service IAM without the risk of privilege escalation beyond a team's own scope.
- Version-control all IAM resources in Terraform or CloudFormation, and gate deployments with Access Analyzer's CI/CD policy checks. IAM policy drift is inevitable when policies are managed through the console.
- Run an organisation-scoped IAM Access Analyzer, feed findings into Security Hub, and align your controls baseline to CIS AWS Foundations Benchmark v5.0.0, which is a widely accepted reference for FCA and NCSC compliance assurance.

<!-- INTERNAL_LINK: AWS Inspector Vulnerability Management | aws-inspector-vulnerability-management -->
<!-- INTERNAL_LINK: What is CSPM | what-is-cspm-cloud-security-posture-management -->