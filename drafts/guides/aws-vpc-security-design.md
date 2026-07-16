---
title: "AWS VPC Security Design: A Practitioner's Guide to Building a Defensible Network Foundation"
date: 2026-07-16
description: "A technical deep-dive into AWS VPC security design covering subnet architecture, security controls, encryption, monitoring, and common pitfalls to avoid."
tags: ["aws", "vpc", "network-security", "cloud-security", "aws-security"]
slug: "aws-vpc-security-design"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2227
draft: false
---

# AWS VPC security design: a practitioner's guide to building a defensible network foundation

If you are running workloads on AWS, your VPC architecture is not a networking concern. It is a security concern.

Every EC2 instance, RDS database, Lambda function, and container runs inside a VPC. If the network layer is misconfigured, attackers can move laterally, exfiltrate data, or reach resources that should never be publicly accessible, regardless of how well you have configured IAM or encryption. AWS has been raising the floor, with VPC Block Public Access arriving in November 2024 and VPC Encryption Controls following in November 2025, yet misconfigured VPCs remain one of the most reliable attack paths in cloud environments today. This guide covers the architectural decisions and service-level controls that separate a defensible VPC from a liability.

<!-- INTERNAL_LINK: AWS Well-Architected Security pillar | aws-well-architected-security -->
<!-- INTERNAL_LINK: Cloud network security fundamentals | cloud-network-security -->

---

## Why VPC security design matters more than ever

In 2025, multiple real-world incidents demonstrated what poor VPC hygiene actually costs. A misconfigured security group exposing port 22 to the internet led to a full EC2 compromise and lateral movement across an organisation's production environment. In a separate incident, attackers used overly permissive egress rules to exfiltrate data via DNS tunnelling before GuardDuty alerted the team.

From a compliance standpoint, the UK context adds another dimension. The NCSC's 14 Cloud Security Principles set out what UK cloud users and cloud service providers should implement to maintain a defensible security posture. AWS provides conformance packs through AWS Config that map to these principles, helping customers implement appropriate controls on their side of the shared responsibility model. For FCA-regulated firms, getting VPC architecture right is not optional. It underpins your ability to demonstrate network segmentation, data-in-transit protection, and controlled access across your cloud estate.

---

## Foundational architecture: subnet design and account isolation

The first and most consequential decision in VPC security design is how you structure subnets and isolate workloads. Getting this wrong is expensive to undo.

### Public vs. private subnet separation

Public subnets should exist only for ALBs and API Gateways. Private subnets should house RDS, ECS, and EKS workers with no direct internet paths. This is the correct default posture. The moment you place a database or application server in a public subnet, you are betting on your security group rules being correct, indefinitely.

Public subnets host resources that need to be reachable from the internet, such as load balancers. Private subnets contain databases and application servers that should never be directly accessible.

### Multi-AZ deployment

Create subnets across multiple Availability Zones. An Availability Zone is one or more discrete data centres with redundant power, networking, and connectivity in an AWS Region. Do not treat multi-AZ as a reliability feature only. A single-AZ VPC means a single blast radius.

### Account and environment isolation

Split your production, staging, and pre-production environments across different VPCs. This limits the blast radius if a breach occurs. In multi-account AWS Organisation architectures, you can use Transit Gateway route table associations and propagations, attaching development VPCs to a route table that has no propagation from production attachments, to prevent development VPCs from communicating with production VPCs through a Transit Gateway, which acts as a centralised router.

### CIDR planning

Plan your address space before you build, not after. All VPC connectivity options require non-overlapping IP ranges. Before assigning CIDR blocks, map every network you may ever need to connect to, including remote networks, data centres, offices, and other AWS VPCs. None of these should conflict or overlap. Mergers, acquisitions, and Direct Connect connections are where CIDR debt becomes acutely painful.

---

## Layered security controls: security groups, NACLs, and Network Firewall

Effective VPC security relies on multiple overlapping control layers, not a single firewall rule set.

### Security groups: your stateful instance firewall

Security groups are stateful firewalls attached to ENIs (Elastic Network Interfaces). They are the primary network access control for EC2 instances, RDS databases, ECS tasks, Lambda functions, and most other VPC resources. A single overly permissive rule can expose critical infrastructure to the entire internet.

Two rules worth enforcing immediately:

