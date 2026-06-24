---
title: "Recent Cloud Security CVEs: What AWS Architects Need to Act On Right Now"
date: 2026-06-21
description: "A practitioner's breakdown of recent cloud security CVEs in 2026, covering wormable Windows flaws, Defender exploits, and how to respond in AWS environments."
tags: ["cloud security", "CVE", "vulnerability management", "AWS", "patch management", "Windows security"]
slug: "recent-cloud-security-cves"
author: "Steve Harrison, Principal Security Architect"
word_count: 2277
draft: false
---

# Recent cloud security CVEs: what AWS architects need to act on right now

If you run Windows workloads on EC2, hybrid environments bridging on-premises Windows Server to AWS, or multi-tenant platforms where Windows-based tooling touches your cloud management plane, the crop of recent cloud security CVEs disclosed in mid-2026 should be sitting at the top of your risk register right now, not buried in a monthly patching ticket.

Microsoft's June 2026 Patch Tuesday released fixes for 208 CVEs across Windows, Windows components, Office, Azure, .NET, Visual Studio, GitHub Copilot, Defender, Exchange Server, Hyper-V, Secure Boot, and BitLocker. That is not a routine update cycle. It is a structural signal about where the threat surface is moving.

This guide covers the highest-priority vulnerabilities from the April to June 2026 window, explains what they mean for cloud security architects running AWS infrastructure, and gives you the tooling patterns and code to operationalise your response.

<!-- INTERNAL_LINK: AWS shared responsibility model explained | aws-shared-responsibility-model -->

---

## The 2026 vulnerability landscape at a glance

Before drilling into specific CVEs, it helps to understand the macro trend. In 2026 there have been 404 Microsoft vulnerabilities with an average CVSS score of 7.2. The raw count is actually lower than 2025, but the severity profile is worse. The number of critical vulnerabilities doubled year over year, from 78 to 157, and Microsoft Azure and Dynamics 365 experienced a nine-times rise in critical vulnerabilities, from 4 to 37.

Read that last number again. Azure-native critical CVEs are no longer a footnote in a threat briefing. They are a primary risk category for cloud architects.

It is worth noting what CVEs do not capture: identity misconfigurations, over-privileged machine accounts, and AI agents with unconstrained access do not get CVE identifiers, but they carry the same critical consequences. The vulnerabilities below are the ones that do carry identifiers, and they are severe enough that patching delays have real consequences for your AWS estate.

---

## CVE-2026-45657: the wormable Windows kernel flaw

This is the headline vulnerability of 2026 so far, and it directly affects EC2 instances running Windows Server.

CVE-2026-45657 is a use-after-free flaw in the Windows Kernel with a CVSS base score of 9.8. Microsoft confirmed that an attacker can exploit it by sending specially crafted network traffic to a vulnerable Windows system. What makes it particularly dangerous is the combination of characteristics: no authentication required, no user interaction required, network-reachable via specially crafted TCP/IP packets, and SYSTEM-level code execution if exploitation succeeds.

Security researchers at the Zero Day Initiative have confirmed this flaw's characteristics allow it to self-propagate across networks, with a profile similar to EternalBlue, the vulnerability behind WannaCry. That comparison carries genuine weight. In May 2017, a wormable Windows flaw allowed the WannaCry ransomware to spread to more than 200,000 systems across 150 countries, even though Microsoft had issued a patch two months earlier. Organisations that delayed deploying that patch paid the price.

Affected platforms include Windows 11 versions 23H2 through 26H1 and Windows Server 2022 and 2025, including Server Core installations. If you have EC2 instances in this range without the June 2026 cumulative update applied and rebooted, you have an unmitigated wormable RCE on a network-accessible host.

### AWS-specific response

The AWS Shared Responsibility Model is unambiguous here: AWS secures the hypervisor; you own the guest OS. Use AWS Systems Manager Patch Manager to enforce patching at scale. The SSM document below creates a baseline patch policy targeting Windows Server 2022 and 2025 instances:

```json
{
  "name": "CriticalWindowsPatchBaseline-June2026",
  "operatingSystem": "WINDOWS",
  "approvalRules": {
    "patchRules": [
      {
        "patchFilterGroup": {
          "patchFilters": [
            {
              "key": "CLASSIFICATION",
              "values": ["CriticalUpdates", "SecurityUpdates"]
            },
            {
              "key": "MSRC_SEVERITY",
              "values": ["Critical", "Important"]
            }
          ]
        },
        "approveAfterDays": 0,
        "complianceLevel": "CRITICAL",
        "enableNonSecurity": false
      }
    ]
  },
  "description": "Zero-day approval for Critical/Important patches. Targets CVE-2026-45657 class flaws.",
  "tags": [
    { "Key": "ManagedBy", "Value": "SecurityTeam" },
    { "Key": "PatchUrgency", "Value": "Critical" }
  ]
}
```

