+++
title = "What is Zero Trust Architecture?"
date = "2026-06-08T09:25:28Z"
slug = "what-is-zero-trust-architecture"
description = "Zero Trust Architecture for cloud practitioners: why the perimeter model failed, identity as the new security boundary, MFA, conditional access policies, and practical implementation across AWS, Azure, and GCP."
keywords = ["zero trust", "identity", "least privilege", "network security"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"

[[faqs]]
question = "What is Zero Trust Architecture?"
answer = "Zero Trust Architecture is a security model based on the principle of never trust, always verify. Every user, device, and connection must be authenticated and authorised before accessing any resource, regardless of whether the request originates inside or outside the corporate network. It is defined in NIST SP 800-207 and recognised by NCSC, CISA, and all three major cloud providers as the foundational approach to modern security."

[[faqs]]
question = "What are the core principles of Zero Trust?"
answer = "The core principles of Zero Trust are: verify explicitly (authenticate and authorise every request using identity, device health, location, and other signals); use least privilege access (limit user and workload permissions to only what is required); and assume breach (design systems as if the network is already compromised, using micro-segmentation, end-to-end encryption, and continuous monitoring to limit blast radius)."

[[faqs]]
question = "How do you implement Zero Trust in AWS?"
answer = "Implementing Zero Trust in AWS involves: enforcing MFA and strong identity controls via IAM Identity Centre; applying least privilege IAM policies with regular access reviews; using AWS Verified Access for application-level access without VPN; implementing micro-segmentation with VPC security groups and Network Firewall; enabling CloudTrail, GuardDuty, and Security Hub for continuous monitoring; and using AWS Private Link to keep traffic off the public internet."

[[faqs]]
question = "What is the difference between Zero Trust and VPN?"
answer = "A VPN grants broad network access once a user authenticates — anyone inside the VPN tunnel can typically reach many internal resources. Zero Trust replaces this with per-application, per-request authorisation based on identity, device posture, and context. Zero Trust is more granular, harder to laterally traverse after a compromise, and better suited to cloud-native and hybrid environments where the traditional network perimeter no longer exists."
+++

Zero Trust is a security architecture built on the principle of never trust, always verify. Every user, device, and connection must be explicitly authenticated and authorised before accessing any resource, regardless of whether the request originates inside or outside the corporate network. It replaces the assumption that network location confers trust — the premise at the heart of traditional perimeter security, and the assumption that credential theft, phishing, insider threats, and supply chain compromises systematically exploit.

Zero Trust was formalised in NIST Special Publication 800-207 (2020) and is recognised by the UK NCSC, US CISA, and all three major cloud providers as the baseline security architecture for cloud and hybrid environments. Its operating mechanism: every session is authenticated using all available signals — identity, device health, location, and risk score — every resource access is authorised against policy, every action is logged, and access is continuously re-evaluated rather than granted once at login. No identity, human or machine, receives implicit trust based on network location alone.

---

## Why the Traditional Perimeter Model Failed

The classic castle-and-moat approach assumed that threats came from outside a well-defined boundary. Once a user or system was inside the perimeter — authenticated via VPN or simply present on the corporate LAN — they were largely trusted to move freely.

That model collapsed for several reasons:

- **Cloud adoption** dissolved the traditional perimeter. Workloads now run in AWS, Azure, and GCP, accessed from anywhere.
- **Remote and hybrid working** means users connect from home networks, coffee shops, and personal devices — locations the organisation neither controls nor trusts.
- **Lateral movement** became a primary attack vector. Threat actors who compromise a single endpoint can traverse the flat network and reach sensitive systems with minimal friction.
- **SaaS proliferation** means critical business data lives in Salesforce, Microsoft 365, and dozens of other platforms entirely outside the network boundary.

The perimeter didn't just weaken — it became effectively meaningless. Zero Trust architecture exists to fill that void.

---

## Identity as the New Perimeter

If the network boundary can no longer be trusted, something else must serve as the control plane. That something is **identity**.

In a Zero Trust model, identity — whether of a human user, a workload, a service account, or a device — is the primary signal for access decisions. Every access request is evaluated in context: who is requesting access, from what device, from which location, at what time, and to which resource.

This is why Identity and Access Management (IAM) is no longer purely an IT administration function — it is now a core security control. Key capabilities that support identity as the new perimeter include:

- **Multi-factor authentication (MFA)** — the baseline requirement for any Zero Trust deployment. Passwords alone are insufficient.
- **Conditional access policies** — granting or blocking access based on contextual signals such as device compliance status, user risk score, or geographic location.
- **Privileged Identity Management (PIM)** — enforcing just-in-time access for highly privileged roles to reduce the blast radius of compromised accounts.
- **Workload identity** — assigning managed identities or service accounts to compute resources and pipelines so that machine-to-machine authentication is equally rigorous.

Tools such as Microsoft Entra ID, Okta, and AWS IAM Identity Center all provide the underpinning for this identity-centric control model. The key architectural principle is that no identity — human or machine — should receive implicit trust based on network location alone.

---

## The Core Principles of Zero Trust

Several foundational principles define a mature Zero Trust architecture:

### Verify Explicitly
Every access request must be authenticated and authorised using all available signals. This goes beyond a username and password check — it encompasses device health, user behaviour analytics, session risk scoring, and data sensitivity.

### Enforce Least Privilege
Users and systems should have access to the minimum set of resources necessary to perform their function, and only for as long as needed. **Least privilege** is one of the most impactful controls in any security programme — unnecessarily broad permissions are a primary enabler of both insider threats and post-compromise lateral movement. In practice, this means regular access reviews, role-based access control (RBAC) scoped tightly to job function, and avoiding standing privileged access wherever possible.

### Assume Breach
Design systems and processes on the assumption that a breach has already occurred or will occur. This drives segmentation, strong logging and monitoring, encryption of data in transit and at rest, and incident response readiness. The goal is to contain the impact of a compromise, not merely to prevent initial access.

### Inspect and Log Everything
Zero Trust requires comprehensive visibility. Every access event, authentication attempt, and data transfer should be logged and, where feasible, analysed in near real-time. This telemetry feeds security information and event management (SIEM) platforms and enables threat detection that would be invisible in a purely perimeter-focused model.

---

## Practical Roadmap for Adopting Zero Trust in the Cloud

Zero Trust is not a product you buy — it is an architecture you build incrementally. The following phased approach reflects how mature organisations typically progress.

### Phase 1 — Establish Strong Identity Foundations
Before anything else, get your identity infrastructure right:
- Enforce MFA across all users without exception.
- Integrate cloud workloads with a centralised identity provider.
- Eliminate shared service accounts and rotate all credentials.
- Audit existing permissions and remove entitlements that violate least privilege.

This phase alone eliminates a large proportion of common attack paths.

### Phase 2 — Implement Device Trust
An authenticated user on a compromised device is still a risk. Integrate mobile device management (MDM) or endpoint detection and response (EDR) telemetry into your conditional access policies. Block or restrict access from unmanaged or non-compliant devices. In AWS or Azure environments, leverage integration between your endpoint management platform and your identity provider to enforce device compliance as an access condition.

### Phase 3 — Micro-Segment Your Network
Replace flat network architectures with **micro-segmentation** — isolating workloads so that even if one system is compromised, lateral movement is constrained. In cloud environments, this is achieved through:
- VPC/VNet segmentation with strict security group and network ACL policies.
- Service mesh architectures (Istio, AWS App Mesh) for workload-to-workload mTLS.
- Private endpoints and service perimeters to prevent data exfiltration paths.

### Phase 4 — Protect Data Directly
Apply controls at the data layer rather than relying solely on network perimeter controls. This includes data classification, information rights management, and data loss prevention (DLP) policies applied to sensitive content regardless of where it travels.

### Phase 5 — Continuous Monitoring and Adaptive Access
Mature Zero Trust deployments use continuous validation — not just point-in-time authentication. User and Entity Behaviour Analytics (UEBA) can detect anomalies mid-session and trigger step-up authentication or access revocation without waiting for a human analyst to intervene.

---

## What Architects Should Do

- **Start with an asset inventory.** You cannot apply Zero Trust controls to resources you don't know exist. Map all users, devices, workloads, and data flows first.
- **Treat identity as infrastructure.** Apply the same rigour to IAM configurations that you apply to network and compute security. Misconfigured roles and overly permissive policies remain among the leading causes of cloud breaches.
- **Don't boil the ocean.** Identify your most sensitive systems and apply Zero Trust controls there first. A risk-prioritised approach delivers measurable security improvements faster than attempting a full-estate transformation simultaneously.
- **Measure least privilege continuously.** Use cloud-native tools such as AWS IAM Access Analyzer or Microsoft Entra Permission Management to identify and remediate excessive entitlements on an ongoing basis.
- **Align with a recognised framework.** NIST SP 800-207 is the authoritative reference for Zero Trust architecture and provides detailed guidance on deployment models and use cases.

---

## Key Takeaways

- **Zero Trust** is a strategic security model, not a single product — "never trust, always verify" applies to every user, device, and workload, regardless of network location. NIST SP 800-207 is the authoritative implementation reference.
- **Identity** has replaced the network boundary as the primary security perimeter. Rigorous IAM — MFA, least privilege, conditional access, short-lived credentials — is the operational foundation, not an add-on.
- **Least privilege and assume-breach** are the two principles with the highest direct impact on real-world risk: least privilege limits blast radius; assume-breach drives segmentation, logging, and detection investment.
- **Cloud adoption makes Zero Trust more achievable**, not less — AWS IAM Identity Centre, Microsoft Entra ID, and GCP Workforce Identity Federation provide the federation and conditional access capabilities that Zero Trust requires.
- **Adoption is sequential:** identity foundations first (MFA, federation, access reviews), then device trust, then network micro-segmentation, then data-layer controls. Each phase delivers measurable risk reduction independently.


## Related Guides

- [Cloud Security Posture Management (CSPM)](/guides/what-is-cspm-cloud-security-posture-management/) — CSPM tools are a core enforcement mechanism for Zero Trust in cloud environments, providing continuous visibility into misconfigurations and policy violations.
- [Cloud Infrastructure Entitlement Management (CIEM)](/guides/what-is-ciem-cloud-infrastructure-entitlement-management/) — Zero Trust's least-privilege principle depends on granular identity controls. CIEM provides the tooling to discover and enforce entitlement boundaries across cloud identities.
- [AWS IAM Security Best Practices](/guides/aws-iam-security-best-practices/) — Implementing Zero Trust on AWS begins with a hardened IAM configuration. This guide covers the specific controls and policies required.
- [Kubernetes Security Best Practices](/guides/kubernetes-security-best-practices/) — Applying Zero Trust principles within Kubernetes clusters, including network policy enforcement and workload identity.
- [The Shared Responsibility Model in Cloud Security](/guides/shared-responsibility-model-cloud-security/) — Understanding where your Zero Trust responsibilities begin and where the cloud provider's end.
- [Cross-Cloud Security Services Comparison](/guides/aws-azure-gcp-security-service-comparison/) — Compare the native Zero Trust and identity enforcement tools available across AWS, Azure, and GCP.
