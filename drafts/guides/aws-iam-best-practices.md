---
title: "AWS IAM Best Practices: A Practitioner's Guide for 2026"
date: 2026-07-29
description: "A comprehensive guide to AWS IAM best practices in 2026 — covering least privilege, SCPs, ABAC, credential hygiene, and common pitfalls to avoid."
tags: ["aws-iam", "cloud-security", "identity-access-management", "least-privilege", "aws-security"]
slug: "aws-iam-best-practices"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2397
draft: false
---

# AWS IAM best practices: a practitioner's guide for 2026

Identity is the new perimeter. If you work with AWS at any serious scale, you already know that getting IAM wrong is not an academic concern. It is the single most likely reason you will be on an incident call at 2am. With the shared responsibility model placing identity, configuration, and workload protection squarely on customers, permission creep and misconfiguration now drive most incidents.

Nearly 80% of cloud security exposures stem from identity or permission misconfigurations, not zero-days or novel supply-chain attacks. The fix is not a product. It is disciplined, consistent application of identity hygiene across every account, workload, and pipeline you run.

This guide is written for practitioners who already understand what IAM is and need opinionated, production-tested guidance on where to focus effort in 2026. I will cover the policy model, credential hygiene, ABAC and TBAC patterns, workload identity for EKS, and the pitfalls that keep coming up in architecture reviews.

<!-- INTERNAL_LINK: AWS shared responsibility model explained | shared-responsibility-model-cloud-security -->

---

## 1. Stop creating IAM users for humans

This is the most impactful change most organisations can make, and it is still not universal. AWS recommends using IAM users only when federation or IAM Identity Center is not an option: break-glass access, tools that require static keys, or workloads that cannot assume roles.

For everyone else, developers, SREs, data engineers, auditors, IAM Identity Center is the right answer. Users get short-term credentials scoped to the accounts and permission sets they need, and it works with whatever IdP you already have: Okta, Azure Active Directory via SAML 2.0, or any other compatible provider.

The business case is not complicated. Exposed long-term credentials remain the top entry point used by threat actors in incidents observed by the AWS Customer Incident Response Team. Short-lived federated credentials issued through IAM Identity Center or STS eliminate that risk class entirely. Rotating credentials reduces risk; eliminating them removes it.

For UK-regulated organisations, this aligns with NCSC guidance. The ICO and NCSC both treat identity as a primary control layer in cloud-first environments, particularly where staff access data across multiple services and devices. Treating it as an afterthought increases exposure as data flows become more distributed.

<!-- INTERNAL_LINK: AWS IAM Identity Centre deep dive | aws-iam-identity-centre-guide -->

---

## 2. Apply least privilege rigorously, then enforce it with SCPs

Least privilege means giving every identity, whether user, role, or service, only the permissions it actually needs. In practice this is one of the harder security problems to get right on AWS. Most organisations start with overly broad permissions to get things working, and the tightening never happens.

Two tools complement each other well here: permission boundaries and Service Control Policies.

A permission boundary is a policy attached to an IAM entity that defines the maximum permissions that entity can hold. The effective permissions are always the intersection of the entity's identity policy and the boundary. This is the safe way to let developers create IAM roles for their own services without opening the door to privilege escalation. They can create and manage roles, but they cannot grant those roles more power than the boundary allows.

SCPs operate at a different scope entirely. They are organisation-level policies that cap the maximum permissions for every account, OU, or the whole AWS organisation. They do not need to be applied per identity; they apply to every IAM principal in scope automatically, whether human or non-human, existing or created tomorrow. Even if an identity policy grants something, an SCP denial overrides it. That ceiling is exactly what you want for org-wide guardrails.

A practical baseline SCP to deny access outside approved regions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonApprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "iam:*",
        "organizations:*",
        "support:*",
        "sts:*",
        "cloudfront:*",
        "route53:*",
        "waf:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "eu-west-2",
            "eu-west-1"
          ]
        }
      }
    }
  ]
}
```

This is a common starting point for FCA-regulated UK environments where data residency and regional control are non-negotiable. Make sure you exclude global services from the deny (IAM, CloudFront, Route 53, STS) or you will break things you did not intend to.

<!-- INTERNAL_LINK: AWS Well-Architected security pillar | aws-well-architected-security -->

---

## 3. Eliminate long-lived access keys

If you cannot immediately migrate to federated access, you need rigorous access key hygiene in the meantime. IAM access keys are one of the most common attack vectors in AWS. They get committed to Git repositories, shared in Slack, and left unrotated for years. They do not expire on their own. If compromised, they provide a persistent backdoor.

The CIS Amazon Web Services Foundations Benchmark requires rotating long-term IAM access keys at least every 90 days. The reasoning is simple: limiting the rotation window limits the exposure window if a key is quietly disclosed.

For workloads, there is no good reason to use access keys at all. EC2 instances, Lambda functions, and ECS tasks should use IAM roles, which rotate credentials automatically. Access keys are only warranted for CLI access from non-AWS environments, third-party services that do not support IAM roles, and legacy applications that genuinely cannot use roles.

Use the IAM credential report to surface stale keys across your accounts:

```bash
# Generate the credential report
aws iam generate-credential-report

