---
title: "AWS IAM Best Practices: A Practitioner's Guide for 2026"
date: 2026-08-12
description: "A technical deep-dive into AWS IAM best practices covering least privilege, SCPs, OIDC federation, Access Analyzer, and AI workload identity."
tags: ["aws-iam", "cloud-security", "identity-access-management", "least-privilege", "aws-organisations"]
slug: "aws-iam-best-practices"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2072
draft: false
---

# AWS IAM best practices: a practitioner's guide for 2026

Identity is the perimeter now. Not metaphorically. Almost every meaningful cloud breach traces back to misconfigured permissions or compromised credentials, not infrastructure-level vulnerabilities. If you are responsible for an AWS environment and you are not actively working through your IAM posture, this guide is for you. It covers the controls that matter in production, the trade-offs you will actually face, and two AWS capabilities from mid-2026 that are quietly changing how teams approach IAM governance for AI workloads and data platforms.

<!-- INTERNAL_LINK: cloud identity and access management overview | cloud-identity-and-access-management -->

---

## Why IAM discipline is non-negotiable in 2026

The AWS shared responsibility model places identity, configuration, and workload protection squarely on customers. Misconfiguration and permission creep drive most incidents, and that line in the shared responsibility model is also a regulatory one. From an FCA and GDPR perspective, if your IAM posture is weak, the regulator's view is that you failed, not AWS.

The NCSC's position is equally unambiguous. The NCSC's 14 Cloud Security Principles form the basis of UK cloud security guidance and help organisations assess whether cloud services meet their security requirements. Principle 9, Identity and Authentication, maps directly to your IAM configuration choices.

The CIS AWS Foundations Benchmark v3.0.0 covers 60+ security controls across IAM, storage, logging, monitoring, and networking. AWS Security Hub now also supports the CIS AWS Foundations Benchmark v5.0, which includes 40 controls performing automated checks against AWS resources.

Between the NCSC principles, the CIS benchmark, and AWS's own security documentation, there is no shortage of authoritative guidance. The problem is consistent execution at scale.

---

## Least privilege: the foundation you keep skipping

Least privilege is the most cited, least implemented control in AWS environments. Every team agrees with it in principle; almost no team enforces it rigorously in practice.

The practical approach I recommend for teams at scale is to start with IAM Access Analyzer. It identifies unused access across your organisation and accounts, validates IAM policies against policy grammar and AWS best practices, and can generate IAM policies based on actual access activity recorded in CloudTrail logs. That last capability matters: you can replace over-broad policies with ones derived from real usage rather than guesswork.

That said, be clear-eyed about what the tool does and does not do. Access Analyzer surfaces unused roles, keys, passwords, and permissions. It does not remove them. Remediation still falls to your security team, and that gap between detection and action is where most organisations stall. You need a human, or an automation with real teeth, to act on the findings.

### Separation of duties

Critical actions should not be controlled by a single identity. The person deploying infrastructure should not be the same person approving security policies. In AWS terms, that means distinct roles for pipeline execution, security administration, and break-glass access. A single `DevOps` role with `AdministratorAccess` doing all three is a risk, not a convenience.

<!-- INTERNAL_LINK: devsecops shift-left security and IAM policy validation | devsecops-shift-left-security -->

---

## Roles over users: no exceptions

Long-lived IAM user credentials are a liability. The rule in 2026 is straightforward: if it is a workload on AWS, use an instance, task, or execution role. If it is CI/CD, use OIDC federation. IAM users exist only for the small number of cases where neither option is possible.

### OIDC federation for CI/CD

OIDC federation lets external identity providers such as GitHub Actions, GitLab CI, or CircleCI exchange short-lived OIDC tokens for temporary AWS credentials. This eliminates the need to store `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as secrets in your CI/CD system. It also gives you better auditability and fine-grained access control. This is not a nice-to-have for production pipelines.

The trust policy below scopes an OIDC role so that only your specific repository's `main` branch can assume it:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:my-org/my-repo:ref:refs/heads/main"
        }
      }
    }
  ]
}
```

