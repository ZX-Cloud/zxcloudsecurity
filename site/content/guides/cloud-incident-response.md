+++
title = "Cloud Incident Response: A Practitioner's Guide"
date = "2026-06-24T06:00:00Z"
slug = "cloud-incident-response"
description = "Cloud incident response for architects — preparation, detection, containment, evidence preservation, AWS-native tooling (Detective, Security Lake, GuardDuty), and UK regulatory notification obligations."
keywords = ["cloud incident response", "AWS incident response", "security incident cloud", "Amazon Detective", "AWS Security Lake", "IR playbook AWS", "cloud forensics", "GuardDuty incident response"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

Cloud incident response is the organised process of detecting, containing, investigating, and recovering from security incidents in cloud environments — and then learning from them. It differs from traditional incident response in important ways: there are no physical servers to seize, logs are ephemeral unless explicitly preserved, infrastructure can be destroyed and rebuilt in minutes, and the blast radius of a compromised cloud identity is global rather than local. These differences make cloud IR both more powerful in some respects and more dangerous in others. More powerful because automation can contain incidents faster than any human response. More dangerous because evidence disappears and attackers can move at machine speed.

This guide covers the phases of cloud incident response, the AWS-native tooling that makes each phase tractable, evidence preservation in cloud environments, containment and eradication strategies, UK regulatory notification obligations, and how to build a response capability before it is needed.

---

## How Cloud IR Differs from Traditional Incident Response

In a traditional data centre, incident response involves physically isolating affected servers, seizing hard drives, and preserving memory images. The attack surface is bounded by the physical perimeter. Logs are on-premises. The attacker must maintain a foothold through techniques that leave forensic traces on persistent infrastructure.

Cloud incidents do not follow this pattern:

**Identity is the primary attack vector and the primary persistence mechanism.** Most cloud incidents begin with credential theft — exposed access keys, phished IAM users, SSRF attacks against instance metadata endpoints — and attackers maintain persistence by creating new IAM users, access keys, or modified trust policies. The initial intrusion leaves no filesystem trace on any server. Containment requires IAM actions, not network isolation.

**Infrastructure is ephemeral.** Auto-scaling instances terminate when load drops. Lambda functions execute and disappear. Container tasks complete and are removed. Without explicit log preservation, the evidence of what ran, when, and what it did is gone minutes after the fact.

**The blast radius is account-wide or organisation-wide.** A compromised set of credentials with `AdministratorAccess` can read every secret, exfiltrate every S3 bucket, and create backdoor accounts across every region — simultaneously, via scripted API calls — in under five minutes. Containment is a race against automation.

**The cloud provides better native tooling.** GuardDuty, Detective, CloudTrail, Security Lake, and VPC Flow Logs give cloud responders a quality of visibility that most on-premises environments cannot match. A well-instrumented AWS environment is significantly easier to investigate than an on-premises network with inconsistent logging.

---

## The Six Phases of Cloud Incident Response

### Phase 1: Prepare

Preparation is the only phase that happens before an incident. Everything done in preparation determines the speed and quality of every subsequent phase.

**Build the IR team and define roles.** At minimum: an IR lead (owns the response), a technical analyst (investigates), a communications lead (handles stakeholder and regulatory notifications), and an IAM responder (executes containment actions). In smaller organisations these roles may overlap, but they must be explicitly assigned.

**Create the IR IAM role in advance.** A dedicated IAM role (`SecurityIRRole` or similar) with permissions scoped to response actions — read CloudTrail, describe EC2, snapshot EBS volumes, modify security groups, disable access keys — should exist before it is needed. This role should not have `AdministratorAccess`. The permissions required for investigation and containment are specific and enumerable. Granting broad administrative access to responders is itself a security risk.

**Pre-provision a forensic account.** A separate, clean AWS account used exclusively for forensic analysis. EBS snapshots from compromised accounts are shared to this account for analysis. The forensic account has no connections to production — no VPC peering, no cross-account roles from production. Its isolation is what makes it trustworthy for analysis.

**Write runbooks for the most likely scenarios.** The four scenarios worth having runbooks for: compromised IAM credentials, exposed S3 bucket, compromised EC2 instance, and ransomware or destructive attack. A runbook is not a novel — it is a numbered decision tree that a responder under stress can follow at 2am. Keep it to two pages maximum. Store it somewhere accessible if your AWS environment is compromised (not in an S3 bucket in the affected account).

**Test the plan.** Tabletop exercises should happen at minimum annually. A realistic tabletop scenario for a cloud environment: "GuardDuty has just fired a finding — `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS`. Walk us through the first 30 minutes." The gaps in your runbook become obvious when responders have to narrate their way through a scenario with no preparation pressure.

---

### Phase 2: Detect

Detection is addressed in depth in the [Cloud Threat Detection guide](/guides/cloud-threat-detection/). In the context of IR, the relevant question is: what is your mean time to detect (MTTD), and does your detection tooling generate actionable alerts or noise?

**GuardDuty** is the primary detection layer for most AWS environments. The findings most likely to initiate an IR process:

| GuardDuty Finding | What It Indicates | Typical Priority |
|---|---|---|
| `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS` | EC2 role credentials being used from a non-AWS IP — almost always malicious | P1 — respond immediately |
| `Backdoor:EC2/C&CActivity.B` | EC2 instance communicating with known C2 infrastructure | P1 — contain immediately |
| `Impact:S3/MaliciousIPCaller` | API calls to S3 from known-malicious IPs | P1 |
| `Persistence:IAMUser/UserPermissions` | Unexpected IAM permission changes | P1 — review immediately |
| `UnauthorizedAccess:IAMUser/ConsoleLoginSuccess.B` | Console login from unusual geography or tor exit node | P1 |
| `Discovery:S3/MaliciousIPCaller` | S3 enumeration from known-malicious IP | P2 |
| `CryptoCurrency:EC2/BitcoinTool.B` | EC2 instance making cryptocurrency mining API calls | P2 |

Route GuardDuty findings to EventBridge and trigger an automated initial response — at minimum, creating a ticket in your incident management system and paging the on-call responder for P1 findings.

---

### Phase 3: Contain

Containment in cloud environments is primarily an IAM and network action, executed via API.

**For compromised IAM credentials:**

```
1. Identify all access keys associated with the compromised principal
2. Disable (not delete) the access key(s) — disabling preserves the key ID for forensic correlation
3. Attach an explicit deny policy to the IAM user or role: {"Effect": "Deny", "Action": "*", "Resource": "*"}
4. Revoke all active sessions (for IAM roles: update the role's trust policy to deny sts:AssumeRole)
5. Do NOT rotate the key yet — rotation destroys the original key value, potentially losing forensic data
```

**For compromised EC2 instances:**

```
1. Take an EBS snapshot of all volumes before any other action (preserves evidence)
2. Isolate the instance: remove from load balancer target groups, modify the security group to deny all inbound and outbound traffic except to the forensic analysis subnet
3. Do NOT terminate the instance — termination destroys volatile memory and makes root cause analysis significantly harder
4. Capture instance metadata (describe-instance, get-console-output, get-console-screenshot) before isolation
```

**For exposed S3 buckets:**

```
1. Enable S3 Block Public Access at the bucket level immediately
2. Review and revoke any pre-signed URLs if exposure was via pre-signed URL
3. Enable S3 access logging if not already enabled (you will need it for the investigation)
4. Query CloudTrail for all GetObject API calls against the bucket for the prior 90 days
```

**Automated containment with EventBridge and Lambda** can execute steps 1–3 in seconds of a GuardDuty finding being generated. An EventBridge rule that matches `detail-type: GuardDuty Finding` with severity ≥ 7 triggering a Lambda function that disables the associated access key or isolates the EC2 instance reduces MTTC (mean time to contain) from the 30+ minutes a manual response requires to under 60 seconds.

---

### Phase 4: Investigate

Investigation aims to establish: what happened, when, how the attacker gained access, what they accessed or exfiltrated, and whether any persistence mechanisms remain.

**Amazon Detective** is the most efficient investigation tool available for AWS environments. It ingests GuardDuty findings, CloudTrail logs, and VPC Flow Logs, builds a behavioural graph, and surfaces relationships that manual log analysis would take hours to establish. For a compromised IAM principal, Detective visualises every API call that principal made, the resources it accessed, the volume of data it touched, and the network traffic associated with its sessions — in a single view.

**CloudTrail investigation queries via Athena** are necessary when Detective does not cover the full investigation scope or for queries spanning longer time periods than Detective's default retention window. Key queries:

- All API calls made by the compromised principal in the 48 hours before and after the GuardDuty finding
- All IAM changes (CreateUser, CreateAccessKey, AttachUserPolicy, PutRolePolicy) across the account for the relevant period
- All S3 GetObject calls against sensitive buckets
- All AssumeRole calls to identify lateral movement between roles or accounts

**AWS Security Lake** centralises security logs — CloudTrail, VPC Flow Logs, GuardDuty, Route 53 resolver logs — in OCSF format in a dedicated S3 bucket, queryable via Athena. For organisations running multi-account environments, Security Lake eliminates the per-account log query problem: a single Athena query covers all accounts simultaneously.

**Evidence preservation checklist:**

- CloudTrail logs (90-day default retention in CloudWatch Logs — export to S3 with indefinite retention for investigations that may take longer)
- VPC Flow Logs for the relevant subnets and time window
- EBS snapshots of affected instances
- S3 access logs for buckets accessed during the incident
- GuardDuty findings exported to S3 before the 90-day retention window closes
- AWS Config snapshots showing resource state at the time of the incident

---

### Phase 5: Eradicate and Recover

Eradication removes the attacker's access and any persistence mechanisms they established. Recovery restores normal operation.

**Eradication checklist:**

- Delete or deactivate all IAM users, access keys, and roles created by the attacker
- Review and revert any IAM policy modifications made during the incident period
- Rotate all credentials that may have been exposed — access keys, secrets in Secrets Manager, database passwords, API keys
- Audit all S3 bucket policies, Lambda resource policies, KMS key policies, and SNS topic policies for modifications
- Terminate compromised EC2 instances and replace with fresh instances from a known-good AMI
- Review CloudTrail for any SCPs or organisation policy changes (an attacker with sufficient privilege may attempt to modify guardrails)

**Recovery:**

Rebuild from infrastructure as code, not from the compromised state. If Terraform or CloudFormation defines the environment, use it to provision fresh infrastructure. Do not attempt to clean a compromised instance — the risk of leaving residual persistence is too high. The rebuild time is the cost of not having immutable infrastructure; it is a strong argument for IaC from day one.

Before restoring to full production, verify that the initial access vector has been closed. Returning a patched but still-vulnerable environment to production guarantees a repeat incident.

---

### Phase 6: Post-Incident Review

The post-incident review (PIR) is not optional and not a blame exercise. It has two outputs: a timeline of what happened and why, and a set of action items that prevent recurrence.

A PIR should be completed within five working days of incident closure while memories are fresh. The questions it must answer:

- What was the initial access vector, and how do we close it?
- What was the dwell time — how long was the attacker present before detection?
- What logging or detection gaps made the incident harder to detect or investigate than it should have been?
- Were the runbooks accurate? If not, what needs updating?
- Were regulatory notification obligations met on time?

---

## UK Regulatory Notification Obligations

**UK GDPR (ICO):** If personal data was accessed, exfiltrated, or potentially exposed, you must notify the ICO within 72 hours of becoming aware that a breach has likely occurred. This clock starts when you have sufficient information to conclude a personal data breach is probable — not when the investigation is complete. Notification must include: the nature of the breach, categories and approximate number of individuals affected, likely consequences, and measures taken or proposed to address the breach. If 72-hour notification is not possible, notify as soon as possible with reasons for the delay.

**FCA (regulated firms):** FCA-regulated firms must notify the FCA of material operational incidents under the Senior Managers and Certification Regime (SM&CR). DORA (for in-scope firms from 2025) requires notification of major ICT-related incidents within 4 hours of classification, an intermediate report within 72 hours, and a final report within one month. The FCA also expects firms to maintain a cyber incident response plan and test it.

**Practical implication:** Your IR runbook must include a decision point — "Is personal data likely involved? Who is the designated DPO?" and "Is this firm FCA-regulated? Who is the MLRO/DPO authorised to notify?" These decisions must be made in the first hour of an incident, not after the investigation is complete. The [Cloud Compliance Frameworks guide](/guides/cloud-compliance-frameworks/) covers UK GDPR, FCA, DORA, ISO 27001, and Cyber Essentials Plus obligations in full, including how each maps to AWS, Azure, and GCP controls.

---

## What Architects Should Do

**Build the IR infrastructure before an incident, not during one.** The forensic account, the IR IAM role, the EBS snapshot automation, the EventBridge containment rules — none of these should be improvised at 2am under a live incident.

**Enable GuardDuty, CloudTrail, and VPC Flow Logs in every account with log retention of at least 12 months.** The single most common problem in cloud IR investigations is evidence gaps — CloudTrail logs expired, Flow Logs not enabled, GuardDuty disabled in a region the attacker used. These are preventable with organisational policy.

**Wire GuardDuty findings to automated containment for your highest-severity scenarios.** Automated containment of `InstanceCredentialExfiltration.OutsideAWS` — the single most dangerous GuardDuty finding — can be implemented in an afternoon and reduces MTTC from 30+ minutes to under 60 seconds.

**Run a tabletop exercise before you need to run a real one.** Use a realistic GuardDuty finding as the scenario. Identify who gets paged, who makes containment decisions, who writes the ICO notification. The gaps in your process are far cheaper to find in a tabletop than in a live incident.

**Document your regulatory notification obligations and assign owners.** The ICO 72-hour clock and FCA notification requirements are not optional. If the person responsible for notification is not identified before an incident, critical time is lost identifying them during one.

---

## Key Takeaways

- **Cloud IR is identity-first** — most incidents begin and end with IAM. Containment means IAM actions (disabling credentials, attaching deny policies, revoking sessions), not network isolation.
- **Evidence is ephemeral in cloud** — logs, instance state, and metadata disappear unless explicitly preserved. The first action after identification of a compromise should always be evidence preservation, before containment.
- **Preparation determines speed** — MTTD and MTTC are the metrics that determine incident outcomes. Both are set by the preparation work done before an incident occurs.
- **GuardDuty + Detective + Security Lake is the AWS investigation stack** — together they provide detection, behavioural investigation, and cross-account log analysis that manual investigation cannot match at speed.
- **UK regulatory clocks start early** — the ICO 72-hour clock begins when a personal data breach is probable, not when investigation is complete. FCA notification obligations are tighter still under DORA.

---

## Related Guides

- [Cloud Threat Detection](/guides/cloud-threat-detection/) — The detection layer that initiates IR: signal sources, GuardDuty findings, and how to build a detection programme that surfaces real attacks.
- [AWS Security Hub: A Practitioner's Guide](/guides/aws-security-hub-guide/) — Security Hub aggregates findings across accounts and provides the centralised view that makes multi-account IR tractable.
- [AWS CloudTrail Configuration Best Practices](/guides/aws-cloudtrail-configuration-best-practices/) — Organisation trails, integrity validation, and long-term log retention — the audit trail that makes post-incident investigation possible.
- [Cloud Identity and Access Management](/guides/cloud-identity-and-access-management/) — IAM is the primary attack surface and the primary containment layer in cloud IR.
- [AWS IAM Security Best Practices](/guides/aws-iam-security-best-practices/) — Least privilege, permission boundaries, and access analysis — the IAM hygiene that limits blast radius when credentials are compromised.
- [AWS Well-Architected Security](/guides/aws-well-architected-security/) — SEC 10 (Incident Response) covers IR preparation, tooling, and testing requirements in the context of the full Security Pillar.
- [Cloud Compliance Frameworks](/guides/cloud-compliance-frameworks/) — UK GDPR, FCA, and DORA notification obligations explained in the context of cloud security incidents.
