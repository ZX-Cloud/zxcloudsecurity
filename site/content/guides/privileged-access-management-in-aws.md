---
title: "Privileged Access Management in AWS: A Practitioner's Guide"
date: 2026-06-23
description: "Eliminating standing privilege in AWS: JIT access with TEAM, IAM Identity Centre, SCPs, break-glass controls, and PAM architecture for regulated environments."
tags: ["aws", "iam", "privileged-access-management", "cloud-security", "identity"]
slug: "privileged-access-management-in-aws"
author: "Steve Harrison, Principal Security Architect"
word_count: 2318
draft: false
---

# Privileged Access Management in AWS: a practitioner's guide

Credential compromise remains the dominant initial access vector in cloud breaches, and the reason most incidents spiral is standing privilege. Engineers and service accounts with `AdministratorAccess` attached permanently, just waiting for an attacker to find them. For UK financial services firms navigating FCA expectations, government departments aligned to the NCSC's 14 Cloud Security Principles, or any enterprise with GDPR obligations, getting privileged access management right in AWS is no longer negotiable. The good news is that AWS now provides a mature toolchain: IAM Identity Center, Service Control Policies (SCPs), IAM Access Analyzer, and the open-source TEAM solution. You don't need to build everything from scratch. You do need to use these tools properly.

<!-- INTERNAL_LINK: AWS IAM Identity Center setup guide | aws-iam-identity-center-setup -->

---

## Why standing privilege is the real problem

Before getting into tooling, it is worth being precise about the threat model. A compromised principal with perpetual access to everything it will ever need is categorically more damaging than a compromised principal with limited access that must request elevation when required.

In practice, most AWS estates suffer from exactly this. IAM is extremely flexible, and that is precisely the problem. Roles get created in a rush, permissions get copied from other roles, and nobody circles back to audit them. Over time, permissions accumulate and your exposure grows quietly in the background.

The NCSC is unambiguous on this. Their guidance on privileged access workstations notes that when designed and implemented correctly, PAWs are an indispensable tool for defending against real-world threats. More directly: a dedicated PAW is one of the most effective controls for protecting administrators from credential theft and malware infection, and the NCSC recommends always using one for high-risk access to cloud services handling sensitive data.

For cloud-native AWS estates, a PAW is typically enforced via IAM condition keys that restrict console access to specific source IP ranges or VPC endpoints, which translates the physical PAW concept into a policy control you can audit and version-control.

---

## The foundation: principle of least privilege

The AWS guidance here is straightforward: grant only the permissions required to perform a task, defined as the actions that can be taken on specific resources under specific conditions.

The honest challenge is that "least privilege" is aspirational at the start of a project. You will likely start with broader permissions while you work out what a role actually needs. That is acceptable, provided you treat it as a temporary state and revisit it as the workload matures.

### Using IAM Access Analyzer to right-size policies

The most practical tool for tightening real-world permissions is IAM Access Analyzer's policy generation feature. It reviews your CloudTrail logs and generates a policy template based on what the entity actually did during a specified date range, up to 90 days back.

I find this genuinely useful in production. The workflow is:

1. Enable an organisation-level CloudTrail trail (multi-region, log file validation on)
2. Let a role operate for 30 to 90 days under broad permissions
3. Generate a policy via the IAM console or CLI
4. Review, trim, and attach

```bash
# Start policy generation from CloudTrail activity
aws accessanalyzer start-policy-generation \
  --policy-generation-details '{
    "principalArn": "arn:aws:iam::123456789012:role/ops-deploy-role"
  }' \
  --cloud-trail-details '{
    "trails": [
      {
        "cloudTrailArn": "arn:aws:cloudtrail:eu-west-2:123456789012:trail/org-trail",
        "regions": ["eu-west-2", "eu-west-1"],
        "allRegions": false
      }
    ],
    "accessRole": "arn:aws:iam::123456789012:role/access-analyzer-service-role",
    "startTime": "2025-03-01T00:00:00Z",
    "endTime": "2025-06-01T00:00:00Z"
  }'

# Poll for completion and retrieve the generated policy
aws accessanalyzer get-generated-policy \
  --job-id <job-id-from-above>
```

One important caveat: if a role only runs certain tasks quarterly, a 30-day analysis window will give you an incomplete policy. You will end up breaking the quarterly batch job the first time it runs after you tighten permissions. Use a window that covers your full operational cycle, apply the generated policy in staging first, and monitor CloudTrail for `AccessDenied` events before promoting to production.

<!-- INTERNAL_LINK: AWS CloudTrail logging best practices | aws-cloudtrail-logging-best-practices -->

---

## SCPs as organisational guardrails

IAM policies control what a principal can do within an account. SCPs set the outer boundary: they define what IAM users and roles in your organisation are permitted to do at all, including the root user of each member account. That last point matters more than most teams realise.

For privileged access management in AWS, two SCP patterns matter most.

The first is denying root usage across member accounts:

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

Attach this to every OU except the management account. The root user bypasses all IAM policies and has unrestricted access to all resources, billing, and account closure. This SCP prevents accidental or malicious use of root credentials and forces all activity through IAM principals with proper audit trails.

The second pattern is protecting your central security role from modification. Your central security team likely has a common administrative role deployed across all member accounts for audit and remediation work. An SCP can prevent any IAM entity in those accounts from modifying that role or its attached permissions, ensuring it remains available when you need it.

One important gotcha: SCPs do not affect users or roles in the management account. They apply only to member accounts. Your management account needs its own tight IAM controls because the SCP safety net simply does not exist there.

