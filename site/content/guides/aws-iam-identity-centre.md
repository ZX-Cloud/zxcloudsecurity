---
title: "AWS IAM Identity Centre: A Practitioner's Guide to Centralised Workforce Access"
date: 2026-06-23
description: "AWS IAM Identity Centre for multi-account environments: permission sets, SCIM federation, eliminating long-term credentials, and common implementation pitfalls."
tags: ["aws-iam-identity-centre", "aws-security", "identity-federation", "permission-sets", "multi-account"]
slug: "aws-iam-identity-centre-guide"
author: "Steve Harrison, Principal Security Architect"
word_count: 2302
faqs:
  - question: "What is AWS IAM Identity Centre?"
    answer: "AWS IAM Identity Centre (formerly AWS Single Sign-On) is the recommended service for centralising workforce access to multiple AWS accounts and applications. It integrates with your existing identity provider (Active Directory, Okta, Entra ID) via SAML 2.0 or SCIM, maps identity provider groups to permission sets (predefined IAM policy bundles), and issues short-lived temporary credentials for each session. Users authenticate once with their corporate identity and gain access to the AWS accounts and applications they are assigned, without managing separate IAM users or long-term access keys."
  - question: "What is the difference between AWS IAM Identity Centre and IAM users?"
    answer: "IAM users are long-term identities with permanent credentials (passwords and access keys) stored in individual AWS accounts. AWS IAM Identity Centre provides federated access using your existing corporate directory — users authenticate with their organisational credentials and receive temporary STS credentials scoped to the accounts and permission sets they are assigned. Identity Centre eliminates the need to create and manage IAM users across accounts, ensures leavers are automatically de-provisioned when their corporate account is disabled, enforces MFA at the identity provider layer, and provides a centralised audit trail of all session activity."
  - question: "How does SCIM work with AWS IAM Identity Centre?"
    answer: "SCIM (System for Cross-domain Identity Management) is a protocol that enables your identity provider (Okta, Entra ID, JumpCloud) to automatically synchronise user and group changes to IAM Identity Centre in near real-time. When a user is added to or removed from a group in your IdP, SCIM propagates that change to Identity Centre within minutes, updating their account assignments and permission sets without manual intervention. SCIM provision covers create, update, and deprovision events — a user removed from a group loses the associated AWS account access automatically, which is critical for leaver processing."
  - question: "What is a permission set in AWS IAM Identity Centre?"
    answer: "A permission set is a collection of IAM policies and access boundaries defined centrally in IAM Identity Centre and deployed as IAM roles in member accounts. You create a permission set (e.g., 'ReadOnly', 'SecurityAudit', 'DeveloperAccess') attaching managed or inline policies, then assign it to specific groups and accounts. When a user in an assigned group authenticates, they can assume the corresponding IAM role in the account. Permission sets decouple role definitions from individual accounts — update a permission set once and it propagates to every account where it is assigned."
draft: false
---

# AWS IAM Identity Centre: centralised workforce access done right

If you are still issuing long-term IAM user credentials to engineers in a multi-account AWS estate, you are carrying a risk that regulators and your own incident response team will eventually force you to address. AWS IAM Identity Centre (formerly AWS Single Sign-On) is the answer, and as of June 2026 it has matured to the point where it is the only defensible choice for human access to AWS. This guide covers the architecture, the configuration decisions that matter, the quotas that will bite you at scale, and the mistakes I see repeated across nearly every organisation I work with.

<!-- INTERNAL_LINK: Understanding AWS Organisations and SCPs | aws-organisations-scp-guide -->
<!-- INTERNAL_LINK: Least Privilege IAM Policy Design | iam-least-privilege-policy-guide -->

---

## What AWS IAM Identity Centre actually is (and what it isn't)

AWS IAM Identity Centre is a centralised workforce identity management service that provides single sign-on access to multiple AWS accounts and business applications. It sits at the organisation level, not the account level. That distinction matters more than it might first appear.

The service operates on two primitives.

Permission sets define the level of access that users or groups have to an AWS account. They can contain AWS managed policies, customer managed policies, inline policies, and permissions boundaries.

