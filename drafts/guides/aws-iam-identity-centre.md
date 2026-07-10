---
title: "AWS IAM Identity Centre: A Practitioner's Guide to Secure Multi-Account Access"
date: 2025-07-10
description: "A practitioner's guide to AWS IAM Identity Centre covering permission sets, SCPs, OAuth for AI agents, common pitfalls, and key security takeaways."
tags: ["aws iam identity centre", "aws security", "iam", "cloud security", "zero trust", "multi-account"]
slug: "aws-iam-identity-centre-practitioners-guide"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2461
draft: false
---

# AWS IAM Identity Centre: a practitioner's guide to secure multi-account access

If you are running more than a handful of AWS accounts and still relying on long-lived IAM access keys for workforce access, you have a problem. AWS IAM Identity Centre is the service AWS explicitly recommends to fix it, and with the recent addition of OAuth 2.0 support for AI agent workflows, it has moved from "best practice for enterprises" to something every cloud team needs to understand properly. This guide is not a rehash of the AWS docs. It covers the architecture decisions that bite you later, the SCP patterns that actually hold in production, the OAuth integration that changes how your developers and AI agents authenticate, and the mistakes I have seen cost organisations real money and real incidents.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: What is Zero Trust Architecture | what-is-zero-trust-architecture -->

---

## What AWS IAM Identity Centre actually is (and is not)

AWS IAM Identity Centre, formerly AWS Single Sign-On before the rename in July 2022, is an AWS service for managing access to multiple AWS accounts and applications from one place. That sounds straightforward, but there is a conceptual trap here: Identity Centre is not just a login portal. It is the authoritative control plane for workforce identity across your entire AWS Organisation.

Managing workforce access across multiple AWS accounts using individual IAM users is a security risk that does not scale. You end up with long-term access keys scattered across accounts, duplicated user management, and fragmented audit trails. Identity Centre solves this with centralised single sign-on, temporary credentials, and unified access management across your Organisation. AWS recommends using it to manage access to your accounts and permissions within those accounts, whether you store your user identities in Identity Centre itself or in an external identity provider.

One thing worth stating plainly: Identity Centre is free. You only pay for the underlying AWS services your users access. There is no excuse for not deploying it.

---

## Architecture: identity sources and the SCIM integration

The first architectural decision is where your identities live. You have three options: the built-in Identity Centre directory, an external IdP via SAML 2.0, or AWS Managed Microsoft AD.

Connecting an existing identity source is the recommended approach. It gives your workforce single sign-on access, a consistent experience across AWS services, and a single location to manage identities rather than maintaining multiple sources.

Identity Centre supports federation with SAML 2.0, which allows it to authenticate users from external IdPs. It also supports SCIM v2.0 for automatic provisioning, updating, and deprovisioning of users and groups between your IdP and Identity Centre.

In practice, most UK enterprise clients I work with connect Microsoft Entra ID or Okta. Identities from external directories must be provisioned into Identity Centre before you can grant them access to AWS managed services, so getting SCIM configured correctly early matters.

One operational detail that trips up teams: SCIM tokens expire after one year. You need to generate a new token and update your IdP configuration before that deadline, or you will wake up to a synchronisation failure that blocks user provisioning. Put a reminder in your calendar twelve months after initial setup. The service does not warn you proactively.

<!-- INTERNAL_LINK: AWS Compliance and Governance | aws-compliance-and-governance -->

---

## Permission sets: the right abstraction for multi-account access

Permission sets are the core unit of access control in Identity Centre. They are reusable access templates that define what users can do in an AWS account. Internally, they create IAM roles automatically. The IAM roles you see in member accounts, the ones with the `AWSReservedSSO_` prefix, are managed entirely by Identity Centre. Do not touch them directly. If you have CDK or Terraform referencing these role ARNs, you are doing it wrong. Manage permissions through the permission set itself.

Permission sets let you define an access level once and assign it across multiple accounts within your Organisation. A sound permission set taxonomy for a regulated environment looks roughly like this:

- ReadOnly: for auditors, security reviewers, and on-call engineers doing investigation
- Developer: scoped service access aligned to the team's workload, no IAM write
- PlatformEngineer: broader infra access, still no `iam:*`
- SecurityOperator: read access to security tooling (GuardDuty, Security Hub, CloudTrail)
- BreakGlass: `AdministratorAccess`, tightly restricted by SCP, monitored in real time

Standing access, where permissions remain active indefinitely, creates unnecessary risk from compromised credentials. Identity Centre supports just-in-time access by allowing you to set session durations on permission sets, granting temporary permissions only when needed. For FCA-regulated environments, short session durations (one to four hours) on privileged permission sets are not optional. Under SM&CR, you need to demonstrate that privileged access is controlled, auditable, and time-limited. The session duration setting on a permission set is where you enforce that at the platform level.

<!-- INTERNAL_LINK: AWS Well-Architected Security | aws-well-architected-security -->

---

## SCPs and Identity Centre: layered guardrails

Understanding how SCPs interact with Identity Centre matters. SCPs define the maximum available permissions for IAM users and roles in your Organisation. They do not grant permissions on their own. They set the outer boundary, and everything sits inside that boundary.

The layered evaluation model is worth understanding clearly: permission sets project ordinary IAM roles into member accounts, and SCPs apply on top. A user with AdministratorAccess at the permission set level can still be denied by a Deny SCP at the OU level.

Two SCP patterns you should deploy immediately after enabling Identity Centre:

Pattern 1: prevent rogue Identity Centre instances in member accounts. After enabling Identity Centre, AWS recommends creating an SCP to prevent additional instances being created. Any additional instance indirectly adds roles and identity providers to IAM, which is exactly what you do not want.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyMemberAccountIICInstances",
      "Effect": "Deny",
      "Action": ["sso:CreateInstance"],
      "Resource": "*"
    }
  ]
}
```

Pattern 2: lock down Identity Store API access from member accounts. This prevents users in member accounts from accessing any API operation in the identity store.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ExplicitlyBlockIdentityStoreAccess",
      "Effect": "Deny",
      "Action": ["identitystore:*", "sso-directory:*"],
      "Resource": "*"
    }
  ]
}
```

Apply this to all OUs that are not your management or security tooling account.

<!-- INTERNAL_LINK: AWS CloudTrail Configuration Best Practices | aws-cloudtrail-configuration-best-practices -->

---

## OAuth 2.0, AI agents, and why Identity Centre is now more critical than ever

This is where things have shifted significantly in 2025 and 2026. AI coding agents operating inside your AWS environment mean Identity Centre is no longer just about human access.

The AWS MCP Server can now authenticate using the same credentials and sign-in methods your workforce already uses for the AWS Management Console or CLI, through a browser-based flow using OAuth. This sign-in path supports IAM federation, IAM Identity Centre, and root or IAM users. AWS has also introduced new global condition keys for OAuth, token introspection and revocation, dynamic client registration, new CloudTrail elements, and an API for headless OAuth connectivity, all compatible with your existing IAM configuration.

The trust model is clear: authorising an agent allows it to access the AWS MCP Server on your behalf. It does not grant the agent additional AWS permissions. Every request is still evaluated against your existing IAM policies, SCPs, RCPs, permission boundaries, and other organisational controls.

This is the correct model. It means your existing Identity Centre permission sets and SCPs govern what AI agents can do. You do not need a parallel permissions architecture for agentic workloads. What you do need is to think carefully about which permission set your developers authenticate under when using tools like Claude Code or Amazon Kiro, because that is the blast radius if an agent makes a destructive API call.

Unlike traditional applications with deterministic code paths, agents reason dynamically, choosing different tools or accessing different data depending on context. You must assume an agent can do anything within its granted entitlements, whether OAuth scopes, API keys, or IAM permissions, and design your controls accordingly. Agents operate at machine speed, so the impact of misconfigured permissions scales quickly.

<!-- INTERNAL_LINK: Beginners Guide to AI LLM Security | beginners-guide-ai-llm-security -->
<!-- INTERNAL_LINK: Social Engineering AI Agents | social-engineering-ai-agents -->