<!-- INTERNAL_LINK: AWS Organizations multi-account security architecture | aws-organizations-multi-account-security -->

---

## Just-in-time access with AWS TEAM

The gold standard for privileged access management in AWS is eliminating standing privilege entirely in favour of just-in-time (JIT) access. The principle is that a user requests access for a specified time period, the request is validated, time-bound access is granted, all activity during that window is monitored, and access can be revoked if conditions change.

AWS's open-source Temporary Elevated Access Management (TEAM) solution handles this natively within your AWS estate. It integrates with IAM Identity Center and manages time-bound elevated access across a multi-account environment at scale.

The workflow is straightforward. A user requests elevated access, an approver reviews it, and if approved, TEAM activates access with the scope and duration specified. The requester then uses the IAM Identity Center access portal to reach the AWS console or retrieve temporary credentials. Access ends when the duration elapses or is explicitly revoked in the TEAM application.

TEAM defines four personas that map cleanly to operational reality:

- Requester: raises a time-bound access request with justification
- Approver: reviews and approves or rejects requests, but cannot approve their own
- Auditor: can view the full history of TEAM sessions, approval decisions, and CloudTrail-backed activity logs for each session
- Admin: manages eligibility policies and global settings

All actions performed during an elevated access session are logged as auditable events via CloudTrail. TEAM itself is serverless (Lambda, DynamoDB, Amplify), so running costs are minimal. For organisations already using Microsoft Entra ID, you can map Entra security groups to IAM Identity Center permission sets and integrate with Entra PIM, automating provisioning and deprovisioning based on defined policies and approval workflows.

---

## Break-glass access: plan for the failure mode

Every PAM implementation needs a tested break-glass procedure. Root account credentials should be stored securely and only accessed through a well-documented, tightly controlled process.

In practice this means:

- Root credentials stored in an offline vault (physical or HSM-backed), not in your day-to-day password manager
- MFA hardware token stored separately from the password, ideally requiring two-person access
- A documented runbook tested at least annually
- A CloudWatch alarm on any root API activity, with PagerDuty or equivalent escalation

For UK public sector and regulated financial services clients: your NCSC CAF assessment and FCA operational resilience framework both require evidence that emergency access procedures exist, are documented, and are tested. "We have a note in Confluence" does not constitute evidence.

---

## Auditing and continuous monitoring

Comprehensive tracking of privileged user activity is what makes detection and response viable when something goes wrong. In AWS, this requires three controls working together.

CloudTrail at organisation scope covers all management events, with S3 log validation enabled and CloudTrail Lake available for correlating TEAM session activity. GuardDuty can detect anomalous usage of powerful IAM credentials, which is worth enabling even if you are already doing everything else right. IAM Access Analyzer continuously surfaces unintended external access findings and flags unused access so you can act on it.

IAM provides last-accessed information to help you identify users, roles, permissions, policies, and credentials that are no longer needed. Use this to build a quarterly access review process: pull last-accessed data, remove roles not used in 90 days, and feed the output to your security team. This is a reasonable control to evidence to FCA supervisors and auditors under GDPR Article 32.

<!-- INTERNAL_LINK: AWS GuardDuty threat detection configuration | aws-guardduty-configuration -->

---

## Common pitfalls

After 15 years doing this across UK financial services and government, these are the mistakes I see repeatedly.

Assuming SCPs protect the management account. They do not. SCPs apply only to member accounts. Management account IAM must be locked down separately, and ideally no workloads run there at all.

Using `AdministratorAccess` for automation roles. CI/CD pipelines do not need it. A pipeline allowed `iam:*` creates unnecessary attack surface. Generate a scoped policy from CloudTrail activity as described above and attach that instead.

Treating TEAM session duration as the same as session token duration. Sessions invoked just before elevated access ends may remain valid beyond the end of that access window. If this concerns you, minimise the session duration configured in your permission sets, for example by setting it to one hour.

Not testing break-glass procedures. A break-glass procedure that has never been tested is not a control, it is a hypothesis. Run an annual tabletop exercise and attempt the actual login with a witnessing security officer present.

Generating policies from too short an analysis window. A 30-day window that misses a quarterly backup job will produce a policy that breaks it the first time it runs. Make sure your analysis window covers the full operational cycle for that role.

Conflating IAM policies with SCPs when debugging access issues. When a user in a member account requests access to a resource, AWS evaluates both SCPs and IAM policies together. For an action to succeed, both must allow it. Teams routinely debug access problems by looking only at IAM and miss an SCP denial entirely.

---

## Key takeaways

Eliminate standing privilege. Every human operator should request time-bound access via TEAM or an equivalent JIT solution. Persistent `AdministratorAccess` roles for humans are a liability.

Use SCPs as your outer guardrail. Deny root actions across all member OUs, protect your central security roles from modification, and restrict to approved regions. SCPs set the ceiling that IAM policies cannot exceed.

Use IAM Access Analyzer to operationalise least privilege. Generate policies from CloudTrail activity across a 60 to 90 day window, test in staging, promote to production, and run unused access reviews quarterly.

Build and test your break-glass procedure. Root credentials must be offline, MFA-protected, and dual-controlled. Test annually and evidence that testing for FCA and NCSC CAF assessments.

Implement phishing-resistant MFA for all privileged access. The NCSC recommends FIDO2 security keys or passkeys for administrative access. TOTP codes are not sufficient for your highest-privilege operators.

Monitor continuously. CloudTrail at organisation scope, GuardDuty for anomalous IAM usage, and Access Analyzer findings reviewed on a defined cadence. Alerting on root login should be in place from day one.