---
title: "Privileged Access Management in AWS: A Practitioner's Guide"
date: 2026-07-12
description: "A deep-dive into privileged access management in AWS — covering JIT access, SCPs, IAM Access Analyzer, Secrets Manager, and common PAM pitfalls to avoid."
tags: ["aws", "privileged-access-management", "iam", "cloud-security", "zero-trust"]
slug: "privileged-access-management-in-aws"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2585
draft: false
---

# Privileged Access Management in AWS: a practitioner's guide

Privileged access management in AWS is not an optional bolt-on. It is the difference between a controlled, auditable estate and one that is a single leaked credential away from serious trouble. Attackers target high-level access first because it is the most direct path to everything that matters.

For UK financial services organisations under FCA oversight, or public sector bodies procuring via G-Cloud, this is not academic. It is a regulatory obligation. The NCSC's cloud security principles explicitly address secure service administration, and your PAM posture will be scrutinised in any serious assurance engagement.

This guide is aimed at practitioners who already understand IAM fundamentals and want a clear, opinionated view of how to design and operate a robust privileged access management framework on AWS.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: AWS IAM Identity Centre guide | aws-iam-identity-centre-guide -->

---

## Why PAM in AWS is a different problem

On-premises PAM is largely a solved problem. CyberArk, BeyondTrust, Delinea, and others have mature tooling. In AWS, the surface area is radically different. You are dealing with human identities, machine identities (IAM roles assumed by Lambda functions, EC2 instances, ECS tasks, CI/CD pipelines), cross-account trust relationships, and API-level access, all of which can grant administrative privilege without anyone picking up a keyboard.

IAM handles MFA, role-based access control, and policies for regular users. A dedicated PAM solution adds session monitoring and real-time analytics for high-risk privileged accounts, along with controls such as least privilege enforcement and just-in-time access. The two are complementary, not interchangeable.

The core tenet is simple: just-in-time administration and just-enough administration. Everything else follows from those two principles.

---

## Foundational controls: where to start

### Lock down the root user

AWS account root users should be controlled by two people. The individual or team that controls the root password of an AWS account should not also control its MFA token. Use a trusted password or privileged access management solution to secure these secrets.

In practice, this means the root credentials for every account in your AWS Organisation should be sealed in a vault (whether that is AWS Secrets Manager, CyberArk, or a physically secured envelope for the MFA seed), and the break-glass procedure to use them should be documented, tested annually, and never used for routine tasks. Cloud foundation teams should not hand root credentials to application teams. IAM roles cover day-to-day administrative tasks. Root access is for genuine emergencies only.

### Treat static IAM credentials as toxic

Long-lived IAM access keys are the single biggest source of credential compromise in AWS. If you have them, rotate them. If you can eliminate them entirely, do that instead. The right model is federation through AWS IAM Identity Centre backed by your corporate IdP, whether that is Okta, Microsoft Entra ID, or AWS's own directory. Static credentials should be prohibited by default, with human access flowing through federated authorisation.

<!-- INTERNAL_LINK: AWS IAM Identity Centre | aws-iam-identity-centre -->

---

## Just-in-time access: the centrepiece of modern PAM

Standing privilege is the problem. A DevOps engineer holding `AdministratorAccess` permanently is a disaster waiting to happen, whether through account compromise, insider threat, or an accidental destructive action. Just-in-time (JIT) access is the answer: elevated permissions are granted for a bounded duration, for a specific task, and then automatically revoked.

The mechanism is straightforward. Instead of using a credential to access an administration interface directly, it is used to request access. If the request is approved, a temporary credential is issued. That temporary credential is what the administrator actually uses to reach the privileged interface.

Adopting a JIT model substantially reduces your attack surface and moves you towards a zero trust posture. Privileged access becomes the exception rather than the standing state.

<!-- INTERNAL_LINK: Zero Trust Architecture | what-is-zero-trust-architecture -->

### JIT on AWS: native and third-party options

