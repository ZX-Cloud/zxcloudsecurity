---
title: "Recent Cloud Security CVEs: What Architects Need to Know in 2026"
date: 2026-06-18
description: "A practitioner's guide to recent cloud security CVEs in 2026, covering active exploits, attacker infrastructure, detection tooling, and remediation playbooks."
tags: ["cloud security", "CVE", "vulnerability management", "AWS", "Azure", "patch management"]
slug: "recent-cloud-security-cves"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 3284
draft: false
---

# Recent Cloud Security CVEs: a practitioner's guide for 2026

The signal-to-noise ratio around cloud CVEs has never been worse. Microsoft released 209 security patches on a single June 2026 Patch Tuesday, covering 24 product families and pushing the 2026 total beyond 500 CVEs. Meanwhile, the window between vulnerability disclosure and mass exploitation has collapsed from weeks to days. If your vulnerability management process still runs on a 30-day patch cycle with a change freeze in place, you are handing adversaries a standing head start. This guide focuses on what actually matters: the CVEs seeing active cloud exploitation right now, the attacker infrastructure behind them, the AWS and Azure detective controls that surface them fastest, and the operational mistakes that leave organisations perpetually behind.

---

## The 2026 threat landscape

Threat actors exploited third-party software vulnerabilities (44.5%) more frequently than weak credentials (27.2%) in observed cloud incidents, a significant increase from the start of 2025. That is not a marginal shift. It inverts the attack model that shaped cloud security doctrine for the past decade. Misconfig-hunting and credential-stuffing are still very much alive, but unpatched application-layer software is now the primary door in.

Identity compromise underpinned 83% of compromises. Attackers have moved away from traditional phishing toward voice-based social engineering and credential harvesting from third-party SaaS tokens, funding large-scale, silent data exfiltration.

The two trends reinforce each other. Attackers exploit a CVE to extract credentials from a workload. Those credentials then fund the identity-based lateral movement that makes the intrusion profitable. Data theft, executed through compromised but legitimate access channels, was the primary goal in 73% of cloud-related incidents.

For UK-regulated organisations, whether FCA-supervised firms, NHS Digital suppliers, or central government OFFICIAL-tier environments, the dwell-time problem is severe. A GDPR breach notification clock starts the moment personal data is at risk, not when you detect the incident. 45% of intrusions resulted in data theft without immediate extortion attempts, typically involving prolonged dwell and stealthy persistence.

<!-- INTERNAL_LINK: cloud security shared responsibility model explained | cloud-shared-responsibility-model -->

---

## CVE-2026-4020: the Gravity SMTP credential harvester and its cloud-rented army

This one deserves more attention from cloud architects than it typically receives, because it is not really a WordPress story. It is a credential supply chain story.

### What the vulnerability does

The Gravity SMTP plugin for WordPress is vulnerable to sensitive information exposure in all versions up to and including 2.1.4. A REST API endpoint registered at `/wp-json/gravitysmtp/v1/tests/mock-data` has a `permission_callback` that unconditionally returns `true`. When the `?page=gravitysmtp-settings` query parameter is appended, the endpoint returns approximately 365 KB of JSON containing the full system report, including PHP version, all active plugins, WordPress configuration details, database table names, and any API keys or tokens configured in the plugin.

That system report is the prize. Any unauthenticated visitor gets back SMTP credentials, SendGrid and Mailgun API keys, and DKIM tokens. If you configured a transactional email service through Gravity SMTP, which is precisely the use case, your third-party API keys are sitting in that JSON response.

### The attacker infrastructure behind it

This is where the HoneyLabs analysis becomes genuinely useful for defenders. CrowdSec flagged the endpoint under active exploitation, logging 412 distinct IPs against it between May 27 and June 1. HoneyLabs sensors logged 566 IPs reaching for it. 561 of them, 99.1%, sent the same HTTP client fingerprint.

That fingerprint convergence tells you something important. Behind it is a Google Cloud fleet of thousands of short-lived instances, disguised by 3,299 rotating user-agents, sweeping more than 36,000 ports for `.env` files, git configs, credentials, and database dumps.

The CVE is simply the latest entry on a standing wordlist. The same operation sweeps for `terraform.tfstate`, `terraform.tfvars`, Spring Boot `/actuator/configprops`, `/actuator/threaddump`, AWS credential JSON files, and Dockerfiles. The operation does not treat a CVE as a CVE. It treats it as one more file that returns a credential. When the next unauthenticated information disclosure bug ships, it gets appended and swept on the following pass.

That is why a week-old CVE already had hundreds of source IPs on it: the collector was running before the bug existed.

