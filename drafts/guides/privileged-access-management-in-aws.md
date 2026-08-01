---
title: "Privileged Access Management in AWS: A Practitioner's Guide"
date: 2025-08-01
description: "A practical guide to privileged access management in AWS — covering JIT access, SCPs, elevated access workflows, Session Manager, and NCSC alignment for UK enterprises."
tags: ["privileged access management", "aws iam", "cloud security", "zero trust", "aws organizations"]
slug: "privileged-access-management-in-aws"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2167
draft: false
---

# Privileged Access Management in AWS: a practitioner's guide

The blast radius of a compromised admin credential in AWS is enormous: full account takeover, data exfiltration, ransomware propagating across your entire AWS Organisation. Yet most AWS environments I review still hand out standing `AdministratorAccess` roles to engineers who need them once a fortnight. Privileged access management in AWS is not something you bolt on after your landing zone is live. It needs to be designed in from day one. This guide covers what a mature PAM posture looks like in AWS, the native tooling available, the compliance context UK teams are operating under, and the mistakes that undermine otherwise solid implementations.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: AWS IAM Identity Centre guide | aws-iam-identity-centre-guide -->

---

## Why privileged access management matters right now

Credentials that remain active indefinitely — admin passwords, hard-coded tokens, access keys — are a persistent risk. Whether it is a forgotten service account, a dormant admin role, or an AI agent with unrestricted access to sensitive data, over-permissioned identities create vulnerabilities that sit quietly until something goes wrong.

The regulatory context for UK organisations adds further pressure. Three frameworks shape the UK PAM market: FCA Supervisory Statement SS1/21 (operational resilience) drives PAM adoption at banks, insurers, and asset managers; NHS DSPT requires privileged access controls for all NHS Trusts and healthcare suppliers; NCSC guidance on protecting privileged access is the reference for CNI operators. Firms in scope of FCA operational resilience rules had until 31 March 2025 to demonstrate they could operate important business services within their impact tolerances. In 2025, 27% of incidents reported to the FCA were attributed to a third-party issue, and 37% of those were cyber-related. Privileged credential abuse sits squarely inside that threat category.

Just-in-time access is not a future-state aspiration. The threat landscape, the compliance environment, and the architectural principles of Zero Trust all point to the same conclusion: standing privileges are an unacceptable risk in cloud environments, and the tools to eliminate them exist on every major platform today.

---

## Core principles of PAM in AWS

Before reaching for tooling, be clear on the model you are implementing. Users should have only the minimum access required to do their job, and that access should persist only for as long as the task requires. That is the principle of least privilege, and in a cloud context it needs to be enforced dynamically, not just written into a policy document.

Zero Standing Privileges (ZSP) is the model where no identity — human, machine, or AI agent — retains persistent access to critical systems or data. Access is provisioned just-in-time and revoked automatically when it is no longer needed.

Preventing direct human interaction with production systems through automation is the primary mechanism here. For the cases where automation is not yet in place, a controlled, time-bound method for temporary elevated access is the next best option. What you want to avoid is the default state most teams end up in: permanent access granted once and never reviewed.

These principles map directly onto the NCSC's Cloud Security Principles. Under Principle 12 (Secure Service Administration), privileged APIs should be restricted to privileged access workstations and require the caller to actively request higher privileges. That approach makes both accidental misuse and deliberate attack harder, and it produces a meaningful audit trail of privileged activity.

<!-- INTERNAL_LINK: AWS Well-Architected Security | aws-well-architected-security -->

---

## AWS-native PAM tooling

### AWS IAM Identity Centre and temporary credentials

The starting point for AWS PAM is eliminating long-lived IAM user credentials entirely. IAM Identity Centre acts as the cloud-native broker, mapping external directory groups to short-lived AWS Permission Sets. AWS Security Token Service (STS) issues ephemeral credentials valid for a bounded duration, typically one to twelve hours, directly to the local CLI environment.

AWS's own IAM best practice documentation is explicit on this: require human users to federate with an identity provider and access AWS using temporary credentials, require workloads to use IAM roles rather than long-lived keys, and require multi-factor authentication.

<!-- INTERNAL_LINK: AWS IAM Identity Centre | aws-iam-identity-centre -->

### Time-bound elevated access workflows

For teams that need to go further than IAM Identity Centre's baseline temporary credentials, the next step is a dedicated just-in-time access broker built specifically for privileged access workflows. It should integrate with IAM Identity Centre and let you manage time-bound elevated access to a multi-account AWS environment at scale. Users request access to an account only when needed and only for a defined period. Approvers review requests before access is granted, and when the time window closes, access is removed automatically.

