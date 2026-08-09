---
title: "Privileged Access Management in AWS: A Practitioner's Guide"
date: 2026-08-09
description: "A practical guide to privileged access management in AWS: covering JIT access, SCPs, Session Manager, IAM Access Analyzer, and common pitfalls to avoid."
tags: ["aws", "privileged-access-management", "iam", "cloud-security", "zero-trust"]
slug: "privileged-access-management-in-aws"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2465
draft: false
---

# Privileged Access Management in AWS: A practitioner's guide

Privileged access management in AWS is not a product you buy. It is an architecture discipline you build, layer by layer, across IAM, AWS Organizations, Systems Manager, and your identity provider. Most cloud security incidents trace back to customer-side issues: identity misuse, misconfiguration, and exposed workloads. That makes controlling who can do what, and for how long, one of the highest-leverage security investments in your AWS estate. Nearly 80% of cloud security exposures now stem from identity or permission misconfigurations, and the breach cost is not abstract: according to IBM, the global average cost of a cloud breach in 2025 was $4.4 million. If you are responsible for a UK financial services, government, or enterprise AWS environment, this guide gives you the practical controls, with working policy examples, to close the most dangerous gaps.

<!-- INTERNAL_LINK: AWS IAM security best practices overview | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: AWS IAM Identity Centre deep-dive | aws-iam-identity-centre-guide -->

---

## Why privileged access in AWS is a different problem

On-premises, "privileged access" meant a handful of domain admins with domain admin accounts. In AWS, privilege is fragmented across thousands of IAM policies, resource-based policies, permission boundaries, SCPs, and role trust documents spread across dozens of accounts. IAM risk grows as identities, roles, and service permissions proliferate across accounts and workloads. As environments scale, access expands faster than it is reviewed. Excess privilege accumulates quietly, without triggering alarms.

The problem also moves fast. AWS service updates routinely introduce new privileged permissions across services, EC2, AWS Backup, Security Hub, and Bedrock being recent examples, that can alter restore approvals, connector integrity, automation rules, and security boundaries. Small permission changes can undermine trust boundaries faster than traditional review cycles catch them.

When AWS credentials are exposed publicly, attackers attempt access within an average of 17 minutes and as quickly as 9 minutes in some cases. That single statistic should calibrate how seriously your team treats credential hygiene and standing privilege.

<!-- INTERNAL_LINK: Shared responsibility model explained | shared-responsibility-model-cloud-security -->

---

## The foundation: least privilege and permission boundaries

Before you reach for a third-party PAM tool, make sure the AWS-native primitives are correctly wired. SCPs give you central control over the maximum available permissions for IAM users and roles in an organisation, but they operate at the organisation level and do not replace fine-grained IAM policies at the account level.

The combination you actually need is:

- SCPs at the Organisational Unit (OU) level as hard guardrails
- Permission boundaries on any role you delegate creation of
- Identity-based policies scoped to specific resource ARNs, not wildcards
- Resource-based policies locked down and reviewed on a regular cadence

Permission boundaries are underused but worth the effort. They define the maximum permissions an identity can ever receive, even if a more permissive policy is attached later. Use them to safely delegate IAM management to teams without creating a privilege escalation path.

On the SCP side, the most important guardrail for PAM is preventing privilege escalation in member accounts. The approach is to restrict administrative IAM actions to approved roles only. A bad actor with access to `iam:UpdateAssumeRolePolicy`, for instance, can modify role trust relationships and assume identities they were never meant to access. Use SCPs to make that impossible outside your designated admin roles.

One nuance worth understanding: an SCP restricts permissions for IAM users and roles in member accounts, including a member account's root user. Any account only has those permissions permitted by every parent above it. If a permission is blocked at any level above the account, no user or role in that account can use it, even with `AdministratorAccess` attached. However, SCPs have no effect on users or roles in the management account. That makes your management account the highest-risk surface in your entire estate.

### SCP: deny administrative IAM actions outside approved roles