Set `approveAfterDays` to `0` for Critical severity patches during an active wormable CVE window. Accept the change management overhead. The alternative is a WannaCry-class event on your cloud estate.

<!-- INTERNAL_LINK: AWS Systems Manager Patch Manager guide | aws-ssm-patch-manager -->

---

## CVE-2026-41091 and CVE-2026-45498: actively exploited Microsoft Defender flaws

These two are confirmed in-the-wild. They are not theoretical risks. CISA has added both to its Known Exploited Vulnerabilities catalogue.

CVE-2026-41091 scores 7.8 on CVSS. Microsoft describes it as improper link resolution before file access in Microsoft Defender, allowing an authorised attacker to elevate privileges locally to SYSTEM level. CVE-2026-45498 is a denial-of-service bug affecting Defender, rated 4.0. Used together, an attacker can blind your endpoint protection with the DoS flaw before escalating privileges through the first. Chaining a DoS against your AV with a local privilege escalation is a classic attacker pattern, and here you have both primitives confirmed exploited in production environments.

Both vulnerabilities are addressed in Microsoft Defender Antimalware Platform versions 1.1.26040.8 and 4.18.26040.7. For most enterprise deployments, automatic updates will handle this, but the critical word is "most." EC2 instances in isolated subnets, air-gapped environments, or Windows AMIs that haven't been refreshed in weeks will not have received automatic updates. Verify rather than assume.

<!-- INTERNAL_LINK: Securing Windows EC2 instances on AWS | securing-windows-ec2-aws -->

---

## CVE-2026-42897: Exchange Server XSS actively exploited

If your estate includes on-premises Exchange Server, which is still common in UK financial services where legacy mail infrastructure persists well past its natural lifespan, this one needs immediate attention.

CVE-2026-42897 is a cross-site scripting flaw in Exchange Outlook Web Access, rated CVSS 8.1, and it has been weaponised in real-world attacks. An attacker sends a specially crafted email; if the recipient opens it in OWA and certain interaction conditions are met, arbitrary JavaScript executes in the browser context. The June 2026 security update addresses this. Exchange Online is not affected. If you are in a hybrid migration state, this is a reasonable prompt to accelerate the transition.

---

## CVE-2026-41103: SSO plugin for Jira and Confluence elevation of privilege

This one is particularly relevant to cloud security architects because it sits at the intersection of developer tooling and identity, a combination that rarely gets patched quickly.

CVE-2026-41103 is a Critical-severity elevation of privilege flaw caused by incorrect implementation of an authentication algorithm (CWE-303). It permits an attacker to bypass authentication and sign in as a valid user.

If your engineering organisation uses Jira and Confluence, and those tools are federated into AWS IAM Identity Centre or Azure AD via SSO, a bypass here can pivot directly into your cloud management plane. That is not a Jira problem. That is an AWS access problem.

<!-- INTERNAL_LINK: AWS IAM Identity Centre federation guide | aws-iam-identity-centre-federation -->

---

## Operationalising CVE response in AWS: beyond Patch Manager

Patching is necessary but not sufficient. For each CVE wave like this one, you need detective controls that can tell you whether a vulnerability has been exploited before you have finished patching, because your patching SLA is measured in hours to days and exploitation can happen in minutes.

Amazon Inspector continuously scans EC2 workloads for software vulnerabilities and maps CVE identifiers directly to installed packages and OS versions. AWS Security Hub aggregates Inspector findings alongside GuardDuty threat detections, letting you correlate a vulnerable unpatched instance with suspicious network activity on the same host. When those two signals appear together, you need automated response, not an alert waiting in a queue.

The workflow I recommend for critical CVE windows:

1. Amazon Inspector identifies which EC2 instances are vulnerable to specific CVEs
2. AWS Security Hub correlates Inspector findings with GuardDuty threat detections against the same instance
3. EventBridge and Lambda automate first response: isolate the instance by replacing its security groups with a quarantine SG if GuardDuty fires on a vulnerable host

```python
import boto3
import json

def lambda_handler(event, context):
    """
    Triggered by EventBridge rule on GuardDuty HIGH/CRITICAL findings.
    Isolates the affected EC2 instance by replacing its security groups
    with a quarantine SG that permits no inbound/outbound traffic.
    """
    ec2 = boto3.client('ec2')
    guardduty_finding = event['detail']

    instance_id = (
        guardduty_finding
        .get('resource', {})
        .get('instanceDetails', {})
        .get('instanceId')
    )

    if not instance_id:
        print("No EC2 instance ID in finding. Skipping.")
        return

    quarantine_sg_id = 'sg-0QUARANTINE000000'  # Pre-created SG: deny all

    # Replace all security groups with quarantine SG
    ec2.modify_instance_attribute(
        InstanceId=instance_id,
        Groups=[quarantine_sg_id]
    )

    print(f"Instance {instance_id} quarantined. GuardDuty finding: "
          f"{guardduty_finding.get('type', 'Unknown')}")

    # Tag for incident tracking
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {'Key': 'SecurityStatus', 'Value': 'QUARANTINED'},
            {'Key': 'IncidentId', 'Value': guardduty_finding.get('id', 'unknown')}
        ]
    )
```