### Fix and immediate mitigations

- Update Gravity SMTP to 2.1.5 or later.
- If you were running an affected version during the May 27 to June 1 exploitation window, treat your SMTP provider API keys, SendGrid/Mailgun credentials, and DKIM tokens as fully compromised and rotate immediately.
- Block web-server access to all dotfiles and `.git` directories at the WAF or NGINX/Apache layer (see the config block below).
- Add `terraform.tfstate` and `terraform.tfvars` to your web-server deny list. These files should never be reachable from the internet in any configuration.

```nginx
# Nginx: deny dot-files, git configs, and common credential leaks
# Add to your server {} block
location ~* (\.env|\.git|terraform\.tfstate|terraform\.tfvars|actuator|\.bash_history|phpinfo\.php) {
    deny all;
    return 404;
}

location ~ /\. {
    deny all;
    access_log off;
    log_not_found off;
}
```

<!-- INTERNAL_LINK: secrets management in AWS with Secrets Manager and SSM | aws-secrets-manager-guide -->

---

## Microsoft Azure and Windows CVEs: the June 2026 Patch Tuesday wave

Microsoft's June 2026 security update includes 206 vulnerabilities, 32 of which are marked critical. Of those 32 critical entries, 28 are remote code execution vulnerabilities affecting Windows Active Directory, Windows Kerberos KDC, Windows Remote Desktop client, Azure Kubernetes Service (AKS), Microsoft Office, Microsoft Outlook, and the Windows HTTP Protocol Stack.

For cloud architects the Azure-facing items are the priority triage. The June batch includes virtualisation escapes, identity service bugs, and management API vulnerabilities, alongside code injection and tampering fixes in .NET, Visual Studio, and PowerShell.

