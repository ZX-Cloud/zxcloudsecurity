+++
title = "AWS Well-Architected Security: A Practitioner's Deep Dive"
date = "2026-06-24T06:00:00Z"
slug = "aws-well-architected-security"
description = "AWS Well-Architected Security Pillar explained for architects — all 11 security questions, service-level controls, high-risk findings, UK compliance alignment, and how to run a meaningful review."
keywords = ["AWS Well-Architected security", "Well-Architected Framework security pillar", "AWS security review", "AWS security best practices", "SEC pillar AWS", "AWS Well-Architected Tool", "cloud security architecture AWS"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

The AWS Well-Architected Security Pillar is a structured framework for evaluating and improving the security posture of workloads running on AWS. It defines eleven security questions — organised across seven best practice areas — that cover the full range of security decisions an architect must make: identity, detection, network protection, data security, incident response, and application security. A workload that answers all eleven questions with evidence-backed "yes" responses is, by definition, a well-secured workload.

The broader Well-Architected Framework has six pillars: Security, Operational Excellence, Reliability, Performance Efficiency, Cost Optimisation, and Sustainability. This guide ignores the other five. Security is not one concern among equals — it is the prerequisite for everything else. A performant, cost-optimised workload that leaks customer data or is compromised via an overprivileged IAM role is not well-architected. It is a liability.

---

## The Six Security Design Principles

Before the eleven questions, the Well-Architected Framework articulates six design principles that should govern how security decisions are made. These are not aspirational statements — they have direct implementation implications.

**Implement a strong identity foundation.** Centralise identity management. Eliminate long-term credentials. Enforce least privilege through every role and permission boundary. Identity is the primary attack surface in cloud; every other control depends on it being correct.

**Maintain traceability.** Every action taken in your AWS environment — every API call, every configuration change, every data access — should generate a log that is stored securely, immutable, and queryable. Incidents you cannot reconstruct are incidents you cannot learn from and cannot report accurately.

**Apply security at all layers.** Defence in depth means security controls at the network edge, the VPC, the subnet, the compute layer, the application layer, and the data layer. If an attacker bypasses one control, the next one should contain them. No single control should be load-bearing.

**Automate security best practices.** Security controls implemented manually are inconsistently applied and impossible to scale. Infrastructure as code, automated compliance checking, and event-driven remediation should replace manual configuration wherever possible.

**Protect data in transit and at rest.** Classify your data. Apply appropriate encryption to sensitive data at rest. Enforce TLS for all data in transit. Never treat provider-managed encryption as a substitute for customer-controlled key management where the sensitivity of the data demands it.

**Keep people away from data.** Reduce or eliminate the need for direct human access to production data. Automated processing, anonymisation for development environments, and break-glass procedures for emergency access are all expressions of this principle.

**Prepare for security events.** Incident response is not a process you design during an incident. Runbooks, escalation paths, evidence preservation procedures, and regulatory notification obligations should be documented, tested, and rehearsed before they are needed.

---

## The Seven Security Best Practice Areas

### 1. Security Foundations (SEC 1)

**The question:** How do you securely operate your workload?

Security foundations address the organisational and structural controls that underpin everything else: account structure, governance guardrails, incident escalation, and the mechanisms by which security standards are maintained across a multi-account environment.

**AWS Organizations and multi-account architecture** is not optional at anything beyond small scale. Separate accounts provide the strongest available blast radius control: a compromised set of credentials in one account cannot directly affect resources in another without an explicit cross-account trust relationship. The minimum viable separation is production, staging/test, and a shared services or security account. For regulated workloads, further segmentation by business unit, data classification, or regulatory scope is appropriate.

**Service Control Policies (SCPs)** attached at the organisational root or OU level establish the maximum permissions available to any principal in any account, regardless of what IAM policies within the account grant. Foundational SCPs every organisation should implement:

- Deny leaving the organisation
- Restrict API calls to approved regions only
- Require encryption on S3 objects
- Prevent disabling CloudTrail, GuardDuty, or Security Hub
- Deny creation of IAM users with console access (enforce federation)
- Require MFA for sensitive actions

**AWS Control Tower** provides the landing zone scaffolding — a pre-built multi-account structure with guardrails, logging accounts, and a security baseline — for organisations that want a structured starting point rather than building from scratch.

The Well-Architected review for SEC 1 focuses on whether you have threat modelling processes, whether you maintain a security contact per account (AWS sends critical security notifications to the account's security contact email — if it points to a distribution list no one reads, you will miss them), and whether you have defined and exercised incident escalation paths.

---

### 2. Identity and Access Management (SEC 2 and SEC 3)

**The questions:** How do you manage identities for people and machines? How do you manage permissions for people and machines?

IAM is where the majority of critical Well-Architected findings occur in practice. The two questions cover different failure modes: SEC 2 focuses on credential type and authentication strength; SEC 3 focuses on what those credentials are permitted to do.

**For human identities (SEC 2):**

The Well-Architected answer requires federation — no IAM users with long-term access keys for human access. Engineers should authenticate to a corporate IdP (Okta, Entra ID, JumpCloud) and receive short-lived AWS credentials through AWS IAM Identity Centre. The credentials should expire within 8–12 hours, requiring re-authentication. MFA must be enforced at the IdP level.

If IAM users with long-term keys exist in your environment — for legacy tooling, third-party integrations, or CI/CD systems that have not been migrated — this is a high-risk finding in Well-Architected terms. Each key represents a persistent credential that does not expire, can be shared, is frequently committed to source control, and provides access until explicitly revoked.

**For machine identities (SEC 2):**

EC2 instances, Lambda functions, ECS tasks, and EKS pods should authenticate using IAM roles, not access keys. IAM roles attached to compute resources generate short-lived credentials automatically via the instance metadata service (IMDS). Enforcing IMDSv2 (token-required metadata access) closes the SSRF-to-IMDS credential theft vector that was the mechanism of the 2019 Capital One breach — an IMDSv1 endpoint exposed credentials that a misconfigured WAF allowed to be read remotely.

**For permissions (SEC 3):**

Least privilege is the standard, but the Well-Architected review pushes further than most organisations go. The high-risk questions are:

- Do any principals have `AdministratorAccess` or `*:*` policies outside break-glass accounts?
- Do any machine identities (roles, service accounts) have permissions they have not used in the last 90 days?
- Are permission boundaries applied to prevent privilege escalation?
- Are resource-based policies (S3 bucket policies, KMS key policies, Lambda resource policies) reviewed regularly?

AWS IAM Access Analyzer generates least-privilege policies based on actual CloudTrail activity, making the transition from broad policies to right-sized policies operationally feasible. Use it.

---

### 3. Detection (SEC 4)

**The question:** How do you detect and investigate security events?

Detection asks whether you can see attacks when they happen and reconstruct them when they have already happened. The Well-Architected answer requires logging at sufficient breadth and depth, detection tooling processing those logs, and alerting that reaches the right people in time to respond.

**CloudTrail** is non-negotiable. Enable an organisation-wide trail logging management events (all API calls) and data events for high-sensitivity resources (S3 buckets containing sensitive data, KMS key usage). Store logs in a centralised S3 bucket in a dedicated log archive account with Object Lock enabled — this prevents both accidental deletion and deliberate log tampering by an attacker who has compromised the workload account. Validate log integrity using CloudTrail digest files.

**Amazon GuardDuty** analyses CloudTrail, VPC Flow Logs, DNS logs, and S3 data events to detect known-bad patterns: malicious IP communication, DNS-based C2, port scanning, unusual API call patterns (EC2 crypto-mining, S3 exfiltration), and compromised IAM credential usage. It is the best-value detection investment available in AWS — the signal-to-noise ratio is high and the findings map directly to actionable responses. Enable it in every account in your organisation.

**AWS Security Hub** aggregates findings from GuardDuty, Inspector, Macie, and AWS Config across accounts, applies security standards (the Foundational Security Best Practices standard maps closely to Well-Architected requirements), and provides a cross-account view of security posture. For Well-Architected compliance, Security Hub's FSBP standard is a direct operationalisation of the Security Pillar controls.

**AWS Config** records every resource configuration change, enabling you to query the historical state of your environment: who made this change, when, from where, and what was the configuration before and after. Config Rules continuously evaluate resource configurations against your security baseline, generating findings when drift occurs.

The high-risk Well-Architected finding for SEC 4 is an environment where CloudTrail is not enabled in all regions, GuardDuty is disabled, and there is no alerting on IAM changes. This describes an environment that cannot detect, reconstruct, or respond to a compromise.

---

### 4. Infrastructure Protection (SEC 5 and SEC 6)

**The questions:** How do you protect your network resources? How do you protect your compute resources?

**Network protection (SEC 5):**

The Well-Architected baseline for network security requires:

- VPC architecture with public and private subnets — compute in private subnets, internet-facing load balancers in public subnets
- Security groups with least-privilege ingress rules — no `0.0.0.0/0` inbound rules on compute resources
- Network ACLs as a second layer of subnet-level control
- VPC endpoints for AWS service access, eliminating public internet traversal for S3, DynamoDB, SSM, and other services
- AWS WAF on internet-facing endpoints (CloudFront, ALB, API Gateway) with managed rule groups enabled

AWS Network Firewall provides stateful packet inspection for traffic flows that security groups alone cannot address — east-west traffic between subnets, DNS filtering, or deep packet inspection requirements. For workloads with regulatory requirements around network monitoring (PCI DSS, UK GDPR), Network Firewall's flow logs provide the evidence of traffic inspection that auditors expect.

**Compute protection (SEC 6):**

Compute protection addresses the host layer — what is running on your EC2 instances, containers, and serverless functions, and how is it kept secure.

**Amazon Inspector** provides continuous vulnerability assessment for EC2 instances, ECR container images, and Lambda function code — generating CVE-matched findings with EPSS-enriched prioritisation. Inspector findings integrate with Security Hub for centralised triage.

**AWS Systems Manager Patch Manager** automates OS and application patching across EC2 instances. A Well-Architected workload has no unpatched critical CVEs on production instances. Systems Manager Session Manager eliminates the need for open SSH/RDP ports — engineers access instances through a fully audited browser-based shell with no inbound security group rules required.

**EC2 Image Builder** enforces hardened AMI baselines. Rather than patching running instances indefinitely, Image Builder pipelines produce new hardened AMIs on a defined cadence. Instances are replaced rather than patched in place, ensuring configuration drift cannot accumulate.

---

### 5. Data Protection (SEC 7, SEC 8, and SEC 9)

**The questions:** How do you classify your data? How do you protect your data at rest? How do you protect your data in transit?

Data protection questions probe whether you know what data you have (classification), whether it is stored securely (encryption at rest), and whether it is transmitted securely (encryption in transit).

**Data classification (SEC 7):**

You cannot protect data you have not classified. The Well-Architected approach requires a defined classification scheme (at minimum: public, internal, confidential, restricted) applied to all data stores, with controls matched to classification level. **Amazon Macie** automates sensitive data discovery in S3 — identifying buckets containing PII, financial data, credentials, and other sensitive content that should be classified confidential or restricted. Macie findings feed into Security Hub and trigger remediation workflows.

**Encryption at rest (SEC 8):**

All sensitive data at rest should be encrypted with customer-managed keys (CMKs) in AWS KMS. This includes S3 objects, EBS volumes, RDS databases, DynamoDB tables, Secrets Manager secrets, and any other persistent data store. Provider-managed encryption (SSE-S3, default RDS encryption) provides protection against physical media theft but does not give you key control, key audit trails, or the ability to revoke access by disabling a key — all of which regulated workloads typically require.

KMS key policies should enforce separation of duties: the AWS account root user can manage keys but not use them for cryptographic operations; application roles can use keys but cannot modify key policies; a dedicated key administrator role manages key lifecycle. CloudTrail logs every KMS API call — `kms:Decrypt`, `kms:GenerateDataKey`, `kms:DescribeKey` — providing a complete audit trail of who accessed what, when.

**Encryption in transit (SEC 9):**

All data in transit should be encrypted. TLS 1.2 minimum, TLS 1.3 preferred. This is enforced at the load balancer level via ALB/NLB SSL policies (prefer `ELBSecurityPolicy-TLS13-1-2-2021-06`), at the CloudFront level (require HTTPS, minimum TLS version), and at the application level for service-to-service communication. ACM manages public certificate provisioning and renewal automatically. Verify no legacy services are serving HTTP — the Well-Architected review flags any ALB or CloudFront distribution serving unencrypted traffic.

---

### 6. Incident Response (SEC 10)

**The question:** How do you anticipate, respond to, and recover from incidents?

Incident response in AWS requires preparation long before an incident occurs: documented runbooks, pre-provisioned response tooling, tested escalation paths, and clear understanding of regulatory notification obligations.

**Pre-incident preparation:**

- Define an AWS Security Incident Response role with permissions to isolate compromised resources (detach IAM roles, modify security groups, take EBS snapshots) without granting broader administrative access
- Maintain a "clean room" account — a separate AWS account used for forensic analysis, isolated from the incident environment, with pre-installed tooling
- Store runbooks in a location accessible even if your primary AWS environment is compromised (external document store, not an S3 bucket in the affected account)
- Test the response process with tabletop exercises and, ideally, red team exercises that create realistic incidents

**AWS-native response tooling:**

- **Amazon Detective** correlates GuardDuty findings, CloudTrail logs, and VPC Flow Logs into an interactive investigation graph. For an alert indicating compromised credentials, Detective visualises every API call made by that principal, the resources affected, and the network traffic associated with those calls — reducing investigation time from hours to minutes.
- **AWS Security Lake** centralises security logs from multiple accounts and sources into a normalised OCSF (Open Cybersecurity Schema Framework) format, queryable by Athena or a third-party SIEM. For large organisations, Security Lake is the foundation of a scalable detection and response programme.
- **EBS volume snapshots** preserve the state of compromised instances for forensic analysis without affecting the running environment.

**Regulatory considerations for UK architects:**

UK GDPR requires notification to the ICO within 72 hours of becoming aware of a personal data breach. This clock starts when you have sufficient information to conclude a breach has likely occurred — not when the investigation is complete. This means your incident response runbook must include a decision point: "Is personal data likely involved? If yes, start the 72-hour clock and notify the DPO now." FCA-regulated firms have parallel notification obligations under the FCA's operational resilience framework and DORA (for those in scope). The Well-Architected review asks whether notification obligations are documented and the responsible person is identified. If the answer is "we'd figure it out during the incident," that is a high-risk finding.

---

### 7. Application Security (SEC 11)

**The question:** How do you incorporate and validate the security properties of applications throughout the design, development, and deployment lifecycle?

Application security asks whether security is built into the development and deployment process or applied as an afterthought at deployment. The Well-Architected answer requires security checks at the code level, the dependency level, the container image level, and the infrastructure configuration level — all automated within the CI/CD pipeline.

**Shift-left controls:**

- **Static Application Security Testing (SAST)**: code analysis tools (Semgrep, Checkov for IaC, SonarQube) running at pull request time, blocking merges that introduce high-severity findings
- **Software Composition Analysis (SCA)**: dependency scanning (AWS Inspector for Lambda, ECR scanning for container images, Dependabot or Snyk for application dependencies) identifying known-vulnerable libraries before they reach production
- **IaC security scanning**: Checkov, tfsec, or cfn-nag scanning CloudFormation or Terraform before deployment, blocking infrastructure changes that introduce security misconfigurations — security groups open to 0.0.0.0/0, unencrypted S3 buckets, missing CloudTrail configuration

**Amazon CodeGuru Security** provides ML-based code review for Python, Java, JavaScript, TypeScript, and Go, identifying security vulnerabilities, hardcoded credentials, and insecure API usage. It integrates with CodePipeline and can gate deployments on security findings.

**AWS Secrets Manager** and **Parameter Store** eliminate hardcoded credentials from application code — one of the most common application security failures and one of the easiest to prevent. Applications retrieve secrets at runtime via API; the secret value never appears in source code, logs, or environment variables.

---

## Running a Well-Architected Security Review

The AWS Well-Architected Tool (available in the AWS console at zero additional cost) guides you through the eleven questions with sub-questions, best practice references, and risk classifications. Running a formal review generates a Pillar Report identifying high-risk issues (HRIs) and medium-risk issues, with links to remediation guidance.

**How to run a meaningful review:**

1. Create a workload in the Well-Architected Tool. Define it specifically — a production AWS environment, a specific application, a migration project — rather than "our whole AWS estate." Specificity produces actionable findings; generality produces noise.
2. Invite the right stakeholders. The Security Pillar questions span IAM (answer requires the IAM lead), networking (answer requires the network architect), and incident response (answer requires the security operations lead). No single person can answer all eleven questions accurately.
3. Be honest about the current state, not the aspired state. A Well-Architected review is only useful if the inputs are accurate. Answering questions based on what you plan to implement rather than what exists produces a false score and hides the actual risk.
4. Prioritise high-risk issues. The tool categorises findings as high, medium, or low risk. Address every HRI before any medium-risk finding. A single HRI — open S3 bucket, no CloudTrail, `AdministratorAccess` on a service role — typically represents more actual risk than a dozen medium findings combined.

AWS Partner Network (APN) members can conduct Well-Architected Reviews formally on your behalf. For regulated workloads or pre-certification reviews, an external Well-Architected partner review provides independent verification that your self-assessment is accurate.

---

## Mapping to UK Compliance Frameworks

The Well-Architected Security Pillar aligns well with the compliance frameworks most relevant to UK cloud architects:

| Well-Architected Area | NCSC Cloud Security Principles | Cyber Essentials Plus | ISO 27001:2022 |
|---|---|---|---|
| Identity and Access Management | Principle 9 (Identity and Authentication) | Access Control | A.5.15, A.8.2 |
| Detection | Principle 13 (Audit Information) | Monitoring | A.8.15, A.8.16 |
| Infrastructure Protection | Principle 11 (External Interface) | Network Controls, Malware Protection | A.8.20, A.8.21 |
| Data Protection (at rest) | Principle 2 (Asset Protection) | — | A.8.24 |
| Data Protection (in transit) | Principle 4 (Secure Transmission) | — | A.8.24 |
| Incident Response | Principle 6 (Personnel Security) | — | A.5.24, A.5.26 |
| Application Security | Principle 10 (Secure Design) | — | A.8.25, A.8.28 |

For UK-regulated firms, the Security Pillar controls also map directly to FCA Operational Resilience requirements (important business services, impact tolerances, self-assessment obligations) and UK GDPR Article 32 (technical and organisational measures appropriate to the risk). A workload that passes a Well-Architected Security review has substantially addressed its Article 32 obligations for the technical measures component.

---

## What Architects Should Do

**Run the Well-Architected Tool review now, before any remediation.** The current-state assessment is the baseline. Without it, you have no evidence of improvement and no prioritised list of what to fix.

**Treat every high-risk issue as a production defect.** HRIs in a Well-Architected review should be tracked in your engineering backlog with the same urgency as a P1 bug. Most HRIs are not difficult to remediate — they are difficult to prioritise without a framework that makes their risk visible.

**Enable GuardDuty, Security Hub, and CloudTrail across your entire organisation in the next sprint.** These three services together provide the detection and audit baseline that addresses SEC 4 (Detection) and a significant portion of SEC 1 (Security Foundations). None of them require extensive configuration to be useful. Not having them enabled is the single most common Well-Architected HRI in AWS environments.

**Migrate human access to IAM Identity Centre.** Eliminating long-term IAM user credentials for human access addresses SEC 2 at its root. AWS IAM Identity Centre can federate with any SAML 2.0 IdP. The migration path from IAM users to federated access can be executed account by account without service interruption.

**Apply SCPs to your organisation before the next account is provisioned.** Retroactive SCP application to existing accounts requires careful sequencing to avoid breaking running workloads. New accounts provisioned without SCPs accumulate as technical debt. The best time to apply SCPs is before the first workload; the second best time is now.

**Automate remediation for common misconfigurations.** AWS Config Rules with EventBridge and Lambda remediation functions can automatically correct known-bad configurations: public S3 buckets made private, security groups with 0.0.0.0/0 SSH access revoked, GuardDuty re-enabled if disabled. Automated remediation provides a backstop against configuration drift that manual review cannot match.

---

## Key Takeaways

- **The Well-Architected Security Pillar defines eleven questions across seven areas** — Security Foundations, IAM, Detection, Infrastructure Protection, Data Protection, Incident Response, and Application Security. Answering all eleven with evidence is the definition of a well-secured AWS workload.
- **High-risk issues are the priority** — the Well-Architected Tool classifies findings by risk level. Every HRI (open credentials, missing logging, no MFA, public data stores) should be remediated before any medium-risk finding.
- **GuardDuty + Security Hub + CloudTrail is the minimum detection stack** — these three services, enabled across all accounts in the organisation, address the largest single category of Well-Architected security gaps.
- **IMDSv2 enforcement and elimination of long-term access keys are the two highest-impact IAM changes** available to most AWS environments — addressing the credential theft vectors responsible for the majority of significant AWS breaches.
- **UK compliance obligations map directly to Well-Architected controls** — a workload that passes a Well-Architected Security review has substantially addressed NCSC Cloud Security Principles, Cyber Essentials Plus, ISO 27001:2022, and UK GDPR Article 32 technical measures.

---

## Related Guides

- [Cloud Identity and Access Management](/guides/cloud-identity-and-access-management/) — The hub guide for IAM fundamentals: principals, federation, least privilege, PAM — the controls that address SEC 2 and SEC 3.
- [AWS IAM Security Best Practices](/guides/aws-iam-security-best-practices/) — Detailed AWS-specific IAM implementation: SCPs, permission boundaries, access analysis, and long-term credential elimination.
- [AWS Security Hub: A Practitioner's Guide](/guides/aws-security-hub-guide/) — Security Hub is the operational layer for Well-Architected Security Pillar monitoring — aggregating GuardDuty, Inspector, and Config findings with FSBP standard coverage.
- [AWS CloudTrail Configuration Best Practices](/guides/aws-cloudtrail-configuration-best-practices/) — Organisation trails, KMS encryption, log integrity validation — the audit trail that addresses SEC 4.
- [Privileged Access Management in AWS](/guides/privileged-access-management-in-aws/) — JIT access and zero standing privilege: the advanced implementation of Well-Architected's IAM best practices.
- [AWS KMS Key Management Best Practices](/guides/aws-kms-key-management-best-practices/) — Customer-managed keys, key policies, and audit controls — the implementation layer for SEC 8 (data at rest protection).
- [Cloud Network Security](/guides/cloud-network-security/) — VPCs, security groups, WAF, private connectivity — the implementation detail behind SEC 5 (network protection).
- [Cloud Threat Detection](/guides/cloud-threat-detection/) — How GuardDuty, Security Hub, and Detective work together to build a detection programme that addresses SEC 4.
- [AWS Compliance and Governance](/guides/aws-compliance-and-governance/) — Control Tower, SCPs, AWS Config — the governance layer that operationalises SEC 1 (Security Foundations).
- [Cloud Compliance Frameworks](/guides/cloud-compliance-frameworks/) — How Well-Architected Security controls map to ISO 27001, SOC 2, UK GDPR, NCSC, Cyber Essentials Plus, and FCA requirements.