This is not a substitute for a proper IR runbook, but it removes a compromised host from the network without waiting for a human to notice a GuardDuty alert at 3am. For wormable-class flaws, that timing difference matters.

<!-- INTERNAL_LINK: GuardDuty automated response patterns | guardduty-automated-response -->

---

## Common pitfalls when responding to high-volume CVE releases

The June 2026 Patch Tuesday is a useful stress test of patching maturity. Here is where teams consistently go wrong.

### 1. Treating CVSS score as the only prioritisation signal

A CVSS 9.8 score on a flaw requiring physical access to exploit (CVE-2026-45585, the BitLocker bypass) is categorically different to a CVSS 9.8 flaw that is network-accessible and unauthenticated (CVE-2026-45657). Teams that sort by CVSS and work downwards miss this distinction entirely. Use Microsoft's Exploitability Index and the CISA Known Exploited Vulnerabilities catalogue as primary triage signals. Use CVSS as a secondary filter.

### 2. Conflating "update deployed" with "update applied"

Many Windows shops still confuse "update offered" with "update installed," and "installed" with "rebooted into the fixed build." Kernel fixes require a reboot to take effect. An SSM run command that reports "patch applied" on an EC2 instance that has not rebooted is reporting an incomplete state. Build reboot confirmation into your patch compliance verification queries.

### 3. Ignoring Defender auto-update in isolated environments

EC2 instances in private subnets without Systems Manager endpoints configured, or instances in AWS GovCloud with restricted egress, will not receive automatic Defender definition updates. Verify your connectivity assumptions rather than relying on the default auto-update behaviour.

### 4. Treating CVE response as a one-team problem

Under GDPR and FCA operational resilience requirements, a significant exploitation event on your cloud estate is not just a technical incident. It is a notifiable event with defined timelines. Your security team cannot be the only function that knows CVE-2026-45657 is wormable. Legal, compliance, and communications need visibility before exploitation occurs, not during.

### 5. Deferring patches because of "exploitation less likely" designations

Microsoft's Exploitability Index reflects the probability of functional exploit code being developed within 30 days of disclosure. "Less Likely" still means exploitation is possible, particularly for high-CVSS flaws attracting intense researcher attention. Multiple security researchers have assessed the window between CVE-2026-45657's patch release and a reliable public exploit as days rather than weeks. "Less Likely" is not the same as "will not happen."

---

## NCSC guidance alignment

The NCSC's vulnerability management guidance is explicit: prioritise patching based on exploitability and network reachability, not just vendor severity ratings. All three wormable-class CVEs in June 2026 (CVE-2026-45657, CVE-2026-47291, CVE-2026-44815) meet NCSC's threshold for immediate action: unauthenticated, network-reachable, with SYSTEM-level impact. The NCSC's 14-day patching target for internet-facing systems is the outer boundary for these flaws, not the target.

For FCA-regulated firms, the operational resilience framework introduced in 2022 creates explicit obligations around tolerances for disruption to important business services. A wormable kernel flaw sitting unpatched on an EC2 instance running your trading middleware is not a patching backlog item. It is an operational resilience risk that your Chief Risk Officer should know about.

---

## Key takeaways

CVE-2026-45657 is the highest priority item in 2026 so far. A wormable, unauthenticated, CVSS 9.8 Windows Kernel RCE affecting Windows Server 2022 and 2025. Deploy the June 2026 cumulative update and reboot. Verify the running build number, not just deployment status.

CVE-2026-41091 and CVE-2026-45498 are confirmed exploited in the wild. If your EC2 instances or on-premises servers rely on Microsoft Defender and are not on auto-update, push Defender Antimalware Platform 1.1.26040.8 and 4.18.26040.7 manually via SSM.

Monitoring CVEs with CVSS alone is insufficient. Cross-reference Microsoft's Exploitability Index and the CISA KEV catalogue. Wormable characteristics and active exploitation are the signals that should collapse your patching SLA to hours.

Amazon Inspector combined with AWS Security Hub is your minimum viable detection stack. Security Hub correlates Inspector vulnerability findings with GuardDuty threat detections in near real-time. Use that correlation rather than treating each service's findings in isolation.

Automate quarantine, not just alerting. The Lambda and EventBridge pattern above removes a compromised host from network reach without waiting for human triage. For wormable-class flaws, automated containment is the difference between one affected instance and fifty.

UK regulatory obligations apply. NCSC guidance, FCA operational resilience rules, and GDPR's 72-hour breach notification window all have implications when a CVE of this severity is in active exploitation. Get legal and compliance visibility before an incident occurs, not during one.