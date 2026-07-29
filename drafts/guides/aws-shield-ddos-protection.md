---
title: "AWS Shield DDoS Protection: A Practitioner's Guide for 2025 and Beyond"
date: 2026-07-29
description: "A deep-dive guide to AWS Shield DDoS protection covering Standard vs Advanced, the new Anti-DDoS managed rule group, SRT engagement, and common pitfalls."
tags: ["aws-shield", "ddos-protection", "aws-waf", "cloud-security", "aws"]
slug: "aws-shield-ddos-protection"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2439
draft: false
---

# AWS Shield DDoS protection: a practitioner's guide for 2025 and beyond

The threat environment for UK organisations running workloads on AWS is genuinely active right now. In December 2025, the NCSC co-sealed an advisory calling out pro-Russian hacktivist groups targeting government and private sector entities in NATO member states, with the NCSC's Director of National Resilience noting that "denial-of-service attacks may be technically simple, their impact can be significant." Whether you are protecting a retail payment platform, a government-facing portal, or a regulated financial service, AWS Shield DDoS protection is the foundational layer you need to get right. It is also going through its most significant architectural change in years. This guide covers tier selection, the new Anti-DDoS managed rule group, SRT engagement, multi-account deployment, and the mistakes I see organisations make repeatedly.

<!-- INTERNAL_LINK: AWS WAF configuration deep-dive | aws-waf-configuration -->
<!-- INTERNAL_LINK: shared responsibility model | shared-responsibility-model-cloud-security -->

---

## Shield Standard vs Shield Advanced: choosing the right tier

AWS Shield offers two tiers: Standard (free) and Advanced ($3,000/month). The choice is not purely a cost question. It is a question of what operational risk you are willing to carry.

### Shield Standard

Shield Standard is included at no additional cost for all AWS accounts. It provides always-on detection that monitors network traffic continuously and applies dynamic, automatic inline mitigations without any additional configuration.

Standard protects against commodity volumetric and protocol attacks at Layers 3 and 4. For anything business-critical or revenue-generating, that is not enough.

### Shield Advanced

Shield Advanced extends protection to include sophisticated Layer 7 defences, real-time attack visibility, cost protection guarantees, and access to the AWS Shield Response Team (SRT). It supports a broader range of protected resource types and integrates tightly with AWS WAF for application layer mitigation.

AWS describes the coverage as enhanced protections for applications running on protected Amazon EC2, Elastic Load Balancing, Amazon CloudFront, AWS Global Accelerator, and Route 53 resources against more sophisticated and larger attacks.

The resource types matter in practice:

- CloudFront distributions get the most comprehensive protection, drawing on AWS edge network scale and tight WAF integration.
- Route 53 hosted zones gain protection against DNS-specific attack vectors including query floods.
- Application Load Balancers and Classic Load Balancers support both network and application layer protection when associated with WAF WebACLs.
- Elastic IP addresses attached to EC2 instances or Network Load Balancers cover workloads requiring direct internet exposure.

For FCA-regulated firms and organisations processing personal data under UK GDPR, the cost protection argument is often the deciding factor. Shield Advanced includes DDoS cost protection against scaling charges that result from a DDoS attack causing usage spikes on protected EC2, ELB, CloudFront, Global Accelerator, or Route 53 resources. If those resources scale up in response to an attack, you can request credits via the regular AWS Support channel. A sustained L7 flood that triggers auto-scaling across a large estate can run up a significant AWS bill in hours. Credits do not cover everything, but they take the edge off the worst outcomes.

---

## The new Anti-DDoS managed rule group: what has changed

This is the most operationally significant development in AWS Shield DDoS protection for some time. If you are an existing Shield Advanced customer, you need to act before January 2027.

In June 2025, AWS launched the AWS WAF Anti-DDoS managed rule group, built specifically for application-layer (L7) DDoS protection. Shield Advanced is adopting it as the default application-layer protection, and eventually as the only one.

AWS will discontinue Shield Advanced application-layer automatic mitigation on January 1, 2027. Resources that have not migrated to the rule group will lose automatic application-layer DDoS protection on that date. Do not leave this until Q4 2026.

### What the new rule group delivers

The improvements over the legacy L7 automatic mitigation are material:

- Detection and mitigation happens within seconds rather than minutes.
- The web ACL capacity requirement drops from 150 to 50 WCUs. A dashboard showing DDoS events and traffic insights is included, and every inspected request gets a label you can reference in custom AWS WAF rules.
- You do not pay for attack traffic. During active mitigation, blocked DDoS requests are excluded from your monthly count, covering AWS WAF request fees, Anti-DDoS managed rule group request fees, and Shield Advanced request charges.
- The rule group learns normal traffic patterns, responds to attacks independently of health checks, and introduces a Challenge action alongside Block and Count.

The rule group generates labels with the namespace prefix `awswaf:managed:aws:anti-ddos:`. Two labels worth understanding:

