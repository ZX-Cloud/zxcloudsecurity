+++
title = "Cloud Compliance Frameworks: What Security Architects Need to Know"
date = "2026-06-24T09:00:00Z"
slug = "cloud-compliance-frameworks"
description = "Cloud compliance for architects: ISO 27001, SOC 2, PCI DSS, UK GDPR, Cyber Essentials Plus, NCSC Cloud Principles, and FCA requirements — how each maps to AWS, Azure, and GCP controls."
keywords = ["cloud compliance", "ISO 27001 cloud", "SOC 2 AWS", "PCI DSS cloud", "UK GDPR AWS", "Cyber Essentials cloud", "NCSC cloud security principles", "FCA cloud compliance"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

Compliance in cloud environments is widely misunderstood and frequently mishandled. The misunderstanding takes two forms: organisations that treat cloud compliance as a mapping exercise — draw lines between framework controls and AWS services, tick boxes, file the report — and organisations that treat cloud as a compliance risk and avoid it entirely. Both miss the point. Cloud platforms, when correctly configured, can make compliance significantly more achievable than traditional data centre environments. But "correctly configured" is doing enormous work in that sentence.

This guide covers the compliance frameworks most relevant to UK cloud security architects, what each actually demands in a cloud context, how the shared responsibility model interacts with compliance obligations, and the tooling that makes continuous compliance operational rather than a quarterly project.

---

## The Shared Responsibility Model and Compliance

Every cloud compliance conversation starts here, because failing to understand it results in either under-delivering on your obligations or spending resources protecting things the provider already protects.

The shared responsibility model divides security and compliance obligations between the cloud provider and the customer. The exact boundary varies by service type:

- **Infrastructure (IaaS) — EC2, Azure VMs, GCP Compute Engine**: The provider secures the physical data centre, network, hypervisor, and host OS. The customer is responsible for the guest OS, runtime, middleware, application code, data, and all configuration decisions above the hypervisor.
- **Platform (PaaS) — RDS, Lambda, Azure App Service, GCP Cloud Run**: The provider additionally manages the OS and runtime. The customer retains responsibility for application code, configuration, and data.
- **Software (SaaS) — Microsoft 365, Google Workspace**: The provider manages nearly everything; the customer is responsible primarily for data, identity, and access control configuration.

In practice, this means your compliance evidence must cover what is within your responsibility boundary, while relying on provider certifications and compliance documentation for the provider's boundary. AWS, Azure, and GCP all maintain extensive compliance certification portfolios — ISO 27001, SOC 2 Type II, PCI DSS, CSA STAR, and others — that you can reference in your own compliance submissions. The certifications cover the provider's infrastructure; they do not automatically cover your workloads running on it.

AWS Artifact, Azure Service Trust Portal, and GCP Compliance Reports Manager provide access to provider compliance documentation, audit reports, and certification letters. Use these when you need to demonstrate provider compliance posture to auditors.

---

## ISO 27001

ISO 27001 is the international standard for information security management systems (ISMS). It specifies requirements for establishing, implementing, maintaining, and continuously improving an ISMS. Annex A contains 93 controls across four domains — Organisational, People, Physical, and Technological — that organisations implement to address information security risks.

**What ISO 27001 requires in cloud contexts:**

- **A.5.23 (Information security for use of cloud services)** — explicitly requires policies for cloud service acquisition, use, management, and exit. This is new in ISO 27001:2022 and specifically mandates that organisations address cloud-specific risks.
- **A.8.25 (Secure development life cycle)** includes IaC (Infrastructure as Code) and cloud deployment pipelines within secure development scope.
- Controls on access control, cryptography, vulnerability management, logging, and incident management all apply to cloud workloads and must be evidenced against your cloud environment specifically.

**Practical implications:** ISO 27001 certification requires you to demonstrate controls working in practice, not just documented in policy. For cloud environments, this means: demonstrable least-privilege IAM configuration with evidence from IAM Access Analyzer, audit logging enabled and tamper-protected (CloudTrail with object lock), vulnerability scanning running continuously (Amazon Inspector), and incident response procedures tested against cloud-specific scenarios.

AWS, Azure, and GCP are all ISO 27001 certified, but their certification covers their data centre infrastructure — not your workload configuration. Your auditor will want evidence that the controls in Annex A are implemented in your cloud deployment specifically.

---

## SOC 2

SOC 2 (Service Organization Control 2) is a US framework from the American Institute of CPAs (AICPA), but it is widely required by UK and European organisations procuring SaaS and technology services. SOC 2 evaluates controls against five Trust Service Criteria: Security (required), Availability, Processing Integrity, Confidentiality, and Privacy.

**Type I** reports evaluate whether controls are suitably designed at a point in time. **Type II** reports evaluate whether controls operated effectively over a period (typically 12 months) — this is what customers and regulators generally require.

**What SOC 2 requires in cloud contexts:**

- **CC6.1 (Logical and physical access controls)** — maps directly to IAM configuration, MFA enforcement, least privilege, and access reviews
- **CC6.7 (Transmission and disposal)** — encryption in transit and at rest; TLS enforcement, KMS key management
- **CC7.2 (System monitoring)** — continuous monitoring; CloudTrail, GuardDuty, Security Hub
- **CC9.2 (Risk mitigation)** — vendor risk management, which includes your cloud provider's compliance posture

SOC 2 is process-oriented: it requires evidence of controls operating consistently over time, not just a configuration snapshot. For cloud environments, this means automated evidence collection — AWS Config snapshots, CloudTrail exports, Security Hub compliance data — stored in a tamper-evident audit log for the audit period.

Tools like Drata, Vanta, and Secureframe automate SOC 2 evidence collection from AWS, Azure, and GCP, pulling configuration data, access logs, and vulnerability reports directly from cloud APIs and mapping them to SOC 2 criteria. For organisations targeting SOC 2 Type II in cloud environments, automated evidence collection is the practical choice over manual evidence gathering.

---

## PCI DSS

PCI DSS (Payment Card Industry Data Security Standard) v4.0 applies to any organisation that stores, processes, or transmits payment card data. For AWS environments, this means the accounts and resources that constitute or connect to the cardholder data environment (CDE).

**Key PCI DSS requirements in cloud:**

- **Requirement 1 (Network security controls)** — CDE accounts must have well-defined network perimeters; VPC security groups and NACLs must restrict ingress to only authorised sources; no direct internet access for CDE resources where not required
- **Requirement 2 (Secure configurations)** — all EC2 instances, RDS databases, and cloud services in the CDE must have documented hardened configurations; default passwords must be changed; services not needed must be disabled
- **Requirement 7 (Access to system components)** — least privilege for all CDE access; IAM policies must grant only the specific permissions required; regular access reviews with evidence
- **Requirement 10 (Audit logging)** — CloudTrail must be enabled for all CDE accounts, covering all API calls; logs must be tamper-protected and retained for 12 months (3 months immediately available)
- **Requirement 11 (Testing)** — quarterly vulnerability scanning and annual penetration testing of the CDE; Amazon Inspector satisfies the continuous vulnerability scanning requirement with appropriate scoping

**Scoping is everything in PCI DSS cloud deployments.** The CDE includes any system that stores, processes, or transmits cardholder data, plus connected systems. In cloud environments, the CDE boundary is defined by your network segmentation, not physical location. Accounts that have no connectivity to CDE accounts are out of scope; accounts with even indirect connectivity require controls appropriate to their connected status.

Use separate AWS accounts for CDE and non-CDE workloads, with no cross-account IAM trust relationships that would bring non-CDE accounts into scope. Use Transit Gateway with strict security group and routing controls for any required connectivity.

---

## UK GDPR and Data Protection Act 2018

UK GDPR applies to any organisation processing personal data of UK residents. For cloud architectures, the key obligations that have direct technical implementation requirements:

**Data transfers.** UK personal data processed in a cloud region outside the UK must have a lawful transfer mechanism. AWS has UK regions (`eu-west-2` — London); for AWS customers, restricting personal data processing to `eu-west-2` eliminates the transfer problem. If other regions are used, an appropriate transfer mechanism (UK Adequacy Decision, Standard Contractual Clauses under the UK framework) must be in place and documented.

Enforce data residency using SCPs that deny `ec2:RunInstances`, `s3:CreateBucket`, `rds:CreateDBInstance`, and equivalent actions in non-UK regions for accounts processing personal data:

```json
{
  "Effect": "Deny",
  "Action": "*",
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestedRegion": ["eu-west-2", "eu-west-1"]
    }
  }
}
```

**Article 25 (Data protection by design and default).** Technical controls must be embedded in system design, not bolted on. In cloud terms: encryption at rest by default (enforced by SCP requiring KMS encryption for S3, RDS, EBS), minimal data collection (application-level), and access control by default (least privilege IAM).

**Article 32 (Security of processing).** Requires "appropriate technical and organisational measures" — explicitly mentions pseudonymisation, encryption, confidentiality, integrity, availability, and resilience. In cloud: encryption at rest and in transit, IAM controls, backups, multi-AZ deployments for critical data stores, and access logging.

**Right to erasure.** Implementing data deletion in cloud environments requires knowing where personal data is stored. DSPM tooling (Amazon Macie, Microsoft Purview) is relevant here — you cannot delete data you cannot find.

---

## Cyber Essentials and Cyber Essentials Plus

Cyber Essentials is a UK government-backed certification that provides a baseline for cyber security hygiene. Cyber Essentials Plus adds independent technical verification. It is required for UK government contracts handling personal data and increasingly expected by enterprise customers.

The five Cyber Essentials technical controls in a cloud context:

**1. Firewalls.** Cloud security groups and NACLs constitute the firewall boundary. Default-deny with explicit allow rules for required traffic. Inbound rules must be documented and scoped — `0.0.0.0/0` on port 22 or 3389 is a Cyber Essentials failure.

**2. Secure configuration.** Default credentials changed (AWS does not use default credentials for managed services, but EC2 AMIs may have default OS configurations that require hardening). Services and features not required disabled. Security group rules reviewed and minimised.

**3. User access control.** Least privilege IAM. Removal of access for departed employees. MFA for all accounts with administrative access, including AWS console access. Regular access reviews. The Cyber Essentials scheme specifically addresses privileged accounts and requires MFA for all accounts with privileged access.

**4. Malware protection.** For EC2 workloads, GuardDuty Malware Protection and Amazon Inspector (with SSM agent) provide malware detection and vulnerability scanning. Cloud-native services (Lambda, managed databases) are managed by AWS and not in scope for malware protection controls.

**5. Patch management.** All software on customer-managed instances must be patched within 14 days of a critical patch release. AWS Systems Manager Patch Manager supports automated patching with compliance reporting. Managed services (RDS, Lambda, EKS control plane) are patched by AWS — confirm this in AWS's shared responsibility documentation.

---

## NCSC Cloud Security Principles

The NCSC's 14 Cloud Security Principles provide a framework specifically designed for cloud service evaluation, widely referenced by UK government departments, NHS, and regulated sectors when assessing cloud suppliers.

The 14 principles and their primary AWS implementation:

| Principle | AWS Implementation |
|---|---|
| 1. Data in transit protection | TLS enforced by policy; AWS Certificate Manager; PrivateLink |
| 2. Asset protection and resilience | Multi-AZ deployments; S3 object lock; KMS CMKs |
| 3. Separation between consumers | VPC isolation; account separation; no cross-tenant data access |
| 4. Governance framework | AWS Control Tower; SCPs; AWS Config |
| 5. Operational security | GuardDuty; Security Hub; CloudTrail; patch management |
| 6. Personnel security | AWS employee vetting (documented in AWS compliance documentation); customer-side IAM controls |
| 7. Secure development | AWS responsibility for managed services; customer responsibility for application code |
| 8. Supply chain security | AWS supplier assurance (available in AWS Artifact); customer-side dependency management |
| 9. Secure user management | IAM Identity Centre; SCPs; conditional access |
| 10. Identity and authentication | IAM; MFA; federation; session management |
| 11. External interface protection | Security groups; WAF; Shield; network ACLs |
| 12. Secure service administration | Restricted admin access; CloudTrail; Config |
| 13. Audit information for users | CloudTrail; VPC Flow Logs; Config; Security Hub |
| 14. Secure use of the service | Customer responsibility for workload configuration |

Principle 14 is the most operationally significant: secure use of the service is entirely the customer's responsibility. AWS cannot prevent you from creating an overpermissive IAM role, an unencrypted S3 bucket, or a security group open to the world — that is what your security controls, Security Hub, and CSPM tooling exist to prevent.

---

## FCA SYSC Requirements

The FCA's Senior Management Arrangements, Systems and Controls (SYSC) sourcebook applies to FCA-authorised firms and sets expectations for operational resilience, outsourcing, and technology risk. For cloud deployments specifically:

**SYSC 8 (Outsourcing)** treats cloud services as material outsourcing arrangements requiring: due diligence on the provider, contractual provisions for audit rights and business continuity, exit planning, and ongoing monitoring of third-party performance. AWS Business Associate Agreements and AWS's compliance certifications form part of the due diligence evidence trail.

**PS21/3 (Operational Resilience)** requires firms to identify Important Business Services, set impact tolerances, and demonstrate the ability to remain within those tolerances during disruption. For cloud deployments, this means: multi-AZ and multi-region architectures for critical services, documented recovery time objectives, tested disaster recovery runbooks, and CloudWatch alarms tied to operational resilience metrics.

**FCA Cloud Outsourcing guidance** (published 2023) explicitly expects firms to maintain control of data and systems even when outsourcing to cloud providers, retain the ability to audit cloud deployments, and ensure concentration risk across cloud providers is understood and managed.

---

## Continuous Compliance: The Operational Model

One-time compliance audits are insufficient in cloud environments where infrastructure changes continuously. The correct model is continuous compliance:

**Policy as code** — compliance controls are codified as IaC (Terraform modules, AWS CloudFormation Guard rules, OPA policies) and enforced during deployment, not evaluated afterwards. A resource that cannot be deployed in a non-compliant configuration cannot become non-compliant.

**Continuous evaluation** — AWS Config rules, Security Hub standards, and CSPM tools (Wiz, Prisma Cloud, Orca) evaluate resource configuration continuously against defined standards and alert on drift from the compliant baseline.

**Automated evidence collection** — compliance evidence (access logs, configuration snapshots, vulnerability reports, patch compliance data) is collected automatically from cloud APIs and stored in tamper-evident archives for auditors. Manual evidence gathering for cloud environments is neither scalable nor reliable.

**Compliance as an engineering metric** — Security Hub compliance scores, Config rule pass rates, and CSPM posture scores belong in engineering dashboards alongside uptime and error rates. Compliance is an operational property, not an annual event.

---

## What Architects Should Do

- **Scope each compliance framework correctly** — understand which accounts, services, and data are in scope before implementing controls; over-scoping wastes resource; under-scoping creates audit risk
- **Use the cloud provider's compliance documentation** to cover the infrastructure layer — AWS Artifact, Azure Service Trust Portal, and GCP Compliance Reports provide the evidence that the provider's infrastructure is compliant
- **Implement data residency controls via SCPs** for UK GDPR obligations — region restriction is the most reliable technical control for data sovereignty
- **Enable Security Hub's FSBP standard as the baseline** for continuous compliance monitoring across your AWS estate — it covers the majority of controls relevant to ISO 27001, Cyber Essentials, and NCSC Cloud Principles
- **Treat compliance evidence collection as an engineering problem** — automate it from day one; manual compliance evidence does not scale and is error-prone under audit conditions
- **Build operational resilience architecture before the FCA asks** — multi-AZ deployments, tested DR, documented impact tolerances — not as a compliance exercise but as sound engineering

---

## Key Takeaways

- **The shared responsibility model determines your compliance boundary** — the cloud provider's certifications cover their infrastructure; your workload configuration is yours to evidence
- **UK GDPR data residency is solvable with SCPs** — region restriction enforced at the organisation layer is reliable technical evidence of data residency controls
- **Cyber Essentials in cloud is achievable** — the five controls map directly to standard AWS configuration practices; the common failure points are over-permissive security groups and unpatched EC2 instances
- **NCSC Principle 14 (Secure Use) is entirely your responsibility** — misconfiguration is the dominant cloud compliance risk; continuous monitoring via Security Hub and CSPM closes it
- **Continuous compliance is an engineering discipline** — policy as code, automated evidence collection, and compliance metrics in engineering dashboards make cloud compliance sustainable

---

## Related Guides

- [AWS Compliance and Governance](/guides/aws-compliance-and-governance/) — SCPs, Control Tower, AWS Config, and the governance architecture that enforces compliance controls across an AWS organisation.
- [AWS Security Hub: A Practitioner's Guide](/guides/aws-security-hub-guide/) — How Security Hub's security standards map to ISO 27001, PCI DSS, CIS, and NIST controls with continuous evaluation.
- [What is CSPM?](/guides/what-is-cspm-cloud-security-posture-management/) — CSPM platforms extend Security Hub's compliance visibility with cross-cloud coverage and deeper misconfiguration detection.
- [Cloud Identity and Access Management](/guides/cloud-identity-and-access-management/) — IAM controls are central to ISO 27001 Annex A, SOC 2 CC6, PCI DSS Requirement 7, and every other framework's access control requirements.
- [AWS KMS Key Management Best Practices](/guides/aws-kms-key-management-best-practices/) — Encryption at rest is a requirement across ISO 27001, SOC 2, PCI DSS, and UK GDPR Article 32; this guide covers the KMS implementation.
- [What is the Shared Responsibility Model?](/guides/shared-responsibility-model-cloud-security/) — The foundational concept that determines compliance responsibility allocation between provider and customer.
