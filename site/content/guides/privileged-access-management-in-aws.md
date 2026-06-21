---
title: "Privileged Access Management in AWS: A Practitioner's Guide"
date: 2026-06-21
description: "A practical guide to privileged access management in AWS — covering JIT access, SCPs, permissions boundaries, IAM Identity Center, and common pitfalls to avoid."
tags: ["aws", "iam", "privileged-access-management", "cloud-security", "zero-trust"]
slug: "privileged-access-management-in-aws"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2417
draft: false
---

# Privileged Access Management in AWS: a practitioner's guide

If there is one area of AWS security where I see mature organisations still making elementary mistakes, it is privileged access management. The threat model has shifted, but the blast radius of a misconfigured privileged role remains as catastrophic as ever. For UK organisations operating under FCA supervision, GDPR obligations, or public sector mandates, getting PAM wrong is not just a security failure. It is a compliance event.

In a typical enterprise AWS deployment you have thousands of privileged identities: IAM users, service accounts, Lambda execution roles, cross-account assume roles, Kubernetes service accounts, and CI/CD pipeline credentials scattered across multiple accounts. The attack surface has grown by an order of magnitude and most organisations' PAM strategies have not kept pace.

This guide focuses on what you actually need to implement, not the theory.

<!-- INTERNAL_LINK: AWS IAM fundamentals | aws-iam-fundamentals -->

---

## Why traditional PAM thinking fails in AWS

On-premises PAM was designed around a small, well-defined set of privileged humans: DBAs, domain admins, network engineers. In a typical enterprise cloud deployment, machine identities (service accounts, IAM roles, API keys) outnumber human identities by 10:1 or more. A Kubernetes cluster alone can generate hundreds of service account identities. Traditional PAM tools were not built for that scale.

The second structural problem is Infrastructure as Code. When infrastructure is defined in Terraform or CloudFormation, IAM policies are created by developers in pull requests, not by security teams in a PAM console. Governance has to shift left into the development pipeline, which most PAM vendors still do not handle well.

The NCSC's zero trust architecture guidance reinforces this directly. The Home Office Engineering Guidance mandates access policies based on least privilege and the assumption that all requests are potentially hostile. AWS IAM has grown more granular and more powerful over time, but also considerably more complex. Managing least-privilege access across ephemeral workloads, cross-account roles, and dynamic developer environments requires more than the built-in tooling offers by default.

---

## The four pillars of PAM in AWS

### 1. Eliminate standing privilege and federate everything

The single most impactful change you can make is eliminating long-lived IAM user credentials for humans entirely.

AWS's own guidance is unambiguous on this: do not create IAM user access keys for human users. Use AWS IAM Identity Center (formerly SSO) with your corporate IdP (Okta, Azure AD) for federated access. Every human should authenticate through SSO and assume a role. Static credentials are not an acceptable alternative.

Treat static AWS IAM credentials as toxic and prohibit them by default. The NCSC recommends phishing-resistant MFA (FIDO2 security keys or passkeys) for administrative access. If you are running FIDO2 hardware tokens for privileged users, that satisfies both AWS security guidance and NCSC Cloud Security Principle 9 in one go.

<!-- INTERNAL_LINK: AWS IAM Identity Center setup guide | aws-iam-identity-center-setup -->

### 2. Just-in-time access: no more always-on admin

Standing privilege is the problem. Persistent access to production environments gives attackers a ready-made lateral movement path if any credential is compromised. Preventing direct human interaction with systems through automation is the primary way to address this. Where automation is not yet in place, time-bound elevated access is the next best option.

AWS publishes an open-source solution for exactly this: Temporary Elevated Access Management (TEAM). It integrates with AWS IAM Identity Center and lets users request access to an AWS account only when needed and only for a defined period. Approvers review requests before access is granted, and once the time window expires, elevated access is removed automatically.

For organisations already in the Microsoft ecosystem, combining AWS IAM Identity Center with Entra PIM works well. You map Entra security groups to IAM Identity Center permission sets, and Entra PIM handles the approval workflow and time-bounding. Access is provisioned only for the duration required to complete a task.

A practical JIT workflow in TEAM produces audit records that satisfy FCA SYSC requirements for access logging, which is a useful collateral benefit.