- `awswaf:managed:aws:anti-ddos:event-detected` indicates that the rule group has detected a DDoS event on the protected resource. Every request going to that resource gets this label while the event is active, so legitimate and attack traffic both receive it.
- `awswaf:managed:aws:anti-ddos:ddos-request` indicates the request is coming from a source suspected of participating in the event.

You can match on those labels in your own AWS WAF rules when you need logic the rule group does not cover on its own.

### Migration approach

Between July 27 and August 7, 2026, AWS will add the Anti-DDoS managed rule group in Count mode to eligible Shield Advanced web ACLs. Customers can evaluate and migrate as soon as the rule group appears in their web ACL, ahead of the automatic upgrade in October.

During the evaluation period: start with the Low sensitivity setting for Block actions, review the dashboard and label data before adjusting, check rule priority, configure URI exemptions for any unsupported paths, and update your infrastructure-as-code templates once the rule group is added automatically.

If you manage rules through AWS Firewall Manager, contact AWS Support before you start. It will save you having to unwind things later.

### CloudFormation / CDK example: adding the Anti-DDoS rule group to a web ACL

The rule group name is `AWSManagedRulesAntiDDoSRuleSet` with vendor `AWS`. The snippet below adds it to an existing WAF Web ACL in Count mode, which is the right starting point for any migration:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: Web ACL with Anti-DDoS managed rule group in Count mode

Resources:
  AppWebACL:
    Type: AWS::WAFv2::WebACL
    Properties:
      Name: app-web-acl-with-antiddos
      Scope: CLOUDFRONT          # or REGIONAL for ALB/API GW
      DefaultAction:
        Allow: {}
      VisibilityConfig:
        SampledRequestsEnabled: true
        CloudWatchMetricsEnabled: true
        MetricName: AppWebACL
      Rules:
        - Name: AWSAntiDDoSRuleSet
          Priority: 0
          OverrideAction:
            Count: {}            # Switch to None: {} once validated in production
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: AWSAntiDDoSRuleSet
          Statement:
            ManagedRuleGroupStatement:
              VendorName: AWS
              Name: AWSManagedRulesAntiDDoSRuleSet
              # Optional: configure sensitivity overrides
              ManagedRuleGroupConfigs:
                - AWSManagedRulesACFPConfig:
                    EnableRegexInPath: false
```

Once you have validated detection in Count mode by comparing `DDoSDetected` and `DDoSAttackRequests` CloudWatch metrics against your baseline, switch `OverrideAction` to `None: {}` to allow the rule group to block and challenge as configured. Update your IaC templates in source control at the same time. Do not leave production state divergent from your repository.

<!-- INTERNAL_LINK: AWS Security Hub for centralised findings | aws-security-hub-guide -->

---

## SRT engagement and health-based detection

The Shield Response Team is one of the most underused features in the Shield Advanced subscription. Many teams subscribe to Advanced and never configure SRT access properly, which means during an active attack they are starting from scratch.

The SRT consists of security engineers who specialise in DDoS event response. You can optionally grant them permissions to manage resources on your behalf during an event. For customers on Business or Enterprise support plans, Shield Advanced provides 24/7 access to the SRT, which can be engaged before, during, or after an attack. They will triage incidents, identify root causes, and apply mitigations directly.

### Proactive engagement: the configuration most teams skip

With proactive engagement enabled, the SRT contacts you directly if the Route 53 health check associated with your protected resource becomes unhealthy during a Shield Advanced-detected event. This gets expert eyes on your incident faster, at the point where application availability is actually at risk.

Health checks are required for SRT proactive engagement. Using them with Shield Advanced also reduces false positives and speeds up detection and mitigation when a protected resource is unhealthy.

To configure this via the AWS CLI:

```bash
# Step 1: Register emergency contacts (replace with your on-call details)
aws shield update-emergency-contact-settings \
  --emergency-contact-list \
    '[
      {
        "EmailAddress": "security-oncall@example.co.uk",
        "PhoneNumber": "+44-20-0000-0000",
        "ContactNotes": "Primary SOC — available 24/7. Escalate to CISO if no response in 15 mins."
      },
      {
        "EmailAddress": "ciso@example.co.uk",
        "PhoneNumber": "+44-20-0000-0001",
        "ContactNotes": "Secondary — CISO. Engage if SOC unavailable."
      }
    ]'

# Step 2: Enable proactive engagement
aws shield enable-proactive-engagement

# Step 3: Associate a Route 53 health check with a protected resource
# (replace ARNs and health check ID with your own values)
aws shield associate-health-check \
  --protection-id <YOUR_PROTECTION_ID> \
  --health-check-arn arn:aws:route53:::healthcheck/<YOUR_HEALTH_CHECK_ID>
