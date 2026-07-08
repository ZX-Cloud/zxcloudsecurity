---
title: "AWS Secrets Manager Best Practices: A Practitioner's Guide"
date: 2026-07-08
description: "A practical guide to AWS Secrets Manager best practices covering encryption, rotation, IAM access control, VPC endpoints, monitoring, and common pitfalls."
tags: ["aws-secrets-manager", "secrets-management", "aws-security", "iam", "credential-rotation"]
slug: "aws-secrets-manager-best-practices"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2425
draft: false
---

# AWS Secrets Manager best practices: stop treating secrets as an afterthought

Stolen credentials remain the single most common initial access vector in cloud breaches. If your organisation stores database passwords in environment variables, commits API keys to Git, or rotates secrets manually on a quarterly basis, you are already behind. For FCA-regulated firms, organisations in scope for UK GDPR, and any enterprise running production workloads on AWS, proper secrets management is a baseline expectation, not optional hygiene. This guide covers what production-grade secrets management actually looks like: encryption choices, access control, automatic rotation, network hardening, monitoring, and the mistakes I see repeatedly in client environments.

> A note on CVE references: The two CVEs originally cited in the brief for this guide (CVE-2026-43867 and CVE-2026-46590) do not appear as published, indexed entries in the National Vulnerability Database at the time of writing. Rather than invent vulnerability details, I have grounded the threat context in verified, current sources. Always check the [NVD](https://nvd.nist.gov/) directly for emerging Secrets Manager-adjacent CVEs.

<!-- INTERNAL_LINK: recent cloud security CVEs roundup | recent-cloud-security-cves -->

---

## Why secrets management still goes wrong

The 2025 Verizon DBIR confirmed that stolen credentials remain the top initial access vector. A leaked secret on GitHub can be discovered and exploited within minutes of the commit landing.

Hardcoded secrets in source code, environment variables, and configuration files are the root cause of most credential leaks. Secrets committed to Git are indexed by automated scanners within seconds. Environment variables are accessible to any process running on the same host and are routinely captured by monitoring tools.

The NCSC is direct on this point: poorly secured secrets increase the likelihood of credential theft, particularly when secrets are stored in multiple places, making auditing difficult. That problem has a name: secrets sprawl.

Secrets Manager eliminates the need to store credentials in code, environment variables, or configuration files. It integrates natively with RDS, Redshift, and DocumentDB for automatic rotation, and supports custom rotation via Lambda for any other secret type. Combined with KMS encryption, resource policies, and VPC endpoints, it gives you a defence-in-depth approach to credential management.

<!-- INTERNAL_LINK: IAM security best practices | aws-iam-security-best-practices -->

---

## Encryption: choose your KMS key deliberately

Secrets Manager encrypts secrets at rest using keys you own and store in AWS KMS. When you retrieve a secret, Secrets Manager decrypts it and transmits it to your local environment over TLS.

AWS gives you two encryption paths. The `aws/secretsmanager` AWS managed key costs nothing and works for most use cases. A customer managed key (CMK) is required if you need cross-account access or want direct control over the key policy.

My recommendation for financial services clients is to use a CMK in every production account. It gives you key policy control, cross-account access scoping, and a clear audit trail for key usage, all of which matter for PCI DSS and FCA operational resilience obligations.

In the key policy, assign `secretsmanager.<region>.amazonaws.com` to the `kms:ViaService` condition key. This restricts the key to requests originating from Secrets Manager, nothing else.

There is also a forward-looking consideration worth flagging. Secrets Manager supports TLS 1.3 with hybrid post-quantum key exchange for clients that support it. The hybrid approach combines traditional cryptography (X25519) with post-quantum algorithms (ML-KEM), protecting secrets against both current classical attacks and future quantum threats. If your organisation is working through a post-quantum cryptography migration (which UK government bodies now need to plan for), updating your Secrets Manager client SDKs to support this is a low-effort, worthwhile step.

---

## Automatic rotation: the most underused feature

Credentials that never change are credentials that will eventually be compromised. Secrets Manager supports automatic rotation as frequently as every four hours. It offers two rotation strategies: single user and alternating users.

The alternating-users strategy is the safer choice for production databases. It creates a cloned user, updates the password, and only deprecates the previous version after confirming the new credentials work. Turn on rotation wherever the downstream system supports it. A rotated credential is a time-bound credential. Use alternating-users rotation for anything that cannot tolerate a connection interruption during switchover.

The NCSC is explicit on this: the lifetime of a credential should match the use case and threat model, rotation should be automated, and no human should be involved in the rotation process itself.

For databases not natively supported by Secrets Manager, write a custom Lambda rotation function. Define a rotation period based on sensitivity, typically 30 to 60 days for standard database credentials, with more frequent rotation for admin credentials.

One practical note: before enabling rotation in production, validate the configuration in a staging environment and confirm that applications pick up refreshed credentials correctly. I have seen rotation break overnight batch jobs in two separate client environments because nobody tested the connection pooling behaviour first.

<!-- INTERNAL_LINK: AWS Well-Architected Security | aws-well-architected-security -->

---

## IAM access control: least privilege is not a slogan

Access to secrets operates across two policy layers. Identity-based IAM policies are attached to users and roles. Resource-based policies are attached directly to the secret itself, so a database credential can carry its own policy governing which identities can access it and how.

An application role should be able to call `secretsmanager:GetSecretValue` on the specific secrets it needs, and nothing more. Here is a working example of a least-privilege IAM policy for an application role that needs to read a single RDS credential:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowGetSpecificSecret",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "arn:aws:secretsmanager:eu-west-2:123456789012:secret:prod/payments/rds-credentials-*"
    },
    {
      "Sid": "AllowKMSDecrypt",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:GenerateDataKey"
      ],
      "Resource": "arn:aws:kms:eu-west-2:123456789012:key/mrk-abc123def456",
      "Condition": {
        "StringEquals": {
          "kms:ViaService": "secretsmanager.eu-west-2.amazonaws.com"
        }
      }
    }
  ]
}
```

The ARN uses a trailing wildcard to accommodate the random suffix Secrets Manager appends, but scopes to a specific path prefix rather than `*`. That is the right balance between precision and operational flexibility.

For `PutResourcePolicy` calls, AWS recommends setting `BlockPublicPolicy: true`. This means users can only attach a resource policy to a secret if the policy does not allow broad access. Secrets Manager uses Zelkova automated reasoning to analyse resource policies for overly permissive access.

At the organisational level, Resource Control Policies (RCPs) apply org-wide and constrain who can access resources in your accounts regardless of how permissive a resource policy is. This is particularly useful for Secrets Manager, where misconfigured resource policies have historically been responsible for the worst credential leaks.

<!-- INTERNAL_LINK: AWS IAM Identity Centre guide | aws-iam-identity-centre-guide -->
<!-- INTERNAL_LINK: what is CIEM | what-is-ciem-cloud-infrastructure-entitlement-management -->

---

## Network hardening: keep traffic off the public internet

By default, calls to the Secrets Manager API traverse the public internet. A VPC interface endpoint (powered by AWS PrivateLink) ensures that all Secrets Manager API traffic stays within the AWS network.

AWS recommends running as much infrastructure as possible on private networks, and Secrets Manager is no exception. Creating a VPC interface endpoint is straightforward:

```bash
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0abc123def456 \
  --service-name com.amazonaws.eu-west-2.secretsmanager \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-0aaa111bbb222 subnet-0ccc333ddd444 \
  --security-group-ids sg-0eee555fff666 \
  --private-dns-enabled
