---
title: "AWS IAM Best Practices: A Practitioner's Guide for 2026"
date: 2026-08-01
description: "A technical guide to AWS IAM best practices covering least privilege, SCPs, MFA, workload identity, and the updated IAM Policy Simulator."
tags: ["aws", "iam", "cloud-security", "identity-access-management", "least-privilege"]
slug: "aws-iam-best-practices"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2116
draft: false
---

# AWS IAM best practices: a practitioner's guide for 2026

Identity and Access Management is where most AWS breaches start. Most cloud security incidents trace back to the customer side: identity misuse, misconfiguration, exposed workloads. If you are responsible for securing an AWS environment, whether for an FCA-regulated financial firm, a UK public sector body, or a SaaS scale-up, getting IAM right is the highest-leverage investment you can make in your security posture.

IAM answers two questions: who can access your cloud environment, and what can they do once they are in. Get it wrong and a single compromised credential can cascade into a full account takeover.

This guide covers the controls that matter, the tooling that has matured significantly in mid-2026, and the mistakes I keep seeing teams make in production.

<!-- INTERNAL_LINK: AWS IAM Identity Centre overview | aws-iam-identity-centre -->
<!-- INTERNAL_LINK: AWS Well-Architected Security pillar | aws-well-architected-security -->

---

## Principle 1: Lock down the root account first

Before touching anything else, address root. The root account has unrestricted access to all AWS resources, billing, and account closure. It bypasses all IAM policies and SCPs. A compromised root account is a total account takeover.

The practical steps are straightforward:

- Delete all root access keys immediately. Root should never have programmatic access.
- Enable hardware MFA (FIDO2/passkey). AWS now recommends phishing-resistant passkeys over TOTP for root.
- Use root only for the handful of tasks that genuinely require it: account closure, certain AWS Support plan changes, and a small number of billing actions.

The NCSC recommends phishing-resistant MFA (FIDO2 security keys or passkeys) for administrative access. That aligns directly with what AWS is pushing natively, so there is no longer a reason to settle for TOTP apps on privileged accounts. CIS Benchmark v5.0 says the same thing explicitly.

---

## Principle 2: Eliminate long-lived credentials

This is the position I take into every architecture review. IAM users rely on long-lived credentials, passwords and access keys, that never automatically expire and are easily leaked.

The migration path is IAM Identity Center for humans, IAM Roles Anywhere for on-prem workloads, and OIDC federation for CI/CD. There is no good reason for an IAM user with a static access key in 2026.

Enforce this at the organisational level with an SCP that prevents anyone from creating new access keys:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyIAMUserAndKeyCreation",
      "Effect": "Deny",
      "Action": [
        "iam:CreateUser",
        "iam:CreateAccessKey"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalTag/BreakGlassRole": "true"
        }
      }
    }
  ]
}
```

Apply this SCP to all non-management OUs. It forces the conversation and blocks the easy path of handing out access keys. The condition allows a narrow break-glass exemption without punching a hole in the control for everyone.

<!-- INTERNAL_LINK: Shared Responsibility Model | shared-responsibility-model-cloud-security -->

For workloads, IAM roles for EC2, Lambda, and automation mean services assume permissions using temporary credentials rather than long-term keys. Less credential sprawl, smaller blast radius.

---

## Principle 3: Enforce least privilege, and use tooling to get there

Least privilege is not a state you arrive at. It is a continuous process. As environments scale, access expands faster than it gets reviewed. Excess privilege accumulates quietly.

The practical answer is IAM Access Analyzer. It provides access analysis, policy checks, and policy generation, and it is the mechanism that takes least privilege from an aspiration to something you can actually measure and enforce.

The policy generation feature is the one teams consistently underuse. Access Analyzer examines CloudTrail logs over a specified time window, identifies which AWS services and actions a role or user actually called, and produces a policy template based on that activity for you to review and refine.

A worked CLI example, generating a least-privilege policy from real CloudTrail activity for an application role:

```bash
# Step 1: Start policy generation job based on actual CloudTrail activity
aws accessanalyzer start-policy-generation \
  --policy-generation-details '{
    "principalArn": "arn:aws:iam::123456789012:role/MyAppRole"
  }' \
  --cloud-trail-details '{
    "trails": [{
      "cloudTrailArn": "arn:aws:cloudtrail:eu-west-2:123456789012:trail/management-trail",
      "regions": ["eu-west-2"],
      "allRegions": false
    }],
    "accessRole": "arn:aws:iam::123456789012:role/AccessAnalyzerRole",
    "startTime": "2026-06-01T00:00:00Z",
    "endTime": "2026-07-31T00:00:00Z"
  }'

