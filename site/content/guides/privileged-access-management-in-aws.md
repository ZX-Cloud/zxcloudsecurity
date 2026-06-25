---
title: "Privileged Access Management in AWS: A Practitioner's Guide"
date: 2026-06-25
description: "A technical guide to privileged access management in AWS — covering least privilege, JIT access, SCPs, Session Manager, and common IAM mistakes."
tags: ["aws", "iam", "privileged-access-management", "cloud-security", "identity"]
slug: "privileged-access-management-in-aws"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2586
draft: false
---

# Privileged Access management in AWS: a practitioner's guide

Privileged access management in AWS is not a product you bolt on at the end of a project. It is a foundational design decision that shapes every layer of your security posture. UK financial services firms are facing increasingly prescriptive FCA operational resilience requirements, and GDPR enforcement actions that frequently trace breaches back to over-privileged identities. Getting PAM right matters, and it matters early. A single compromised administrator credential can cause catastrophic data loss, operational disruption, and regulatory exposure. This guide covers the core architectural patterns, native AWS tooling, and the mistakes I see most often in production environments.

<!-- INTERNAL_LINK: AWS IAM fundamentals for security engineers | aws-iam-fundamentals -->

---

## What "privileged access" actually means in AWS

The term gets used loosely. In an AWS context, privileged access refers to any identity, human or machine, that can perform actions with significant security or business impact: creating or modifying IAM roles and policies, disabling security services, accessing production data stores, or modifying networking controls.

PAM is about implementing security controls to govern and monitor access to those critical resources. For cloud foundation teams specifically, it means safeguarding the administrative roles that underpin core infrastructure, so you retain the visibility and control needed to oversee what application teams are doing in their accounts.

Three tiers are worth distinguishing:

1. Root user. The AWS account root user should never be used for day-to-day operations. Protect it with a hardware MFA token and vault the credentials behind a documented break-glass procedure.
2. High-privilege IAM roles. Roles with broad permissions such as `AdministratorAccess`, or roles with the ability to modify IAM, modify SCPs, or disable CloudTrail and GuardDuty.
3. Scoped administrative roles. Elevated but bounded permissions, such as a network engineer role that can only manage VPC resources in a specific region.

The goal of PAM is to ensure that tier-one and tier-two access is treated as an exception, not the default.

---

## The least-privilege foundation

Everything in PAM rests on least privilege: grant only the permissions required to perform a specific task, on specific resources, under specific conditions.

In practice, this is harder than it sounds. AWS managed policies are a useful starting point, but they are not least-privilege by design. They are built for broad applicability across all AWS customers, which means they routinely grant permissions that your workload will never use. The right approach is to treat managed policies as temporary scaffolding and replace them with customer-managed policies scoped to your actual usage patterns.

The most practical tool for doing this is IAM Access Analyzer. It analyses the services and actions your IAM roles actually invoke, based on CloudTrail data, and generates a least-privilege policy from that activity. The workflow I recommend: deploy AWS managed policies on day one, run for 90 days, then generate customer-managed policies from Access Analyzer output. Build that review cycle into your change management process. If it is not in the process, it will not happen.

<!-- INTERNAL_LINK: AWS IAM Access Analyzer deep dive | aws-iam-access-analyzer -->

---

## Enforcing guardrails with Service Control Policies

IAM policies alone are not sufficient at enterprise scale. Service Control Policies at the AWS Organisations level are your enforcement layer. They define the maximum available permissions for IAM entities in an account, and they cannot be overridden by any IAM policy, regardless of what a development team configures locally.

SCPs use the IAM policy language but do not grant permissions themselves. If an SCP denies an action for an account, no entity in that account can take that action, including the root user. If a role has an IAM permission policy that grants access to an action that an SCP does not allow, the role cannot perform that action.