- Never allow `0.0.0.0/0` or `::/0` on ingress. Restrict source CIDRs to known ranges, use security group references for internal communication, and restrict ports to exact needs. Port ranges like `0-65535` are not acceptable.
- Reference security groups by ID, not by CIDR, for east-west traffic between tiers. This is more maintainable and less error-prone at scale.

### NACLs: your stateless subnet guard

Network Access Control Lists are stateless firewalls at the subnet level. Unlike security groups, NACLs evaluate inbound and outbound rules independently and process them in order by number. Use them for coarse-grained deny rules, such as blocking known bad CIDR ranges or enforcing subnet-to-subnet isolation, rather than trying to replicate security group logic at the subnet level. The NCSC's network security guidance is clear on this point: network segmentation is about breaking your network into smaller networks so you control how traffic flows and what access is permitted between them.

### AWS Network Firewall: layer 7 inspection

For mature environments, there are scenarios where you need a Layer 3-7 firewall or IPS/IDS within a multi-account environment to inspect traffic between VPCs (east-west) or between an on-premises data centre and a VPC (north-south). You can incorporate AWS Network Firewall with Transit Gateway in a centralised architecture. The hub-and-spoke model of Transit Gateway supports a simplified central deployment where Network Firewall sits in a dedicated security VPC.

<!-- INTERNAL_LINK: Cloud threat detection and response | cloud-threat-detection -->

---

## VPC Block Public Access and Encryption Controls

Two features launched in 2024-2025 that every production estate should now be evaluating.

### VPC Block Public Access

VPC Block Public Access lets you block resources in VPCs and subnets from reaching or being reached from the internet through internet gateways and egress-only internet gateways. Enable it in Block ingress mode as a baseline for all accounts in your organisation, and use SCP-based guardrails to prevent member accounts from disabling it. For financial services environments where internet-routable compute is an exception rather than the norm, this is one of the more useful controls AWS has shipped in recent years.

### VPC Encryption Controls

VPC Encryption Controls lets you audit and enforce encryption in transit for all traffic within and across VPCs in a Region. Traditional approaches to tracking encryption compliance require piecing together multiple solutions and manually monitoring different network paths, which becomes increasingly unreliable as infrastructure scales.

---

## VPC endpoints and the data perimeter

Every time your private workload calls an AWS service, whether S3, Secrets Manager, KMS, or SQS, over a NAT Gateway, that traffic is taking an unnecessary excursion to the public internet. VPC endpoints are the fix.

Amazon VPC endpoints, powered by AWS PrivateLink, establish private connectivity to supported AWS services using private IP addresses, without requiring internet gateways or NAT devices.

There are three endpoint families to understand:

- Gateway endpoints are free and cover S3 and DynamoDB only. Deploy these immediately. There is no reason not to.
- Interface endpoints (PrivateLink) support a large and growing catalogue of AWS services, check the current AWS PrivateLink documentation for the up-to-date list. They carry per-ENI-per-AZ hourly charges, so centralise them in a hub VPC shared via Transit Gateway to avoid per-VPC cost sprawl.
- Gateway Load Balancer endpoints are the third family, used to transparently insert third-party or custom traffic inspection appliances into the data path via an endpoint service, without requiring you to manage the load balancer yourself in every consuming VPC.

Combined with VPC endpoint policies, these form the network dimension of AWS's data perimeter model. The framework uses three dimensions to control access: trusted identities, trusted resources, and expected networks. VPCs are the foundation of the network perimeter dimension. By combining VPC endpoints with endpoint policies, SCPs, and resource control policies, you can ensure that data flows only between authorised principals and resources.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: AWS compliance and governance | aws-compliance-and-governance -->

---

## Flow logs and log enrichment

You cannot defend what you cannot see. Enable VPC Flow Logs to monitor IP traffic going to and from a VPC, subnet, or network interface. Enable them at the VPC level at minimum. Subnet-level logging gives you more granularity for sensitive tiers.

This matters in large organisations where a VPC Flow Log entry containing a private IP address tells you almost nothing without knowing which team and service owns it. Enriching flow log entries with metadata, whether through a lookup table mapping ENI IDs or private IPs to service names, or through consistent resource tagging carried through to your logging pipeline, turns an opaque log stream into something you can actually act on.

