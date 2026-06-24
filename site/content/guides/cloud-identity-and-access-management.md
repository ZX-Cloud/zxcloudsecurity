+++
title = "Cloud Identity and Access Management: The Architect's Guide"
date = "2026-06-24T06:00:00Z"
slug = "cloud-identity-and-access-management"
description = "Cloud IAM explained for security architects: principals, policies, federation, least privilege, PAM, and the identity controls that prevent the majority of cloud breaches."
keywords = ["cloud IAM", "identity and access management", "cloud security", "least privilege", "IAM federation", "cloud identity", "privilege management", "zero standing privilege"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

Identity is the new perimeter. That phrase has been repeated so often it risks becoming meaningless — but in cloud environments it is structurally true in a way it never was in the data centre era. There is no network boundary to cross, no physical server room to enter. The only thing standing between an attacker and your cloud resources is whether they can obtain and use valid credentials. Cloud identity and access management is therefore not a supporting discipline within cloud security; it is the foundation on which everything else rests.

This guide covers what cloud IAM actually is, why it differs from traditional access control, the principal threat patterns it must defend against, and the architectural controls that make a cloud IAM programme resilient rather than brittle.

---

## What Cloud IAM Is — and How It Differs from Traditional Access Control

In a traditional enterprise environment, identity infrastructure was built around Active Directory or LDAP: users authenticated to a directory, received Kerberos tickets or NTLM tokens, and accessed network resources within a well-defined perimeter. The assumption was that the network itself provided a trust boundary.

Cloud IAM works differently. Every interaction with a cloud platform — provisioning a resource, reading a secret, invoking a function, storing an object — is an authenticated API call. The cloud provider acts as both the identity provider and the policy enforcement point. There is no network boundary; authentication is the boundary.

The practical consequence is that IAM mistakes that would have been partially mitigated by network segmentation in a data centre become directly exploitable in cloud. An overpermissive IAM role in AWS, Azure, or GCP is an externally accessible vulnerability, not merely an internal policy gap.

---

## Core IAM Concepts

Understanding cloud IAM requires familiarity with a small number of foundational concepts that apply across AWS, Azure, and GCP, even where the terminology differs.

**Principals** are the entities that can make API calls and be granted permissions. In AWS, principals are IAM users, IAM roles, AWS services, and federated identities. In Azure, principals are users, groups, service principals, and managed identities. In GCP, principals are Google accounts, service accounts, groups, and domains. The most important architectural decision is which principal types you allow: IAM users with long-term access keys (high risk, should be eliminated for human access), roles assumed via federation (preferred for humans), or service accounts and managed identities (preferred for workloads).

**Policies** define what a principal is allowed or denied to do. In AWS, policies are JSON documents attached to principals or resources that specify `Effect`, `Action`, `Resource`, and optional `Condition` elements. In Azure, role definitions are assigned at a scope (management group, subscription, resource group, or resource). In GCP, IAM bindings attach roles — collections of permissions — to principals at the resource hierarchy level.

**Federation** is the mechanism by which external identity providers (your corporate IdP, Okta, Entra ID) are trusted by the cloud platform to assert user identities. Federation eliminates long-term cloud-native credentials for human users: engineers authenticate to your IdP and receive short-lived cloud credentials through SAML 2.0, OIDC, or platform-specific mechanisms. AWS IAM Identity Centre, Azure Entra ID, and GCP Workforce Identity Federation provide this capability.

**Roles and service identities** are the mechanism by which workloads (EC2 instances, Lambda functions, containers, Kubernetes pods) authenticate to cloud APIs without long-term credentials. An EC2 instance assumes an IAM role; a GKE pod uses Workload Identity. These short-lived, automatically rotated credentials are the correct model for all non-human access.

---

## The Cloud IAM Attack Surface

The dominant patterns in cloud security incidents all trace back to IAM failures:

**Credential exposure** remains the most common initial access vector. Access keys committed to public GitHub repositories, hardcoded in application code, leaked through misconfigured logging, or extracted from instance metadata endpoints have initiated the majority of significant cloud breaches in recent years. The 2023 Codecov breach, the CircleCI incident, and countless smaller incidents follow this pattern.

**Overprivileged roles and principals** transform initial access into catastrophic compromise. An attacker who obtains credentials for a principal with `AdministratorAccess` or equivalent has unrestricted access to the environment. The damage radius of credential theft is bounded by the permissions attached to the compromised principal — which is why least privilege is not just a best practice but a direct control on breach impact.

**Privilege escalation via IAM** is a well-documented attack pattern. Certain IAM permissions — `iam:CreatePolicyVersion`, `iam:AttachUserPolicy`, `iam:PassRole` combined with service creation, `sts:AssumeRole` — allow a low-privilege attacker to elevate to a higher-privilege principal if those permissions are carelessly granted. The Rhino Security Labs privilege escalation paths document over twenty distinct escalation vectors in AWS IAM alone.

**Lateral movement via role chaining** is specific to multi-account cloud environments. An attacker who compromises a principal in Account A may be able to assume a role in Account B if a cross-account trust relationship exists. Without centralised detection across all accounts, this movement is invisible to account-level monitoring.

**Persistence through IAM modification** — creating new access keys, adding new IAM users, modifying trust policies, creating new service principals — is the mechanism by which attackers who gain temporary access convert it into durable access.

---

## The Core IAM Controls

### Eliminate Long-Term Credentials for Humans

IAM users with access keys are the single highest-risk primitive in cloud IAM. Access keys do not expire, can be shared, and are frequently mishandled. The correct model for human access is federation: engineers authenticate to a corporate IdP, receive short-lived cloud credentials (12 hours maximum), and re-authenticate for each session. AWS IAM Identity Centre, Azure Entra ID B2B, and GCP Workforce Identity Federation all provide this capability.

If long-term access keys cannot be immediately eliminated, enforce rotation, require MFA, apply IP-based conditions, and continuously monitor for keys that have not been used in 90 days via AWS IAM Access Analyzer, Azure Entra ID access reviews, or equivalent tooling.

### Apply Least Privilege Relentlessly

Least privilege means granting the minimum permissions required for a principal to perform its function — not `*` on `*` because it is convenient, not a broad managed policy because the specific permissions are unknown. In practice, this requires:

- Starting from zero permissions and adding what is needed, not starting from broad access and trying to trim
- Using IAM Access Analyzer policy generation to derive policies from actual CloudTrail activity for existing roles
- Applying conditions — `aws:SourceIp`, `aws:RequestedRegion`, `aws:MultiFactorAuthPresent` — to constrain where and how permissions can be exercised
- Reviewing and ratcheting down permissions quarterly, removing unused permissions identified through access analysis

### Use Roles and Managed Identities for Workloads

No application, Lambda function, container, or automation script should use long-term access keys. AWS IAM roles (assumed via instance profiles, Lambda execution roles, or EKS service accounts with IRSA), Azure Managed Identities, and GCP service accounts with Workload Identity provide short-lived, automatically rotated credentials with no secret management overhead. The metadata endpoint (`169.254.169.254` on AWS) provides credentials to workloads automatically — no key distribution required.

### Enforce MFA on Every Privileged Action

For any access that reaches a cloud console or performs sensitive API actions, MFA should be mandatory. For AWS IAM users that cannot be immediately eliminated, enforce MFA using `aws:MultiFactorAuthPresent` conditions on sensitive actions. For federated access via an IdP, enforce MFA at the IdP level and ensure the cloud platform trusts only MFA-authenticated sessions.

### Apply Preventive Controls at the Organisation Layer

In AWS, Service Control Policies (SCPs) attached to the organisation's root or OUs establish the maximum permissions available to any principal in any account — they cannot be overridden by even an administrator within the account. Essential SCPs: deny leaving the organisation, restrict API calls to approved regions, protect security services from disablement (CloudTrail, GuardDuty, Security Hub), require encryption at rest.

Azure Management Group policies and GCP Organisation Policy Constraints serve equivalent roles. These organisation-layer controls are the backstop that limits the blast radius of a compromised account administrator.

### Instrument the IAM Surface for Detection

IAM configuration changes — policy modifications, new trust relationships, access key creation, new role attachments — should generate near-real-time alerts. CloudTrail logs every IAM API call; route these to a centralised SIEM or detection platform and alert on: new IAM users created, access keys created for existing users, `iam:CreateLoginProfile` (grants console access), `sts:AssumeRole` with novel cross-account destinations, and any SCP modification.

---

## Privileged Access Management in Cloud

Privileged access — the ability to make infrastructure-level changes, access sensitive data, or modify security controls — requires additional controls beyond standard IAM:

**Zero standing privilege** means that no principal holds persistent administrator access. Engineers request elevated access for a specific task, receive time-limited credentials, and the access expires automatically. AWS TEAM (Temporary Elevated Access Management), Azure Privileged Identity Management (PIM), and GCP's IAM Recommender with custom just-in-time workflows implement this pattern.

**Break-glass accounts** provide emergency access when the normal federation path is unavailable. These accounts should be tightly constrained (specific IP ranges, hardware MFA only), monitored in near-real-time (any usage generates an immediate alert), and audited after every use. The credentials should be stored out-of-band (sealed envelope in a physical safe, or a separate secret management system inaccessible to the cloud automation that manages normal credentials).

---

## What Architects Should Do

- **Eliminate long-term access keys for human access** — this is the single highest-impact IAM improvement available in most AWS environments; federation via IAM Identity Centre or Entra ID should be the default
- **Audit and right-size every IAM role** — use AWS IAM Access Analyzer, Azure Access Reviews, or GCP Policy Insights to identify unused permissions and remove them
- **Apply SCPs or equivalent organisation-policy controls** to every account or subscription from day one — retrofitting preventive controls is far harder than including them in landing zone design
- **Instrument IAM changes for detection** — every IAM modification should be logged, centralised, and alertable; configuration changes that disable logging should themselves be highest-priority alerts
- **Implement zero standing privilege for all privileged access** — if your engineers have permanent administrator access, your blast radius from any credential compromise is unlimited

---

## Key Takeaways

- **Cloud IAM is the security perimeter** — there is no network boundary; the authentication and authorisation layer is the only control between an attacker and your resources
- **Credential exposure is the dominant initial access vector** — eliminate long-term access keys for humans, use federation and short-lived credentials
- **Least privilege limits blast radius** — overprivileged roles convert credential theft into catastrophic compromise; tight permissions convert it into limited damage
- **Organisation-layer preventive controls are the backstop** — SCPs and equivalent organisation policies protect against compromised account administrators
- **IAM changes must be detectable in near-real-time** — privilege escalation, lateral movement, and persistence all leave IAM traces; detection depends on monitoring them

---

## Related Guides

- [AWS IAM Security Best Practices](/guides/aws-iam-security-best-practices/) — Detailed implementation guidance for AWS IAM: least privilege design, SCPs, permission boundaries, and access analysis.
- [AWS IAM Identity Centre: A Practitioner's Guide](/guides/aws-iam-identity-centre-guide/) — Centralised workforce federation, permission sets, SCIM provisioning, and common pitfalls.
- [Privileged Access Management in AWS](/guides/privileged-access-management-in-aws/) — JIT access, zero standing privilege, break-glass controls, and AWS TEAM implementation.
- [What is CIEM?](/guides/what-is-ciem-cloud-infrastructure-entitlement-management/) — Discovering and governing the entitlement sprawl that standard IAM reviews miss.
- [Zero Trust Architecture](/guides/what-is-zero-trust-architecture/) — IAM is the identity enforcement layer that makes Zero Trust operational in cloud environments.
- [Cloud Threat Detection](/guides/cloud-threat-detection/) — How IAM attack patterns — credential theft, privilege escalation, lateral movement — appear in CloudTrail and how to detect them.
