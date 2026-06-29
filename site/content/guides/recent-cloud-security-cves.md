---
title: "Recent Cloud Security CVEs: What Practitioners Need to Know in 2026"
date: 2026-06-29
description: "A practitioner's guide to recent cloud security CVEs in 2026 — covering critical vulnerabilities, SSRF risks, NVD changes, and AWS remediation steps."
tags: ["cloud security", "CVE", "vulnerability management", "AWS", "SSRF", "IMDSv2"]
slug: "recent-cloud-security-cves"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2183
draft: false
---

# Recent cloud security CVEs: what every cloud security practitioner must track in 2026

If you manage cloud workloads for UK financial services, government, or enterprise clients, staying current with recent cloud security CVEs is a core operational control, not optional housekeeping. The vulnerability picture in 2026 has shifted in ways that matter: disclosure volumes have tripled in five years, the NVD's enrichment model has changed fundamentally, and adversaries are using AI-assisted tooling to find exploitable paths faster than most enterprise patch cycles can absorb. This guide covers the most operationally significant vulnerabilities and trends from mid-2026 and tells you what to do about them.

---

## Why the vulnerability landscape changed in 2026

CVE submissions to the NVD increased 263% between 2020 and 2025. Submissions during the first three months of 2026 alone ran nearly one-third higher than the same period last year. That volume drove a structural change that will affect how your team operates.

On 15 April 2026, NIST announced a shift to a heavily constrained, risk-based model for vulnerability enrichment. In practice, this creates a significant information gap for organisations and security tools that rely on the NVD. Most vulnerabilities will now enter the CVE ecosystem without the CVSS metadata that automated downstream tooling needs to prioritise them.

From 15 April 2026, NIST will prioritise enrichment for CVEs appearing in CISA's Known Exploited Vulnerabilities (KEV) Catalog, CVEs for software used within the federal government, and CVEs for critical software as defined by Executive Order 14028.

The practical consequence for UK teams: your scanner feeds will surface CVEs without severity scores. If your vulnerability management workflow gates remediation on a CVSS score threshold, that workflow is now broken by design. The NCSC is explicit on this point: decisions should be made on the overall level of risk of an application or asset, not simply the severity of a vulnerability such as the CVSS score.

This class of vulnerabilities is also likely to grow as researchers use advances in LLM capability to probe not just specific software but the standards on which software rests.

---

## High-impact recent cloud security CVEs you should have actioned

### CVE-2026-40175: Axios cloud metadata exfiltration

This is the cloud-native CVE that deserves the most attention from AWS-heavy teams.

CVE-2026-40175, titled "Unrestricted Cloud Metadata Exfiltration via Header Injection Chain", involves a header injection chain in the Axios redirect handler that can be combined with cloud provider metadata services (AWS IMDSv1, GCP metadata, Azure IMDS) to exfiltrate credentials from compromised servers.

The flaw enables remote code execution and full cloud compromise. Attackers can chain prototype pollution, SSRF, and request smuggling to bypass AWS IMDSv2 and steal credentials. A public proof of concept is already available, which raises the risk materially.

What makes this particularly nasty is that it requires zero direct user input. If an attacker can pollute `Object.prototype` via any other library in the stack (such as `qs`, `minimist`, `ini`, or `body-parser`), Axios will automatically pick up the polluted properties during its config merge.

The exploit demonstrates bypass of AWS's IMDSv2 security layer. A smuggling request to the AWS Metadata Service returns a session token, allowing attackers to steal IAM credentials and pivot to the cloud account.

Affected versions are all 1.x and 0.x releases up to but not including 1.15.0 and 0.31.0.

Remediation is to upgrade to 1.15.1 (or 0.31.1 if you are on the legacy branch). You also need to audit your transitive dependency tree. Axios is a dependency of dozens of popular SDKs and CLIs, including cloud provider SDKs, observability agents, and internal HTTP clients. If a parent package pins Axios to an old version, your top-level upgrade is overridden unless you use `overrides` (npm) or `resolutions` (Yarn), or the equivalent.

---

### CVE-2026-41091 and CVE-2026-45498: Microsoft Defender zero-days under active exploitation

Both CVEs are directly relevant to any organisation running Windows workloads on EC2, Azure VMs, or a hybrid estate.

CVE-2026-41091 carries a CVSS score of 7.8. Successful exploitation allows an attacker to gain SYSTEM privileges. Microsoft's description: "Improper link resolution before file access ('link following') in Microsoft Defender allows an authorised attacker to elevate privileges locally."