AWS does not ship a native JIT PAM solution, but you can construct one. The AWS-published approach uses 
Temporary Elevated Access Management (TEAM), an open-source solution
 that integrates with IAM Identity Centre to grant time-bounded permission sets via an approval workflow.

If your organisation already uses Microsoft Entra ID, a JIT pattern built around Entra PIM and IAM Identity Centre is worth evaluating. Be clear about what this is: not a turnkey, first-party integration, but a solution you assemble yourself. The pattern uses Entra PIM for Groups to control membership of security groups, which are synchronised to IAM Identity Centre via SCIM provisioning and mapped to permission sets, with PIM's activation policies and approval workflows driving the provisioning and deprovisioning of privileged access. Done properly, access is granted only for the duration required to complete a task.

Third-party tools such as CyberArk, StrongDM, and BeyondTrust provide richer session recording, keystroke logging, and real-time session termination if you need a full PAM capability beyond what AWS native tooling provides.

---

## Service control policies: your organisation-wide guardrails

SCPs are not IAM policies. They do not grant permissions. They define the maximum permissions that any principal in a member account can ever hold, regardless of what IAM policies say. If a user or role has an IAM permission policy that grants access to an action that is not allowed or is explicitly denied by an applicable SCP, that action cannot be performed. This applies to all users and roles in attached accounts, including the root user.