The following SCP blocks any identity from making structural IAM changes unless they are assuming one of your designated break-glass or IAM-admin roles. Attach this to your Workloads OU, not to the Root.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyIAMAdminOutsideApprovedRoles",
      "Effect": "Deny",
      "Action": [
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:AttachRolePolicy",
        "iam:DetachRolePolicy",
        "iam:PutRolePolicy",
        "iam:DeleteRolePolicy",
        "iam:CreateUser",
        "iam:DeleteUser",
        "iam:AttachUserPolicy",
        "iam:CreateAccessKey",
        "iam:UpdateAssumeRolePolicy"
      ],
      "Resource": "*",
      "Condition": {
        "ArnNotLike": {
          "aws:PrincipalArn": [
            "arn:aws:iam::*:role/BreakGlassAdminRole",
            "arn:aws:iam::*:role/CentralIAMAdminRole",
            "arn:aws:iam::*:role/aws-reserved/sso.amazonaws.com/*/AWSReservedSSO_*"
          ]
        }
      }
    }
  ]
}
```

`iam:UpdateAssumeRolePolicy` is included deliberately. A misconfigured role that allows this action lets an attacker rewrite trust relationships and assume identities they were never intended to access.

<!-- INTERNAL_LINK: AWS Well-Architected Security pillar | aws-well-architected-security -->

---

## Just-in-time access: the right model for elevated privilege

Standing privilege, a developer permanently assigned `AdministratorAccess` to production, is the PAM equivalent of leaving a master key under the doormat. JIT access takes a different approach: temporary, on-demand grants scoped to a specific task and duration. It removes the assumption that elevated access needs to persist, which is exactly how you enforce least privilege in practice and reduce the window of exposure when credentials are compromised.

AWS Systems Manager now offers native just-in-time node access, giving you a built-in, officially supported way to grant time-bound access to managed nodes without standing permissions. AWS Systems Manager Change Manager and Automation can also handle JIT privileged access requests via IAM Identity Centre, and Temporary Elevated Access Management (TEAM), an open-source reference solution published through AWS Samples, remains a widely used option where teams need a fuller request-and-approval workflow. For those infrequent cases where automation is not yet in place, a structured process still needs to cover the basics: minimum required access, time-bound grants, an eligibility and approval workflow, and full auditing of what was approved and what was done.

If you are operating a hybrid Microsoft and AWS estate, Entra PIM integrates directly with IAM Identity Centre via SCIM. You get time-bound access with start and end dates, MFA enforcement, and justification tracking, all from a single approval workflow spanning both clouds.

<!-- INTERNAL_LINK: AWS IAM Identity Centre configuration guide | aws-iam-identity-centre -->

---

## Replacing bastion hosts with AWS Systems Manager Session Manager

Bastion hosts are a PAM anti-pattern in AWS. Connection logging, persistent open SSH ports, certificate and SSH key management, and instance patching all represent standing attack surface with no access-level granularity. Session Manager removes all of it.

AWS Systems Manager Session Manager gives you shell access to EC2 instances through the SSM agent with no SSH keys, no open ports, and no bastion hosts. Access is controlled through IAM, and every session is logged to CloudTrail and optionally to S3 or CloudWatch. You can also use Session Manager with AWS PrivateLink to keep traffic off the public internet entirely. IAM becomes your single, central place to grant and revoke instance access.

The IAM policy below allows a specific team role to start sessions, but only on instances tagged `Env: production`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSSMSessionManagerProductionOnly",
      "Effect": "Allow",
      "Action": "ssm:StartSession",
      "Resource": "arn:aws:ec2:eu-west-2:123456789012:instance/*",
      "Condition": {
        "StringEquals": {
          "ssm:resourceTag/Env": "production"
        }
      }
    },
    {
      "Sid": "AllowSSMSessionVisibility",
      "Effect": "Allow",
      "Action": [
        "ssm:DescribeSessions",
        "ssm:GetConnectionStatus"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowSSMSessionTermination",
      "Effect": "Allow",
      "Action": "ssm:TerminateSession",
      "Resource": "arn:aws:ssm:*:*:session/${aws:username}-*"
    }
  ]
}
```