# Decode and save locally
aws iam get-credential-report \
  --query 'Content' \
  --output text | base64 -d > credential-report.csv

# Surface users with keys older than 90 days
awk -F',' 'NR>1 && $9 != "N/A" {
  cmd = "date -d " $9 " +%s"
  cmd | getline key_epoch
  close(cmd)
  now = systime()
  age_days = int((now - key_epoch) / 86400)
  if (age_days > 90) print $1, "key age:", age_days, "days"
}' credential-report.csv
```

---

## 4. Adopt attribute-based access control and tag-based access control

Scaling IAM policy management across dozens of accounts and hundreds of roles by enumerating ARNs in every policy statement is a maintenance problem that compounds quickly. Attribute-based access control (ABAC) addresses this by using tags on both principals and resources as the access control dimension instead.

You can combine IAM Identity Center permission sets with session tags from Microsoft Entra ID to implement fine-grained ABAC across multiple AWS accounts. AWS has been extending ABAC support across managed services steadily, and a notable addition landed in July 2026: Amazon Neptune now supports tag-based access control (TBAC) for IAM, enabling customers to use resource tags and principal tags as conditions in IAM policies and SCPs to control access to Neptune data-plane operations.

This matters in practice. Neptune already provides solid security through VPC isolation, TLS encryption, and IAM authentication, but customers managing multiple clusters at scale needed a dynamic mechanism to enforce organisational access boundaries without enumerating specific cluster ARNs in every policy. With TBAC, a principal tagged `Project=FraudDetection` is automatically restricted to Neptune clusters sharing that tag. For financial services organisations running graph databases for fraud detection and AML workloads, this meaningfully reduces policy maintenance overhead.

The pattern looks like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "neptune-db:*",
      "Resource": "arn:aws:neptune-db:eu-west-2:123456789012:cluster/*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Project": "${aws:PrincipalTag/Project}"
        }
      }
    }
  ]
}
```

One statement replaces a sprawling set of per-cluster policies. The discipline required: if you are managing access to Neptune resources via tagging, you also need to secure access to the tags themselves. Restrict the `AddTagsToResource` and `RemoveTagsFromResource` actions explicitly. ABAC is only as strong as your tag governance.

<!-- INTERNAL_LINK: AWS KMS key management best practices | aws-kms-key-management-best-practices -->

---

## 5. Secure workload identity: IRSA and the new EKS OIDC PrivateLink

For Kubernetes workloads on EKS, IAM Roles for Service Accounts (IRSA) is the right pattern for workload identity. Not node-level instance profiles, not injected access keys. IRSA scopes IAM permissions to the pod level, which dramatically reduces blast radius if a workload is compromised.

Until recently there was a genuine constraint: each EKS cluster publishes its OIDC signing keys at a public endpoint, which created a problem for clusters running inside VPCs without internet egress. AWS PrivateLink for the EKS cluster OIDC endpoint resolves this. Tools running inside your VPC, eksctl, Terraform, or custom token validators, can now reach the OIDC discovery document and JWKS privately by creating an interface VPC endpoint for `com.amazonaws.<region>.oidc-eks`. This also ensures correct DNS resolution when the EKS management VPC endpoint is enabled with private DNS.

For organisations running fully private EKS clusters, which is increasingly common in UK public sector and financial services environments, this closes a gap that previously required awkward DNS workarounds. AWS PrivateLink for the OIDC endpoint is available at no additional cost beyond standard PrivateLink pricing in all regions where EKS is available.

<!-- INTERNAL_LINK: Kubernetes security best practices | kubernetes-security-best-practices -->

---

## 6. Continuous visibility: IAM Access Analyzer and Security Hub

Getting policies right at deployment time is necessary but not sufficient. IAM Access Analyzer continuously evaluates your resource policies, trust relationships, and IAM usage to surface three finding types: external access, internal access, and unused access. Unlike periodic scans, it uses automated reasoning to provide mathematically provable analysis of what your policies actually permit.

The unused access findings are particularly useful in production environments where permissions accumulate over time. They surface unused roles, unused access keys for IAM users, unused passwords, and for active principals, visibility into which services and actions have never been exercised.

