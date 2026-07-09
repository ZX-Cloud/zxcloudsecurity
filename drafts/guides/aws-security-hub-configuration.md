---
title: "AWS Security Hub Configuration: A Practitioner's Guide for 2026"
date: 2026-07-09
description: "A deep-dive into AWS Security Hub configuration for multi-account AWS environments — covering delegated admin setup, standards, network scanning, and common pitfalls."
tags: ["aws-security-hub", "cloud-security", "cspm", "aws-organisations", "security-configuration"]
slug: "aws-security-hub-configuration"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2281
draft: false
---

# AWS Security Hub configuration: a practitioner's guide for 2026

If your Security Hub configuration still looks like something you stood up in an afternoon back in 2023, you're almost certainly leaving significant detection capability on the table. As of July 2026, Security Hub is no longer a simple findings aggregator. It's a unified security operations platform spanning CSPM, vulnerability management, threat detection, and active network scanning across AWS and Azure environments. For UK financial services organisations under FCA scrutiny and NCSC Cyber Assessment Framework obligations, getting this right matters.

This guide covers how to configure Security Hub properly: multi-account architecture, standards selection, integration with the broader AWS security services stack, the new Network Scanning capability, and the mistakes I see on almost every engagement.

<!-- INTERNAL_LINK: what is CSPM | what-is-cspm-cloud-security-posture-management -->

## Why AWS Security Hub configuration matters more than ever

AWS has brought GuardDuty, Amazon Inspector, Security Hub CSPM, and Amazon Macie together into a single experience that continuously analyses security signals across threats, vulnerabilities, misconfigurations, and sensitive data.

The practical consequence is this: newer capabilities such as exposure findings, real-time risk analytics, and automated correlation require Security Hub CSPM and Amazon Inspector to be enabled. Without them, you won't see those features at all.

If you have Security Hub running but Inspector and CSPM aren't fully wired in, you have a partially assembled engine. This guide helps you assemble it correctly.

<!-- INTERNAL_LINK: AWS Inspector vulnerability management | aws-inspector-vulnerability-management -->

## Multi-account architecture: start with the delegated administrator

The single most impactful architectural decision in any Security Hub deployment is where you run the administrator account. The answer should never be your AWS management account.

Security Hub should be managed from a dedicated security tooling account designated as the delegated administrator. This follows the AWS recommended pattern of separating security operations from billing and organisational management. AWS is explicit about this: users who have access to the management account to handle billing are typically different from the people who need Security Hub access for security management, and the two concerns shouldn't share an account.

The risk argument is straightforward. A compromised Security Hub delegated administrator is serious, but the blast radius is limited to security operations. The attacker cannot delete accounts, change billing, or modify organisation structure, because those capabilities stay in the management account. Keep them separate.

### Enabling delegated administration via CLI

Run the following from the management account to enable trusted access and designate your security tooling account:

```bash
# Step 1: Enable Security Hub as a trusted service in AWS Organisations
aws organizations enable-aws-service-access \
  --service-principal securityhub.amazonaws.com

# Step 2: Designate the delegated administrator
aws securityhub enable-organization-admin-account \
  --admin-account-id <SECURITY_TOOLING_ACCOUNT_ID>

# Step 3: Verify delegation
aws organizations list-delegated-administrators \
  --service-principal securityhub.amazonaws.com

# Step 4: Enable AWS Config (required dependency) across the organisation
aws organizations enable-aws-service-access \
  --service-principal config.amazonaws.com

aws organizations enable-aws-service-access \
  --service-principal config-multiaccountsetup.amazonaws.com

aws organizations register-delegated-administrator \
  --service-principal config.amazonaws.com \
  --account-id <SECURITY_TOOLING_ACCOUNT_ID>
```

> Note: AWS Config is a hard dependency for Security Hub controls. Config rules evaluate resource configurations, and Security Hub uses Config to run its automated compliance checks. Skipping this step is one of the most common reasons controls show up as `NO_DATA`.

<!-- INTERNAL_LINK: AWS compliance and governance | aws-compliance-and-governance -->

## Central configuration: don't leave it as local

Once delegation is established, switch to central configuration immediately. When you integrate Security Hub CSPM with AWS Organisations, you can use central configuration to set up and manage Security Hub across the organisation. AWS strongly recommends it, because it lets the delegated administrator customise security coverage per account and OU rather than relying on account-level settings that you can't control centrally.

With central configuration, you can create a single policy for your entire organisation or different policies for different OUs. Test accounts and production accounts can use completely different configuration policies. That flexibility matters once you're operating at scale.

Here's a representative CloudFormation snippet for setting up the organisation configuration in central mode, deployable from the security tooling account in your home Region:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Security Hub Central Configuration'