One SCP you should deploy across all member accounts is a blanket deny of root account API usage. The following policy also protects your core security services from being disabled by a compromised high-privilege role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyRootAccountAccess",
      "Effect": "Deny",
      "Action": ["*"],
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "aws:PrincipalArn": ["arn:aws:iam::*:root"]
        }
      }
    },
    {
      "Sid": "ProtectSecurityServices",
      "Effect": "Deny",
      "Action": [
        "guardduty:DeleteDetector",
        "guardduty:DisassociateFromMasterAccount",
        "cloudtrail:DeleteTrail",
        "cloudtrail:StopLogging",
        "config:DeleteConfigRule",
        "config:StopConfigurationRecorder"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotLike": {
          "aws:PrincipalArn": "arn:aws:iam::*:role/SecurityBreakGlassRole"
        }
      }
    }
  ]
}
```

The second statement addresses a well-documented attack pattern. GuardDuty's Extended Threat Detection correlates suspicious activity with follow-on actions such as disabling CloudTrail and modifying bucket policies, which are classic defence evasion moves. Blocking those actions at the SCP level means even a fully compromised `AdministratorAccess` role cannot blind your logging pipeline.

One useful development: as of September 2025, SCPs support the full IAM policy language. Conditions in Allow statements, individual resource ARNs, NotAction with Allow, NotResource in both Allow and Deny, and wildcards in Action strings are all supported. This opens up considerably more expressive guardrail patterns than were previously possible.

<!-- INTERNAL_LINK: AWS Organisations and multi-account security architecture | aws-organisations-multi-account -->

---

## Just-in-time access: the right model for privileged operations

Standing privileged access, meaning permanent assignments to high-privilege roles, is the root cause of most cloud privilege abuse. The right model is to keep people away from systems through automation wherever possible, and to provide a controlled path for temporary elevated access when automation is not yet in place.

AWS provides a native mechanism for this: the Temporary Elevated Access Management (TEAM) pattern built on IAM Identity Center. A user requests access for a defined duration. If approved, that time window is the only period during which they can invoke sessions against the target environment. Once the window closes, access is gone.

For organisations already running Microsoft Entra ID, there is a well-documented integration path using Entra PIM. Security groups in Entra map to permission sets in IAM Identity Center, giving you automated provisioning and deprovisioning of privileged access based on defined policies and approval workflows. Access is granted only for the duration required to complete the task.

The trade-off here is operational friction, and I would rather be honest about it than pretend it does not exist. JIT access introduces approval workflow latency. Your on-call engineers will feel that at 2am. The answer is not to skip JIT; it is to invest in eligibility policy design and pre-approved windows for known emergency scenarios. Do that work upfront, not after your first incident.

---

## Replacing bastion hosts with AWS Systems Manager Session Manager

Eliminating bastion hosts and SSH key management is one of the most impactful PAM improvements available to AWS teams. Session Manager provides secure node management without opening inbound ports, maintaining bastion infrastructure, or managing SSH keys.

Leaving inbound SSH ports open on managed nodes materially increases the attack surface. Session Manager closes those ports entirely. Access is controlled through IAM policies, and all session activity is logged to CloudTrail and, if you configure it, to an S3 bucket in your security account. The connection model is IAM-authenticated, auditable, and does not require credentials that can be stolen and reused.

For private subnet deployments, which should be the default in any regulated environment, you need three VPC interface endpoints:

```bash
# Create the required VPC endpoints for Session Manager in private subnets
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-abc123 \
  --service-name com.amazonaws.eu-west-2.ssm \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-private-a subnet-private-b \
  --security-group-ids sg-endpoint

aws ec2 create-vpc-endpoint \
  --vpc-id vpc-abc123 \
  --service-name com.amazonaws.eu-west-2.ssmmessages \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-private-a subnet-private-b \
  --security-group-ids sg-endpoint

aws ec2 create-vpc-endpoint \
  --vpc-id vpc-abc123 \
  --service-name com.amazonaws.eu-west-2.ec2messages \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-private-a subnet-private-b \
  --security-group-ids sg-endpoint
