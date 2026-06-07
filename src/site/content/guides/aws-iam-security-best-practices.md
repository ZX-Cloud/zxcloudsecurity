+++
title = "AWS IAM Security Best Practices"
date = "2026-06-07T13:49:05Z"
slug = "aws-iam-security-best-practices"
description = "AWS IAM Security Best Practices — a practical guide for cloud security architects."
keywords = ["AWS IAM", "least privilege", "roles", "policies", "MFA"]
type = "guides"
draft = false
+++

Effective AWS IAM security rests on three pillars: granting the minimum permissions necessary to perform a task, using short-lived credentials wherever possible, and continuously validating that access remains appropriate over time. Getting these fundamentals right is not a one-time exercise — it requires deliberate architectural decisions, automated guardrails, and ongoing review cycles built into your operational practice.

---

## Why IAM Remains Your Most Critical Attack Surface

Every AWS breach of significance involves IAM in some form. Overly permissive roles, exposed access keys, and absent MFA are the paths of least resistance for attackers. IAM is unique in that a misconfiguration here doesn't just affect one service — it can grant lateral movement across your entire AWS environment. Treating IAM as an afterthought, or as something to be tightened up later, is one of the most common and costly mistakes organisations make during cloud adoption.

---

## Least Privilege: Beyond the Principle

Least privilege is cited constantly, but rarely implemented rigorously. The gap between what a workload *needs* and what it's *given* is where breaches happen.

**Start with IAM Access Analyzer.** Use it to generate policies based on actual CloudTrail activity. Rather than guessing what permissions a Lambda function or EC2 instance profile requires, let activity data inform the initial policy, then review and tighten it. Access Analyzer policy generation supports a 90-day lookback window — run it in production after a representative period of activity.

**Avoid wildcard actions and resources.** `s3:*` on `*` is not a policy; it's an abdication. Define actions explicitly and scope resources to specific ARNs. Where you genuinely need broad access, use conditions to constrain by IP range, VPC endpoint, request time, or tag values. Condition keys such as `aws:SourceVpc`, `aws:PrincipalTag`, and `s3:prefix` are underused tools for tightening policies without breaking functionality.

**Use IAM Access Advisor.** Within the IAM console, Access Advisor surfaces last-accessed service data per principal. Any service not accessed in 90 days is a candidate for removal. This is particularly valuable during periodic entitlement reviews.

---

## Roles Over Users — Without Exception

IAM users with long-lived access keys are a liability. For human access, federate through an identity provider — AWS IAM Identity Centre (formerly SSO), Okta, Azure AD, or a similar SAML/OIDC-compatible IdP — and issue short-lived credentials via role assumption. For machine workloads, use instance profiles, ECS task roles, Lambda execution roles, and IRSA (IAM Roles for Service Accounts) in EKS. There is no legitimate modern use case that requires a long-lived IAM user access key for a workload.

The architectural principle here is straightforward: credentials that expire cannot be harvested and used indefinitely. A 1-hour STS token stolen from a compromised host becomes worthless quickly; a static access key rotated annually is effectively permanent.

**Role assumption patterns worth knowing:**

- **Cross-account roles** — Define roles in target accounts, trust the source account's identity, and scope permissions tightly. Avoid using `sts:AssumeRole` with `Principal: AWS: "*"` — always specify the exact trusted entity.
- **IRSA for EKS** — Links Kubernetes service accounts to IAM roles via OIDC, scoping pod-level permissions rather than granting broad node-level access via the EC2 instance profile.
- **ECS task roles** — Separate the task execution role (what ECS needs to run the task) from the task role (what the application needs at runtime). Never conflate the two.

---

## MFA: Mandatory, Not Optional

MFA should be required for all human access to AWS. This means enforcing it at the identity provider level for federated users, and using IAM policies with `aws:MultiFactorAuthPresent: true` conditions to enforce it for IAM users where federation isn't yet in place.

A common pattern for legacy IAM user environments is the "MFA enforcement policy" — a boundary policy that denies all actions except `iam:CreateVirtualMFADevice` and `iam:EnableMFADevice` unless MFA has been authenticated. This forces users to enrol before they can do anything meaningful.

For sensitive operations — role assumption into production accounts, access to KMS key management, or secrets retrieval from Parameter Store — consider requiring MFA even within a federated context using session-level condition checks.

Do not accept hardware token exemptions without a documented exception process. FIDO2/WebAuthn hardware keys (such as YubiKeys) are the gold standard; TOTP authenticator apps are acceptable; SMS-based MFA is not — AWS supports disabling SMS MFA entirely, and you should.

---

## Permission Boundaries and SCPs: Guardrails at Scale

As AWS environments grow, individual policy management becomes unmanageable. Two mechanisms provide structural guardrails at scale.

**Service Control Policies (SCPs)** operate at the AWS Organisation level and define the maximum permissions available to accounts within OUs. They do not grant permissions — they constrain what can be granted. Use SCPs to enforce non-negotiable controls: prevent root account usage, restrict regions to approved geographies, deny disabling of CloudTrail or GuardDuty, and block creation of IAM users or access keys in managed accounts.

A practical SCP structure follows a deny-list model on a `FullAWSAccess` baseline: apply broadly permissive access at the root, then add targeted deny statements as you descend the OU hierarchy. This is more maintainable than trying to enumerate every allowed action.

**Permission boundaries** operate at the IAM principal level and are essential for delegated administration — allowing teams to create and manage their own roles and policies without exceeding a defined ceiling. If you're giving a DevOps team the ability to manage IAM within their account, attach a permission boundary that prevents them from escalating beyond their own team's scope or creating roles with broader access than they themselves hold.

Combining SCPs with permission boundaries and identity-based policies gives you a three-layer defence: what the organisation permits, what the boundary allows, and what the policy grants. All three must permit an action for it to succeed.

---

## What Architects Should Do: Actionable Checklist

- **Eliminate IAM user access keys** — audit with `aws iam generate-credential-report` and remove or rotate any keys older than 90 days; work towards zero long-lived keys.
- **Enable MFA** for all IAM users and enforce it via policy; require MFA-authenticated sessions for sensitive role assumptions.
- **Deploy IAM Access Analyzer** in every region and account; review findings weekly and integrate into your CI/CD pipeline using the `aws-iam-access-analyzer` CLI for policy validation before deployment.
- **Use permission boundaries** when delegating IAM management to development teams.
- **Define SCPs** at each OU level to enforce baseline controls — at minimum, deny root usage, restrict approved regions, and prevent disabling audit services.
- **Run Access Advisor reports** quarterly; remove permissions for services unused in the past 90 days.
- **Validate policies in CI/CD** using tools such as `cfn-nag`, `checkov`, or the IAM Access Analyzer policy validation API — catch `*` resources and missing conditions before they reach production.
- **Tag IAM roles** with owner, environment, and team metadata — this enables attribute-based access control (ABAC) patterns and makes access reviews tractable at scale.
- **Review trust policies** on all cross-account roles — ensure the `Principal` element is as specific as possible and that `sts:ExternalId` is used where third parties are involved.

---

## Key Takeaways

AWS IAM is not a configuration task — it's an ongoing discipline. The most robust IAM postures share common characteristics: they are built on roles and short-lived credentials, enforced by structural controls (SCPs and permission boundaries) rather than individual policy vigilance, and continuously validated through Access Analyzer and regular entitlement reviews.

Least privilege is only meaningful when it's measured against actual access patterns, not theoretical requirements. MFA is non-negotiable for human access. And the organisations that manage IAM at scale do so by building guardrails into their pipelines and organisational structures, not by relying on manual review of individual policies.
