+++
title = "What is the Shared Responsibility Model in Cloud Security?"
date = "2026-06-07T13:46:50Z"
slug = "shared-responsibility-model-cloud-security"
description = "What is the Shared Responsibility Model in Cloud Security? — a practical guide for cloud security architects."
keywords = ["shared responsibility model", "cloud security", "AWS", "Azure", "GCP"]
type = "guides"
draft = false
+++

The shared responsibility model is a framework that defines the division of security obligations between a cloud provider and its customers. In essence, the provider secures the underlying infrastructure — physical hardware, networking, and the hypervisor layer — whilst the customer remains responsible for everything they deploy on top of it. Understanding exactly where that boundary sits is one of the most operationally critical concepts in cloud security.

---

## The Core Principle: Security "of" the Cloud vs Security "in" the Cloud

AWS articulated this distinction particularly clearly when it coined the phrase "security of the cloud versus security in the cloud." The provider owns the former; you own the latter.

**Cloud provider responsibilities typically include:**
- Physical data centre security (access controls, surveillance, environmental protection)
- Hardware lifecycle management and disposal
- The global network backbone and DDoS mitigation at the infrastructure level
- Hypervisor and virtualisation layer security
- Managed service software patching (for fully managed services)

**Customer responsibilities typically include:**
- Identity and access management (IAM) configuration
- Data classification and encryption
- Operating system patching (for IaaS workloads)
- Network security groups, firewall rules, and segmentation
- Application-layer security controls
- Compliance and regulatory obligations for your data

The precise boundary shifts significantly depending on whether you are consuming IaaS, PaaS, or SaaS — which is where many organisations go wrong.

---

## How the Boundary Shifts Across IaaS, PaaS, and SaaS

### IaaS: The Customer Carries the Most Weight

With infrastructure-as-a-service — think AWS EC2, Azure Virtual Machines, or GCP Compute Engine — the provider manages the physical hardware and virtualisation layer. Everything above the hypervisor is yours. That means you are responsible for the guest OS, installed runtimes, middleware, your application code, and all data. If you leave an EC2 instance running an unpatched kernel, that is your exposure, not Amazon's.

### PaaS: Responsibility Shifts Upward

Platform-as-a-service abstracts away the OS and runtime. Services like AWS Elastic Beanstalk, Azure App Service, or GCP App Engine mean the provider patches the underlying OS and manages the runtime environment. However, the customer remains accountable for application code, application-level configurations, data handling, and IAM. A misconfigured Azure App Service with overly permissive managed identity assignments is still a customer problem.

### SaaS: The Provider Handles the Stack, But Not Everything

Software-as-a-service offerings like Microsoft 365, Google Workspace, or Salesforce place the bulk of technical responsibility with the provider. The application, platform, and infrastructure are all managed. Even so, the customer retains ownership of user account governance, data access policies, data retention decisions, and regulatory compliance obligations. A misconfigured sharing policy in SharePoint Online that exposes sensitive documents externally is a customer failure, not Microsoft's.

---

## Provider-Specific Nuances Worth Knowing

### AWS

AWS publishes its shared responsibility model prominently and applies it consistently across services — though the boundary genuinely shifts per service. For Lambda (serverless), AWS manages the execution environment and OS; you own the function code, its permissions, and the data it touches. For Amazon RDS, AWS handles OS and database engine patching; you own database user privileges, encryption-at-rest configuration, and network access controls. Always check per-service documentation rather than assuming a single model applies universally.

### Azure

Microsoft's model mirrors AWS structurally but introduces additional nuance around hybrid connectivity. Organisations using Azure Arc or Azure Stack to extend cloud services on-premises carry greater responsibility for those environments. Azure's model also distinguishes clearly between Microsoft's responsibility for Azure Active Directory (now Microsoft Entra ID) infrastructure and the customer's responsibility for tenant configuration — conditional access policies, privileged identity management settings, and guest user governance all sit firmly with you.

### GCP

Google Cloud follows the same foundational split, but GCP's emphasis on its "secure by default" configurations and services like BeyondCorp Enterprise can create a false sense of coverage. GCP manages the Kubernetes control plane in GKE Autopilot mode, for instance, but you remain responsible for workload identity bindings, pod security policies, and the container images you deploy. Google's infrastructure-level security is genuinely strong, but it does not extend into your workload configuration.

---

## Common Misconceptions That Lead to Incidents

**"The cloud provider handles security."** This is the most dangerous assumption in cloud security. It is also the root cause of a disproportionate share of cloud breaches — misconfigured S3 buckets, exposed Azure Blob containers, and over-permissive GCP service accounts are all customer-side failures.

**"Compliance certifications mean I'm covered."** AWS, Azure, and GCP hold extensive compliance certifications (ISO 27001, SOC 2, PCI DSS, and so on). These cover the provider's scope. You must independently demonstrate compliance for your own workloads, configurations, and data handling practices.

**"Managed services eliminate my security obligations."** Moving to a managed database or container service reduces your operational surface, but it does not eliminate your responsibility for access controls, encryption choices, audit logging, and data governance.

**"The provider will alert me to misconfigurations."** Native tooling like AWS Security Hub, Microsoft Defender for Cloud, and GCP Security Command Center can surface issues — but only if you have enabled, configured, and are actively monitoring them. These tools do not act autonomously on your behalf.

---

## What Cloud Security Architects Should Do

- **Map your shared responsibility boundary per service, not per provider.** Build a service inventory that explicitly documents what the provider manages and what your team owns for each service in scope. This is particularly important in multi-cloud environments.

- **Treat IAM configuration as a first-order security control.** Misconfigurations here consistently sit at the top of cloud breach root cause analyses. Enforce least privilege, audit role assignments regularly, and use tools like AWS IAM Access Analyzer, Azure PIM, or GCP IAM Recommender.

- **Enable and act on native security posture tooling.** AWS Security Hub, Defender for Cloud, and GCP Security Command Center provide continuous visibility into customer-side misconfigurations. These should feed into your operational security processes, not sit dormant.

- **Encrypt data at rest and in transit with keys you control.** Provider-managed encryption is better than nothing, but customer-managed keys (AWS KMS, Azure Key Vault, GCP Cloud KMS) give you cryptographic control that persists even if provider-side access is compromised.

- **Test your incident response assumption.** Providers will respond to infrastructure-level incidents. They will not investigate your application layer. Tabletop your response to a cloud breach scenario and identify explicitly who does what across the shared boundary.

- **Include the shared responsibility model in onboarding for all cloud engineers.** Cultural misunderstanding is as dangerous as technical misconfiguration. Make the boundary explicit and revisit it whenever you adopt new services.

---

## Key Takeaways

- The shared responsibility model divides security obligations between the cloud provider and the customer; providers secure the infrastructure, customers secure their deployments on top of it.
- The customer's responsibility increases as you move from SaaS to PaaS to IaaS, with IaaS placing the greatest burden on your team.
- AWS, Azure, and GCP follow the same broad model, but the precise boundary varies by individual service — always verify per service, not per provider.
- The most common and costly mistakes arise from assuming the provider's responsibilities are broader than they are, particularly around IAM, data exposure, and compliance.
- Effective cloud security requires deliberately owning your half of the model — through posture management tooling, IAM discipline, encryption controls, and tested incident response.
