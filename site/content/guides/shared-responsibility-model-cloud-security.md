+++
title = "What is the Shared Responsibility Model in Cloud Security?"
date = "2026-06-07T14:16:37Z"
slug = "shared-responsibility-model-cloud-security"
description = "What is the Shared Responsibility Model in Cloud Security? — a practical guide for cloud security architects."
keywords = ["shared responsibility model", "cloud security", "AWS", "Azure", "GCP"]
draft = false
+++

The shared responsibility model is a framework that defines which security obligations belong to the cloud provider and which belong to the customer. Every major cloud platform — AWS, Azure, and GCP — publishes its own version of this model, but the core principle is consistent: the provider secures the underlying infrastructure, while the customer is responsible for securing what they deploy on top of it. Misunderstanding where that boundary sits is one of the most common root causes of cloud security incidents.

---

## How the Model Works in Practice

At its simplest, the shared responsibility model divides security into two domains:

- **Security *of* the cloud** — the physical data centres, hardware, hypervisors, and managed service infrastructure. This is the provider's remit.
- **Security *in* the cloud** — the operating systems, applications, data, identity configurations, and network controls that customers deploy. This is the customer's remit.

AWS, Azure, and GCP each publish documentation describing these boundaries explicitly. AWS's model is perhaps the most widely referenced, clearly stating that AWS manages "the hardware, software, networking, and facilities" while customers manage everything from the guest OS upwards (in an IaaS context). Azure and GCP use comparable language. Where organisations get into trouble is in treating these documents as theoretical rather than operational guides.

---

## Where the Boundary Sits Across IaaS, PaaS, and SaaS

The division of responsibility is not static — it shifts significantly depending on the service model you're consuming.

### Infrastructure as a Service (IaaS)

With IaaS (EC2 on AWS, Azure Virtual Machines, GCP Compute Engine), the customer carries the heaviest security burden. The provider manages the physical host and hypervisor; the customer owns:

- Guest OS patching and hardening
- Network security groups, firewall rules, and routing
- Identity and access management within the instance
- Data encryption at rest and in transit
- Application security

A misconfigured security group exposing port 22 to the internet, or an EC2 instance running an unpatched kernel — these are entirely customer failures, not provider failures.

### Platform as a Service (PaaS)

PaaS services (AWS RDS, Azure App Service, GCP Cloud SQL) shift more responsibility to the provider. The cloud vendor manages the underlying OS and runtime; the customer no longer needs to patch the database engine itself. However, customers still own:

- Access controls and authentication
- Data classification and encryption configuration
- Application-layer security
- Secure configuration of the service (e.g., disabling public endpoints, enabling audit logging)

The reduced operational burden of PaaS can create a false sense of comprehensive security coverage. Leaving an Azure SQL instance with public network access enabled, or failing to enforce TLS on a GCP Cloud SQL connection, remains a customer failure regardless of how managed the service appears.

### Software as a Service (SaaS)

With SaaS (Microsoft 365, Google Workspace, Salesforce), the provider manages almost the entire stack. Customer responsibility narrows to:

- User identity and access management
- Data governance and classification
- Endpoint security
- Configuration of the SaaS platform's security controls (conditional access policies, DLP rules, sharing permissions)

Even here, breaches occur regularly — almost always due to misconfiguration, over-permissioned accounts, or failures in identity governance. The provider securing the application infrastructure does not protect you from an administrator granting excessive permissions or an OAuth integration with excessive scopes.

---

## Common Misconceptions

### "The cloud provider handles encryption"

Most cloud providers offer encryption capabilities, but enabling and configuring them correctly is the customer's job. AWS S3 buckets are not encrypted by default in legacy configurations; even where server-side encryption is enabled, managing your own KMS keys (SSE-KMS) versus provider-managed keys (SSE-S3) is a customer decision with meaningful security implications. GCP and Azure have analogous choices around customer-managed encryption keys (CMEK).

### "Compliance certifications mean the provider has covered security"

AWS, Azure, and GCP hold extensive compliance certifications (ISO 27001, SOC 2, PCI DSS, and so on). These certifications cover the provider's infrastructure and managed services. They do not extend to workloads customers run on top of those services. An organisation hosting cardholder data on AWS is not PCI compliant simply because AWS is — the customer's systems and configurations must independently satisfy the relevant requirements.

### "Managed services eliminate security risk"

Using a managed Kubernetes service like AWS EKS, Azure AKS, or GCP GKE removes the burden of managing control plane security. It does not remove the customer's responsibility for RBAC configuration, pod security standards, network policies, image vulnerability management, or secrets management within the cluster. The attack surface shifts, but it does not disappear.

### "The provider monitors for threats"

AWS GuardDuty, Azure Defender, and GCP Security Command Center provide threat detection capabilities — but they must be enabled and configured by the customer, and the customer is responsible for acting on findings. These are tools the customer uses, not services the provider operates on the customer's behalf.

---

## How AWS, Azure, and GCP Differ

The core model is structurally similar across all three, but there are nuances worth understanding:

- **AWS** provides the most granular published boundary documentation and has a well-established shared responsibility model page that maps responsibilities per service type. AWS also distinguishes between "inherited" controls (fully managed by AWS), "shared" controls, and "customer-specific" controls.
- **Azure** extends the model into hybrid environments more explicitly, which matters for organisations running Azure Arc or Azure Stack. Microsoft also integrates the responsibility model directly into its compliance documentation via Microsoft Service Trust Portal.
- **GCP** frames responsibilities similarly to AWS but places particular emphasis on its BeyondCorp-influenced approach to identity, making IAM configuration a more explicitly customer-facing concern in its documentation.

None of these differences change the fundamental principle, but understanding how each provider documents and surfaces the model helps architects make it operationally concrete for their teams.

---

## What Architects Should Do

- **Document your responsibility boundary per service.** For every cloud service in your estate, explicitly note what the provider manages and what you manage. This is particularly important for PaaS and SaaS where the boundary is less obvious.
- **Map responsibilities to internal owners.** Shared responsibility means nothing if no named internal team owns the customer side. Assign explicit ownership for OS patching, encryption configuration, IAM governance, and monitoring.
- **Use the model as a compliance gap analysis tool.** When assessing against ISO 27001 or PCI DSS controls, use the provider's shared responsibility documentation to identify which controls require customer evidence versus inherited provider evidence.
- **Enable and configure native security tooling actively.** GuardDuty, Azure Defender, Security Command Center, and equivalent services do not operate in a set-and-forget mode. Review findings, tune policies, and integrate with your SIEM.
- **Audit third-party and SaaS configurations regularly.** OAuth integrations, API keys, and admin permissions in SaaS platforms accumulate over time. Periodic access reviews are a customer responsibility the model makes easy to overlook.
- **Include the model in onboarding for engineering teams.** Developers deploying services need to understand they inherit security obligations when they provision infrastructure. Make the shared responsibility model part of your cloud governance training, not just an architect-level concern.

---

## Key Takeaways

- The shared responsibility model defines what the cloud provider secures versus what the customer must secure — it does not imply the provider handles security comprehensively.
- Customer responsibility increases with IaaS and decreases with PaaS and SaaS, but it never reaches zero.
- AWS, Azure, and GCP all publish detailed versions of the model; the structural principle is consistent across all three.
- The most common security failures in cloud environments stem from customers misunderstanding or underestimating their side of the model — particularly around misconfiguration, identity governance, and unmonitored services.
- Treating the shared responsibility model as an operational framework, not just a conceptual one, is what separates organisations with mature cloud security from those that rely on assumptions.