Account assignments are the binding of a group or user to a permission set, scoped to a target AWS account. When you create an assignment, Identity Centre creates corresponding IAM roles in each target account and attaches the policies specified in the permission set to those roles.

Those roles carry the `AWSReservedSSO_` naming prefix. You will see them everywhere once the service is running. If you delete all assignments to a permission set in an account, the corresponding role is deleted too. Create a new assignment to the same permission set later and Identity Centre creates a new role with a different unique suffix in the ARN. That suffix behaviour has real implications for any trust policies or CloudTrail regex filters you have written. Pin to the `AWSReservedSSO_<PermissionSetName>_` prefix pattern, not the full ARN.

Identity Centre is not a replacement for IAM. SCPs still govern what those roles can do. IAM resource policies still apply. Identity Centre controls who gets which role, nothing more.

---

## Pre-enablement decisions you cannot easily reverse

Before you click Enable in the console, you need to make four decisions. Two of them are genuinely difficult to walk back.

### Instance type

An organisation instance is created from the management account of an AWS Organisation and is the only instance type that can manage cross-account permissions. An account instance is bound to a single account and is intended for AWS-managed application access only. Do not use an account instance for workforce console access.

### Home region

The organisation instance is created in one home region. Replication to additional regions is supported for resiliency, but the original home region selection is operationally sticky. Pick a region that aligns with your data residency requirements and your CloudTrail or Organisation Trail region. For UK clients subject to GDPR or FCA data-residency requirements, `eu-west-2` (London) is almost always the right answer.

### Identity source

Your options are the Identity Centre directory (the default), Active Directory, or an external IdP via SAML 2.0 and SCIM v2. Switching between sources later deletes existing users and groups and removes all assignments, which means everyone including admins loses SSO access until reprovisioned. Decide early.

### Delegated administrator

After enablement, register one member account as the delegated administrator so that day-to-day Identity Centre operations do not require the management account. The delegated administrator can do almost everything except modify permission sets that grant access to the management account itself.

AWS recommends delegating Identity Centre administration to limit who has access to the management account and to reserve it for tasks that genuinely require it.

---

## Connecting your identity provider: SAML and SCIM

You can connect to existing identity providers using SAML 2.0 and SCIM, whether that is Entra ID, Okta, or Google Workspace. SAML handles authentication; SCIM handles automated provisioning and deprovisioning.

The SCIM integration is what makes the security model work at scale. Default to `PrincipalType: GROUP` for account assignments and treat `USER` as a documented exception, not a normal pattern. Group memberships propagate via SCIM and unwind cleanly on offboarding. Per-user assignments do not, and they linger as orphan IAM roles after the user is removed from the IdP.

One operational problem that causes incidents: SCIM tokens expire after one year. You must generate a new token and update your IdP configuration before expiry. Automatic warning emails go out 30, 15, and 3 days before expiry, but those emails need an owner. I have seen UK financial services clients lose all SSO provisioning for 48 hours because nobody owned that calendar event. Create the reminder, document the rotation procedure, and assign a named owner.

For organisations using Microsoft Entra ID, you can go further and implement just-in-time privileged access using Entra Privileged Identity Management. Because the group is assigned to the enterprise application and configured for provisioning, updated group membership is automatically synchronised via SCIM with the connected Identity Centre instance.

---

## Permission set design: practical patterns

Per permission set you get up to one inline policy (capped at 32,768 characters), up to 10 attached managed policies (the underlying IAM role limit, raiseable via IAM service quotas), a session duration configurable up to 12 hours, and one optional permissions boundary.

The most powerful and underused feature is the ability to reference customer-managed policies by name rather than embedding the policy body. The customer-managed policy must already exist in each target account, with the same name, before the permission set is assigned. At assignment time, Identity Centre looks up the named policy in the target account and attaches it to the `AWSReservedSSO_` role. That indirection lets the same permission set adapt to per-account specifics without duplicating policy bodies across accounts.