Pair this with a session document that enforces KMS encryption of session output to an S3 bucket and you have an auditable, zero-open-port privileged access path to every managed instance in your estate.

---

## Continuous right-sizing with IAM Access Analyzer

Getting PAM right at deployment is only half the problem. Permissions only grow by default. Every incident fix, migration, and "just unblock me" request adds grants, and nothing removes them. There is no natural driver for revocation, so an account's permission surface expands until an audit or a breach forces the question.

IAM Access Analyzer reviews your CloudTrail logs and generates a policy template containing only the permissions the entity actually used in a specified date range. You can then use that template to create a fine-grained policy, replacing the over-broad grants that accumulated over time. Access Analyzer now evaluates organisation-wide policies, identifies who can access sensitive resources, flags unused permissions, and recommends least-privilege updates based on CloudTrail activity.

Run policy generation against roles that have been in production for at least 30 days to capture real access patterns before tightening. Use the `start-policy-generation` API call, specifying a CloudTrail trail and a date range of up to 90 days.

<!-- INTERNAL_LINK: AWS Security Hub for centralised findings | aws-security-hub-guide -->

---

## Network-layer PAM: IPAM and BYOIP governance

PAM is not purely an identity concern. Network-layer privilege governance matters too, particularly for organisations with Bring Your Own IP (BYOIP) address space. Amazon VPC IP Address Manager (IPAM) centralises the management of BYOIP prefixes across your accounts and regions, but the Resource Public Key Infrastructure (RPKI) side of that relationship sits outside IPAM, with your Regional Internet Registry (ARIN, RIPE, APNIC, or LACNIC).

Route Origin Authorisations (ROAs) validate which Autonomous System Numbers are authorised to announce your prefixes. Before you can bring a range into IPAM, you need a valid ROA scoped to the correct ASNs and prefix lengths, and keeping it accurate as your routing arrangements change is a customer responsibility, not something AWS manages on your behalf.

For organisations using BYOIP to maintain stable IP reputation or allowlist entries, which is common in UK financial services where third-party connectivity agreements reference specific CIDRs, this remains one of the most error-prone manual processes in the network lifecycle, precisely because nothing forces a review when a ROA lapses. An invalid or expired ROA leaves your BGP advertisements open to route hijacking, which directly threatens the availability of services your privileged users depend on.

<!-- INTERNAL_LINK: AWS Shield DDoS protection | aws-shield-ddos-protection -->

---

## NCSC alignment and UK regulatory context

The NCSC's 14 Cloud Security Principles address privileged access directly. Your cloud provider should make tools available to securely manage your use of the service, covering identity and access management, multi-factor authentication, role-based access controls, and privileged access management.

Principle 12 (Secure Service Administration) is explicit: systems used for administration of cloud services have highly privileged access to that service, and their compromise would have significant impact, including the ability to bypass security controls and steal or manipulate large volumes of data.

Access to service interfaces should be constrained to authenticated and authorised individuals, and the NCSC recommends phishing-resistant MFA (FIDO2 security keys or passkeys) for administrative access. In practice, that means deploying FIDO2 hardware keys for all break-glass and IAM-admin roles, and enforcing MFA via the `aws:MultiFactorAuthPresent: "true"` condition key on any policy that permits destructive or administrative actions.

The NCSC also published its Principles for secure privileged access workstations (PAWs) guidance in March 2025. Where possible, use automation to replace manual administrative processes, including Infrastructure as Code and a secure CI/CD mechanism. For AWS teams, that translates to routing all privileged actions through your IaC pipeline (CloudFormation or CDK) rather than the console, and treating console access as an exception requiring JIT approval.

For FCA-regulated firms, the GDPR obligation to maintain records of processing activities intersects with PAM through access logs. Every JIT elevation, every SSM session, and every cross-account role assumption must be captured in CloudTrail and retained in a tamper-resistant manner. Use an S3 bucket with Object Lock enabled and an SCP that prevents any account from disabling CloudTrail.

