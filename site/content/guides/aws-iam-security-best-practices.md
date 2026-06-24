+++
title = "AWS IAM Security Best Practices"
date = "2026-06-08T09:26:19Z"
slug = "aws-iam-security-best-practices"
description = "Practical AWS IAM security for architects: least privilege enforcement, long-lived credential elimination, SCPs, permission boundaries, and preventive guardrails that scale from startup to enterprise."
keywords = ["AWS IAM", "least privilege", "roles", "policies", "MFA"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

AWS IAM is the control plane for everything you do in AWS — misconfigured policies and poorly scoped permissions are consistently the root cause of serious cloud breaches. Securing IAM correctly means enforcing least privilege at every layer, eliminating long-lived credentials where possible, and building preventive controls that survive organisational change. The practices below are applicable at any scale, from a single-account startup to a multi-account enterprise estate.

---

## Least Privilege: More Than a Slogan

Most engineers understand the principle; fewer apply it rigorously. Least privilege in AWS IAM means granting only the permissions required for a specific task, scoped to the narrowest possible set of resources, for the shortest necessary duration.

In practice this requires deliberate effort:

- **Start from deny.** Build policies from scratch using only what the workload actually calls, rather than starting from broad managed policies and trimming. Tools like IAM Access Analyzer's policy generation feature can bootstrap this by analysing CloudTrail logs to identify what a principal actually used over a given period.
- **Scope resources explicitly.** Avoid `"Resource": "*"` in action-specific statements. An EC2 instance that stops and starts itself should reference only its own instance ID, not all instances in the account.
- **Use conditions aggressively.** Condition keys like `aws:RequestedRegion`, `aws:SourceVpc`, `aws:PrincipalTag`, and `s3:prefix` dramatically narrow the blast radius of any policy without adding operational complexity once they are templated.

The cost of over-permissioning compounds over time. An IAM role created for a proof-of-concept with `AdministratorAccess` attached will, in many organisations, still exist three years later with production workloads relying on it.

---

## Roles Over Users, Always

IAM users with long-lived access keys remain one of the most exploited attack vectors in AWS. A key committed to a public repository, leaked via a container image, or exfiltrated from a CI/CD system gives an attacker persistent, programmatic access with no expiry.

The mitigation is architectural: **replace IAM users with roles wherever possible.**

- **Workloads on AWS compute** (EC2, Lambda, ECS, EKS) should authenticate via instance profiles or execution roles. These deliver short-lived credentials through the Instance Metadata Service, rotated automatically by the STS service.
- **Human access** should flow through a centralised identity provider — AWS IAM Identity Center (formerly SSO) federated to your corporate IdP (Entra ID, Okta, Google Workspace) is the recommended pattern. Users assume roles with time-limited sessions rather than holding static credentials.
- **CI/CD pipelines** should use OIDC federation. GitHub Actions, GitLab, and most modern CI platforms support OIDC tokens that can be exchanged for temporary AWS credentials via `sts:AssumeRoleWithWebIdentity`, with no long-lived secrets stored anywhere.

Where IAM users genuinely cannot be avoided — some legacy tooling or external partner integrations — treat them as exceptions, enforce MFA, and enforce credential rotation via AWS Config rules. Audit them in every access review.

---

## MFA: Enforce It, Don't Just Enable It

Enabling MFA is insufficient. You must enforce it. An IAM user with MFA registered but not required can authenticate without it via the API using their access key alone — MFA only gates the console login.

**For console access via federation**, MFA enforcement is handled at the IdP layer. Ensure your IdP enforces MFA for all AWS-bound SAML or OIDC assertions, ideally with phishing-resistant methods (hardware keys, passkeys).

**For IAM users that still exist**, attach an inline policy or use a permissions boundary that denies all actions unless `aws:MultiFactorAuthPresent` is true. The classic pattern uses a `Deny` statement with a `BoolIfExists` condition:

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "BoolIfExists": {
      "aws:MultiFactorAuthPresent": "false"
    }
  }
}
```

Note the `IfExists` variant — without it, API calls using access keys (which carry no MFA context) would be incorrectly denied.

For privileged roles in sensitive accounts, consider requiring MFA at assume-role time using the `aws:MultiFactorAuthPresent` condition on the role's trust policy.

---

## Permission Boundaries: Guardrails for Delegation

Permission boundaries are an underused IAM feature that become critical once you delegate IAM management — to platform teams, to automation, or to application teams who self-service their own roles.

A permission boundary is an IAM managed policy attached to a principal that sets the **maximum** permissions that principal can be granted. Effective permissions are the intersection of the identity-based policy and the boundary — even if someone grants `AdministratorAccess`, the boundary caps what can actually be done.

Practical use cases:

- A platform team creates a boundary that prevents application teams from creating policies with `iam:*` or accessing other teams' S3 buckets, then grants application teams `iam:CreateRole` and `iam:AttachRolePolicy` so they can manage their own roles within those guardrails.
- An infrastructure-as-code pipeline is given permission to create and manage IAM roles, but the boundary ensures it cannot grant permissions it does not itself hold (preventing privilege escalation via automation).

The key design principle: the boundary should be maintained by a higher-trust principal than the one it constrains.

---

## Service Control Policies: Account-Level Preventive Controls

In a multi-account AWS environment, SCPs applied through AWS Organizations are the most powerful preventive control available. They set a permission ceiling across entire OUs or accounts, regardless of what IAM policies inside those accounts allow.

High-value SCPs to implement:

- **Deny leaving the organisation** — prevents an account from being detached and used outside governance controls.
- **Restrict to approved regions** — deny all actions where `aws:RequestedRegion` is not in an approved list, reducing the blast radius of a compromised credential.
- **Prevent disabling security services** — deny `cloudtrail:StopLogging`, `guardduty:DeleteDetector`, `securityhub:DisableSecurityHub`, and similar destructive actions to protect your detective controls.
- **Require encryption** — deny S3 PutObject without server-side encryption, deny creation of unencrypted RDS instances.
- **Protect root** — while you cannot fully constrain root via SCPs (root is exempt from them), you can enforce that no IAM users are created with root-equivalent policies.

SCPs do not replace IAM policies — they constrain what is possible. A `Deny` SCP is absolute; an `Allow` SCP only enables, it does not itself grant access.

---

## Access Analysis and Continuous Monitoring

Preventive controls degrade without continuous visibility. AWS IAM Access Analyzer provides two essential capabilities:

1. **External access analysis** — identifies resources (S3 buckets, KMS keys, Lambda functions, IAM roles) that are accessible from outside your AWS organisation or account. Run this at the organisation level, not account level, to catch cross-account paths you did not intend.
2. **Unused access analysis** — a newer capability that surfaces unused roles, unused access keys, and unused permissions within roles, helping you right-size over time. Integrate its findings into your regular access review process.

Complement Access Analyzer with:

- **AWS Config rules** — `iam-no-inline-policy`, `iam-user-no-unused-credentials-check`, `access-keys-rotated`, and `mfa-enabled-for-iam-console-access` cover the common hygiene baselines.
- **CloudTrail + Athena or Security Lake** — for detecting anomalous API patterns, privilege escalation attempts, and use of rarely-invoked permissions.
- **Regular access reviews** — at minimum quarterly for privileged roles, monthly for service accounts, and triggered on any role change for sensitive resources.

---

## What Architects Should Do

- Model permissions from actual usage, not assumed usage — use Access Analyzer policy generation for existing roles
- Replace all long-lived access keys with role-based or OIDC-based authentication; track remaining keys via Config
- Enforce MFA at the IdP for federated access; enforce it via policy condition for any remaining IAM users
- Implement permission boundaries before delegating IAM creation to any automation or application team
- Deploy a baseline SCP set to every OU: region restriction, security service protection, and organisation exit prevention
- Run IAM Access Analyzer at organisation scope and review external-access findings weekly
- Review unused roles and permissions quarterly and remove anything unused for 90 days

---

## Key Takeaways

AWS IAM security is not a one-time configuration — it is an ongoing discipline. The architectural fundamentals are consistent: eliminate static credentials, enforce least privilege through policy design and boundaries, apply preventive controls at the organisation layer via SCPs, and maintain visibility through Access Analyzer and CloudTrail. Organisations that treat IAM as a foundational control plane — rather than an administrative afterthought — dramatically reduce their exposure to both external attack and insider threat. Every gap in IAM hygiene is a gap in your entire AWS security posture.


## Related Guides

- [Zero Trust Architecture](/guides/what-is-zero-trust-architecture/) — IAM is the foundation of Zero Trust on AWS. This guide explains the broader architectural principles your IAM configuration should support.
- [Cloud Infrastructure Entitlement Management (CIEM)](/guides/what-is-ciem-cloud-infrastructure-entitlement-management/) — CIEM tools provide the visibility layer for discovering and remediating IAM entitlement risks at scale across AWS accounts.
- [Cloud Security Posture Management (CSPM)](/guides/what-is-cspm-cloud-security-posture-management/) — CSPM platforms continuously monitor IAM configuration for policy violations and misconfigurations.
- [Kubernetes Security Best Practices](/guides/kubernetes-security-best-practices/) — IAM roles for service accounts (IRSA) and workload identity federation connect AWS IAM controls into Kubernetes workloads.
- [The Shared Responsibility Model in Cloud Security](/guides/shared-responsibility-model-cloud-security/) — AWS manages the security of IAM as a service; you are responsible for how you configure and use it.
- [Cross-Cloud Security Services Comparison](/guides/aws-azure-gcp-security-service-comparison/) — Compare AWS IAM with Azure Entra ID and Google Cloud IAM to understand capability differences across providers.