Define trust policies to allow role assumption only from specific repositories and branches. This ensures only approved workflows can authenticate with AWS. Create separate IAM roles for development, staging, and production environments, each with different trust policies and permissions. Your production role might trust only the `main` branch, while development roles trust feature branches.

---

## Service control policies: your organisational guardrails

SCPs are the most powerful preventive control available in multi-account AWS environments, and most organisations underuse them. Applied at the organisation root or to specific Organisational Units, they define a permission boundary for every IAM principal in an account. An explicit `Deny` in an SCP overrides any `Allow` in an IAM policy, making them the backstop for enforcing compliance and security baselines.

In September 2025, AWS Organisations extended SCPs with full IAM policy language support, adding `Conditions`, individual resource ARNs, and `NotAction` to Allow statements as well as Deny. That opens up controls that were previously awkward to implement: restricting access to specific AWS regions, preventing deletion of shared administrative roles, and defining exceptions for specific administrator roles while restricting everyone else.

A useful companion to SCPs is the Resource Control Policy type, a distinct AWS Organisations policy introduced by AWS in November 2024. RCPs handle resource-side governance that SCPs cannot fully address; coverage is limited to a specific and expanding list of AWS services, which at launch included S3, STS, KMS, Secrets Manager, and SQS. An RCP can enforce that an S3 bucket may only be accessed by principals from within your organisation, regardless of how the bucket's own resource policy is configured. SCPs cannot enforce that boundary on the resource itself because they only act on principals.

The following SCP denies root account usage across all member accounts. It is a baseline every AWS Organisation should have in place:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyRootAccountUsage",
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

The root user bypasses all IAM policies and has unrestricted access to all resources, billing information, and account closure. This SCP prevents accidental or malicious use of root credentials and enforces the use of IAM roles with proper audit trails and scoped permissions.

<!-- INTERNAL_LINK: AWS Well-Architected Security pillar and multi-account governance | aws-well-architected-security -->

---

## IAM and AI workloads: a new governance dimension

As Bedrock usage scales across enterprise AWS estates, a new IAM governance challenge emerges: how do you attribute and control AI inference costs and access by identity?

Until recently, answering "which team or application is driving Bedrock spend?" required manual reconciliation, correlating CloudTrail logs with billing data to map API calls back to specific identities. That process is slow, error-prone, and difficult to maintain at scale.

Amazon Bedrock now supports cost allocation by IAM principal, covering IAM users and IAM roles, in AWS Cost and Usage Report 2.0 and Cost Explorer. You can tag IAM users and roles with attributes such as team, project, or cost centre, activate them as cost allocation tags, and analyse Bedrock model inference costs by those tags in Cost Explorer or at line-item level in CUR 2.0. IAM principal tags appear in billing with the `iamPrincipal/` prefix to avoid collision with resource tags.

The security implication is as significant as the FinOps one. You now have a native, attribution-grade audit trail linking every Bedrock inference call to a specific IAM identity, without custom logging pipelines. Pair this with IAM Access Analyzer and GuardDuty to detect over-privileged AI service roles. That risk is growing. According to Teleport's 2026 Infrastructure Identity Survey, 70% of organisations grant AI systems more access than they would give a human employee performing the same job.

<!-- INTERNAL_LINK: securing AI agents on cloud infrastructure | securing-ai-agents-cloud-infrastructure -->

Also worth noting for data platform teams: when working in the AWS Glue console, you now have one-click access to open SageMaker Unified Studio using the same IAM role. For Glue console customers who have not yet set up SageMaker Unified Studio, a new inline permissions panel helps you create and configure the required IAM policies directly within the setup workflow. Convenient, but review those inline-generated policies carefully. Inline policy generation tools produce permissive starting points; they do not enforce least privilege on your behalf.

<!-- INTERNAL_LINK: AWS KMS key management best practices | aws-kms-key-management-best-practices -->

---

## Common IAM pitfalls in production environments

I see these mistakes repeatedly across client environments. They are all easy to fall into.

1. Wildcard actions on broad resources. The pattern `"Action": "*"` combined with `"Resource": "*"` is equivalent to `AdministratorAccess` and frequently appears in developer-created inline policies that never get reviewed. Enforce custom policy checks in your CI/CD pipeline using IAM Access Analyzer's policy validation APIs.