# Step 2: Poll for completion (status: IN_PROGRESS → SUCCEEDED)
aws accessanalyzer get-generated-policy \
  --job-id "<job-id-from-previous-step>" \
  --query 'jobDetails.status'

# Step 3: Retrieve and review the generated policy
aws accessanalyzer get-generated-policy \
  --job-id "<job-id-from-previous-step>"
```

It gives you a solid starting point grounded in real usage data rather than guesswork. Run it quarterly at minimum.

For CI/CD pipelines and Terraform workflows, `iamlive`, a third-party open-source tool maintained by the community rather than an AWS-managed service, is a useful complement. It runs as a local proxy, captures the actual AWS API calls your application makes, and generates a minimum policy. It is the right tool when Access Analyzer's policy generation is too coarse for your workload.

<!-- INTERNAL_LINK: DevSecOps shift-left security | devsecops-shift-left-security -->

---

## Principle 4: Use SCPs as guardrails, not permissions

SCPs and IAM policies serve different purposes. SCPs set the maximum permissions for accounts in your AWS Organisation. They do not grant access; they define the boundary of what IAM policies can grant. They are a ceiling, not a floor. Teams that write SCP Allows expecting them to grant access are building a false sense of security.

In September 2025, AWS significantly expanded the IAM policy language supported in SCPs, adding conditions in Allow statements, individual resource ARNs, the NotAction element with Allow statements, wildcards at the start or middle of Action element strings, and the NotResource element. That is a substantial expansion, and it enables much more precise guardrails than were previously possible, though it is not complete parity with IAM policies. Some elements, including certain uses of Principal, remain unsupported in SCPs, so it is worth checking the current documentation before assuming an IAM policy construct will carry over unchanged.

A practical minimum SCP baseline for a production OU should cover:

- Deny leaving the AWS Organisation
- Deny root account usage
- Deny creation of IAM users and access keys (as shown above)
- Region restriction to approved regions (relevant for UK data residency and FCA/GDPR requirements)
- Deny disabling CloudTrail

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->

---

## Principle 5: Use permission boundaries to delegate safely

This is the IAM feature most teams either ignore or implement incorrectly. Permission boundaries let you safely give developers `iam:CreateRole` without handing them effective admin access to the entire account.

Without them, you have a privilege escalation path that has contributed to real incidents. The pattern goes like this: a user with `iam:CreateRole` and `iam:AttachRolePolicy` creates a new role, attaches the AWS-managed `AdministratorAccess` policy, assumes that role, and is now an admin. It is not subtle once you see it, but it catches teams out regularly.

Permission boundaries work by restricting the effective permissions of a principal to the intersection of its identity-based policies and the boundary, whichever is more restrictive. Enforce the boundary at creation time by requiring it as a condition on the `iam:CreateRole` action.

<!-- INTERNAL_LINK: AWS KMS key management best practices | aws-kms-key-management-best-practices -->

---

## Principle 6: Workload identity, IRSA, Pod Identity, and beyond

For containerised workloads, the no-static-credentials principle extends to Kubernetes. In the early days of EKS, if pods needed to access AWS services like S3 or DynamoDB, you attached IAM policies to the node's instance profile. Every pod on that node got the same permissions. That is a serious problem at any meaningful scale.

IAM Roles for Service Accounts (IRSA) fixes this by letting you assign specific IAM roles to individual Kubernetes service accounts. Each pod gets exactly the permissions it needs.

For EKS clusters, AWS also offers EKS Pod Identity as a simpler alternative. Launched at re:Invent 2023, it eliminates the need for OIDC provider setup and per-cluster trust policies. The association model maps Kubernetes service accounts to IAM roles directly through the EKS API.

The trade-off is portability. IRSA works across EKS in the cloud, EKS Anywhere, self-managed Kubernetes on EC2, and ROSA. If you are running a hybrid Kubernetes setup, a pattern I see regularly in UK financial services where teams run workloads both on-prem and in AWS, IRSA with a self-hosted OIDC provider remains the right mechanism. The OIDC discovery endpoint and JWKS must be publicly reachable by AWS STS; a public S3 bucket configured for static hosting is one common way to expose them for a self-managed cluster, though any HTTPS-reachable endpoint will do. Key rotation requires updating the JWKS in lockstep; operationally, that is the primary pain point to plan for.

For new EKS-in-cloud clusters with no portability requirement, EKS Pod Identity is the simpler path.

<!-- INTERNAL_LINK: Cross-cloud security services comparison | cross-cloud-security-services-comparison -->

---

## Principle 7: Test policies before you deploy them

IAM Policy Simulator has long been part of the IAM toolkit, and it has been able to test how Service Control Policies interact with identity and resource policies since late 2023. What has changed more recently is the depth of that SCP modelling and the flexibility to cover more of the scenarios that security and platform teams care about in practice.

For multi-account organisations, SCP simulation is the feature most worth building into your workflow. You can test how your organisation's SCP hierarchy interacts with identity and resource policies, and through the API, test how condition keys such as region restrictions and tag requirements affect the outcome.

The ability to exclude specific policies also matters. Modelling "what if I remove this policy?" is a common scenario during triage, and previously you had to do it manually. Cross-account simulations now report per-policy decisions for identity and resource-based policies, with matched statements returned for denied requests.

Embed policy simulation into your CI/CD pipeline using `aws iam simulate-principal-policy` as a pre-deployment check. It gives you a safety net before any policy change reaches production.

One caveat worth keeping in mind: policy simulator results can differ from your live environment. AWS recommends checking policies against your live environment after testing to confirm you are getting the results you expect.

<!-- INTERNAL_LINK: Cloud incident response | cloud-incident-response -->

---

## Common pitfalls

After fifteen years of reviewing AWS IAM configurations, these are the patterns that keep costing teams.

Using `"Resource": "*"` without conditions. Wildcarding resources is sometimes unavoidable, as List* actions often have no resource-level support, but doing it habitually on write actions is a significant blast-radius problem. Always pair resource wildcards with condition keys where available: `aws:ResourceTag`, region restrictions, or `aws:SourceAccount`.

Confusing SCP allows with granted permissions. An action must be allowed by both SCPs and IAM policies. An SCP Allow does not grant permissions; it only permits the possibility of having that permission via an IAM policy. Teams that misunderstand this end up with controls that look right on paper but do nothing.

Ignoring service-linked roles in audits. These are managed by AWS, but their permissions can still surprise you, particularly when a service updates them without notice. Audit them quarterly.

Stacking inline policies. Inline policies attached directly to users or roles are invisible to policy searches and difficult to audit at scale. Everything should go through managed policies with a clear naming convention, defined in IaC (Terraform or CDK), and reviewed through version control.

Letting IRSA fall back silently to the node instance profile. If the web identity lookup fails for any reason, a missing file, an expired JWT, or STS rejecting the call, the SDK falls back to IMDS and silently uses the EC2 node instance profile. This is why a broken IRSA setup often looks like "my pod works, just with the wrong permissions" rather than a loud failure. Set the IMDS hop limit to 1 on your EC2 node groups to harden against this.

Skipping the credential report. AWS generates a credential report showing last-used timestamps for every IAM user and key. Running it quarterly and acting on stale credentials is basic hygiene that many teams skip entirely.

<!-- INTERNAL_LINK: Cloud security vulnerability management | cloud-security-vulnerability-management -->
<!-- INTERNAL_LINK: Cloud threat detection | cloud-threat-detection -->

---

## Summary

Root account is your highest-risk identity. Enable FIDO2 MFA, delete all access keys, and use it only for the tasks that genuinely require it. NCSC and CIS Benchmark v5.0 both explicitly recommend phishing-resistant authentication for privileged access.

Long-lived credentials are a solved problem. Use IAM Identity Center for humans, IAM roles for workloads, OIDC federation for CI/CD, and IAM Roles Anywhere for on-prem systems. An SCP denying `iam:CreateAccessKey` makes this non-negotiable across your organisation.

Least privilege requires active tooling, not good intentions. IAM Access Analyzer's policy generation feature, driven from real CloudTrail activity, is the most practical mechanism to right-size permissions at scale.

SCPs are guardrails, not permissions grants. An action must be allowed by both SCPs and IAM policies. In September 2025, AWS significantly expanded the IAM policy language supported in SCPs, including conditions in Allow statements and NotResource, though some elements, such as certain uses of Principal, are still not supported.

Test policy changes before they reach production. IAM Policy Simulator's SCP simulation capability, built into the IAM console, removes the excuse for deploying untested policy changes. Automate `simulate-principal-policy` checks in your CI/CD pipeline.

For containerised workloads, choose EKS Pod Identity for new EKS-in-cloud clusters and retain IRSA where you need cross-environment portability, self-hosted Kubernetes, or EKS Anywhere. In either case, set the IMDS hop limit to 1 to prevent silent fallback to node credentials.