A broker of this kind should use AWS CloudTrail Lake for querying, auditing, and logging API activity during elevated access sessions. That matters in a regulated environment. You need an immutable, queryable audit trail, not just CloudTrail JSON sitting in an S3 bucket that nobody looks at.

One important operational note: approval workflows of this type are only as strong as their request input validation. If a workflow lets a user modify a valid request after submission, that opens the door to spoofed approvals. Whichever solution you run, keep it patched and check release notes for security fixes before anything else.

### AWS Systems Manager Session Manager

One of the highest-impact changes you can make to your compute access model is retiring bastion hosts and replacing them with Session Manager. It is a fully managed AWS service that allows you to open secure shell sessions to EC2 instances without inbound ports or SSH keys. Connections route through the AWS API.

Access is controlled through IAM, and every session is logged to CloudTrail and optionally to S3 or CloudWatch. CloudWatch Logs integration provides a complete session audit trail for compliance purposes (SOC 2, PCI-DSS, HIPAA), and S3 session logging captures full terminal output for forensic analysis.

<!-- INTERNAL_LINK: cloud incident response | cloud-incident-response -->

The IAM policy controlling Session Manager access should be scoped by instance tags so that, for example, a developer role can open sessions against sandbox EC2 instances but not production ones:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSSMSessionByTag",
      "Effect": "Allow",
      "Action": [
        "ssm:StartSession",
        "ssm:TerminateSession",
        "ssm:ResumeSession"
      ],
      "Resource": "arn:aws:ec2:eu-west-2:123456789012:instance/*",
      "Condition": {
        "StringEquals": {
          "ec2:ResourceTag/Environment": "dev"
        }
      }
    },
    {
      "Sid": "DenyProductionSessions",
      "Effect": "Deny",
      "Action": "ssm:StartSession",
      "Resource": "arn:aws:ec2:eu-west-2:123456789012:instance/*",
      "Condition": {
        "StringEquals": {
          "ec2:ResourceTag/Environment": "production"
        }
      }
    }
  ]
}
```

### Service Control Policies as guardrails

Service Control Policies are the top-level guardrails in AWS. They set the maximum permissions for every identity in a member account, including the root user. Unlike IAM policies, SCPs only restrict; they never grant. They are your organisation's safety net, preventing actions like disabling CloudTrail, operating outside regions you actually use, or spinning up instance types nobody approved.

From a PAM perspective, SCPs are your last-resort enforcement layer. Use them at the AWS Organisations level to explicitly deny dangerous IAM actions such as `iam:CreatePolicyVersion`, `iam:AttachUserPolicy`, and `iam:PassRole` for identities that have no business performing them.

A minimal SCP to block root API usage across member accounts:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyRootAPIAccess",
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
      "Sid": "ProtectCloudTrail",
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

Since Spring 2025, AWS has required MFA for root users in member accounts that have not enabled centralised root access management, and centralised root access management lets you remove long-lived root credentials from member accounts entirely. That is a meaningful control improvement. Use it.

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->

### Privileged access workstations

Do not overlook the device layer. The NCSC has published formal principles for privileged access workstations. A privileged access workstation is a highly restricted and audited physical device that minimises the attack surface for high-risk systems. It makes those accesses significantly harder to compromise, and it is one of the most effective tools for defending administrators against credential theft and malware infection.

The NCSC is direct: always use a PAW for high-risk access to a cloud service handling sensitive data. For AWS console and API access, that means your admin sessions originate from a managed, hardened device, not a general-purpose laptop that also handles email and web browsing.

<!-- INTERNAL_LINK: cloud threat detection | cloud-threat-detection -->

---

## Detecting privilege escalation

PAM controls reduce risk; monitoring detects when those controls are bypassed. IAM Access Analyzer integrates with AWS Security Hub and CloudTrail, providing centralised monitoring and detailed audit logs. It can also automatically generate least-privilege IAM policies by analysing your CloudTrail history, so you can replace over-permissive policies with ones that reflect actual usage rather than what someone estimated three years ago.

For threat detection, wire EventBridge rules against CloudTrail. Alert on `iam:CreateAccessKey` for users other than the calling principal, and on `iam:AttachUserPolicy`, `iam:AttachRolePolicy`, and `iam:PutUserPolicy`. These are the API calls that appear in real privilege escalation attacks, not just theoretical scenarios.

<!-- INTERNAL_LINK: cloud security vulnerability management | cloud-security-vulnerability-management -->

---

## Common pitfalls in AWS PAM implementations

Every implementation I have reviewed has hit at least one of these. Most hit several.

1. JIT access with no break-glass planning. Teams roll out just-in-time access and forget to design the emergency procedure for when the approval workflow is unavailable. Break-glass is part of your PAM design. It needs to be time-bound and heavily monitored, not quietly excluded from scope.

2. No ownership after go-live. Policies need tuning as the estate changes. Without someone owning that, the exception list grows until you are effectively back to the old standing-access model with extra steps. This is the most common reason a technically successful deployment stops delivering value.

3. Treating SCPs as a one-time configuration. SCPs drift as new services are adopted and new AWS APIs appear. In Organisations-managed environments, test regularly for SCP gaps that allow IAM modifications the policy was meant to block. They need scheduled review, not just an initial deployment.

4. Running an outdated access broker version. Input validation flaws in request-approval workflows are a real and recurring class of vulnerability. Check your deployed version against the latest release before your next audit, and subscribe to security advisories for whatever tooling you run.

5. Keeping bastion hosts alongside Session Manager. Teams often deploy Session Manager and leave the old bastions running as a fallback. Bastion hosts are an additional attack surface. Open inbound SSH ports increase exposure. Decommission them properly rather than running both indefinitely.

6. Overly broad `iam:PassRole` permissions. Scope `iam:PassRole` tightly using the `iam:PassedToService` condition. A developer who can pass roles to Lambda should not be able to pass them to EC2. Overly broad PassRole is one of the most common lateral movement vectors we find on assessments.

7. TOTP-based MFA on high-privilege accounts. The NCSC recommends phishing-resistant MFA, specifically FIDO2 security keys or passkeys, for administrative access. TOTP is better than nothing, but it is not sufficient for high-privilege accounts in a regulated environment.

<!-- INTERNAL_LINK: shared responsibility model cloud security | shared-responsibility-model-cloud-security -->
<!-- INTERNAL_LINK: devsecops shift left security | devsecops-shift-left-security -->

---

## Implementing PAM iteratively

Zero standing privileges is a destination, not a starting point. Run discovery first. It almost always turns up more than expected: dormant admin accounts, nested group memberships, leftover project access that nobody got around to removing.

Start with one high-value target, production database access or domain admin, and prove the JIT workflow somewhere the risk reduction is obvious. Automate approvals for routine cases early. That is what stops the control decaying over time once the initial momentum fades.

The sequence that works in practice:

1. Discover: use IAM Access Analyzer and IAM Last Access reports to map your current privilege state.
2. Federate: remove IAM user credentials for humans and move everyone to IAM Identity Centre with time-limited STS tokens.
3. Deploy a JIT access broker: gate elevated access behind an approval workflow with mandatory justification and session logging.
4. Enforce at org level: apply SCPs to block root API access and protect CloudTrail from tampering.
5. Replace bastions: migrate EC2 access to Session Manager with tag-scoped IAM policies.
6. Monitor continuously: EventBridge rules on escalation-path API calls and a weekly IAM Access Analyzer review.

---

## Key takeaways

Standing privileges are the core risk. Persistent admin access, particularly long-lived IAM user credentials, is the attack surface that PAM in AWS is designed to eliminate. Replace with federated, time-limited STS tokens via IAM Identity Centre.

A JIT access broker gives you elevated access on demand. A well-implemented broker integrates directly with IAM Identity Centre to provide request, approval, time-bound grant, and automatic revocation workflows without third-party proxies. Keep it patched and review its release notes regularly.

Session Manager makes bastion hosts obsolete. Portless, IAM-controlled, fully audited EC2 access via Session Manager removes SSH key management and closes open inbound ports. There is no good reason to run bastion hosts alongside it.

SCPs are your last line of guardrail. Block root API access, protect CloudTrail, and deny dangerous IAM mutations at the Organisation level. Review them whenever you adopt new AWS services.

NCSC PAW guidance is now formal and public. It makes clear that high-risk AWS administrative access should originate from a hardened, dedicated device, not a general-purpose machine.

Start with discovery, not a full rollout. Pick one high-value standing-access target, prove the JIT workflow, then expand. A technically successful PAM deployment that nobody owns post-launch decays back into the old model with extra steps.