Resources:
  SecurityHubOrgConfig:
    Type: AWS::SecurityHub::OrganizationConfiguration
    Properties:
      AutoEnable: true
      AutoEnableStandards: NONE   # We manage standards via policy, not auto-enable
      ConfigurationType: CENTRAL

  ProductionPolicy:
    Type: AWS::SecurityHub::ConfigurationPolicy
    DependsOn: SecurityHubOrgConfig
    Properties:
      Name: "Production-SecurityHub-Policy"
      Description: "Full FSBP + CIS coverage for production OUs"
      ConfigurationPolicy:
        SecurityHub:
          ServiceEnabled: true
          EnabledStandardIdentifiers:
            - "arn:aws:securityhub:eu-west-2::standards/aws-foundational-security-best-practices/v/1.0.0"
            - "arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/5.0.0"
          SecurityControlsConfiguration:
            EnabledSecurityControlIdentifiers: []  # Empty = all controls enabled
```

> Set `AutoEnableStandards: NONE`. Letting AWS auto-enable default standards on new accounts means you lose control over which standards apply, which complicates compliance reporting for FCA or ISO 27001 audits.

<!-- INTERNAL_LINK: AWS IAM Identity Centre for cross-account access | aws-iam-identity-centre -->

## Choosing the right security standards

Which standards you enable should reflect your actual compliance requirements and operational maturity, not what looks comprehensive on a dashboard. Each standard maps to a set of automated security checks that evaluate your AWS resources, and every enabled control generates findings. Be deliberate.

For UK enterprise and regulated environments, my default recommendation is two standards to start with.

The first is AWS Foundational Security Best Practices (FSBP) v1.0.0. This is AWS's own curated set of best practices across more than 30 AWS services, and it's the right baseline for every customer regardless of other compliance requirements.

The second is CIS AWS Foundations Benchmark v5.0.0, published by CIS in March 2025 and supported in Security Hub since October 2025. It covers 40 automated controls across identity and access management, storage, logging, monitoring, and networking. Security Hub holds CIS Security Software Certification for v5.0.0 Level 1 and Level 2.

Don't enable every available standard on day one. Enabling PCI DSS when you don't process card payments generates noise that drowns out genuine signal. Get to near-zero findings on FSBP first, then layer in CIS v5.0.0 for regulated workloads.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->

## Integrating the core security services

Security Hub works best when it's receiving signals from multiple sources. Each integration has a distinct role, and the correlation engine gets meaningfully better when all four are feeding it.

GuardDuty sends threat detection findings covering malicious activity, unauthorised behaviour, and compromised resources, typically within five minutes of detection.

Inspector sends vulnerability findings for EC2, Lambda, and ECR container images, including CVE details and CVSS scores.

Macie sends sensitive data discovery findings for S3 buckets containing PII, financial data, or credentials. For GDPR and UK GDPR obligations, Macie integration isn't optional.

The exposure findings feature specifically requires both Security Hub CSPM and Amazon Inspector. Together they give the Security Hub correlation engine enough telemetry to identify internet-reachable resources with active vulnerabilities and map what an attacker could reach from there. Neither service alone is sufficient for this.

<!-- INTERNAL_LINK: cloud security vulnerability management | cloud-security-vulnerability-management -->

## New in July 2026: network scanning and impact analysis

Two significant capabilities landed in the first week of July 2026 that change what a complete Security Hub configuration should look like.

### Network scanning

Security Hub now includes Network Scanning, which identifies resources in your environment that are reachable from the public internet. Rather than inferring reachability from security group rules and route tables, it probes resources from the internet to detect actual reachability.

This distinction matters in practice. Security group analysis tells you what could be exposed. Network Scanning tells you what is exposed. Those two sets aren't always the same, and attackers are working from the second one.

The capability discovers public IP addresses, virtual machines, and load balancers across AWS and Azure environments, identifies reachable ports, and determines what services are running behind them. Each reachable port generates a Security Hub finding with evidence of the port and service discovered.

For existing customers, Network Scanning is off by default and must be explicitly enabled, either in individual accounts and Regions or organisation-wide via a configuration policy. New Security Hub customers get it on by default. It's included with Security Hub Essentials at no additional cost in all supported commercial Regions.

If you're an existing customer, enable this now. Update your central configuration policy and roll it out organisation-wide.

### Impact analysis for exposure findings

Security Hub has also added impact analysis to exposure findings. Where an exposure finding identifies a resource reachable from the internet, impact analysis maps the downstream resources that could be compromised if that exposure is exploited.

Security Hub analyses the effective permissions of IAM principals associated with exposed resources to identify privilege escalation paths to other resources in your account. The resulting scope appears in a potential attack path graph, and a new Impact Assessment tab shows the prioritised chains of resources an attacker could traverse along with the specific permissions at each step.

For organisations operating under NCSC guidance on risk management, this is the kind of context-driven prioritisation that turns a finding backlog into an actionable remediation queue.

<!-- INTERNAL_LINK: cloud incident response | cloud-incident-response -->
<!-- INTERNAL_LINK: what is zero trust architecture | what-is-zero-trust-architecture -->

## Extending to Azure

Security Hub now monitors Microsoft Azure resources, covering risk analytics, CSPM, vulnerability management, and security response across both clouds. It automatically discovers Azure Virtual Machines, Azure Container Registry images, Azure Function Apps, and Azure identities, then evaluates them for misconfigurations, internet exposure, and software vulnerabilities.

For UK enterprises that are genuinely multicloud, and many in financial services are, this removes the need to maintain parallel tooling and mentally reconcile two consoles. Security Hub provides a single experience for detecting and responding to risks across both environments.

<!-- INTERNAL_LINK: cross-cloud security services comparison | cross-cloud-security-services-comparison -->

## Automating remediation with EventBridge

Findings are only useful if someone acts on them. Security Hub integrates natively with Amazon EventBridge, and you should be routing CRITICAL and HIGH severity findings to your SIEM, ticketing system, or on-call platform.

```json
{
  "source": ["aws.securityhub"],
  "detail-type": ["Findings Imported V2"],
  "detail": {
    "findings": {
      "Severity": {
        "Label": ["CRITICAL", "HIGH"]
      },
      "RecordState": ["ACTIVE"],
      "WorkflowStatus": ["NEW"]
    }
  }
}
```

Pay attention to the event detail type. The unified Security Hub routes findings through EventBridge with a detail type of `"Findings Imported V2"`. The previous `"Security Hub Findings - Imported"` type relates to Security Hub CSPM findings only. If you have existing EventBridge rules using the old detail type, check whether they're capturing the right findings after you migrate to the unified Security Hub. This is a common source of silent gaps in remediation automation.

<!-- INTERNAL_LINK: AWS CloudTrail configuration best practices | aws-cloudtrail-configuration-best-practices -->

## Common mistakes and pitfalls

These are the issues I find on almost every Security Hub engagement. Some are surprisingly common even in mature organisations.

Running the administrator from the management account concentrates risk at the most sensitive layer of your AWS organisation structure. Covered above, but worth repeating.

Not enabling AWS Config in all accounts and active Regions is a frequent oversight. Even management accounts need AWS Config enabled for proper security monitoring. Without it, Security Hub controls return `NO_DATA`, which is worse than a FAILED finding because it's invisible non-compliance.

Enabling all security standards on day one creates thousands of findings before you have a baseline. Enabling PCI DSS, NIST, and CIS simultaneously across 50 accounts before you've triaged anything is a reliable way to ensure nothing gets fixed. Start with FSBP, get to near-zero, then layer in CIS v5.0.0.

Ignoring the finding format difference is a technical issue that bites automation. The unified Security Hub uses OCSF (Open Cybersecurity Schema Framework) for exposure findings, while Security Hub CSPM uses ASFF (AWS Security Finding Format). Automation written against ASFF fields may break against OCSF-formatted findings. Test your EventBridge rules and Lambda handlers after enabling the unified experience.

Leaving Network Scanning disabled on existing deployments is the most common gap I'm seeing right now. It's off by default for existing customers. If you don't explicitly enable it via your central configuration policy or account settings, you're not getting it, even though new accounts get it automatically.

Not setting a home Region leaves you with fragmented findings that can't be correlated across Regions. Security Hub supports cross-Region aggregation via a designated aggregator Region. For UK deployments, `eu-west-2` is the natural choice for data residency reasons.

Treating suppressed findings as resolved is a compliance risk that surfaces in audits. Suppression hides a finding from the active queue but doesn't fix anything. I regularly see organisations with thousands of suppressed findings that have never been remediated. In FCA-regulated environments, an unexplained suppression backlog is an audit liability.

<!-- INTERNAL_LINK: AWS well-architected security | aws-well-architected-security -->
<!-- INTERNAL_LINK: AWS WAF configuration | aws-waf-configuration -->

## Key takeaways

Delegate properly. Always designate a dedicated security tooling account as the Security Hub delegated administrator, never the management account. Use central configuration mode, not local.

Enable the full integration stack. Security Hub's exposure findings and impact analysis only activate when Security Hub CSPM and Amazon Inspector are both enabled. GuardDuty and Macie add further signal depth. Wire all four in.

Enable Network Scanning now. Existing customers must explicitly enable it. It provides confirmed internet reachability evidence, which is categorically more actionable than configuration-based reachability inference.

Choose standards deliberately. Start with FSBP as your universal baseline, add CIS AWS Foundations Benchmark v5.0.0 for regulated environments, and only enable additional standards when you have the operational maturity to handle the findings they generate.

Automate remediation routing. Use EventBridge to route CRITICAL and HIGH severity findings to your SIEM or ticketing platform. Use the `"Findings Imported V2"` detail type for the unified Security Hub, and validate that existing automation still works after migrating to the new finding format.

Audit your suppression queue. Suppressed findings represent accepted risk. Review them quarterly at minimum. In FCA-regulated environments, an unexplained suppression backlog is an audit liability.