---

## Auditing and CloudTrail integration

All IAM Identity Centre API calls are logged in CloudTrail. This includes `AssumeRoleWithSAML` events that fire each time a user assumes a permission set role. For BreakGlass roles, wire a CloudTrail metric filter on `AssumeRoleWithSAML` for the specific role ARN to a CloudWatch alarm and an SNS or PagerDuty notification. You want real-time alerting when anyone assumes a role with `AdministratorAccess`, not a weekly report.

For GDPR compliance, CloudTrail logs are personal data. They contain email addresses and session identifiers. Ensure your log retention, encryption (SSE-KMS), and access policies reflect your DPIA obligations. S3 Object Lock on your CloudTrail bucket is a straightforward way to meet GDPR's integrity requirements.

<!-- INTERNAL_LINK: AWS Security Hub Guide | aws-security-hub-guide -->
<!-- INTERNAL_LINK: Cloud Incident Response | cloud-incident-response -->

---

## Common pitfalls and how to avoid them

After running Identity Centre deployments across a range of UK public sector and financial services environments, these are the failure modes I encounter most.

Assigning permission sets directly to users instead of groups is a governance anti-pattern. When someone leaves, you delete the group membership in your IdP and SCIM propagates the change. If you assigned the permission set directly to the user in Identity Centre, offboarding becomes a manual, error-prone task that your GDPR DPO will not thank you for.

Choosing the wrong home Region is a one-way decision. Identity Centre runs in a single AWS Region per instance. If you need to change Region later, you must delete your current instance and recreate everything: all users, groups, permission sets, and assignments. For UK data residency requirements, choose `eu-west-2` (London) unless you have a specific reason not to.

Ignoring the SCP and permission set interaction catches teams out regularly. A user with AdministratorAccess at the permission set level can still be denied by a Deny SCP at the OU level. Always test new permission sets against the SCPs of the target OU before assigning them to users.

Over-permissioning developers because "we'll tighten it later" is the single most common mistake I see. Permissive access attracts scrutiny if contractors are involved under IR35, and it guarantees a finding in any ISO 27001 or Cyber Essentials Plus audit.

Letting the SCIM bearer token expire silently causes outages that are entirely preventable. The maximum token lifetime is one year. Document the rotation procedure and set calendar reminders at 30, 15, and 3 days before expiry. If you do not have this today, add it before you close this tab.

Not enabling multi-Region replication is increasingly hard to justify. With the launch of Identity Centre multi-Region replication, you can now replicate your configuration to a secondary Region. For production environments with an RTO under four hours, this is a requirement, not a nice-to-have.

<!-- INTERNAL_LINK: What is CIEM Cloud Infrastructure Entitlement Management | what-is-ciem-cloud-infrastructure-entitlement-management -->

---

## Key takeaways

Deploy at the Organisation level, not per account. Enabling Identity Centre in conjunction with AWS Organisations is the recommended approach for centrally managed access across multiple accounts. Account-level instances are for edge cases only.

Permission sets replace IAM users for all human access. AWS best practice is to require human users to federate through an identity provider and access AWS using temporary credentials. Long-lived access keys for developers are an NCSC 14 Cloud Security Principles violation waiting to happen.

SCPs are your organisation-wide safety net. Use them to deny unapproved Regions, block Identity Store API access from member accounts, and prevent rogue Identity Centre instances. Ship these on day one.

Identity Centre governs AI agent access too. The OAuth 2.0 sign-in path for the AWS MCP Server uses the same permission sets and SCPs as your human workforce. Design your permission sets with agentic workloads in mind, and keep developer permission sets scoped to what is actually needed. An AI agent will use every permission it has.

Audit everything, alert on the critical path. Wire CloudWatch metric filters on `AssumeRoleWithSAML` events for privileged permission sets. Compliance teams need evidence of controlled access, not just configuration screenshots.

Operationalise SCIM token rotation and Region selection before you go live. Both are trivial to get right at the start and expensive to fix after the fact.