```

Once the endpoint is in place, enforce its use via a resource-based policy condition (`aws:SourceVpce`), so no Secrets Manager call from your workloads can succeed unless it arrives through the endpoint. This is a control I mandate on every financial services engagement. It removes an entire class of exfiltration path.

<!-- INTERNAL_LINK: Zero Trust Architecture | what-is-zero-trust-architecture -->

---

## Monitoring and auditing: every secret access must be visible

Every Secrets Manager API call is logged in CloudTrail. You get a record of who retrieved which secret, when, and from which IP address. That is both an operational tool and a compliance requirement under SOC 2 and PCI DSS.

The NCSC gives clear direction on what useful monitoring looks like: focus on anomalous activity, such as a human user accessing a secret normally retrieved by automation, or any single identity accessing many different secrets in a short window.

Translated into concrete AWS controls:

- A CloudWatch alarm on `GetSecretValue` calls from unexpected IAM principals
- An EventBridge rule triggering a Lambda or SNS notification when `DeleteSecret` or `PutResourcePolicy` is called outside your change management window
- The AWS Config rule `secretsmanager-rotation-enabled-check` to confirm rotation is active on all secrets
- Security Hub aggregating Config findings into your central security dashboard

Enable CloudTrail for all API activity, set CloudWatch alarms for unusual access patterns, and use AWS Config rules to enforce rotation and encryption key requirements. Integrate GuardDuty for threat detection. Automate compliance reporting to track access frequency, unused secrets, and lifecycle events across your environment.

<!-- INTERNAL_LINK: AWS CloudTrail configuration guide | aws-cloudtrail-configuration-best-practices -->
<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->

---

## Common pitfalls in AWS Secrets Manager deployments

After reviewing dozens of AWS environments for UK clients, these are the mistakes I encounter most often.

### 1. Granting `secretsmanager:*` on `*`

Overly broad permissions increase risk. Avoid wildcard actions or resources unless there is a documented reason. I regularly find Lambda execution roles with `secretsmanager:*` because it "just worked" during development and nobody tightened it before production.

### 2. Using IP condition keys on secrets

Be careful with `aws:SourceIp` condition keys in Secrets Manager policies. If you enable rotation via Lambda, that function calls Secrets Manager from AWS-internal address space, and requests will fail if IP conditions are applied. Use `aws:SourceVpce` instead.

### 3. Storing AWS IAM credentials as secrets

Use IAM roles for AWS credentials rather than storing them in Secrets Manager. Secrets Manager is for credentials your workloads cannot obtain via IAM role assumption: RDS passwords, third-party API keys, OAuth client secrets. AWS temporary credentials via STS are outside its remit.

### 4. Not testing rotation before enabling it

Production rotation failures are silent killers. An application that caches a database connection pool and never refreshes it will fail after the first rotation cycle. The AWS Workload Credentials Provider handles caching and credential refresh transparently across Lambda, ECS, EKS, and EC2, and is worth using as a standard pattern.

### 5. Ignoring the CLI history risk

Any secret value passed on the command line can land in your shell history and, in some configurations, in process listings or CloudTrail. For sensitive values, read from a file with `--secret-string file://creds.json` rather than typing inline, then clear the file afterwards. AWS flags this explicitly as a CLI risk.