```

Because access is governed by IAM rather than SSH keys, you can lock down `ssm:StartSession` to specific instance tags, specific users, or specific time windows. None of that is possible with SSH. You also get a full session audit trail, tied to IAM identities, at no additional cost.

The NCSC is explicit on the broader principle here: particularly privileged APIs should be restricted to privileged access workstations on company premises, and access should require callers to actively request higher privileges first. These controls make both accidental misuse and deliberate attack harder, while producing a robust audit trail of privileged activity.

---

## Detecting privilege abuse with GuardDuty and CloudTrail

Preventive controls are necessary but not sufficient. No access control model holds indefinitely against a sophisticated adversary or a malicious insider. Detection is not optional.

GuardDuty's Extended Threat Detection is worth understanding properly. It detects multi-stage attacks that span multiple data sources, multiple resource types, and time. Individual events in your account may not look threatening in isolation. When GuardDuty sees them as a sequence, it can identify an attack pattern that would otherwise go unnoticed. Extended Threat Detection is automatically enabled for all GuardDuty accounts at no additional cost, with no manual activation required.

For comprehensive detection of privileged access abuse, you need:

- CloudTrail enabled organisation-wide, multi-region, with log file integrity validation switched on and logs shipped to an immutable S3 bucket in a dedicated security account
- GuardDuty enabled in every region, with a delegated administrator in your security account
- CloudWatch metric filters alerting on `RootAccountUsage`, `ConsoleLoginWithoutMFA`, and changes to IAM policies or CloudTrail configuration
- AWS Config rules including `root-account-mfa-enabled`, `iam-user-no-policies-check`, and `cloudtrail-enabled`

One point that often gets missed: AWS recommends enabling GuardDuty in all regions, including regions where you have no deployed resources. Threats do not restrict themselves to regions where you are active.

<!-- INTERNAL_LINK: AWS GuardDuty configuration for enterprise environments | aws-guardduty-enterprise-setup -->

---

## Break-glass access: the procedure you hope you never use

Every PAM design must account for the scenario where your normal privileged access pathway is unavailable. This is not a theoretical edge case. The NCSC updated its secure system administration guidance specifically to address it.

If an attacker compromises one of your admin accounts, they gain the ability to undermine the very controls you have built. Emergency access, where you bypass normal access routes because they are unavailable, cannot be protected with the same depth as standard high-risk access. The most important compensating control is immediate, robust alerting. When any emergency access is triggered, your operations personnel need to know about it within seconds, not minutes.

In AWS, implement break-glass as follows:

- A dedicated IAM user (not a federated identity) with `AdministratorAccess`, with credentials vaulted in your PAM solution or a physical safe
- A CloudWatch alarm on any login or API call by that user, triggering SNS to your on-call channel
- The `ProtectSecurityServices` SCP statement shown earlier should carve out this role explicitly, as shown in the code example above

Test this procedure at least annually. A break-glass procedure that has never been tested is not a procedure; it is a hope.

---

## Common pitfalls in AWS PAM implementations

These are the mistakes I see repeatedly in client environments.

Long-lived IAM access keys left in rotation. Static IAM access keys are the single biggest PAM failure mode. Use IAM roles and AWS STS for all workload access. If you absolutely must have long-lived keys for a legacy integration that cannot be refactored, rotate them via AWS Secrets Manager automatic rotation and alert immediately on any console login by that IAM user.

Granting `AdministratorAccess` to CI/CD pipelines. A deployment pipeline does not need `AdministratorAccess`. Scope it to the exact services it deploys. Use IAM Access Analyzer to generate a scoped policy from the pipeline's CloudTrail history.

Failing to protect the management account. SCPs apply to member accounts only. They have no effect on users or roles in the management account. That makes your management account your most sensitive account, one that cannot be protected by the same guardrail mechanism you use everywhere else. No workloads, no developer access, MFA on all identities, and access only from a dedicated privileged access workstation.

Not using permissions boundaries when delegating IAM management. Teams that allow developers to create their own IAM roles without permissions boundaries will, eventually, have a developer create a role with `AdministratorAccess`. Segregation of duties means separating high-risk actions across different roles so that no single user has complete control over critical resources.

Skipping access reviews. IAM users, roles, permissions, policies, and credentials accumulate over time. IAM provides last-accessed information specifically to help you identify what you no longer need. Schedule quarterly access reviews, automate findings via Access Analyzer, and route them to your security backlog.

Treating PAM as a project rather than an ongoing programme. The threat landscape changes. Your AWS environment changes. A PAM design that was appropriate eighteen months ago may have gaps today. Build review cycles into your security programme from the start.

---

## Key takeaways

Least privilege is operational, not aspirational. Use IAM Access Analyzer to generate scoped policies from real access activity after a 90-day baseline period. AWS managed policies are a starting point, not a destination.

SCPs are your enforcement layer. Deploy them to deny root account usage and prevent disabling of security services across all member accounts. As of September 2025, SCPs support the full IAM policy language, which gives you considerably more flexibility in how you write guardrails.

Eliminate standing privilege. Implement just-in-time access via IAM Identity Center TEAM or Entra PIM integration. Privileged access should be temporary, scoped, approved, and logged.

Replace bastion hosts with Session Manager. Close port 22, eliminate SSH key sprawl, and get full session audit logging tied to IAM identities at no additional cost.

Build detection alongside prevention. Enable GuardDuty Extended Threat Detection in every region and deploy CloudWatch metric filters for root usage, MFA-less logins, and changes to CloudTrail. Preventive controls alone are not sufficient.

Design your break-glass procedure before you need it. The NCSC is explicit: emergency access must be prepared in advance, with immediate alerting on activation. Test it annually.