Below is a working Terraform example defining a least-privilege permission set for a security operations responder, backed by a permissions boundary:

```hcl
resource "aws_ssoadmin_permission_set" "sec_ops_responder" {
  name             = "SecOpsResponder"
  description      = "Read-only triage access with GuardDuty investigation rights"
  instance_arn     = tolist(data.aws_ssoadmin_instances.main.arns)[0]
  session_duration = "PT4H"  # 4 hours - adequate for a triage shift
}

# Attach the AWS-managed SecurityAudit policy
resource "aws_ssoadmin_managed_policy_attachment" "sec_ops_security_audit" {
  instance_arn       = tolist(data.aws_ssoadmin_instances.main.arns)[0]
  managed_policy_arn = "arn:aws:iam::aws:policy/SecurityAudit"
  permission_set_arn = aws_ssoadmin_permission_set.sec_ops_responder.arn
}

# Permissions boundary - caps maximum effective permissions
resource "aws_ssoadmin_permissions_boundary_attachment" "sec_ops_boundary" {
  instance_arn       = tolist(data.aws_ssoadmin_instances.main.arns)[0]
  permission_set_arn = aws_ssoadmin_permission_set.sec_ops_responder.arn

  permissions_boundary {
    managed_policy_arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
  }
}

# Assign to a group (never directly to a user)
resource "aws_ssoadmin_account_assignment" "sec_ops_prod" {
  instance_arn       = tolist(data.aws_ssoadmin_instances.main.arns)[0]
  permission_set_arn = aws_ssoadmin_permission_set.sec_ops_responder.arn
  principal_id       = aws_identitystore_group.sec_ops.group_id
  principal_type     = "GROUP"
  target_id          = var.prod_account_id
  target_type        = "AWS_ACCOUNT"
}
```

The CLI and API call `create-account-assignment` is asynchronous. You must poll `describe-account-assignment-creation-status` to confirm the IAM role was provisioned in the target account. Your Terraform provider handles this automatically, but custom scripts must not assume immediate consistency.

<!-- INTERNAL_LINK: Managing IAM Permission Boundaries | iam-permission-boundaries-guide -->

---

## The June 2026 quota change: what changed and why it matters

This is the update that will unblock a number of larger organisations that have been hitting a shared ceiling.

AWS IAM Identity Centre now supports separate quotas for the number of AWS accounts and applications that can be configured in an instance. By default, you can configure up to 7,000 AWS accounts and up to 7,000 applications independently, so that using more of one does not consume capacity from the other.

Previously these were pooled. If you had 3,000 accounts and 3,000 applications registered in the same instance you were at the combined cap. Customers with existing higher limits are automatically granted the same limit for both accounts and applications, with no action required. Organisations managing thousands of AWS accounts can now onboard applications without consuming account quota capacity.

Quotas can be increased further by submitting a request through the AWS Service Quotas console. This update is available in all AWS regions where IAM Identity Centre is available.

This matters particularly to UK financial services groups that use Identity Centre to front-door both their AWS estate (often 200 to 500 accounts in a mature organisation) and a catalogue of internal SaaS applications. You no longer have to trade off account growth against application onboarding.

The broader IAM quota improvements from May 2026 are also relevant here. AWS increased maximum quotas for six resources, including customer managed policies per account from 5,000 to 10,000, managed policies per role from 20 to 25, role trust policy length from 4,096 to 8,192 characters, and roles per account from 5,000 to 10,000. The increase to managed policies per role directly affects permission set sizing.

One procedural note: quota increase requests must come from a management or delegated administrator account. Route all Service Quotas requests through your delegated admin account to keep management account activity minimal.

<!-- INTERNAL_LINK: AWS Service Quotas Management at Scale | aws-service-quotas-guide -->

---

## Common pitfalls

These are the mistakes I encounter repeatedly in production environments.

### 1. Enabling in the wrong region

Identity Centre is a regional service at the control plane level. If you enable it in `us-east-1` because that is where your first AWS account was created, you will spend the next three years explaining to your DPO why identity events are flowing through a US region for a UK-only estate. Choose `eu-west-2` before you click Enable. You cannot migrate the home region without deleting the instance.