### 3. Permissions boundaries: defence against privilege escalation

Without permissions boundaries, the most common AWS privilege escalation pattern looks like this. A developer has `iam:CreateRole` and `iam:AttachRolePolicy` permissions for self-service role creation. They create a new role, attach the AWS-managed `AdministratorAccess` policy, assume the new role, and are now an administrator. This is exactly the pattern that several real-world AWS breaches have followed.

A permissions boundary is an advanced policy that defines the maximum permissions a role or user can hold, even if their assigned IAM policy is broader. It acts as a ceiling that cannot be exceeded regardless of what identity policies are attached.

Because permissions boundaries are independently controlled, you can use them to enforce conditions that delegates cannot override. Grant developers permission to use IAM, but add a condition requiring that any role they create or modify must have a specific permissions boundary attached. If the boundary is missing, IAM will block the change.

### 4. Service control policies: organisation-wide guardrails

SCPs operate at the AWS Organizations level. An SCP restricts permissions for IAM users and roles in member accounts, including the member account's root user. A principal has only the permissions allowed by every SCP in the hierarchy above it. If a permission is blocked at any level, the principal cannot use it, even if an administrator has attached `AdministratorAccess` with `*/*` permissions directly to the user or role.

Privilege escalation through stealthy permissions is a real and well-documented attack pattern. SCPs let you restrict administrative IAM actions across all workload accounts, permitting them only from specific approved roles such as a delegated IAM admin role. That constraint applies regardless of what identity policies developers or workload automation attach locally.

---

## Code: an SCP to prevent privilege escalation in workload OUs

