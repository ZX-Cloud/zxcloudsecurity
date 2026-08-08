---
title: "Privileged Access Management in AWS: A Practitioner's Guide"
date: 2026-08-08
description: "A practical guide to privileged access management in AWS — covering JIT access, SCPs, break-glass design, IAM Access Analyzer, and common pitfalls to avoid."
tags: ["aws", "iam", "privileged-access-management", "cloud-security", "zero-trust"]
slug: "privileged-access-management-aws"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2168
draft: false
---

# Privileged Access Management in AWS: a practitioner's guide

Privileged access management in AWS is no longer something you bolt on after the architecture is designed. It is the architecture.

With the shared responsibility model placing identity, configuration, and workload protection squarely on customers, permission creep and misconfiguration now drive most incidents. Nearly 80% of cloud security exposures stem from identity or permission problems. If you're running workloads in regulated UK sectors -- financial services under FCA oversight, public sector under NCSC guidance, or healthcare under GDPR -- the consequences are not abstract. They show up in breach notifications, regulatory findings, and post-mortems.

This guide focuses on the controls that actually work in production multi-account AWS environments.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->

---

## Why standing privilege is your biggest risk

The assumption that administrators, IT staff, and power users should have elevated access all the time -- just in case they need it -- is one of the most dangerous things you can build into your security posture.

Most AWS estates I review look roughly the same: a developer requests extra access "just for a day," an old EC2 role hasn't been touched in years, a contractor key is still active, and the CI pipeline somehow has more privileges than production engineers. Individually, none of those look catastrophic. Together, they're the reason IAM drifts out of control.

The pace of exploitation makes this worse. When AWS credentials are exposed publicly, attackers attempt access within an average of 17 minutes, and as quickly as 9 minutes in some cases. That window is narrower than most security teams' detection SLAs. Granting wide privilege and hoping for the best is simply not a workable model.

The NCSC's 14 Cloud Security Principles are direct on this point: your provider should make tools available for you to securely manage your use of the service, covering identity and access management, MFA, role-based access controls, and privileged access management. The NCSC recommends phishing-resistant MFA (FIDO2 security keys or passkeys) for administrative access, which aligns with what AWS supports natively today.

<!-- INTERNAL_LINK: NCSC cloud security principles and AWS | cloud-compliance-frameworks -->

---

## The PAM control stack for AWS

Effective privileged access management is not a single product. It is a layered set of controls. The following sections cover each layer in turn.

### Layer 1: no long-lived credentials for human access

The foundational rule is straightforward. AWS recommends using IAM users only when federation or IAM Identity Center is not an option -- break-glass access, tools that require static keys, or workloads that cannot assume roles.

For everything else, AWS recommends IAM Identity Center to authenticate user identities and enable single sign-on across AWS accounts. Identity Center lets you integrate with your existing identity store, reuse your joiners/movers/leavers processes, and apply existing authentication policies including MFA. For machine identities -- Lambda functions, EC2 instances, containers -- the position is equally clear: applications should never use long-term access keys embedded in code, environment variables, or config files.

<!-- INTERNAL_LINK: AWS IAM Identity Centre configuration guide | aws-iam-identity-centre-guide -->

### Layer 2: just-in-time elevated access

The most impactful shift in privileged access management over the past few years has been the move from standing privilege to just-in-time access. JIT access allows users to request temporary elevated permissions when needed, with that request going through an approval workflow before anything is granted. AWS puts it plainly: preventing direct human interaction with services through automation is the primary method, and where automation isn't yet possible, providing a secure mechanism for temporary elevated access is the next best option.

The principle is simple: users get only the minimum permissions required to do their job, and those permissions persist only for as long as the task takes.

The AWS-native approach uses IAM Identity Center with time-bound permission set assignments. For organisations using Microsoft Entra ID, Privileged Identity Management (PIM) handles the same requirement -- time-bound access with start and end dates, MFA enforcement, and justification tracking. Temporary Elevated Access Management (TEAM), an open-source AWS Samples solution built on top of IAM Identity Center, adds a governed request-and-approval workflow on top of the native permission set model, allowing developers and administrators to request time-bound access without waiting on a third-party PAM tool.

<!-- INTERNAL_LINK: AWS IAM Identity Centre setup and federation | aws-iam-identity-centre -->

### Layer 3: service control policies as guardrails

Service control policies define the maximum permissions available to IAM users and roles across an AWS Organisation. They are the most powerful preventive control in a multi-account estate and, in my experience, persistently underused.