```

You can configure up to ten contacts for proactive engagement. Include time zones and escalation paths in the `ContactNotes` field. The SRT will use them.

<!-- INTERNAL_LINK: cloud incident response playbooks | cloud-incident-response -->

---

## Multi-account deployment with AWS Firewall Manager

For any organisation running a meaningful AWS estate across multiple accounts under AWS Organisations, deploying Shield Advanced manually per account is not sustainable. AWS Firewall Manager is the right answer.

Firewall Manager lets you configure protections once and apply them automatically across accounts and resources, including new accounts that join the organisation. It will subscribe all member accounts to Shield Advanced and add protection to resources as they are created. You can also integrate Firewall Manager with AWS Security Hub to get a single dashboard reporting DDoS events detected by Shield Advanced alongside Firewall Manager compliance findings, including out-of-compliance resources.

For Financial Services organisations under FCA oversight, this centralised visibility matters. Regulators expect demonstrable evidence of consistent control application across your estate, and "we checked each account manually" is not a credible answer at scale.

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->
<!-- INTERNAL_LINK: cloud compliance frameworks | cloud-compliance-frameworks -->

---

## Common pitfalls and how to avoid them

These are the mistakes I see most often in production deployments across regulated UK sectors.

### 1. Subscribing to Advanced but never protecting resources

Shield Advanced subscription does not automatically protect anything. You must explicitly add resources to protection. Teams often subscribe, check a compliance box, and never complete the resource association step. Audit your protections list in the Shield console. Gaps are common.

### 2. Deploying the Anti-DDoS rule group straight into Block mode

AWS guidance is clear: start with the Low sensitivity setting for Block actions, then adjust based on dashboard data and labels. Going straight to Block without a baseline Count period in production is how you accidentally block legitimate users. Spend at least one full week in Count mode, correlating labels against your application logs.

### 3. Assuming CloudFront is always the right ingress point

Shield Advanced is available globally on CloudFront, Global Accelerator, and Route 53 edge locations, and you can protect web applications hosted anywhere by deploying CloudFront in front of your application. But if your architecture exposes ALBs or Elastic IPs directly to the internet without CloudFront, you lose edge-scale absorption capacity. Review your ingress architecture as part of your DDoS readiness posture.

### 4. Not configuring health checks before an attack

Health checks must be reporting healthy when you associate them with your Shield Advanced protections. You cannot retroactively configure health-based detection during an active incident and expect the SRT to engage immediately. Set this up when things are quiet.

### 5. Ignoring the WCU budget implications

Shield Advanced does not cover additional non-standard AWS WAF costs for protected resources, including Bot Control, the CAPTCHA rule action, and web ACLs using more than 1,500 WCUs. Build your WAF Web ACL with WCU headroom in mind. The new Anti-DDoS rule group costs 50 WCUs, down from 150 for the legacy L7AM, which is a real improvement, but you still need budget headroom for your other managed rule groups.

### 6. Missing the January 2027 L7AM retirement deadline

The Shield Advanced application-layer automatic mitigation feature retires on January 1, 2027. Anything still relying on it needs to be migrated by then. If you are managing rules through AWS Firewall Manager, plan the migration carefully and involve AWS Support early.

<!-- INTERNAL_LINK: AWS WAF configuration and managed rule groups | aws-waf-configuration -->
<!-- INTERNAL_LINK: cloud threat detection | cloud-threat-detection -->

---

## NCSC alignment

The NCSC's guidance on preparing for denial-of-service attacks makes clear that organisations cannot rely solely on their own infrastructure to absorb attacks. A determined attacker will nearly always be able to send more traffic than most organisations can handle unaided, and to successfully mitigate denial of service attacks you may need to call on one or more service providers to help.

AWS Shield Advanced, combined with the edge scale of CloudFront and the SRT, is precisely the kind of upstream defence the NCSC guidance points toward. The NCSC's DoS guidance collection is freely available at `ncsc.gov.uk` and is worth reading alongside your AWS architecture review. The two are complementary.

<!-- INTERNAL_LINK: AWS Well-Architected Security pillar | aws-well-architected-security -->

---

## Key takeaways

- The L7 automatic mitigation retirement is real. AWS will discontinue Shield Advanced application-layer automatic mitigation on January 1, 2027. Migrate to the Anti-DDoS managed rule group before then. Start in Count mode, validate metrics, then enable Block and Challenge.
- Standard is a baseline, not a strategy. For any production or regulated workload, Shield Advanced is the right tier. SRT access, L7 protection, and cost protection together justify the subscription cost.
- Health checks are non-negotiable for SRT proactive engagement. Shield Advanced proactive engagement is only available for resources with health-based detection enabled. Configure them now, not during an incident.
- Use Firewall Manager for consistent, organisation-wide coverage. Firewall Manager applies protections automatically across accounts and resources as your estate grows. Manual per-account management creates coverage gaps.
- Align with NCSC DoS guidance. AWS Shield is the upstream, provider-level defence the NCSC recommends. Document your DDoS response runbook and test it. Having the tooling configured is necessary but not sufficient.
- Review the Anti-DDoS dashboard actively. AWS recommends comparing the `DDoSDetected` and `DDoSAttackRequests` metrics to validate detection and using AWS WAF labels to analyse suspicious requests. Treat it as a regular operational review, not a break-glass console.