2. Inline policies that escape governance. Managed policies are visible, versioned, and auditable. Inline policies are none of those things at scale. Make managed policies the organisational standard and use SCPs to detect or prevent inline policy attachment where necessary.

3. CI/CD roles with `AdministratorAccess`. If your workflow credentials are ever compromised, a custom policy scoped to a specific bucket means an attacker can only affect that bucket, not every S3 bucket in your account. Never attach `AdministratorAccess` to a CI/CD role.

4. Forgetting the `sts:AssumeRole` chain. When Role A assumes Role B which assumes Role C, the effective permissions and trust chain become difficult to reason about. IAM Access Analyzer helps you identify resources shared with external entities and unintended cross-account access. Use it to audit complex role chains.

5. Not enforcing MFA for destructive actions. The NCSC recommends phishing-resistant MFA, specifically FIDO2 security keys or passkeys, for administrative access. A condition block requiring `aws:MultiFactorAuthPresent: "true"` on destructive IAM and billing actions is a low-effort, high-value control. The CIS AWS Foundations Benchmark is explicit on this: MFA for all IAM users with console access, and no credentials unused for 45 or more days.

6. Treating IAM as a one-time setup. Unused roles accumulate. Developers join and leave teams. Services get decommissioned but their roles linger. Schedule quarterly IAM Access Analyzer reviews and act on the findings rather than letting them pile up.

<!-- INTERNAL_LINK: cloud threat detection and monitoring | cloud-threat-detection -->

---

## Operationalising IAM: shift left and automate

IAM policy checks can run directly inside DevOps pipelines, scanning Terraform plans, GitHub and GitLab changes, and policy JSON before deployment. Unsafe permissions get blocked early, before they reach production.

The toolchain for this is mature. AWS CloudFormation Guard, `cfn-policy-validator`, and IAM Access Analyzer's policy validation API can all run in a pre-merge check. If a policy contains `"Effect": "Allow"` with `"Resource": "*"` and no conditions, fail the pipeline. This is not theoretical. Several UK financial services firms I have worked with have eliminated the most common IAM misconfiguration patterns from reaching production using exactly this approach.

For ongoing monitoring, your security teams can automate notification workflows to help development teams identify and remove unused access by integrating with Amazon EventBridge. An integration with AWS Security Hub provides an aggregated view of external and unused access findings alongside your other security findings.

<!-- INTERNAL_LINK: devsecops and shift-left security practices | devsecops-shift-left-security -->

---

## Key takeaways

- Roles always, users rarely. Every workload should authenticate via an IAM role. Every CI/CD system should use OIDC federation. Long-lived access keys are a liability, not a convenience.

- SCPs are your backstop. Even the most permissive account-level IAM policies cannot bypass an SCP `Deny`. Build a baseline SCP layer covering root account denial, region restriction, and CloudTrail protection, and apply it organisation-wide from day one.

- Access Analyzer is a visibility tool, not an enforcement mechanism. It tells you where the problems are; you still need process and automation to act on findings. Build the remediation loop, not just the detection.

- Tag IAM principals for AI cost and access governance. With Bedrock's IAM principal cost allocation now live in CUR 2.0, tagging roles with `team`, `cost-centre`, and `environment` gives you both a FinOps dashboard and an audit trail linking inference activity to specific identities.

- Align to CIS and NCSC baselines from the start. The CIS AWS Foundations Benchmark v5.0 is now supported in AWS Security Hub. Enable it, resolve the IAM-related findings first, and treat it as a continuous compliance gate rather than a one-time audit.

- Inline-generated IAM policies need manual review. Whether from the AWS Console, SageMaker Unified Studio's Glue integration, or any other helper tool, generated policies are permissive starting points. Review, scope down, and version-control them before they reach production.

<!-- INTERNAL_LINK: cloud compliance frameworks overview | cloud-compliance-frameworks -->
<!-- INTERNAL_LINK: PCI DSS on AWS compliance guide | pci-dss-aws-compliance-guide -->
<!-- INTERNAL_LINK: cloud incident response planning | cloud-incident-response -->