SCPs and resource control policies (RCPs) serve different purposes. SCPs cap what principals can do -- users, roles, and root users across member accounts. RCPs cap what can be done to a given resource, regardless of what that resource's own policy allows.

For privileged access specifically, the risk is privilege escalation: a principal uses a combination of permissions to elevate themselves beyond their intended scope. The mitigation is an SCP that restricts administrative IAM actions to a small set of approved roles.

A practical SCP to block the most common privilege escalation paths:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyPrivilegeEscalation",
      "Effect": "Deny",
      "Action": [
        "iam:CreateUser",
        "iam:AttachUserPolicy",
        "iam:PutUserPolicy",
        "iam:CreateAccessKey",
        "iam:UpdateAssumeRolePolicy",
        "iam:CreatePolicyVersion",
        "iam:AttachRolePolicy",
        "iam:PutRolePolicy"
      ],
      "Resource": "*",
      "Condition": {
        "ArnNotLike": {
          "aws:PrincipalArn": [
            "arn:aws:iam::*:role/PlatformSecurityAdmin",
            "arn:aws:iam::*:role/BreakGlassRole"
          ]
        }
      }
    },
    {
      "Sid": "DenyCloudTrailDisruption",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail",
        "cloudtrail:UpdateTrail"
      ],
      "Resource": "*"
    }
  ]
}
```

This blocks privilege escalation actions organisation-wide whilst exempting a named platform security role and a break-glass role -- the `ArnNotLike` condition only matches those two specific role ARNs, not every role in the accounts where they live, so any other principal in those accounts remains subject to the deny. The CloudTrail protection clause is non-negotiable. Without it, an attacker with administrative access can simply disable your audit trail before doing anything else.

> **Note:** Test any deny-based policies carefully against your environment before deploying them. Deny-based SCPs can unintentionally block legitimate AWS service usage unless you add the necessary exceptions.

<!-- INTERNAL_LINK: AWS Well-Architected Security Pillar | aws-well-architected-security -->

### Layer 4: permission boundaries

Permission boundaries define the maximum permissions an identity can ever receive, even if a more permissive policy is attached later. They let you delegate IAM management to application teams or CI/CD pipelines without creating a privilege escalation path.

In practice, you hand IAM management to a team's pipeline, bounded by a policy that prevents them from ever escalating beyond their intended scope. It's a useful control precisely because it lets you say yes to delegation without losing control of the ceiling.

<!-- INTERNAL_LINK: DevSecOps shift-left security in AWS pipelines | devsecops-shift-left-security -->

### Layer 5: continuous unused-access analysis

IAM Access Analyzer provides tools to set, verify, and refine permissions -- access analysis, policy checks, and policy generation from CloudTrail activity logs. The unused access analyser identifies dormant IAM roles, unused access keys, unused console passwords, and principals with unused service or action-level permissions. You can generate least-privilege policies from CloudTrail logs and validate existing ones to remove wildcards and risky actions.

One honest caveat: IAM Access Analyzer is a visibility tool. It surfaces the problem; it does not fix it. Least-privilege programmes stall when findings accumulate faster than teams can safely remediate them, and standing access stays in place. The tooling tells you what to do. Your team still has to do it.

<!-- INTERNAL_LINK: AWS Security Hub configuration and findings | aws-security-hub-guide -->

---

## Break-glass access: design it before you need it

Every AWS estate needs a break-glass account -- an emergency administrative identity used when all normal access paths fail. Most organisations have one. Most of them are poorly designed.

Under a JIT model, the break-glass role should be dormant by default, with no standing credentials and no active session. A well-designed break-glass role:

- Exists as an IAM role, not an IAM user with long-lived credentials
- Requires MFA with a hardware FIDO2 token stored in physical security (a safe, not a desk drawer)
- Generates an immediate CloudWatch alarm on any `AssumeRole` event targeting it
- Is excluded from normal SCPs but subject to enhanced CloudTrail logging
- Triggers a mandatory post-use review, even if the access was legitimate

The AWS account root user has unrestricted access and should be protected with hardware FIDO2 keys or multiple virtual authenticators. The root user is your ultimate break-glass. Treat it accordingly.

<!-- INTERNAL_LINK: Cloud incident response and break-glass procedures | cloud-incident-response -->

---

## The network layer: IPAM permissions as privileged actions

Privilege in AWS does not live solely in IAM identity policies. Increasingly, it is concentrated in networking, traffic control, and collaboration services.

A concrete example: Amazon VPC IPAM lets administrators provision and allocate BYOIP address ranges across an AWS Organisation. Those ranges typically carry RPKI Route Origin Authorisations tying the prefix to your AWS ASN, so IPAM permissions that control who can provision or reassign BYOIP CIDRs are, in effect, controlling who can affect the legitimacy of routes announced on your behalf. Modifying an IPAM prefix list resolver can expand CIDR ranges resolved by a prefix list, potentially broadening network access to sensitive resources protected by security group rules. Removing VPC Encryption Controls eliminates safeguards protecting network traffic confidentiality.

This has a direct bearing on your PAM strategy. Treat `ec2:ModifyIpamPool`, `ec2:ProvisionByoipCidr`, and related IPAM administrative actions as privileged -- restrict them via SCP, require MFA conditions, and audit them in CloudTrail with the same rigour you'd apply to `iam:AttachRolePolicy`.

---

## Common pitfalls

### 1. Treating `AdministratorAccess` as a convenience

Attaching the `AdministratorAccess` managed policy to roles used by engineers or CI/CD pipelines is the single most common failure I see in AWS environments. This policy should be reserved for dedicated break-glass roles. If a pipeline can deploy infrastructure, it does not also need to create IAM users or modify SCPs.

### 2. Forgetting `iam:PassRole`

`iam:PassRole` is one of the most common privilege escalation paths in AWS. A principal with `iam:PassRole` and `ec2:RunInstances` can spin up an EC2 instance with an administrator role attached, which effectively grants them administrator access. Scope `iam:PassRole` to specific role ARNs, always.

### 3. SCPs that don't apply to the management account

SCPs don't affect users or roles in the management account. This catches teams out regularly. Your management account is not protected by the SCPs you've written for workload OUs. Treat it as a separate high-privilege zone: minimise human access, use dedicated automation roles, and never run workloads there.

### 4. JIT access without an approval workflow

JIT access without governance is just slow standing access. Every request for elevated access should require a documented justification, a named approver, and a time limit. Build this into your Identity Center workflow or your third-party PAM tool. An informal Slack message is not an approval workflow.

### 5. Ignoring non-human identities

Non-human identities now outnumber human ones by more than 80 to 1. Service accounts, Lambda execution roles, CI/CD pipeline roles, and EKS service accounts all accumulate privilege over time. Only 20% of organisations have formal processes for offboarding and revoking API keys, and fewer still have procedures for rotating them. Apply the same PAM discipline to machine identities as you apply to human administrators.

### 6. Confusing visibility for remediation

Access Analyzer will tell you about unused permissions. It will not remove them. The gap between a finding and a remediated permission is where most cloud least-privilege programmes stall out. Build a remediation workflow -- triage, test, revoke -- not just a dashboard review process.

<!-- INTERNAL_LINK: Cloud security vulnerability management and remediation workflows | cloud-security-vulnerability-management -->

---

## Key takeaways

- Replace standing privilege with JIT access. Use AWS IAM Identity Center with time-bound permission set assignments, backed by an approval workflow with documented justification and automatic expiry. Break-glass access should follow the same model -- dormant by default, activated with MFA and full audit logging.

- Enforce SCPs at the organisation level as the outermost guardrail. Block privilege escalation paths (`iam:CreateUser`, `iam:AttachRolePolicy`, `iam:PassRole` without ARN conditions) and CloudTrail disruption across all workload OUs. SCPs do not protect the management account -- apply separate controls there.

- Treat network administration as privileged access. IPAM pool management, BYOIP provisioning, and VPC Encryption Control modifications are high-impact actions. Restrict them explicitly in SCPs and audit them in CloudTrail.

- Use IAM Access Analyzer continuously, not just at audit time. Enable both external-access and unused-access analysers across your AWS Organisation. Use CloudTrail-based policy generation to rightsize roles. Build a remediation workflow that converts findings into actual permission removals. Visibility without action is not security.

- Design your break-glass before you need it. A hardware FIDO2 key in a physical safe, an IAM role (not a user), immediate alerting on any assumption event, and a mandatory post-use review. Test it quarterly in a non-production account.

- Extend least-privilege to non-human identities. CI/CD pipeline roles, Lambda execution roles, and EKS service accounts need the same access review cadence as human administrators. Scope `iam:PassRole` tightly and build automated offboarding into your identity lifecycle process.

<!-- INTERNAL_LINK: Shared responsibility model deep dive | shared-responsibility-model-cloud-security -->
<!-- INTERNAL_LINK: AWS KMS key management and access control | aws-kms-key-management-best-practices -->
<!-- INTERNAL_LINK: Cloud threat detection and identity-based alerts | cloud-threat-detection -->