### 2. Managing users directly in Identity Centre when using an external IdP

If you use an external identity source, you should implement policies that limit the identity store write operations that an Identity Centre admin can perform from within the delegated administration account. The external identity source is the source of truth for users, attributes, and group memberships. Changes made via the identity store APIs or the console will be overwritten during normal synchronisation cycles.

### 3. Assigning permission sets to individual users

Default to `PrincipalType: GROUP`. Per-user assignments do not unwind cleanly and linger as orphan IAM roles after the user is removed from the IdP. This is an offboarding failure waiting to happen, and it will almost certainly appear as a finding in your next FCA operational resilience review.

### 4. Ignoring the IAM role quota in member accounts

If you have already configured IAM roles in an account, check whether it is approaching the default quota of 1,000 roles. In an account already using Identity Centre you will see roles beginning with `AWSReservedSSO_`. A busy shared-services account with 30 permission sets assigned to it will consume 30 of those 1,000 slots. Multiply that across teams and you can hit the ceiling faster than expected. Request a quota increase proactively rather than discovering the limit during a deployment.

### 5. Forgetting the SCIM token expiry

Already covered above, but it warrants its own entry because it keeps happening. Build token rotation into your operational runbook, assign a named owner, and test the rotation procedure before you need it under pressure.

### 6. Not enforcing MFA when using the built-in identity store

For organisations using the built-in Identity Centre directory, MFA can be enforced at the identity source level, and IAM policies can deny access to sensitive actions unless MFA has been completed. The NCSC is explicit that phishing-resistant MFA should be used for administrative access, specifically FIDO2 security keys or passkeys. If you are on the built-in directory and not enforcing this, fix it before anything else on this list.

<!-- INTERNAL_LINK: Enforcing MFA in AWS at the organisation level | aws-mfa-enforcement-guide -->

---

## Auditing and observability

All IAM Identity Centre API calls are logged in CloudTrail. For compliance requirements, ensure CloudTrail is configured for organisation-wide logging to capture all Identity Centre activity.

The CloudTrail event source for provisioning activity is `identitystore-scim.amazonaws.com`. For authentication and role assumption events, look for `sso.amazonaws.com` and `sso-oauth.amazonaws.com`. Build EventBridge rules that alert on any assumption of your break-glass permission set. Those events should be rare enough that every single one warrants a page to the on-call engineer.

AWS Config conformance packs include mappings to NCSC Cloud Security Principles. The sample mapping between the UK NCSC Cloud Security Principles and AWS managed Config rules covers specific AWS resources and relates to one or more NCSC Cloud Security Principles controls. Use this pack as a starting point for assurance evidence if you are working towards Cyber Essentials Plus or supporting an FCA authorisation application.

<!-- INTERNAL_LINK: AWS CloudTrail organisation-wide logging | aws-cloudtrail-organisation-guide -->

---

## Summary

AWS IAM Identity Centre is the only defensible human access model for multi-account AWS estates in 2026. Individual IAM users with long-term credentials are not an acceptable control for any regulated UK environment.

Make your four pre-enablement decisions before you click Enable: instance type, home region (use `eu-west-2` for UK data residency), identity source, and delegated administrator. Switching identity source mid-flight locks out everyone, including your admins.

The June 2026 quota update separates account and application limits to 7,000 each, independently. If you were previously holding back SaaS application onboarding because you were near the combined cap, that constraint is gone.

Always assign permission sets to groups, never to individual users. Per-user assignments create orphan `AWSReservedSSO_` roles that survive offboarding, which is both a security exposure and an audit finding.

Rotate your SCIM token before it expires. Calendar it, own it, and test the rotation procedure. A lapsed token stops all automated provisioning and deprovisioning silently, with no console error to point you at the cause.

Monitor the IAM role quota in member accounts. Each permission set assignment creates one `AWSReservedSSO_` role per account. In accounts with many permission sets, the default quota of 1,000 roles is closer than it looks. Request an increase through Service Quotas before you need it.