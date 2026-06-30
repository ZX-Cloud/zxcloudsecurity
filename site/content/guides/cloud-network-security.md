+++
title = "Cloud Network Security: The Architect's Guide"
date = "2026-06-24T06:00:00Z"
slug = "cloud-network-security"
description = "Cloud network security explained for architects — VPCs, security groups, micro-segmentation, WAF, DDoS protection, private connectivity, and network detection across AWS, Azure, and GCP."
keywords = ["cloud network security", "VPC security", "security groups", "network segmentation", "cloud firewall", "micro-segmentation", "cloud WAF", "DDoS protection", "AWS network security", "Azure network security"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"

[[faqs]]
question = "What is the difference between a security group and a network ACL in AWS?"
answer = "Security groups are stateful firewalls attached to individual resources (EC2 instances, RDS databases, Lambda functions in a VPC). They track connection state, so return traffic is automatically allowed without an explicit outbound rule. Network ACLs (NACLs) are stateless firewalls applied at the subnet level, evaluated before traffic reaches any resource. NACLs require explicit rules for both inbound and return traffic. In practice, security groups are the primary network control in AWS; NACLs provide a secondary defence layer for subnet-level blocking, particularly useful for blocking specific IP ranges that need to be stopped before they reach any resource in the subnet."

[[faqs]]
question = "What is micro-segmentation in cloud environments?"
answer = "Micro-segmentation is the practice of applying granular network controls between individual workloads rather than just at the perimeter. In cloud environments, this means: using security groups to restrict communication between EC2 instances even within the same subnet; applying Kubernetes NetworkPolicies to control pod-to-pod traffic within a cluster; using VPC endpoints rather than internet gateways for AWS service access; and designing VPC architecture with separate subnets for different trust tiers (public, application, data). Micro-segmentation limits lateral movement — a compromised workload cannot freely reach other services even within the same VPC."

[[faqs]]
question = "What is AWS PrivateLink and when should I use it?"
answer = "AWS PrivateLink creates private network connectivity between your VPC and AWS services or third-party services via interface VPC endpoints, without traffic traversing the public internet. Use PrivateLink when you need AWS API calls (S3, KMS, SSM, Secrets Manager) to stay within your network perimeter and not traverse the internet, when connecting to SaaS services that support PrivateLink without public IP exposure, and when you need to share a service between VPCs without VPC peering (which exposes entire CIDR ranges). PrivateLink endpoints are required for compliance in regulated environments where outbound internet access must be minimised."

[[faqs]]
question = "What is the difference between AWS WAF and AWS Network Firewall?"
answer = "AWS WAF is a web application firewall that inspects HTTP/HTTPS traffic at Layer 7, protecting CloudFront distributions, API Gateways, Application Load Balancers, and Bedrock endpoints from web exploits (OWASP Top 10), rate-based attacks, and bot traffic. AWS Network Firewall is a stateful network firewall operating at Layers 3–7, deployed in a VPC to inspect and filter all TCP/UDP traffic — not just web traffic. Use WAF for internet-facing web applications and APIs; use Network Firewall for VPC-level traffic inspection, outbound egress filtering, and east-west traffic control between subnets and VPCs."
+++

Cloud network security is the set of controls that govern how traffic moves into, out of, and between resources in a cloud environment — covering ingress and egress filtering, network segmentation, private connectivity, traffic inspection, and detection of anomalous network behaviour. It is structurally different from traditional network security: there is no physical perimeter, no hardware firewall appliance to configure, and no cable you can pull. Instead, the network itself is software-defined, provisioned via API, and controlled through policies attached to virtual constructs. That shift eliminates some traditional attack vectors and introduces entirely new ones.

This guide covers the core primitives every cloud architect must understand, the segmentation and filtering controls that matter most, how network security compares across AWS, Azure, and GCP, and the detection capabilities that make network threats visible.

---

## How Cloud Networking Differs from Traditional Network Security

In a traditional data centre, network security was built around physical segmentation: different VLANs, dedicated firewall appliances at zone boundaries, and DMZs that separated internet-facing services from internal infrastructure. The network topology was stable, changes required physical or out-of-band access, and security teams had reasonable visibility through NetFlow and perimeter logs.

Cloud networking inverts almost every assumption:

**The network is an API.** VPCs, subnets, security groups, routing tables, and network gateways are all created, modified, and destroyed programmatically. An engineer can change a security group rule, modify a route table, or peer two previously isolated VPCs in under a minute, from anywhere, without touching any physical infrastructure.

**Topology changes constantly.** Autoscaling groups add and remove instances in response to load. Container orchestrators schedule workloads across nodes. Serverless functions spin up and disappear. The network map at 09:00 may look entirely different at 11:00.

**East-west traffic dominates.** In microservices architectures, the volume of service-to-service traffic dwarfs the volume of north-south (internet) traffic. Traditional perimeter-focused controls miss the majority of the traffic — and the lateral movement that follows credential compromise.

**The shared responsibility model applies.** Cloud providers secure the physical network fabric — the cables, switches, and routers in their data centres, and the hypervisor networking layer. Everything built on top — VPC configuration, security group rules, routing, traffic inspection — is the customer's responsibility.

---

## Core Network Security Primitives

### Virtual Private Clouds

A Virtual Private Cloud (VPC) is a logically isolated network environment within a cloud provider's infrastructure. AWS, Azure (where the equivalent is a Virtual Network, or VNet), and GCP all use this model. Resources launched within a VPC are isolated from resources in other VPCs by default — they cannot communicate unless you explicitly configure routing or peering.

VPC design is a foundational security decision. Key principles:

- **Separate VPCs by environment**: production, staging, and development workloads should be in separate VPCs. Blast radius from a misconfiguration or compromise in dev should never reach production.
- **Use multiple availability zones**: distributing subnets across AZs provides resilience but also supports network security zoning — different AZs can host different security tiers.
- **Plan CIDR ranges carefully**: overlapping IP ranges prevent peering and cause operational problems. Use non-overlapping RFC 1918 ranges with room to grow.

### Security Groups and Network ACLs

Security groups (AWS), Network Security Groups (Azure NSGs), and firewall rules (GCP) are the primary ingress and egress controls on cloud compute resources. They function as stateful, instance-level firewalls: you define rules by protocol, port, and source/destination, and the cloud platform enforces them on every packet.

Network ACLs (NACLs in AWS) operate at the subnet level and are stateless — both directions of traffic must be explicitly permitted. They provide a second layer of control that security groups alone cannot offer: you can use NACLs to block traffic from specific CIDRs even if a security group rule would otherwise permit it.

Critical hygiene rules for security groups and NSGs:

- **Never use 0.0.0.0/0 as the source for inbound rules except on load balancers intentionally exposed to the internet.** Every other resource should accept traffic only from specific security groups or CIDR ranges.
- **Remove the default allow-all rules** that some environments inherit during provisioning.
- **Audit security groups regularly** for port 22 (SSH) and port 3389 (RDP) open to the internet. AWS Security Hub, Azure Defender, and GCP Security Command Center all flag these automatically.
- **Use security group references, not CIDRs, for inter-service traffic** — when Service A needs to communicate with Service B, reference Service B's security group as the source, not a CIDR range that may expand unpredictably.

### Subnets and Routing

Subnets divide a VPC into smaller network segments, each associated with a routing table. The routing table determines where traffic goes: to the internet via an internet gateway, to other VPCs via peering or Transit Gateway, to on-premises networks via VPN or Direct Connect, or nowhere.

**Public subnets** have a route to an internet gateway. Resources in public subnets are reachable from the internet if they have a public IP and a permissive security group.

**Private subnets** have no direct route to the internet. Resources in private subnets can reach the internet through a NAT gateway (for egress-only connectivity) but cannot be reached from it directly.

The correct model for most workloads: application and data tier in private subnets, with a load balancer in a public subnet handling internet-facing traffic. Nothing in the data tier should have a route to the internet.

---

## Network Segmentation and Micro-Segmentation

### Account and VPC Segmentation

At the broadest level, cloud environments should be segmented by AWS account, Azure subscription, or GCP project. This is the most effective blast-radius control available: a compromised role in Account A cannot directly affect resources in Account B without a trust relationship explicitly configured between them. AWS Organizations, Azure Management Groups, and GCP folders provide the management layer above this.

Within a single account, VPC-level segmentation provides the next tier. Workloads with different security classifications — PCI-scoped card processing, internet-facing web tiers, internal tooling — should live in separate VPCs with explicit, minimal peering relationships.

### Micro-Segmentation for East-West Traffic

Micro-segmentation applies security controls at the workload level — per container, per pod, per function — rather than at the network perimeter. It addresses the fundamental weakness of perimeter-only controls: once traffic is inside a trusted zone, it can move laterally with little resistance.

In Kubernetes environments, **Network Policies** (implemented by the CNI plugin — Calico, Cilium, or equivalent) define which pods can communicate with which other pods. A pod in the payments namespace should not be able to reach pods in the logging namespace unless that connection is explicitly permitted. Default-deny Network Policies with specific allow rules is the correct baseline.

For VM-based workloads, security group rules that permit traffic only from specific security groups (rather than broad CIDRs) achieve similar micro-segmentation. For service mesh environments, mutual TLS (mTLS) between services — enforced by Istio, Linkerd, or AWS App Mesh — provides cryptographic identity verification alongside traffic filtering.

---

## Ingress Controls: WAF and DDoS Protection

### Web Application Firewall

A cloud WAF sits in front of internet-facing applications and filters HTTP/HTTPS traffic before it reaches application code. It provides protection against OWASP Top 10 vulnerabilities — SQL injection, cross-site scripting, command injection — and can enforce rate limits, geo-blocking, and IP reputation filtering.

| Service | Provider | Key Capabilities |
|---|---|---|
| AWS WAF | AWS | Managed rule groups, rate limiting, Bot Control, Fraud Control, integration with CloudFront/ALB/API Gateway |
| Azure Web Application Firewall | Azure | OWASP Core Rule Set, custom rules, integration with Application Gateway and Front Door |
| Cloud Armor | GCP | Adaptive protection (ML-based), preconfigured WAF rules, geo-blocking, integration with Cloud Load Balancing |

WAF is a meaningful control, but it is not a substitute for secure application code. A WAF can be bypassed by a sufficiently crafted payload, misconfigured to permit traffic it should block, or bypassed entirely if the application is accessible via a path that doesn't route through the WAF.

### DDoS Protection

All three major cloud providers offer baseline DDoS protection at no additional cost — absorbing volumetric attacks that would overwhelm on-premises connectivity. AWS Shield Standard, Azure DDoS Protection Basic, and GCP Cloud Armor's basic mode are automatically applied.

For higher-risk workloads, enhanced DDoS services provide additional capabilities: AWS Shield Advanced (24/7 DRT access, cost protection, application-layer attack detection), Azure DDoS Network Protection (adaptive tuning, telemetry, attack analytics), and GCP Cloud Armor's Managed Protection Plus tier.

---

## Private Connectivity

### VPN

Site-to-site VPN connects on-premises networks to cloud VPCs over encrypted tunnels across the public internet. AWS Site-to-Site VPN, Azure VPN Gateway, and GCP Cloud VPN provide this capability. VPN is the correct starting point for hybrid connectivity: it is straightforward to configure, requires no physical provisioning, and provides encrypted connectivity for moderate bandwidth requirements.

Limitations: VPN tunnels traverse the public internet, introducing variable latency. Bandwidth is constrained by the internet connection on the on-premises side and the VPN gateway throughput limit in the cloud.

### Dedicated Private Connectivity

For production workloads with high bandwidth, low latency, or regulatory requirements for private connectivity, dedicated circuits bypass the public internet entirely:

- **AWS Direct Connect**: dedicated 1 Gbps or 10 Gbps connections from AWS Direct Connect locations to AWS regions
- **Azure ExpressRoute**: private connections via connectivity partners or directly from co-location facilities to Azure
- **GCP Cloud Interconnect**: Dedicated Interconnect (direct) or Partner Interconnect (via connectivity provider)

These connections do not traverse the public internet. Traffic between on-premises and cloud is encrypted at the application layer (TLS) or optionally at the tunnel layer (MACsec for Direct Connect, IPsec for VPN overlays on dedicated circuits). Compliance frameworks that prohibit data traversing the public internet — certain PCI DSS and UK government requirements — typically require dedicated connectivity.

### VPC Peering and Transit Architectures

**VPC peering** connects two VPCs with a direct routing relationship. Traffic travels on the provider's backbone, not the public internet. Peering is non-transitive: if VPC A peers with VPC B and VPC B peers with VPC C, VPC A cannot route to VPC C through B without an additional peering relationship.

At scale, VPC peering becomes unmanageable — N*(N-1)/2 relationships for N VPCs. **AWS Transit Gateway**, **Azure Virtual WAN**, and **GCP Network Connectivity Centre** provide hub-and-spoke architectures where all VPCs connect to a central routing plane, eliminating the mesh of peering relationships. Transit Gateway also supports routing policies, attachment-level security groups, and integration with SD-WAN.

---

## Network Detection and Monitoring

### Flow Logs

Every major cloud provider captures metadata about network traffic at the VPC level:

- **AWS VPC Flow Logs**: source IP, destination IP, protocol, port, bytes, packets, action (ACCEPT/REJECT) for each traffic flow
- **Azure Network Watcher NSG Flow Logs**: equivalent metadata for traffic through NSGs
- **GCP VPC Flow Logs**: flow records at the VM network interface level

Flow logs are the foundation of cloud network detection. They do not capture packet contents, but the metadata is sufficient to identify port scanning, unusual outbound connections to new external IPs, lateral movement between subnets, and data exfiltration by volume. Route flow logs to a SIEM or detection platform — AWS Security Lake, Microsoft Sentinel, Chronicle — where anomaly detection and correlation can run continuously.

### Network Threat Detection

| Service | Provider | What It Detects |
|---|---|---|
| AWS GuardDuty | AWS | Malicious IPs, DNS-based C2, port scanning, crypto-mining via VPC Flow Log and DNS log analysis |
| Microsoft Defender for Cloud | Azure | Suspicious network activity, lateral movement, unusual outbound connections |
| GCP Security Command Center | GCP | Anomalous network activity, open firewall rules, unusual data exfiltration patterns |
| Network Detection and Response (NDR) tools | Third-party | Deep packet inspection, encrypted traffic analysis, ML-based anomaly detection |

GuardDuty's network findings — particularly C2 activity via DNS and unusual outbound connections on uncommon ports — have proven reliable in practice and are worth enabling in every AWS account. The signal-to-noise ratio is considerably better than raw flow log alerting.

---

## Cross-Cloud Network Security Comparison

| Capability | AWS | Azure | GCP |
|---|---|---|---|
| Network isolation unit | VPC | Virtual Network (VNet) | VPC |
| Instance-level firewall | Security Groups | Network Security Groups (NSGs) | Firewall Rules |
| Subnet-level firewall | Network ACLs (stateless) | NSGs applied to subnet | VPC firewall (stateful) |
| Internet gateway | Internet Gateway | Default internet access | Cloud Router + Internet Gateway |
| NAT for private subnets | NAT Gateway | NAT Gateway | Cloud NAT |
| Web Application Firewall | AWS WAF | Azure WAF | Cloud Armor |
| DDoS (enhanced) | Shield Advanced | DDoS Network Protection | Cloud Armor Managed Protection |
| Private connectivity | Direct Connect | ExpressRoute | Cloud Interconnect |
| Hub-and-spoke routing | Transit Gateway | Virtual WAN | Network Connectivity Centre |
| Network flow logs | VPC Flow Logs | NSG Flow Logs | VPC Flow Logs |
| Network threat detection | GuardDuty | Defender for Cloud | Security Command Center |

---

## What Architects Should Do

**Enforce private subnets as the default for workloads.** Every compute resource — EC2, AKS node, Cloud Run service — should launch into a private subnet with no direct route to the internet. The only resources in public subnets should be load balancers, NAT gateways, and bastion hosts (ideally replaced by Systems Manager Session Manager or equivalent). Audit for public subnets containing compute; many environments have accumulated these through expedient provisioning.

**Apply default-deny security group rules and audit exceptions.** Start from a position of no inbound access and add rules only when a specific, documented communication path requires it. Review every rule that permits inbound access from 0.0.0.0/0 quarterly. AWS Security Hub's FSBP controls, Azure Policy, and GCP Security Command Center surface security group misconfigurations automatically.

**Enable VPC Flow Logs on every VPC and route them to a central store.** Flow logs have a cost but provide the foundational network visibility that makes detection and incident response possible. Without them, you are investigating post-incident with a significant evidence gap. Route logs to a centralised S3 bucket or Log Analytics workspace with lifecycle policies — 90 days hot, 12 months archived is a reasonable baseline.

**Enable GuardDuty (or equivalent) in every account.** GuardDuty, Azure Defender for Cloud network detection, and GCP SCC network findings provide continuous, low-noise detection of the network threat patterns most likely to appear in real attacks: C2 communication, port scanning, unusual outbound connections. The cost is low relative to the detection value.

**Segment Kubernetes workloads with Network Policies.** Default Kubernetes installs permit all pod-to-pod communication within a cluster. This is the correct behaviour for getting started but wrong for production. Apply default-deny Network Policies and explicitly permit only the communication paths that services actually need. Cilium's network policy visualiser or Calico's flow logs make the actual communication graph visible.

**Use VPC endpoints for AWS service traffic.** By default, traffic to AWS services (S3, DynamoDB, SQS) traverses the public internet even when originating from inside a VPC. VPC endpoints route this traffic through the AWS backbone, eliminating the public internet path. This is particularly important for data-tier services: an EC2 instance writing to S3 should never send that traffic out to the internet and back.

**Build private connectivity into your hybrid architecture from the start.** If on-premises connectivity is in scope, plan for Direct Connect or ExpressRoute before production workloads migrate. Retrofitting dedicated connectivity after the fact involves downtime and architectural changes that are difficult to schedule.

---

## Key Takeaways

- **Cloud network security is software-defined** — the network is an API, and security controls are policies attached to virtual constructs, not physical appliances. This enables more granular control but also means misconfigurations are instant and globally effective.
- **The shared responsibility boundary applies to networking** — the cloud provider secures the physical network fabric; the customer is responsible for VPC design, security group rules, routing, and traffic inspection.
- **East-west traffic is the blind spot** — perimeter controls protect north-south traffic, but lateral movement after credential compromise travels east-west between services. Micro-segmentation and Network Policies are the controls that address this.
- **Flow logs are non-negotiable** — network detection and incident investigation both depend on VPC flow log data. Enable them in every VPC from day one.
- **Private subnets and default-deny security groups should be the baseline** — not a hardening step applied after an incident.

---

## Related Guides

- [Zero Trust Architecture](/guides/what-is-zero-trust-architecture/) — Cloud network security is the enforcement layer for Zero Trust; micro-segmentation and mTLS implement the "never trust, always verify" model at the network level.
- [Cloud Identity and Access Management](/guides/cloud-identity-and-access-management/) — IAM and network controls are complementary; a compromised credential with broad network access is far more dangerous than one constrained by security group rules.
- [What is CSPM?](/guides/what-is-cspm-cloud-security-posture-management/) — CSPM tools continuously surface network misconfigurations — open security groups, public subnets with compute, disabled flow logs — that manual audits miss.
- [Kubernetes Security Best Practices](/guides/kubernetes-security-best-practices/) — Network Policies, CNI plugin configuration, and service mesh are the network security layer for Kubernetes workloads.
- [Cloud Threat Detection](/guides/cloud-threat-detection/) — VPC Flow Logs and GuardDuty network findings are primary inputs to cloud threat detection programmes.
- [AWS Security Hub: A Practitioner's Guide](/guides/aws-security-hub-guide/) — Security Hub aggregates network security findings from GuardDuty, Inspector, and Config Rules into a centralised view with compliance framework mapping.
- [AWS vs Azure vs GCP: Cloud Security Service Comparison](/guides/aws-azure-gcp-security-service-comparison/) — Cross-cloud mapping of WAF, DDoS, private connectivity, and network detection services.