CVE-2026-45498 is a denial-of-service bug affecting Defender with a CVSS score of 4.0.

CISA added both to its KEV catalog, requiring Federal Civilian Executive Branch agencies to apply fixes by 3 June 2026. UK organisations should treat KEV additions as near-mandatory remediation triggers regardless of US federal mandates. If adversaries are exploiting something against federal targets, they will exploit it against UK financial sector targets.

Both vulnerabilities are addressed in Microsoft Defender Antimalware Platform versions 1.1.26040.8 and 4.18.26040.7 respectively. Verify your Defender platform version across your entire estate and do not assume auto-update is working correctly on every workload.

---

### CVE-2026-45585 ("YellowKey"): Windows BitLocker security feature bypass

Microsoft is aware of a security feature bypass vulnerability publicly referred to as "YellowKey". The proof of concept has been made public, which violated coordinated vulnerability disclosure best practice.

CVE-2026-45585 targets the protections provided by Microsoft BitLocker full-disk encryption. An attacker with physical access to a Windows device can exploit the Windows Recovery Environment by manipulating NTFS transaction logs and recovery configuration files, forcing WinRE to launch a privileged command prompt while the disk remains transparently decrypted by the TPM.

For cloud architects: this matters wherever you manage hybrid endpoints, BYOD devices for developers with cloud console access, or physical servers in co-location facilities. An attacker with brief physical access to a developer laptop holding cached AWS or Azure credentials has a complete kill chain.

While a permanent patch was not immediately available, Microsoft released a mitigation script that removes the `autofstx.exe` entry from the `BootExecute` REG_MULTI_SZ value in the offline SYSTEM registry hive of WinRE, preventing the executable from running during boot.

---

## The SSRF and IMDSv1 attack class: still the highest-ROI target

No guide on recent cloud security CVEs is complete without addressing the underlying attack pattern that remains the single most exploited vector in AWS environments. IMDSv1 allows any process on the instance to retrieve credentials without authentication, making it vulnerable to SSRF attacks where a web application vulnerability causes the server to fetch the metadata endpoint and return the instance's IAM credentials to an attacker.

Research from Datadog's 2024 State of Cloud Security report found that 68% of EC2 instances still do not enforce IMDSv2, representing millions of potentially vulnerable instances across the AWS ecosystem.

CVE-2026-40175 is the most recent example, but this attack class has been active for years and continues to be weaponised. Where IMDSv2 is enforced, attacker payloads attempting the initial token retrieval have all requests to the metadata service rejected. If the same application were running in an environment still dependent on IMDSv1, the attack vector would very likely have resulted in credential compromise. IMDSv2 enforcement stops the pivot to the cloud control plane.

<!-- INTERNAL_LINK: How to enforce IMDSv2 across your AWS organisation | enforce-imdsv2-aws-organisation -->

### Enforcing IMDSv2 organisation-wide

The following SCP denies the launch of new EC2 instances unless IMDSv2 is required. Attach this at the OU or root level in AWS Organizations:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceIMDSv2OnLaunch",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "StringNotEquals": {
          "ec2:MetadataHttpTokens": "required"
        }
      }
    }
  ]
}
```

For existing instances, enforce IMDSv2 without a restart using the AWS CLI:

```bash
aws ec2 modify-instance-metadata-options \
  --instance-id i-0123456789abcdef0 \
  --http-tokens required \
  --http-put-response-hop-limit 2 \
  --http-endpoint enabled