The four Microsoft MSRC CVEs referenced in this guide, CVE-2026-46293, CVE-2026-46291, CVE-2026-46274, and CVE-2026-28387, fall within this June 2026 release window. At time of writing the MSRC detail pages require JavaScript to render, but the product families involved (Azure services and Windows networking components) are consistent with the broader June release profile. Check the [MSRC Security Update Guide](https://msrc.microsoft.com/update-guide/) directly for current exploitability ratings and apply patches in priority order based on CVSS score and CISA KEV status.

### Microsoft Defender: three actively exploited CVEs

Three Defender vulnerabilities reached exploitation in the wild earlier in 2026 and warrant specific attention for any hybrid cloud environment that includes Windows endpoints or servers feeding into Azure workloads.

CVE-2026-41091 is a local privilege elevation vulnerability caused by the Microsoft Malware Protection Engine improperly resolving links before accessing files. CISA confirmed active exploitation and added it to the Known Exploited Vulnerabilities catalogue.

CVE-2026-45498 causes a denial-of-service condition that prevents Microsoft Defender from functioning. Knocking out endpoint protection before deploying further payloads is a well-established attacker technique, and this fits that pattern directly.

Both have been addressed in Microsoft Defender Antimalware Platform versions 1.1.26040.8 and 4.18.26040.7 respectively.

CVE-2026-45585, named "YellowKey", is a Windows security feature bypass zero-day that targets BitLocker full-disk encryption protections. The exploit abuses the Windows Recovery Environment by manipulating NTFS transaction logs and recovery configuration files, forcing WinRE to launch a privileged command prompt while the disk remains transparently decrypted by the TPM. For UK public sector and financial services organisations running encrypted Windows estates on Azure-joined devices, this should be in your risk register immediately.

<!-- INTERNAL_LINK: Azure AD Conditional Access and device compliance policies | azure-conditional-access-guide -->

---

## The credential harvesting supply chain

CVE-2026-4020 is a symptom of a wider industrial-scale operation that directly threatens cloud credential stores. You need to understand the full pipeline to defend against it.

The DFIR Report documented the Bissa scanner collecting 30,000 distinct `.env` files in eleven days in April, shipping them to cloud storage. Those files are then parsed for actionable credentials: AWS access key IDs, GCP service account JSON, Azure client secrets. They are either used directly or sold.

The Shai-Hulud offensive framework, attributed to threat actor TeamPCP, sits at the other end of this supply chain. It implements a full AWS credential chain resolver covering environment variables, web identity token files, ECS container metadata, and EC2 IMDSv2. Once credentials are obtained, the toolkit enumerates AWS Secrets Manager and SSM Parameter Store across all 17 default AWS regions, reading every secret value with decryption enabled.

That last point matters. If an attacker gets hold of even a moderately privileged IAM credential, they will enumerate your secrets store. The access key compromise is not the end of the incident. It is the beginning. The actual blast radius depends on what that key can read.

### Hardening your AWS credential surface

The following IAM Service Control Policy (SCP) restricts `secretsmanager:GetSecretValue` and prevents access to `ssm:GetParameter` from outside your trusted account boundary, limiting the damage a stolen credential can do. Apply this at the AWS Organisation level:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenySecretsReadOutsideTrustedAccounts",
      "Effect": "Deny",
      "Action": [
        "secretsmanager:GetSecretValue",
        "ssm:GetParameter",
        "ssm:GetParameters",
        "ssm:GetParametersByPath"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalAccount": [
            "111111111111",
            "222222222222"
          ]
        },
        "BoolIfExists": {
          "aws:PrincipalIsAWSService": "false"
        }
      }
    },
    {
      "Sid": "RequireIMDSv2",
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

The `RequireIMDSv2` statement is not optional. IMDSv1 is the well-documented path by which container escapes and SSRF vulnerabilities turn into full account compromise. TeamPCP's credential chain resolver explicitly targets EC2 IMDSv2. Enforcing IMDSv2 makes that harder, but any instance still on IMDSv1 remains trivially vulnerable to SSRF-to-credential theft.

---

## Detection and response: AWS and Azure tooling

Knowing the CVEs is necessary but not sufficient. The gap between "we know about this CVE" and "we detected exploitation" is where most organisations fail, and where FCA Operational Resilience requirements apply most directly.

### AWS: Amazon Inspector, GuardDuty, and Security Hub

Amazon Inspector calculates a contextualised score for each finding by correlating the CVSS base score with network reachability results and exploitability data. Use this score for triage, not the raw NVD base score.

Security Hub now calculates exposures in near real-time and includes threat correlation from GuardDuty alongside vulnerability and misconfiguration analysis. When GuardDuty detects threats, Amazon Inspector identifies vulnerabilities, or Security Hub CSPM discovers misconfigurations, Security Hub automatically correlates those findings and updates associated exposures.

For your vulnerability management programme, enable Amazon Inspector, Amazon GuardDuty, AWS Health, and IAM Access Analyzer in each account. All four automatically send findings to Security Hub CSPM.

The AWS CLI command below pulls all CRITICAL and HIGH Inspector findings in your current region that have an associated CVE and have not yet been remediated. Run this as a daily triage view during active exploit campaigns:

```bash
# Pull critical and high Inspector CVE findings — active/unfixed only
aws inspector2 list-findings \
  --filter-criteria '{
    "findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}],
    "severity": [
      {"comparison": "EQUALS", "value": "CRITICAL"},
      {"comparison": "EQUALS", "value": "HIGH"}
    ],
    "findingType": [{"comparison": "EQUALS", "value": "PACKAGE_VULNERABILITY"}]
  }' \
  --sort-criteria '{"field": "INSPECTOR_SCORE", "sortOrder": "DESC"}' \
  --query 'findings[*].{
    Resource:resources[0].id,
    CVE:packageVulnerabilityDetails.vulnerabilityId,
    Score:inspectorScore,
    Status:findingStatus,
    Remediation:remediation.recommendation.text
  }' \
  --output table
```

GuardDuty findings to monitor specifically in the context of the credential-harvesting campaigns described in this guide:

- `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.InsideAWS` -- EC2 credentials being used from outside the instance's expected network path
- `Discovery:S3/MaliciousIPCaller.Custom` -- bucket enumeration from a known-bad IP
- `CredentialAccess:IAMUser/AnomalousBehavior` -- unusual `secretsmanager:GetSecretValue` call patterns
- `Execution:Lambda/MaliciousLambdaExecution` -- Lambda function behaviour consistent with the Shai-Hulud toolkit's region-sweeping enumeration

### Azure: Defender for Cloud and Secure Score

For Azure environments, automated malware remediation in Defender for Storage is now generally available. It performs automatic soft-deletion of malicious blobs detected during on-upload or on-demand malware scanning. Soft-deleted blobs are quarantined and recoverable for further investigation.

On the Kubernetes side, Microsoft publishes Critical Security Advisories for AKS covering high-impact security vulnerabilities including zero-days, and maintains a list of ongoing security investigations for CVEs where a patch is not yet available. Subscribe to AKS release notes and security bulletins at `aka.ms/aks/release-notes`. Treating AKS as a managed service that patches itself is one of the most common and costly assumptions I see in enterprise Azure deployments.

<!-- INTERNAL_LINK: AWS Inspector v2 deep dive for container vulnerability scanning | amazon-inspector-containers -->

---

## NCSC guidance and your vulnerability management obligations

The NCSC updated its Vulnerability Management guidance in May 2026. If you have not read it recently, the bar has moved. The NCSC is expecting organisations to deploy software security updates quickly, more frequently, and at scale, including across their supply chains, and is anticipating an influx of updates to address vulnerabilities across all severities, with a number expected to be critical.

Where automatic secure hot patching is available, meaning patching without service disruption, it should be enabled as a priority. Where automatic updates are available more broadly, including for embedded devices, they should be enabled to reduce the workload on support teams.

The NCSC CTO's May 2026 "vulnerability patch wave" blog is direct: where a critical vulnerability is under active exploitation, particularly one affecting an internet-facing system, accelerating the update process is not optional.

For FCA-regulated firms this aligns with PS21/3 Operational Resilience requirements. Your patching SLA for Critical and KEV-listed vulnerabilities needs to be documented, board-approved, and evidenced. A verbal commitment to "patch quickly" is not a demonstrable control. The NCSC's framing is useful for governance conversations too: the decision not to update is a senior-level risk decision, and should be considered in the wider context of organisational risk management policy and practice.

<!-- INTERNAL_LINK: FCA operational resilience and cloud third-party risk | fca-operational-resilience-cloud -->

---

## Common pitfalls and how to avoid them

These are the mistakes I see repeatedly in production AWS and Azure environments during CVE response cycles.

### 1. Treating CVSS score as the sole triage metric

A CVSS 9.8 on a service with no network exposure is lower priority than a CVSS 6.5 on an internet-facing, credential-holding workload. Amazon Inspector's contextualised score correlates the CVSS base score with network reachability and exploitability data. Use that score, not the raw NVD base score.

### 2. Assuming managed services are someone else's problem to patch

They are, until they are not. The AKS Local Privilege Escalation example, CVE-2026-31431 ("Copy Fail"), is instructive. The vulnerability affects the Linux kernel's `algif_aead` module. Although `algif_aead` is not loaded by default on AKS nodes, the kernel's module auto-loading mechanism will load it on demand when any process, including unprivileged containers, creates an AF_ALG socket with AEAD type. The "it's a managed service" assumption breaks whenever your workload's runtime behaviour triggers a kernel module you assumed was dormant.

### 3. Not enforcing IMDSv2 across the fleet

This is the single most common unforced error I encounter. Enforcing it via SCP, as shown above, takes fifteen minutes to deploy organisation-wide via AWS Control Tower. The cost of not doing it is a complete account compromise the first time a workload has an SSRF vulnerability.

### 4. Ignoring the supply chain credential vector

A malicious npm package impersonating the legitimate Bitwarden CLI was published to npm in April 2026. It targets developer workstations, CI/CD pipelines, and cloud provider credentials across AWS, Azure, and GCP. The package was downloaded thousands of times before being flagged. Its payload harvests secrets from local filesystems, environment variables, GitHub Actions, and cloud secret managers.

Your CVE management programme must include dependency scanning of your CI/CD toolchain, not just your deployed application dependencies. If your pipeline runner has read access to `~/.aws/credentials` or injects `AWS_SECRET_ACCESS_KEY` as an environment variable, a malicious package in your dependency tree is equivalent to an IAM credential leak.

### 5. Rotating credentials after the exposure window, not immediately

If you were exposed during a known exploitation window, your credentials were almost certainly read. The instinct to wait before rotating, out of fear of breaking production, is a false economy. Rotating a compromised API key costs minutes. An undetected credential abuse incident costs months of IR work and, in GDPR terms, a potentially reportable breach.

64% of secrets leaked historically were still active years later. Detection without rotation is theatre.

### 6. Over-relying on WAF rules as CVE mitigation

WAF rules are compensating controls, not patches. Deploying a WAF rule to neutralise an exploit at the network edge buys you time to patch. It is not a permanent fix. Treat it as a runway, not a destination.

### 7. Missing the Microsoft coordinated disclosure tension

The Nightmare Eclipse vs. MSRC story running through 2026 is worth understanding. Multiple leading voices in the vulnerability disclosure community have expressed concern that Microsoft's invocation of its Digital Crimes Unit may prove counterproductive, if it causes researchers to back away from mutually beneficial engagements with MSRC. From a defender's perspective, a chilled researcher community means fewer coordinated disclosures and more abrupt zero-day drops, shortening your response window further. Monitor the MSRC Security Update Guide and the Zero Day Initiative blog as primary sources.

---

## Building a cloud CVE response playbook

The following CloudFormation snippet provisions an EventBridge rule that fires a Lambda function whenever AWS Security Hub receives a new CRITICAL finding linked to a CVE from Amazon Inspector. Use this as the skeleton for an automated triage workflow. The Lambda would enrich the finding, create a ServiceNow or Jira ticket, and page the on-call engineer:

```yaml
# CloudFormation: Auto-triage Security Hub Critical CVE findings
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Route critical Inspector CVE findings to triage Lambda'

Resources:
  CveCriticalTriageRule:
    Type: AWS::Events::Rule
    Properties:
      Name: security-hub-critical-cve-triage
      Description: 'Fire on CRITICAL Inspector CVE findings in Security Hub'
      EventPattern:
        source:
          - aws.securityhub
        detail-type:
          - Security Hub Findings - Imported
        detail:
          findings:
            Severity:
              Label:
                - CRITICAL
            FindingProviderFields:
              Severity:
                Label:
                  - CRITICAL
            ProductArn:
              - prefix: 'arn:aws:securityhub:*:*:product/aws/inspector'
            Types:
              - prefix: 'Software and Configuration Checks/Vulnerabilities/CVE'
      State: ENABLED
      Targets:
        - Arn: !GetAtt CveTriageLambda.Arn
          Id: CveTriageTarget

  CveTriageLambdaPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref CveTriageLambda
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt CveCriticalTriageRule.Arn

  CveTriageLambda:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: security-hub-cve-triage
      Runtime: python3.12
      Handler: index.handler
      Timeout: 30
      Role: !GetAtt CveTriageLambdaRole.Arn
      Code:
        ZipFile: |
          import json, boto3, os

          def handler(event, context):
              findings = event['detail']['findings']
              for f in findings:
                  cve_id = f.get('PackageVulnerabilityDetails', {}).get('VulnerabilityId', 'UNKNOWN')
                  resource = f.get('Resources', [{}])[0].get('Id', 'UNKNOWN')
                  score = f.get('FindingProviderFields', {}).get('Severity', {}).get('Original', '?')
                  print(f"CRITICAL CVE FINDING: {cve_id} on {resource} (score: {score})")
                  # TODO: post to Slack/Teams, create ITSM ticket, page on-call
              return {'statusCode': 200}

  CveTriageLambdaRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

This gets you from a CRITICAL Inspector finding to a visible ticket in under 60 seconds. The alternative, a human reviewing Security Hub daily, introduces the exact dwell-time problem that makes recent cloud security CVEs so damaging at scale.

---

## Key takeaways

The exploitation window has collapsed. During one incident, GTIG observed threat actors deploying cryptocurrency miners within approximately 48 hours of a vulnerability's public disclosure. Your patch SLA must reflect this reality, not the 30-day cycles inherited from on-premises practice.

CVEs are now credential delivery mechanisms. CVE-2026-4020 is less about traditional exploitation and more about credential exfiltration. Google's H1 2026 Threat Horizons report puts identity compromise behind 83% of cloud intrusions, much of it seeded by exposed secrets. The harvester fleet described above is what the front of that supply chain looks like in practice.

Software vulnerabilities have overtaken credentials as the primary cloud attack vector. In the second half of 2025, software vulnerabilities accounted for 44.5% of initial access vectors in observed cloud intrusions. Rebalance your detection investment accordingly.

IMDSv2 enforcement and secrets-access SCPs are not optional. They are fast to deploy and materially reduce the blast radius of any credential compromise or SSRF vulnerability. The SCP template in this guide can be deployed today.

Automate the triage loop. Security Hub calculates exposures in near real-time, automatically correlating GuardDuty threats with Inspector CVE findings and Security Hub misconfigurations. Manual daily reviews are not sufficient. Use EventBridge automation to route CRITICAL CVE findings to your ticketing system within seconds of detection.

NCSC guidance has teeth. The NCSC's May 2026 vulnerability management update explicitly frames delayed patching of actively exploited internet-facing systems as an unacceptable risk position. The decision not to update is a senior-level risk decision and should be considered in the wider context of organisational risk management policy and practice. Document your patching SLAs, get them approved at board level, and evidence compliance. Both the NCSC and the FCA now expect it.

---

*This guide reflects the threat landscape as of June 2026. Recent cloud security CVEs evolve quickly; subscribe to the [NCSC vulnerability alerts feed](https://www.ncsc.gov.uk/section/keep-up-to-date/ncsc-alerts-advisories-guidance), CISA's Known Exploited Vulnerabilities catalogue, and your cloud provider's security bulletins to stay current between updates to this guide.*