One thing to be clear about: IAM Access Analyzer is a visibility tool, not an enforcement mechanism. It will not remove dormant permissions for you. Least privilege programmes fail when findings outpace safe remediation and standing access just sits there. Build an operational workflow, ideally event-driven via EventBridge, to route findings to your team and track remediation through to completion.

As of May 2026, Security Hub now detects unused IAM permissions, roles, and credentials across your AWS organisation. Previously, managing identity risk across hundreds of accounts meant toggling between multiple tools. Security Hub now surfaces these identity findings alongside threats, exposures, and posture findings in a single console, which makes prioritisation based on actual organisational risk considerably more tractable.

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->

---

## 7. Common IAM pitfalls and how to avoid them

These are the mistakes I see repeatedly in architecture reviews and post-incident investigations.

### Wildcard actions and resources on allow statements

IAM misconfigurations typically happen when administrators grant excessive permissions to unblock a delivery or resolve an incident quickly. The classic pattern: `AdministratorAccess` attached temporarily, or a custom policy ending with `"Action": "*"`, that nobody removes afterwards. The temporary measure becomes the permanent state.

Use IAM Access Analyzer's policy validation to catch wildcards before deployment. In CDK and CloudFormation pipelines, fail the build on `Action: *` with `Effect: Allow` in production stacks.

### Overly permissive iam:PassRole

`iam:PassRole` is one of the most dangerous permissions in IAM. It controls which principals can pass which roles to which services. A wildcard `PassRole` on `Resource: "*"` means the principal can attach any role, including `AdministratorAccess`, to any service it can launch.

Always scope `iam:PassRole` to specific role ARNs and use the `iam:PassedToService` condition key:

```json
{
  "Effect": "Allow",
  "Action": "iam:PassRole",
  "Resource": "arn:aws:iam::123456789012:role/LambdaExecutionRole-*",
  "Condition": {
    "StringEquals": {
      "iam:PassedToService": "lambda.amazonaws.com"
    }
  }
}
```

### Trust policies that are too wide

Misconfigurations happen when a role's `AssumeRolePolicyDocument` trusts an entire account ID or uses a wildcard Principal. Always scope trust policies to the specific principal (role ARN or service) and add `sts:ExternalId` conditions for cross-account trust relationships.

### Copying policies between environments without review

Copying policies from a sandbox to production without reviewing the context leads to problems: write access to sensitive buckets being the most common example I see. Your CI/CD pipeline should include IAM Access Analyzer policy validation checks as a gating control before deployment to production accounts, not just linting.

### Neglecting non-human identities

In most AWS environments, non-human identities now outnumber human ones, and the gap is widening. Service accounts, Lambda roles, CI/CD pipelines, and AI agents get created rapidly, often with broad permissions that nobody revisits. Permission boundaries are rarely applied consistently to these identities; they are created by automation, attached to ephemeral workloads, and sit outside the human-driven review processes that per-identity controls depend on. SCPs are your backstop here.

<!-- INTERNAL_LINK: DevsecOps shift-left security | devsecops-shift-left-security -->
<!-- INTERNAL_LINK: Cloud threat detection | cloud-threat-detection -->

---

## Key takeaways

These practices will not eliminate all risk, but they close the attack vectors that account for the overwhelming majority of cloud identity incidents:

- Eliminate IAM users for human access. Federate through IAM Identity Center with your existing IdP. Reserve IAM users only for genuine break-glass and legacy scenarios where roles are not feasible.
- Layer your guardrails. Use SCPs for org-wide ceiling enforcement and permission boundaries for safe IAM delegation to development teams. They solve different problems and work best together.
- Rotate or eliminate long-lived access keys. The CIS AWS Foundations Benchmark requires rotation within 90 days; the better answer for workloads is eliminating them entirely in favour of IAM roles and instance profiles.
- Adopt ABAC and TBAC where you manage access at scale. Amazon Neptune now supports tag-based IAM conditions for data-plane operations, and the pattern applies broadly across services that support resource tagging.
- Use IRSA with PrivateLink for Kubernetes workloads. As of July 2026 the EKS OIDC endpoint is reachable privately via PrivateLink, removing the last blocker for fully private IRSA in air-gapped VPCs.
- Treat IAM Access Analyzer as a continuous programme, not a one-off check. Surface findings into Security Hub, route them via EventBridge, and build a remediation workflow with actual accountability. Visibility without remediation is just a longer audit trail.

<!-- INTERNAL_LINK: AWS IAM Identity Centre | aws-iam-identity-centre -->
<!-- INTERNAL_LINK: Cloud compliance frameworks | cloud-compliance-frameworks -->
<!-- INTERNAL_LINK: Cloud incident response | cloud-incident-response -->