For PAM at the organisational level, SCPs are your hardest preventive control. Below is a practical SCP that prevents member accounts from disabling core security services and blocks use of the root user. It is a sensible baseline for any production OU:

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
    },
    {
      "Sid": "PreventSecurityToolsDisable",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:DeleteTrail",
        "cloudtrail:StopLogging",
        "guardduty:DeleteDetector",
        "guardduty:DisassociateFromAdministratorAccount",
        "guardduty:DisassociateFromMasterAccount",
        "config:DeleteConfigurationRecorder",
        "config:StopConfigurationRecorder",
        "securityhub:DisableSecurityHub"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyIAMUserCreation",
      "Effect": "Deny",
      "Action": [
        "iam:CreateUser",
        "iam:CreateAccessKey"
      ],
      "Resource": "*"
    }
  ]
}
```

Note that the GuardDuty deny list includes both `DisassociateFromAdministratorAccount` and the older `DisassociateFromMasterAccount`: AWS has moved from master/member to administrator/member terminology, but the deprecated API action still works, so a guardrail that omits it leaves a bypass open.

The third statement (`DenyIAMUserCreation`) is particularly relevant to PAM. It prevents teams from creating long-lived IAM users with access keys in member accounts, forcing all human access through federated roles. Bear in mind that because SCPs apply to every principal in a member account, including root, the `DenyRootUserActions` statement above blocks all root activity in member accounts outright — not just user creation. Any break-glass procedure that depends on the root user, or on creating an IAM user, in a member account will therefore require the SCP to be temporarily detached or amended from the management account, which sits outside SCP enforcement. Document that step explicitly in your break-glass runbook. Pairing this with just-in-time access for the rare cases where elevated rights are genuinely needed keeps the standing privilege footprint small.

<!-- INTERNAL_LINK: AWS compliance and governance | aws-compliance-and-governance -->

> **Warning:** AWS strongly recommends that you do not attach SCPs to the root of your organisation without thoroughly testing the impact that the policy has on accounts. Instead, create an OU that you can move your accounts into one at a time, or at least in small numbers, to ensure that you do not inadvertently lock users out of services they need.

---

## Right-sizing permissions with IAM Access Analyzer

Granting JIT access is pointless if the permission sets you are granting are bloated. IAM Access Analyzer is the tool that closes this loop. It guides you towards least privilege by providing access findings, policy checks, and policy generation.

The policy generation capability is particularly useful for PAM work. IAM Access Analyzer can generate fine-grained policies based on actual access activity recorded in your CloudTrail logs. You observe what a privileged role does over a representative period, then replace the broad `AdministratorAccess` permission set with a crafted, minimal policy built from real usage data.

Security and development teams can extend this further by integrating custom policy checks into CI/CD pipelines, catching over-permissive policies before they ever reach production.

<!-- INTERNAL_LINK: AWS CloudTrail configuration best practices | aws-cloudtrail-configuration-best-practices -->
<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->

---

## Secrets management for privileged credentials

Any privileged account that cannot be eliminated entirely, whether a legacy service account, a third-party integration, or an RDS superuser, needs its credentials managed properly. That means AWS Secrets Manager. Not environment variables, not SSM Parameter Store for high-sensitivity secrets, and certainly not source control.

Secrets Manager handles rotation, management, and retrieval of database credentials, API keys, and other secrets across their lifecycle. Crucially, rotation can be automated on a schedule, replacing long-term secrets with short-term ones and substantially reducing the risk of compromise.

For RDS, Aurora, and DocumentDB, managed rotation is available without writing a Lambda function. For everything else, you write a rotation Lambda that Secrets Manager invokes on your defined schedule.

<!-- INTERNAL_LINK: Cloud security vulnerability management | cloud-security-vulnerability-management -->

---

## Monitoring and detecting privileged access abuse

Controls prevent; monitoring detects. GuardDuty can detect anomalous usage of powerful IAM credentials. Enable it in every account and every region. Complement it with:

- CloudTrail: management events logged to an immutable S3 bucket in a dedicated security account, with object lock enabled. Logs must be complete, immutable, and queryable.
- AWS Security Hub: aggregates GuardDuty, Config, and IAM Access Analyzer findings into a single view. For FCA-regulated environments where you need evidence of continuous monitoring, this matters.
- CloudWatch Alarms: alert on `ConsoleLogin` events without MFA, `AssumeRoleWithWebIdentity` calls from unexpected sources, and any use of root credentials.

The NCSC's Principle 12 (Secure Service Administration) is explicit on this: administration interfaces should produce detailed audit information that is checked regularly for anomalous or unexpected behaviour. Whether you are an AWS customer or an MSP delivering managed cloud services, the same discipline applies to your own admin interfaces.

<!-- INTERNAL_LINK: Cloud incident response | cloud-incident-response -->
<!-- INTERNAL_LINK: AWS Inspector vulnerability management | aws-inspector-vulnerability-management -->

### Privileged access workstations

For the most sensitive operations, such as management account work, production database administration, or KMS key management, consider requiring access from a hardened Privileged Access Workstation (PAW). A dedicated PAW is one of the most effective controls for protecting administrators from credential theft and malware infection.


The NCSC published a dedicated set of principles for secure privileged access workstations in March 2025.
 A PAW is a highly restricted and audited physical device that reduces the attack surface for high-risk systems, making those accesses significantly harder to compromise in practice.

In an AWS context, you can enforce PAW access using an SCP or IAM policy condition that restricts role assumption to requests originating from a specific IP range (your PAW subnet, via a VPN endpoint) or requiring a specific source identity tag.

---

## Common pitfalls in AWS PAM

I have seen all of these in production.

### 1. Granting `AdministratorAccess` "temporarily" and leaving it

The most common PAM failure. A developer needs broad access during an incident, gets it, and no one revokes it. Automate revocation. If your JIT tooling does not automatically expire access, it is not JIT. It is just a slower version of standing privilege.

### 2. Forgetting machine identities

PAM conversations tend to focus on human users, but in modern AWS environments, Lambda functions, ECS tasks, and CI/CD pipeline roles frequently carry more privilege than any human account. Audit your machine identities with IAM Access Analyzer regularly. Eliminate static IAM keys where possible and use temporary tokens via role assumption. Machine identities are frequently the weakest link.

### 3. Treating SCPs as the only control

SCPs set the permission ceiling, not the floor. They do not replace IAM policies. SCPs define what can never happen in a member account; IAM policies define what is actually permitted within that boundary. You need both layers working together. Relying on SCPs alone leaves you with a ceiling and no walls.

### 4. Not testing SCPs before broad deployment

SCPs can break things at scale if deployed without testing. If your account architecture includes separate environments for development and production, apply changes to lower environments first, test them, then promote. If not, provision a policy staging account in your AWS Organisation specifically for testing SCP effects without touching running workloads.

### 5. Ignoring the management account

SCPs do not apply to users or roles in the management account. They apply only to member accounts in your organisation. This means the management account sits outside the guardrails you have placed everywhere else. Keep the blast radius minimal: no workloads, no developer access, only break-glass and automation roles.

### 6. Hardcoding credentials in code

If AWS access keys appear in code and that code is pushed to a shared or public repository, anyone with access can misuse those credentials. Use IAM roles, instance profiles, and Secrets Manager. Never commit credentials to Git, and never rely on environment variables for secrets in long-running services.

<!-- INTERNAL_LINK: CIEM Cloud Infrastructure Entitlement Management | what-is-ciem-cloud-infrastructure-entitlement-management -->
<!-- INTERNAL_LINK: CSPM Cloud Security Posture Management | what-is-cspm-cloud-security-posture-management -->

---

## NCSC and regulatory alignment

For UK organisations, the NCSC's secure system administration guidance is the authoritative reference. Time-bounded permissions are an effective technique for reducing the risks around highly privileged identities. Global or super-administrator identities should not be used for routine tasks, but may be needed to respond to incidents. Enabling those privileges only for the duration of an incident prevents their use, accidentally or deliberately, once the incident has ended.

Access to particularly sensitive resources, such as raw customer data, should require authorisation from multiple nominated personnel and phishing-resistant MFA. NCSC guidance favours phishing-resistant MFA for privileged and sensitive access, with 
FIDO2 MFA providing guessing resistance, phishing resistance, and theft resistance
 — making hardware security keys a strong choice for administrators. AWS IAM Identity Centre supports FIDO2/WebAuthn authenticators. Mandate them for any permission set that grants administrative access.

Organisations subject to GDPR Article 32 and FCA SYSC requirements have a defensible position when they can demonstrate JIT access, full audit trails, and automated revocation. Without these controls, you are not.

<!-- INTERNAL_LINK: AWS Well-Architected Security | aws-well-architected-security -->

---

## Key takeaways

- Eliminate standing privilege. Implement JIT access using AWS's Temporary Elevated Access Management (TEAM) solution or a JIT pattern built with Entra PIM and IAM Identity Centre. Privileged permission sets should expire automatically. If they do not, your PAM programme has a gap.
- Treat static IAM credentials as toxic. Federate all human access through IAM Identity Centre backed by your corporate IdP. Use IAM roles for machine access. Enforce this at the organisational level with an SCP that denies `iam:CreateUser` and `iam:CreateAccessKey` in member accounts.
- Use SCPs as preventive guardrails, not your only control. SCPs set the permission ceiling across your organisation, but IAM policies must still implement least privilege within that ceiling. Use both layers deliberately. Test SCPs in a staging OU before deploying broadly.
- Right-size permissions continuously. Use IAM Access Analyzer's policy generation capability to produce least-privilege policies from CloudTrail activity. Integrate custom policy checks into your CI/CD pipelines to catch over-permissive policies before deployment.
- Monitor privileged activity without gaps. CloudTrail must be enabled across all accounts and regions, with logs shipped to an immutable S3 bucket in a dedicated security account. GuardDuty detects anomalous IAM usage. Security Hub aggregates everything. Alert on root user activity immediately.
- Align to NCSC guidance. The NCSC's Secure System Administration guidance and 14 Cloud Security Principles set the bar for UK public sector and regulated private sector organisations. JIT access, phishing-resistant MFA, and PAWs for the most sensitive operations are the practical implementation of those principles in AWS.