The following SCP should be attached to your workload Organisational Units. It denies the most commonly abused IAM write actions and prevents any principal from disabling CloudTrail. Adjust the `aws:PrincipalARN` condition to your actual break-glass and IAM-admin role ARNs before deploying.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyPrivilegeEscalationActions",
      "Effect": "Deny",
      "Action": [
        "iam:CreateUser",
        "iam:AttachUserPolicy",
        "iam:PutUserPolicy",
        "iam:CreateAccessKey",
        "iam:UpdateAssumeRolePolicy",
        "iam:CreatePolicyVersion",
        "iam:SetDefaultPolicyVersion"
      ],
      "Resource": "*",
      "Condition": {
        "ArnNotLike": {
          "aws:PrincipalARN": [
            "arn:aws:iam::*:role/IAMAdminRole",
            "arn:aws:iam::*:role/BreakGlassRole"
          ]
        }
      }
    },
    {
      "Sid": "ProtectCloudTrail",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail",
        "cloudtrail:UpdateTrail"
      ],
      "Resource": "*",
      "Condition": {
        "ArnNotLike": {
          "aws:PrincipalARN": "arn:aws:iam::*:role/SecurityAdminRole"
        }
      }
    }
  ]
}
```

> Do not attach SCPs without testing the impact on accounts first. Test in a separate OU that mirrors your production environment, then deploy to progressively broader OUs once you are confident the policy behaves as expected.

<!-- INTERNAL_LINK: AWS Organizations and SCP design | aws-organizations-scp-design -->

---

## Detecting and right-sizing excessive privilege

Privilege creep is inevitable in a fast-moving engineering organisation. AWS managed policies are over-scoped for most use cases, but teams ship on Friday and the planned cleanup never happens. Permissions accumulate during incidents, debugging sessions, and one-off migrations. Few organisations have working processes to remove unused permissions, and IAM Access Analyzer findings sit unactioned for months. I see this on almost every security review I run.

IAM Access Analyzer addresses this directly. Its policy generation feature reads CloudTrail logs and produces a scoped policy matching only the actions and resources actually invoked by a role. It is genuinely useful and widely underutilised. Use it to generate a baseline policy for any role, then use IAM Access Analyzer policy validation in your CI/CD pipeline to catch over-permissive policies before they reach production.

For the root user, which should essentially never be used in day-to-day operations, the person who controls the root password of an AWS account should not also control its MFA token. Those two factors should be held by different people or teams, stored in a trusted PAM solution.

<!-- INTERNAL_LINK: AWS CloudTrail and GuardDuty for identity threat detection | aws-cloudtrail-guardduty-identity-threats -->

---

## Common pitfalls in AWS PAM

These are the issues I encounter repeatedly on security reviews across financial services and government clients.

### Pitfall 1: confusing SCPs with permission grants

An SCP does not grant permissions. It only limits what can be granted. I regularly see teams deploy a restrictive SCP and then wonder why their roles cannot do anything. You still need IAM identity policies to explicitly permit actions. The SCP caps the ceiling; it does not open any doors.

### Pitfall 2: neglecting machine identities

Machine identities outnumber human identities by roughly 82 to 1 according to CyberArk's 2025 Identity Security Landscape report. Organisations that implement JIT for humans but leave Lambda execution roles, ECS task roles, and CI/CD pipeline identities with permanently attached `AdministratorAccess` have addressed perhaps 5% of their PAM problem. Scope your PAM programme to include all identities from the outset.

### Pitfall 3: no break-glass procedure

JIT access workflows are necessary, but they must not become a single point of failure. You need a documented break-glass procedure covering what happens when normal authentication methods are unavailable. Break-glass accounts should have MFA enforced, and every use should trigger an alert to your security team. If nobody is notified when break-glass access is used, it is not a security control.

### Pitfall 4: testing SCPs against the management account

SCPs affect only member accounts. They have no effect on users or roles in the management account. If you test a deny SCP by logging in as a management account principal and find it has no effect, that is expected behaviour, not a bug. Always test SCPs in a dedicated staging OU before applying them to production OUs.

### Pitfall 5: using AWS managed policies indefinitely

AWS managed policies are designed to be usable by all AWS customers, which means they are over-permissive for most specific use cases. Shipping `SecurityAudit` or `PowerUserAccess` as a permanent assignment to a developer is not a PAM strategy. It is a problem deferred until something goes wrong. Define customer managed policies that are scoped to your actual use cases.

### Pitfall 6: no continuous review process

An annual IAM review is a checkbox exercise. Run IAM Access Analyzer continuously to detect external and unused access. Monitor for anomalous IAM API calls via CloudTrail and Amazon GuardDuty. Use AWS Config rules to flag non-compliant IAM configurations automatically. Feed findings into a centralised SIEM or your SOC's alerting pipeline. The goal is to catch privilege creep within days, not discover it twelve months later during an audit.

---

## Tooling: native vs. third-party

AWS-native tooling (IAM Identity Center, IAM Access Analyzer, TEAM, CloudTrail, GuardDuty) covers the majority of PAM requirements for organisations running AWS-only or AWS-primary environments. The native stack costs nothing at the IAM layer and integrates directly with AWS APIs without the latency or complexity of a third-party agent.

Add a third-party solution such as CyberArk when you have hybrid infrastructure spanning on-premise and cloud, more than 500 privileged identities, compliance requirements for session recording, or a need for centralised reporting across multiple cloud providers. For FCA-regulated firms that must demonstrate session-level audit trails, third-party PAM tooling often makes the compliance case more directly than assembling equivalent evidence from CloudTrail alone.

<!-- INTERNAL_LINK: Multi-account AWS security architecture | aws-multi-account-security-architecture -->

---

## Key takeaways

- Federate all human access through AWS IAM Identity Center and your corporate IdP. Long-lived IAM access keys introduce credential exposure risk that federated access eliminates entirely.

- Deploy JIT access for elevated roles using AWS's open-source TEAM solution or Entra PIM. Temporary elevated access reduces the window of exposure from indefinite to minutes or hours.

- Attach permissions boundaries to any role that has `iam:` permissions. Permissions boundaries are the IAM feature most teams should be using but are not. They close the most common privilege escalation path in AWS and cost nothing to implement.

- Use SCPs as organisation-wide guardrails, not as access grants. Layer them at the OU level, test in a staging OU first, and remember they have no effect on the management account.

- Extend PAM to machine identities. Lambda roles, ECS task roles, and CI/CD pipeline credentials are part of your privileged access surface. Treat them with the same rigour as human admin accounts.

- Make review continuous. IAM Access Analyzer can generate scoped policies from CloudTrail activity and flag unused access on an ongoing basis. Automate the findings pipeline into your SIEM rather than running point-in-time reviews.