### 6. Forgetting deletion recovery windows

When you delete a secret, AWS schedules removal with a minimum seven-day recovery window, during which the secret can be restored. Route deletion requests through a change management gate. Accidental deletion of a production database credential is recoverable only if you planned for it before it happened.

<!-- INTERNAL_LINK: cloud incident response | cloud-incident-response -->
<!-- INTERNAL_LINK: cloud security vulnerability management | cloud-security-vulnerability-management -->

---

## Secrets Manager in multi-region and Kubernetes environments

For UK financial services firms with disaster recovery requirements under FCA PS21/3 operational resilience rules, Secrets Manager supports multi-region replication. Replicate production secrets to your DR region as part of your standard deployment pipeline, not as a manual step you remember during an incident.

For Kubernetes workloads, the two patterns I recommend are the Secrets Store CSI Driver and the External Secrets Operator. The CSI Driver mounts secrets as files; the External Secrets Operator syncs them into Kubernetes Secrets. Both require proper IAM setup via IRSA, fine-grained permissions, and audit logging to confirm secrets are retrieved and rotated correctly.

<!-- INTERNAL_LINK: Kubernetes security best practices | kubernetes-security-best-practices -->

---

## Summary

- Eliminate hardcoded credentials now. Use Amazon CodeGuru Reviewer or tools like truffleHog to scan repositories, then migrate to `GetSecretValue` SDK calls. There is no defensible justification for a static credential in application code in 2026.
- Enable automatic rotation on every secret that supports it. Use the alternating-users strategy for production databases, and validate rotation behaviour in staging before enabling it on live workloads.
- Apply least privilege at both the IAM identity layer and the Secrets Manager resource policy layer. Scope `GetSecretValue` to specific secret ARNs, set `BlockPublicPolicy: true` on `PutResourcePolicy` calls, and consider RCPs in multi-account organisations.
- Deploy a VPC interface endpoint for Secrets Manager and enforce its use via policy conditions. Keeping API traffic off the public internet removes a material exfiltration risk and aligns with NCSC guidance on running workloads on private networks.
- Treat CloudTrail and CloudWatch as non-negotiable. Every secret access must be logged, anomalous patterns must trigger alerts, and your incident response runbook must include rotating and invalidating the secret as the first step when a potential exposure is detected.
- Use a customer managed KMS key in production accounts. It gives you policy control, cross-account access scoping, and a richer audit trail, all of which matter for UK GDPR, FCA rules, and PCI DSS obligations.

<!-- INTERNAL_LINK: AWS compliance and governance | aws-compliance-and-governance -->
<!-- INTERNAL_LINK: what is DSPM | what-is-dspm-data-security-posture-management -->