<!-- INTERNAL_LINK: Cloud compliance frameworks for UK organisations | cloud-compliance-frameworks -->

---

## Common pitfalls in AWS PAM implementations

After auditing dozens of production AWS environments, these are the failure patterns I see repeatedly.

1. The management account has IAM users. The management account of an AWS Organisation is exempt from SCPs. Any IAM user or access key there has unconstrained blast radius. Maintain zero IAM users in that account and use IAM Identity Centre with a dedicated, FIDO2-protected admin group whose permission set only exists in that account.

2. CI/CD roles carry `AdministratorAccess`. A CI pipeline somehow ends up with more privileges than production engineers, and it happens constantly. CI roles need `iam:PassRole`, specific service permissions, and nothing else. Generate their policies from CloudTrail after a few sprint cycles.

3. Long-lived access keys in code and configuration. The patterns are predictable: hardcoded AWS access keys in source code, `.env` files committed to GitHub, credentials visible in CI/CD logs, secrets embedded in public Docker images. Recent industry data found 69% of organisations store unencrypted API keys directly in code repositories. Use IAM roles and instance profiles everywhere. Applications, Lambda functions, EC2 instances, and containers should never use long-term access keys embedded in code, environment variables, or config files.

4. SCPs only at the Root OU. Teams that attach a single SCP to Root and consider themselves done miss account-level and OU-level variation entirely. SCPs have no effect on users or roles in the management account. Apply SCPs at the OU level and test in a sandbox OU first.

5. Ignoring `iam:PassRole` as a privilege escalation vector. A developer who can pass an admin-level role to a Lambda function they create has effectively gained admin access. Scope `iam:PassRole` to only the specific role ARNs a team legitimately needs to pass. This is one of the most commonly overlooked escalation paths I see in real environments.

6. Root users without MFA. AWS rolled out mandatory MFA for root users in phases between mid-2024 and spring 2025, extending from management account root users to member account root users that hadn't enabled centralised root access management, but enforcement only bites at sign-in and older, dormant accounts can still slip through. Audit your existing accounts to confirm every root user actually has MFA configured. A root user without MFA is an unguarded master key to the entire account.

7. Treating permission review as a one-time exercise. Permission creep now drives most incidents. Schedule quarterly Access Analyzer unused-access reviews and integrate IAM policy checks into your pull request pipeline.

<!-- INTERNAL_LINK: Cloud incident response playbook | cloud-incident-response -->
<!-- INTERNAL_LINK: DevsecOps shift-left security | devsecops-shift-left-security -->

---

## Key takeaways

- Treat privileged access management in AWS as a continuous control loop, not a one-time configuration. Use IAM Access Analyzer to prune permissions quarterly based on CloudTrail-observed usage.

- Implement JIT elevation via AWS Systems Manager's just-in-time node access (or an open-source option such as TEAM) alongside IAM Identity Centre for all human access to production accounts. Standing privilege is standing risk. Every elevated session should have a defined duration, an approval trail, and an automatic expiry.

- Replace bastion hosts with Session Manager across all managed EC2 workloads. You get IAM-controlled, audited shell access with no open ports, no SSH key sprawl, and CloudTrail evidence for every session, aligned with NCSC Principle 12.

- Use SCPs at the OU level as hard guardrails against privilege escalation, CloudTrail disablement, and region sprawl. Never rely on SCPs attached to Root as your only control layer, and remember the management account is SCP-exempt by design.

- Enforce FIDO2 phishing-resistant MFA for all privileged roles as per NCSC guidance. Include the `aws:MultiFactorAuthPresent: "true"` condition key on any policy that permits administrative or destructive actions.

- Bring network-layer privilege governance into scope. For UK organisations bringing their own IP space into AWS via IPAM, treat RPKI and ROA management with your Regional Internet Registry as a standing governance responsibility, not a one-off setup task, to keep your BGP advertisements protected from hijacking.