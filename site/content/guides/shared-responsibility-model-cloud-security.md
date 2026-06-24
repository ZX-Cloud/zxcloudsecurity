+++
title = "What is the Shared Responsibility Model in Cloud Security?"
date = "2026-06-08T09:24:00Z"
slug = "shared-responsibility-model-cloud-security"
description = "The shared responsibility model explained for AWS, Azure, and GCP — what the provider secures, what the customer owns, and the boundary misunderstandings that cause most cloud security incidents."
keywords = ["shared responsibility model", "cloud security", "AWS", "Azure", "GCP"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

The shared responsibility model is a framework that defines the division of security obligations between a cloud provider and its customers. The provider secures the underlying infrastructure — physical hardware, network fabric, and hypervisor layers — whilst the customer remains responsible for everything they build and configure on top of it. Misunderstanding this boundary is one of the most common root causes of cloud security incidents.

## How the Model Works Across AWS, Azure, and GCP

All three major providers publish explicit statements of their shared responsibility model, but the precise language and boundaries differ enough to cause confusion when operating across multiple clouds.

**AWS** frames it as "security *of* the cloud versus security *in* the cloud." AWS owns the global infrastructure: regions, availability zones, edge locations, and the hardware, software, and networking that underpins its services. Customers own their data, identity and access management, operating systems on EC2, network configuration, and application-layer controls.

**Azure** uses comparable language but emphasises data classification and account management as always being customer responsibilities, regardless of service model. Microsoft's shared responsibility documentation explicitly calls out that identity infrastructure — such as Azure Active Directory tenant configuration and conditional access policies — sits firmly on the customer side.

**GCP** follows the same pattern but adds nuance around its managed services. Google explicitly retains responsibility for encrypting data at rest and in transit by default within its infrastructure, which can create a false sense of security if customers assume this satisfies all their encryption obligations — it does not cover customer-managed keys, envelope encryption strategies, or application-layer encryption requirements.

The core principle is consistent: the provider secures what you cannot physically access or control; you secure everything you can configure, deploy, or manage.

## How Responsibility Shifts Across IaaS, PaaS, and SaaS

The service model in use dramatically changes where the responsibility line sits, and this is where many security programmes fall short.

### Infrastructure as a Service (IaaS)

With IaaS — EC2 on AWS, Azure Virtual Machines, or GCP Compute Engine — the customer carries the heaviest security burden. The provider manages physical hardware and the hypervisor; you own the guest OS, middleware, runtime, application code, and data. Patch management, host-based intrusion detection, endpoint hardening, and network security group configuration all fall to you. An unpatched kernel vulnerability on an EC2 instance is entirely your problem.

### Platform as a Service (PaaS)

PaaS offerings — AWS Elastic Beanstalk, Azure App Service, GCP App Engine — shift OS and runtime management to the provider. The provider patches and maintains the underlying platform; the customer is responsible for application code, data, and configuration of the service itself. This sounds like a significant reduction in burden, and it is — but the misconfiguration risk increases because developers deploying into PaaS environments often assume the platform is handling more than it actually is. Access controls, secret management, and environment variable handling remain customer responsibilities.

### Software as a Service (SaaS)

In SaaS models — Microsoft 365, Google Workspace, Salesforce — the provider manages virtually the entire stack. However, this does not mean customer responsibility disappears. Data governance, user access management, data loss prevention policies, and regulatory compliance obligations still sit with the customer. A poorly configured sharing policy in SharePoint Online or an over-permissioned OAuth application in Google Workspace can expose sensitive data, and no amount of Microsoft or Google infrastructure security will prevent it.

## Common Misconceptions That Lead to Breaches

### "The cloud provider handles security"

This is the most dangerous misconception in cloud security. When an S3 bucket is misconfigured as publicly accessible, AWS has not failed in its responsibility — the customer has failed in theirs. The Capital One breach in 2019 is a useful illustration: AWS infrastructure performed exactly as designed; the failure was a misconfigured WAF and overly permissive IAM role, both squarely customer responsibilities.

### "Managed services mean fully managed security"

Using Amazon RDS instead of running your own database does shift OS and database engine patching to AWS, but database authentication, network access controls, encryption configuration, and data classification remain customer obligations. The same applies to Azure SQL Managed Instance or Cloud SQL on GCP.

### "Encryption at rest provided by the cloud means we're compliant"

Provider-managed encryption (SSE-S3, Azure Storage Service Encryption, GCP default encryption) encrypts data against physical media theft, but it does not satisfy requirements for customer-controlled key management, separation of duties, or regulations that require demonstrable key ownership. For PCI-DSS, GDPR, or UK government security frameworks, you will almost certainly need customer-managed keys (CMKs) and audit evidence of key lifecycle management.

### "The compliance certification transfers to us"

AWS, Azure, and GCP hold certifications such as ISO 27001, SOC 2, and PCI-DSS for their infrastructure. These certifications do not extend to your workloads. You must independently demonstrate compliance for the layers you control. Providers supply compliance reports (AWS Artifact, Azure Service Trust Portal, GCP Compliance Reports Manager) as evidence for the infrastructure layer, but your auditors will require evidence from your side as well.

## What Architects Should Do

- **Document the responsibility matrix for each service you use.** Produce a service-by-service breakdown showing which security controls are provider-owned, shared, and customer-owned. This is essential input for risk assessments and audit responses.

- **Apply the principle of least privilege rigorously.** IAM misconfiguration is consistently the customer-side failure that leads to breaches. Across AWS, Azure, and GCP, enforce least-privilege roles, regularly review permissions, and use tools like AWS IAM Access Analyzer, Azure AD Access Reviews, and GCP IAM Recommender.

- **Do not treat default configurations as secure configurations.** Cloud services are often permissive by default to aid onboarding. Review and harden defaults: restrict public access to storage buckets, enforce MFA, disable unused APIs, and enable logging from day one.

- **Implement continuous compliance monitoring.** Use AWS Security Hub, Microsoft Defender for Cloud, or GCP Security Command Center to surface customer-side misconfigurations. These tools specifically surface deviations within the customer's area of responsibility.

- **Own your data classification and governance.** Regardless of service model, data classification, labelling, retention, and deletion policies are always your responsibility. Build these controls into your data lifecycle from the outset rather than retrofitting them.

- **Treat identity as your primary security perimeter.** In cloud environments, the network perimeter is diffuse. Identity — user accounts, service accounts, federated access — is the boundary you control most directly. Enforce conditional access, monitor for anomalous authentication events, and rotate service account credentials systematically.

- **Validate your understanding of shared responsibility at procurement.** When evaluating new cloud services or SaaS products, explicitly map security responsibilities as part of due diligence. Do not rely on the vendor's marketing language; review the provider's published shared responsibility documentation directly.

## Key Takeaways

- The shared responsibility model divides security obligations between the cloud provider and the customer. The provider secures physical infrastructure and the foundational platform; the customer secures data, identity, configurations, and applications.
- The customer's security burden is largest under IaaS and progressively smaller under PaaS and SaaS — but it never reaches zero.
- AWS, Azure, and GCP follow the same core framework, with differences in scope and terminology that matter in multi-cloud environments.
- The most frequent cloud security failures — exposed storage, misconfigured IAM, unpatched workloads — occur entirely within the customer's area of responsibility.
- Compliance certifications held by providers do not transfer to customer workloads. You must independently evidence controls for the layers you own.


## Related Guides

- [Cloud Security Posture Management (CSPM)](/guides/what-is-cspm-cloud-security-posture-management/) — CSPM tools help you continuously verify that you are fulfilling your side of the shared responsibility model across your cloud estate.
- [Zero Trust Architecture](/guides/what-is-zero-trust-architecture/) — Zero Trust provides the architectural framework for securing the components of cloud infrastructure that fall under your responsibility.
- [AWS IAM Security Best Practices](/guides/aws-iam-security-best-practices/) — IAM configuration is one of the clearest examples of customer responsibility in AWS. This guide covers what you need to get right.
- [Data Security Posture Management (DSPM)](/guides/what-is-dspm-data-security-posture-management/) — Data protection is almost entirely a customer responsibility in cloud environments. DSPM provides the tooling to fulfil that obligation.
- [Cloud Infrastructure Entitlement Management (CIEM)](/guides/what-is-ciem-cloud-infrastructure-entitlement-management/) — Identity and access management is a core customer responsibility. CIEM tooling helps enforce least privilege across your cloud identities.
- [Cross-Cloud Security Services Comparison](/guides/aws-azure-gcp-security-service-comparison/) — Compare how AWS, Azure, and GCP divide security responsibilities and what native tools each provider offers to support your obligations.