For threat detection on top of flow logs, GuardDuty ingests VPC Flow Logs, DNS query logs, and CloudTrail management events as foundational data sources, analysing them together as part of its threat detection across accounts, containers, workloads, and data.

<!-- INTERNAL_LINK: AWS CloudTrail configuration best practices | aws-cloudtrail-configuration-best-practices -->
<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->

---

## Multi-account and Transit Gateway architecture

At scale, you are not managing one VPC. You are managing tens or hundreds across multiple accounts. AWS Transit Gateway provides a hub-and-spoke model for connecting VPCs and on-premises networks as a fully managed service, without requiring virtual appliances.

Transit Gateway can connect thousands of VPCs. You can attach all your hybrid connectivity, including VPN and Direct Connect connections, to a single gateway, consolidating your organisation's entire AWS routing configuration in one place. Route tables control how traffic moves among all the connected networks.

For security inspection at scale, place AWS Network Firewall in an inspection VPC using a centralised deployment model. This approach lets you inspect traffic across hundreds or thousands of VPCs and accounts from a single point, covering traffic between VPCs, the internet, and on-premises networks.

Share the Transit Gateway across accounts using AWS RAM. AWS Resource Access Manager lets you share a Transit Gateway instance for connecting VPCs across multiple accounts in your AWS Organisation within the same Region.

---

## Common pitfalls in AWS VPC security design

These are the mistakes I see repeatedly in production environments, often during incident response rather than design review.

**1. Using the default VPC for production workloads.** The default VPC has all components configured in a way that is quite open to the world, and it has no private subnets. Treat the default VPC as a lab environment and nothing more.

**2. Leaving default security groups uncustomised.** The default group often allows all outbound traffic. Customise it immediately after you create a VPC.

**3. Flat VPC design with no subnet tiering.** If your database and your load balancer are in the same subnet with the same route table, you have no meaningful network boundary. Flat VPC designs expose internal databases to internet scanners within hours.

**4. Overlapping CIDR blocks.** At design time this is a five-minute conversation. After the fact, when you need to peer VPCs or connect via Direct Connect, it becomes a multi-month migration. Plan your address space once, correctly.

**5. Enabling VPC Encryption Controls in enforce mode without running monitor mode first.** Go straight to enforce and you will prevent legitimate plaintext workloads from starting, including legacy instances that do not support Nitro-based transparent encryption. Start in monitor mode, fix application-layer encryption gaps, then switch to enforce.

**6. Neglecting GuardDuty in unused regions.** Enable GuardDuty in every region, including regions you do not actively use. Attackers frequently spin up resources in regions they know teams are not watching.

**7. Not centralising VPC interface endpoints.** Deploying one interface endpoint per VPC per service will drain your budget quietly. Centralise them in a networking account and route spoke VPCs through Transit Gateway. In a Landing Zone setup where multiple VPCs need to interact with the same AWS service, hosting interface endpoints in a centralised VPC and accessing them via Transit Gateway avoids both the cost and the management overhead.

---

## Key takeaways

Start with subnet tiering and account isolation. Public subnets for ingress only, private subnets for every stateful workload, and separate prod, staging, and dev into distinct VPCs from day one.

Layer your controls. Security groups handle stateful instance-level control. NACLs provide stateless subnet-level deny rules. AWS Network Firewall handles Layer 7 inspection in a centralised security VPC. None of these replace the others.

Deploy VPC Block Public Access and plan carefully for VPC Encryption Controls. BPA is free and should be your default posture. Encryption Controls require a careful rollout, monitor first then enforce.

Replace NAT Gateway egress to AWS services with VPC endpoints. Gateway endpoints for S3 and DynamoDB are free with no reason to defer them. Centralise interface endpoints to avoid per-VPC cost sprawl.

Enable VPC Flow Logs everywhere and enrich them with ownership metadata so your security telemetry is actionable rather than opaque.

Audit regularly. CIDR overlap, unused security group rules, and disabled GuardDuty in unused regions are the three findings that appear most consistently in VPC security reviews. Automate detection of all three with AWS Config rules.

<!-- INTERNAL_LINK: What is zero trust architecture | what-is-zero-trust-architecture -->
<!-- INTERNAL_LINK: AWS compliance and governance | aws-compliance-and-governance -->
<!-- INTERNAL_LINK: What is CSPM | what-is-cspm-cloud-security-posture-management -->