```

Set `HttpPutResponseHopLimit` to 2 for ECS EC2 instances. The default of 1 means the PUT session token request is consumed at the first network hop (container-to-host bridge), so the container never receives the token. Setting it to 2 allows the request to traverse one bridge interface and reach the metadata service.

AWS Security Hub includes an EC2 control (`EC2.8: Amazon EC2 instances should use Instance Metadata Service Version 2 (IMDSv2)`) that uses the AWS Config rule `ec2-imdsv2-check` to verify that the instance metadata version is configured with IMDSv2. Enable this control in all regions and accounts. It is one of the highest-signal findings in your Security Hub posture.

---

## Aligning your vulnerability management process with NCSC guidance

All systems contain vulnerabilities. They may take the form of a configuration issue for system administrators to resolve, software defects requiring a vendor update, or a vulnerability the vendor does not yet know exists, for which no mitigation is available. This makes vulnerability management a critical control.

The NCSC's cloud security principles are equally direct: your provider should have a vulnerability management process in place to identify, triage, and mitigate vulnerabilities in all components of the service they are responsible for. But shared responsibility means there is always a customer-side component. A scanner may not tell you that AWS, Microsoft, or Google published an advisory for a managed service, agent, extension, SDK, or platform component your workloads depend on. The hyperscaler owns the service. Your team owns impact analysis, affected scope, customer-side mitigation, tickets, and proof.

Organisations should plan to deploy software security updates quickly, more frequently, and at scale, including across their supply chains. Where a critical vulnerability is under active exploitation, particularly one affecting an internet-facing system, accelerating the update process is not optional.

The FCA's operational resilience rules and DORA (which applies to UK firms with EU operations) both carry implicit requirements for timely patching of critical systems. Treating KEV-listed CVEs as SLA-bound remediation items with board-level visibility is the correct posture for any regulated UK firm.

<!-- INTERNAL_LINK: AWS Security Hub controls for FCA regulated environments | aws-security-hub-fca-compliance -->

---

## Common mistakes when responding to recent cloud security CVEs

Relying solely on CVSS scores for prioritisation is the most common one I see. With the NVD enrichment model in its current state, scores will arrive late or not at all. Use CISA KEV status and EPSS probability alongside any available CVSS data. The changes at NIST are a necessary response to an unsustainable volume of data, but they also mean you can no longer outsource your vulnerability enrichment entirely to public, government-funded databases.

Assuming auto-update covers managed services is the second. Provider-side CVEs covering SDK vulnerabilities, agent updates, and platform components require your team to track vendor advisories directly. A scanner finding OpenSSL vulnerable inside a container is not the same as discovering that your version of Axios is exfiltrating metadata credentials.

Skipping the IMDSv2 audit and jumping straight to enforcement is a mistake I have seen wreck production workloads. IMDSv2 enforcement is a two-phase operation: audit and migrate first, enforce second. Skipping the audit and applying the SCP immediately creates emergency exceptions that never get cleaned up.

Treating BitLocker bypass CVEs as endpoint-only issues misses the cloud risk. Cloud architects own the security of developer endpoints too, particularly where those devices hold cached cloud credentials or SSO sessions. YellowKey (CVE-2026-45585) requires physical access, but in a hybrid working model, physical access now means a laptop left unattended at a hot-desk.

Ignoring transitive dependency exposure is where most teams have blind spots. If you are on any Axios version below 1.15.0 and your application makes outbound requests with a `NO_PROXY` configuration, follows redirects, or runs in a cloud environment with a metadata service, the relevant CVEs are exploitable in your environment. Your direct dependencies are the easy wins. Transitive dependencies are where exposure hides.

Not monitoring for IMDSv1 usage drift is the final gap. Applying IMDSv2 enforcement is a one-time action; detecting regression is continuous work. Use the `MetadataNoToken` CloudWatch metric per instance and set an alarm at threshold 1 to catch any workload falling back to IMDSv1.

<!-- INTERNAL_LINK: AWS CloudWatch security monitoring patterns | aws-cloudwatch-security-monitoring -->

---

## Key takeaways

The NVD enrichment model has fundamentally changed. NIST now prioritises only KEV-listed and federally relevant CVEs for enrichment. Your tooling and triage processes must account for CVEs arriving without CVSS scores.

CVE-2026-40175 (Axios) is a direct cloud credential theft risk. If any of your workloads use Axios below version 1.15.0 and run in an environment with access to a cloud metadata service, treat this as a critical remediation item regardless of the moderate CVSS rating.

KEV additions are de facto mandatory remediation triggers for UK regulated organisations. CVE-2026-41091 and CVE-2026-45498 were actively exploited and CISA-listed. Remediation should be SLA-bound, not advisory.

Enforcing IMDSv2 organisation-wide remains one of the highest-return security controls available on AWS. 68% of EC2 instances still do not enforce it. An SCP at the AWS Organizations level is the only reliable way to ensure new workloads cannot regress.

NCSC vulnerability management guidance and the Cloud Security Principles are the correct reference framework for UK organisations. Align your patch SLAs to NCSC timescales and treat active exploitation as an immediate escalation trigger.

Tracking recent cloud security CVEs is not just about patching. It is about understanding the attack surface created by the shared responsibility model, your supply chain, and the transitive dependencies your workloads carry into production.