+++
title = "Cloud Threat Detection: A Practitioner's Guide"
date = "2026-06-24T06:00:00Z"
slug = "cloud-threat-detection"
description = "Cloud threat detection explained for security architects — signal sources, detection categories, native vs third-party tooling, and how to build a detection programme that actually works across AWS, Azure, and GCP."
keywords = ["cloud threat detection", "GuardDuty", "Microsoft Sentinel", "cloud SIEM", "threat detection AWS", "cloud security monitoring", "CloudTrail analysis", "security operations cloud"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

Cloud threat detection is not a product you buy — it is a discipline you build. The cloud gives you access to more security signal than any on-premises environment could generate, but that abundance is also the problem. Without deliberate architecture, you drown in logs while the attacks that matter go undetected. This guide covers what cloud threat detection actually requires: the signal sources, the threat categories worth instrumenting, the native and third-party tooling landscape, and the architectural decisions that determine whether your detection programme catches real attacks or generates expensive noise.

---

## Why Cloud Detection Is Fundamentally Different

Security teams with on-premises backgrounds often approach cloud detection the way they approached network monitoring: point a SIEM at the perimeter, write rules for known-bad signatures, and wait for alerts. This fails in cloud environments for several structural reasons.

**The perimeter does not exist.** In a cloud environment, the attack surface is the API. Every action — provisioning a resource, reading an object, assuming a role, invoking a Lambda function — is an authenticated API call. The meaningful signal is not network traffic crossing a boundary; it is API call patterns, identity behaviour, and privilege usage. Threat detection in cloud starts with audit logs, not network taps.

**Identity is the primary attack surface.** The majority of significant cloud breaches in recent years — Capital One, Codecov, CircleCI — involved credential compromise or privilege escalation via IAM. An attacker with a valid set of AWS access keys or an Azure service principal token looks, from a network perspective, exactly like a legitimate user. Detection requires understanding what normal credential behaviour looks like and surfacing deviations from it.

**Resources are ephemeral and numerous.** A cloud environment can spin up hundreds of compute instances, containers, and serverless functions in minutes, then destroy them. Detection systems built around static asset inventories break when the assets change faster than the inventory updates.

**Multi-account and multi-cloud complexity.** Lateral movement in cloud environments often traverses account boundaries via IAM role chaining, cross-account trust relationships, or shared identity providers. Detection that operates at the single-account level misses this pattern entirely.

---

## Detection Signal Sources

Effective cloud threat detection is built on four categories of signal. Most detection failures trace back to gaps in signal coverage, not gaps in detection rules.

### Cloud Audit Logs

Cloud audit logs are the backbone of threat detection. Every cloud provider generates comprehensive logs of control-plane API activity:

- **AWS CloudTrail** records every API call made to AWS services — who made the call, from where, what parameters were passed, and whether it succeeded. Management events (resource creation, modification, deletion) and data events (S3 GetObject, Lambda invocations) require separate configuration. CloudTrail organisation trails, enabled at the organisation level and centralised to a single logging account, are the correct baseline — account-level trails miss the cross-account picture.
- **Azure Activity Log** captures control-plane operations across Azure subscriptions. Combined with Microsoft Entra ID sign-in logs and audit logs, it covers the identity and resource management surface. Diagnostic settings must be configured to route logs to a destination — they do not flow anywhere by default.
- **GCP Cloud Audit Logs** comprise Admin Activity logs (always on, no charge), Data Access logs (must be enabled per service), and System Event logs. Organisation-level log sinks to BigQuery or Cloud Storage are the right architecture for centralised detection.

The single most impactful action most cloud security teams can take is ensuring all audit logs are centralised, tamper-evident, and queryable in a single location. Logs that live in individual accounts or subscriptions cannot support cross-account detection and are vulnerable to destruction by a compromised administrator.

### Network Flow Logs

Network flow logs capture connection metadata — source IP, destination IP, port, protocol, bytes transferred, and whether the connection was accepted or rejected. They do not capture payload content, but connection patterns are often sufficient to detect data exfiltration, command-and-control communications, and lateral movement.

- **AWS VPC Flow Logs** can be enabled at the VPC, subnet, or ENI level. Enable at the VPC level for comprehensive coverage, and route to CloudWatch Logs or S3. Consider enabling flow logs on Transit Gateways for cross-VPC visibility.
- **Azure NSG Flow Logs** and **Virtual Network Flow Logs** (now generally available) capture equivalent data. Route to a storage account and optionally to Azure Traffic Analytics for aggregated visualisation.
- **GCP VPC Flow Logs** are enabled per subnet. Log sampling rates default to 0.5 — increase to 1.0 for environments where comprehensive visibility matters more than cost.

### DNS Logs

DNS telemetry is underused in cloud environments and disproportionately valuable. Data exfiltration over DNS, command-and-control callbacks, and DGA (domain generation algorithm) malware all produce distinctive DNS patterns that flow logs and audit logs may not surface.

AWS Route 53 Resolver query logging captures DNS queries made from within your VPCs — enable it across all VPCs and route to CloudWatch Logs. Azure Private DNS zones and Azure Firewall DNS proxy can log DNS queries. GCP Cloud DNS query logging is available per managed zone.

### Runtime and Workload Signals

Audit logs and flow logs cover the cloud control plane. For the workload layer — what is running inside your instances and containers — you need runtime signals: process execution, file system changes, network connections from within the workload, and container escape attempts.

AWS GuardDuty Runtime Monitoring (for EC2, ECS, and EKS) uses a lightweight eBPF agent to capture process-level activity. Microsoft Defender for Servers provides similar coverage on Azure VMs. Google Security Command Center's Container Threat Detection monitors GKE workloads for container escape and privilege escalation.

Third-party runtime security platforms — Falco (open source), Aqua, Sysdig — provide deeper coverage with more customisable rulesets, particularly for container-heavy environments.

---

## Threat Categories to Instrument

Not all threats are equally likely or equally detectable. A useful detection programme is built around the threat categories most relevant to cloud environments.

### Credential Compromise

Compromised credentials are the most common initial access vector in cloud environments. Indicators include:

- API calls from unusual geographic locations or IP reputation categories (Tor exit nodes, VPN providers, residential proxies)
- Access key usage outside of expected time windows or from unexpected source IPs
- First-time use of a principal that has been dormant for an extended period
- Sudden increase in Describe/List API calls following initial access — characteristic of an attacker enumerating the environment
- Console sign-in without MFA for accounts where MFA has historically been used

AWS GuardDuty's `UnauthorizedAccess` and `PenTest` finding families cover many of these patterns. The challenge is building enough behavioural baseline that deviations are meaningful — generic rules produce high false-positive rates.

### Privilege Escalation

An attacker who has obtained low-privilege credentials will typically attempt to escalate. Cloud privilege escalation paths are well-documented — `iam:CreatePolicyVersion`, `iam:AttachRolePolicy`, `iam:PassRole` combined with service creation, `sts:AssumeRole` chaining — and are detectable from CloudTrail if you are watching for them.

Key detection signals: IAM policy modifications (particularly additions of `*` permissions or removal of boundary conditions), creation of new access keys for existing principals, new cross-account trust relationships being established, and SCP modifications at the organisation level.

### Lateral Movement

In multi-account AWS environments, lateral movement typically occurs via `sts:AssumeRole` across accounts. Detecting this requires correlating CloudTrail from multiple accounts — which is precisely why organisation-level trail centralisation matters. Look for role assumption chains that traverse account boundaries in unusual sequences, or that involve accounts not previously seen in the assume-role history of a given principal.

In Azure, lateral movement often involves Managed Identity credential misuse or Entra ID token theft and replay. In GCP, service account key exposure and Workload Identity Federation misconfigurations are common vectors.

### Data Exfiltration

Large-scale data access and egress produces detectable signals. Relevant patterns include:

- S3 GetObject request volumes significantly above baseline for a given principal
- S3 bucket ACL or policy changes making buckets public
- Unusual API export operations — RDS snapshots shared with external accounts, DynamoDB table exports, EBS snapshot copies to attacker-controlled accounts
- VPC flow log anomalies: large outbound data transfers to novel destinations, particularly on uncommon ports
- S3 Glacier restore requests followed by bulk download activity

### Persistence Mechanisms

Attackers who establish initial access will attempt to maintain it. Common cloud persistence techniques include:

- Creating new IAM users or access keys on existing principals
- Modifying Lambda function code to include backdoors
- Establishing new EC2 instances with persistent SSH access or user-data scripts
- Modifying CloudTrail configuration to disable logging or exclude specific event types (a critical detection signal in itself)
- Creating new OAuth applications or service principals in Azure Entra ID

Detecting persistence requires monitoring for these configuration changes in near-real-time and correlating them with the access patterns that preceded them.

### Cryptomining

Cryptomining is lower-severity but high-volume and often an indicator of a broader compromise. Detection signals: GPU or high-CPU instance launches in regions not typically used, security group modifications opening inbound ports associated with mining pool protocols, DNS queries or network connections to known mining pool endpoints, and sudden spikes in compute spend triggering billing alerts.

---

## Native Tooling vs. Third-Party Platforms

### Native Detection Services

Every major cloud provider offers managed threat detection:

**AWS GuardDuty** analyses CloudTrail, VPC Flow Logs, and DNS logs using machine learning and threat intelligence to generate findings categorised by finding type, severity, and affected resource. Runtime Monitoring extends coverage to workloads. GuardDuty is the correct baseline for any AWS environment — it is cost-effective, requires no log infrastructure to operate, and reduces time-to-detection for common cloud attack patterns significantly. Enable it at the organisation level via delegated administrator.

**Microsoft Defender for Cloud** combines posture management with threat protection across Azure services. Defender plans — for Servers, Storage, SQL, Containers, Key Vault, and others — are enabled per resource type and generate alerts that feed into Microsoft Sentinel. For Azure-native environments, Sentinel provides the SIEM and SOAR layer with prebuilt detection rules (analytics rules) for common attack scenarios.

**Google Security Command Center Premium** includes Event Threat Detection, which analyses Cloud Audit Logs and VPC Flow Logs for attack patterns. Container Threat Detection covers GKE runtime. For Google-native environments, Security Command Center is the equivalent baseline.

### Third-Party Detection Platforms

Where native tooling excels at single-cloud depth, third-party platforms address multi-cloud normalisation, enriched detection logic, and integration with enterprise security workflows.

**Panther** and **Matano** are cloud-native SIEM platforms built specifically for cloud telemetry — they ingest cloud logs at scale, support detection-as-code (Python rules in version control), and integrate with cloud-native storage and compute. They are better suited to cloud-heavy environments than traditional SIEMs designed around syslog and on-premises data sources.

**Wiz** and **Orca Security** offer threat detection capabilities as part of their CSPM platforms — correlating runtime signals with configuration context to prioritise the attacks that are most likely to succeed given the environment's actual exposure.

**Traditional SIEMs** (Splunk, IBM QRadar, Elastic SIEM) can ingest cloud logs but require significant engineering to normalise data across providers and build effective detection logic. They are appropriate where an organisation already has a mature SIEM investment and wants to extend it to cloud, but are not the recommended starting point for cloud-first environments.

---

## Detection Architecture: What to Build

The detection architecture that works for most cloud environments at scale:

**Centralise all logs first.** Before detection rules, before SIEM, before anything else — get CloudTrail, Azure Activity Log, and GCP Audit Logs flowing to a single, tamper-evident destination. AWS: organisation trail to a central logging account S3 bucket with object lock. Azure: Diagnostic settings to a central Log Analytics workspace. GCP: organisation log sink to Cloud Storage or BigQuery.

**Enable native detection immediately.** GuardDuty, Defender for Cloud, and Security Command Center are the fastest path to baseline coverage with the lowest operational overhead. Enable them at the organisation level. Route findings to a central aggregation point — AWS Security Hub, Azure Sentinel, or a third-party platform.

**Build detection-as-code.** Detection rules that live in a GUI are hard to review, test, version, and deploy. Treat detection logic as code: store rules in version control, test against historical log data, deploy via CI/CD, and review changes through pull requests. Panther's Python-based rules or Sigma rules (portable across SIEM platforms) are the right model.

**Instrument the highest-risk signals explicitly.** Native detection covers common patterns well. Custom detection rules should target the gaps: your specific account structure, the cross-account assume-role paths in your environment, the IAM roles that would represent catastrophic compromise if abused, and the data stores that represent your highest-value targets.

**Build for investigation, not just alerting.** Detection without investigation capability is a dead end. Ensure you have tooling — Amazon Detective, Microsoft Sentinel investigation graphs, or equivalent — that lets an analyst follow the thread from a GuardDuty finding through to related API calls, affected resources, and lateral movement paths.

---

## What Architects Should Do

- **Centralise organisation-level cloud audit logs before anything else** — without this, detection is incomplete and tampering risk is high
- **Enable GuardDuty, Defender for Cloud, and Security Command Center at the organisation level** — not account-by-account; the cross-account view is essential
- **Enable VPC Flow Logs and DNS query logging across all production VPCs** — network signal fills gaps that audit logs miss
- **Define and protect your critical detection infrastructure** — CloudTrail configuration changes, GuardDuty disablement, and Security Hub configuration should themselves generate high-priority alerts with restricted remediation permissions
- **Build detection rules around your specific threat model** — generic rules generate noise; rules built around your IAM topology, account structure, and data exposure produce signal
- **Establish mean-time-to-detect and mean-time-to-respond as operational metrics** — detection programmes without measurement do not improve
- **Test your detection capability** — run atomic red team tests, simulate credential compromise, and validate that your alerting actually fires; assume detection gaps until you have evidence otherwise

---

## Key Takeaways

- **Cloud threat detection starts with audit logs, not network traffic** — the API is the attack surface; CloudTrail and equivalent services are your primary signal source
- **Identity-based attacks are the dominant threat pattern** — credential compromise, privilege escalation, and lateral movement via role chaining require identity-aware detection
- **Native tooling (GuardDuty, Defender for Cloud, Security Command Center) is the correct baseline** — enable at the organisation level before investing in third-party platforms
- **Detection without centralised, tamper-evident logs is incomplete** — cross-account visibility requires logs aggregated outside the accounts being monitored
- **Detection is a programme, not a product** — rules require testing, tuning, and continuous improvement; a detection deployment that is not actively maintained degrades over time

---

## Related Guides

- [Cloud Security Vulnerability Management](/guides/cloud-security-vulnerability-management/) — Detection surfaces active exploitation; vulnerability management reduces the attack surface that detection has to cover.
- [AWS IAM Security Best Practices](/guides/aws-iam-security-best-practices/) — The IAM misconfigurations that create the privilege escalation and lateral movement paths your detection programme needs to cover.
- [What is CSPM (Cloud Security Posture Management)?](/guides/what-is-cspm-cloud-security-posture-management/) — CSPM and threat detection are complementary disciplines; CSPM prevents the misconfigurations that threat detection has to catch in exploitation.
- [Kubernetes Security Best Practices](/guides/kubernetes-security-best-practices/) — Runtime threat detection for containerised workloads requires different signal sources and detection logic from IaaS environments.
- [AWS CloudTrail Configuration Best Practices](/guides/aws-cloudtrail-configuration-best-practices/) — The foundational logging infrastructure that underpins threat detection on AWS.
- [AWS vs Azure vs GCP: Cloud Security Service Comparison](/guides/aws-azure-gcp-security-service-comparison/) — Compare GuardDuty, Defender for Cloud, and Security Command Center capabilities in detail.
