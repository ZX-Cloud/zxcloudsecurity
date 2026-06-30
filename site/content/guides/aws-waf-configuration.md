+++
title = "AWS WAF Configuration: A Practitioner's Guide"
date = "2026-06-30T08:00:00Z"
slug = "aws-waf-configuration"
description = "A deep-dive into AWS WAF configuration covering managed rules, rate limiting, ALB HTTP/2 CVEs, and AI workload protection for security architects."
keywords = ["AWS WAF", "AWS WAF configuration", "web application firewall AWS", "AWS WAF managed rules", "WAF rate limiting", "AWS WAF terraform", "AWS Firewall Manager", "CVE-2026-13763"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

If you run internet-facing workloads on AWS, getting your WAF configuration right is no longer optional. It is table stakes for FCA-regulated services, GDPR compliance, and the NCSC's Cyber Essentials Plus framework. What has changed in 2026 is the scope of what WAF now needs to protect: not just your ALBs and CloudFront distributions, but agentic AI workloads running on Amazon Bedrock AgentCore Gateway, and APIs that attract a growing volume of automated traffic. Two disclosures in the last 72 hours make this more pressing than usual. One is a major capability release, the other a critical vulnerability bulletin. Both require your attention now.

This guide covers the fundamentals of building a production-grade WAF posture, the rule ordering and logging patterns that matter in practice, and the mistakes I see repeatedly across financial services and government engagements.

---

## What AWS WAF actually protects (and what it doesn't)

Before getting into configuration, be precise about the service model. AWS WAF is a web application firewall that monitors the HTTP(S) requests forwarded to your protected resources.

Supported resource types include CloudFront distributions, API Gateway REST APIs, Application Load Balancers, AppSync GraphQL APIs, Cognito user pools, App Runner services, AWS Amplify, Amazon Bedrock AgentCore Gateway, and Verified Access instances.

What WAF does not do: it is not a network firewall (use AWS Network Firewall or Security Groups for that), it does not provide TLS termination inspection beyond the HTTP layer, and it has no native understanding of your application's authentication state. Those are separate problems requiring separate controls.

### The June 2026 scope expansion: AgentCore Gateway

This is genuinely new and worth flagging to your architects and CTOs. AWS has announced general availability of AWS WAF protection for Amazon Bedrock AgentCore Gateway, giving you the ability to protect agentic AI workloads from common web exploits and abuse.

As enterprises move agentic applications from prototype to production, this launch lets security and platform teams apply consistent, customisable web protections at the Gateway layer, including IP-based access controls, rate-based rules, and AWS Managed Rule Groups covering common rule sets, known bad inputs, and Bot Control.

The practical benefit is straightforward: you configure the protection pack once at the Gateway level, and AWS WAF applies it to every target behind that Gateway. A single configuration covers all downstream tools, agents, and integrations.

If you are building AI agent pipelines on Bedrock, your WAF posture now extends to that surface area. Treat it the same way you would treat any public API endpoint.

---

## Critical bulletin: HTTP/2 multi-frame body inspection (CVE-2026-13762 / CVE-2026-13763)

AWS WAF security bulletin 2026-048-AWS (published 29 June 2026) identifies CVE-2026-13762 and CVE-2026-13763, both affecting HTTP/2 multi-frame request body inspection by AWS WAF.

The remediation path splits depending on your deployment:

- CVE-2026-13762 affects AWS WAF deployed with CloudFront. AWS remediated this server-side; no customer action is required.
- CVE-2026-13763 affects AWS WAF deployed with an Application Load Balancer. On 22 May 2026, AWS released a new configuration option on ALB to address this. AWS recommends that customers review and update the WAF HTTP/2 traffic inspection behaviour under target group attributes for HTTP/2 endpoints. This enables ALB to accumulate HTTP/2 data frames before AWS WAF performs inspection.

If you run WAF with ALB and HTTP/2 endpoints: open the target group attributes for your HTTP/2-enabled target groups and enable the new WAF inspection behaviour. This is not applied automatically. Check your Security Hub findings and ALB target group configurations today.

See the [AWS Security Hub guide](/guides/aws-security-hub-guide/) for how to surface WAF compliance findings at organisation scale.

---

## Building your web ACL: rule priority and structure

A web ACL gives you fine-grained control over all of the HTTP(S) requests that your protected resource responds to. The order in which rules are evaluated determines both your security posture and your cost.

### Rule evaluation order

AWS WAF evaluates rules from the lowest numeric priority setting upwards, stopping when it finds a match that terminates evaluation. If no matching rule terminates evaluation, the web ACL default action applies.

The practical implication: place free AWS Managed Rule Groups before Intelligent Threat Mitigation features to control cost. When a request matches a rule with a terminating action, AWS WAF stops processing entirely, which avoids further charges from intelligent threat mitigation rule groups.

A sensible priority ladder for most workloads looks like this:

| Priority | Rule type | Rationale |
|---|---|---|
| 0 | Amazon IP Reputation List | Cheap; eliminates known-bad IPs early |
| 10 | Geo-blocking (if applicable) | Free; cuts volume for UK-only services |
| 20 | Blanket rate-based rule | DDoS baseline before managed rules fire |
| 30 | AWSManagedRulesCommonRuleSet | OWASP Top 10 baseline |
| 40 | AWSManagedRulesKnownBadInputsRuleSet | Log4Shell, SSRF patterns |
| 50 | AWSManagedRulesSQLiRuleSet | Extended SQLi detection |
| 60 | Bot Control (scoped) | Paid; scope down to sensitive paths only |
| 70 | Custom application rules | Business logic enforcement |

### Core AWS managed rule groups

AWS Managed Rules are pre-built rule groups maintained by the AWS Threat Research Team. They provide immediate protection against OWASP Top 10 vulnerabilities without requiring you to write custom rules.

The groups every web ACL should carry:

- `AWSManagedRulesCommonRuleSet` (CRS) protects against OWASP Top 10 including XSS, SQL injection, path traversal, and remote file inclusion. This is the baseline every web ACL should include.
- `AWSManagedRulesKnownBadInputsRuleSet` blocks request patterns known to be malicious, including Log4j/Log4Shell exploit patterns (CVE-2021-44228).
- `AWSManagedRulesSQLiRuleSet` provides additional SQL injection detection using advanced inspection of request bodies, query strings, and headers.
- `AWSManagedRulesAdminProtectionRuleSet` blocks access to administrative pages and endpoints commonly targeted by attackers.

### A working Terraform example

The snippet below shows a production-ready starting point with IP reputation first, CRS second, and a body size override for the `SizeRestrictions_BODY` rule. That rule is the single most common source of false positives in APIs that accept large JSON payloads:

```hcl
resource "aws_wafv2_web_acl" "main" {
  name        = "prod-web-acl"
  description = "Production WAF — zxcloudsecurity.co.uk reference config"
  scope       = "REGIONAL"

  default_action {
    allow {}
  }

  # Priority 0: Amazon IP Reputation — free, terminates early
  rule {
    name     = "AWSIPReputation"
    priority = 0

    override_action { none {} }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAmazonIpReputationList"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      sampled_requests_enabled   = true
      cloudwatch_metrics_enabled = true
      metric_name                = "IPReputation"
    }
  }

  # Priority 10: Blanket rate-based rule — 2000 req / 5 min per IP
  rule {
    name     = "BlanketRateLimit"
    priority = 10

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 2000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      sampled_requests_enabled   = true
      cloudwatch_metrics_enabled = true
      metric_name                = "BlanketRateLimit"
    }
  }

  # Priority 20: Common Rule Set — OWASP Top 10
  # SizeRestrictions_BODY overridden to Count to prevent false positives
  # on APIs accepting large JSON bodies. Review sampled requests before
  # switching to Block.
  rule {
    name     = "AWSCommonRules"
    priority = 20

    override_action { none {} }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"

        rule_action_override {
          name = "SizeRestrictions_BODY"
          action_to_use { count {} }
        }
      }
    }

    visibility_config {
      sampled_requests_enabled   = true
      cloudwatch_metrics_enabled = true
      metric_name                = "CommonRules"
    }
  }

  # Priority 30: Known Bad Inputs — Log4Shell, SSRF, Spring4Shell
  rule {
    name     = "AWSKnownBadInputs"
    priority = 30

    override_action { none {} }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      sampled_requests_enabled   = true
      cloudwatch_metrics_enabled = true
      metric_name                = "KnownBadInputs"
    }
  }

  visibility_config {
    sampled_requests_enabled   = true
    cloudwatch_metrics_enabled = true
    metric_name                = "ProdWebACL"
  }
}
```

---

## Rate-based rules: setting thresholds that actually work

The lowest allowable rate limit in AWS WAF rate-based rules dropped from 100 requests to 10, so you now have much finer granularity for login endpoints and sensitive API paths. Do not use arbitrary values.

AWS WAF rate-based rules track requests per IP within an evaluation window of one to five minutes. The five-minute window provides smoother traffic evaluation and reduces false triggers during brief spikes. Use CloudWatch Logs Insights to derive your threshold empirically before going to Block mode. Query your WAF log group with:

```
fields httpRequest.clientIp as ClientIP
| stats count(*) as RequestCount by bin(5m), ClientIP
| stats percentile(RequestCount, 95) as R_95
```

This calculates the 95th percentile of all observed (IP, interval) counts, giving you a single value that represents the high end of normal request rates across your user base. Set your threshold 20 to 30 percent above that figure to give headroom for growth without over-blocking legitimate users.

Each AWS WAF rule can publish CloudWatch metrics, which you can use to trigger alerts for your operations team. That distinction matters in practice: a rate rule firing because of a DDoS attempt looks almost identical in the metrics to one firing because your threshold is too low. The alert should send someone to look at the sampled requests, not just acknowledge and close.

---

## Logging, observability, and SIEM integration

AWS Security Hub controls WAF.11 (logging should be enabled) and WAF.12 (rules should have CloudWatch metrics enabled) are both worth enforcing from the start, not retrospectively during an audit.

By default, logging is disabled when you create a web ACL. This is a configuration step that routinely gets missed under delivery pressure. Automate it: use AWS Config with a remediation rule to enforce logging on all new web ACLs, sending to a Kinesis Data Firehose destination that routes to either S3 (for Athena querying) or CloudWatch Logs (for Logs Insights queries).

Redact sensitive fields from logs, specifically Authorisation headers, cookies, and custom tokens, to avoid storing credentials in plain text. Use log filter expressions to reduce log volume by excluding known-good traffic patterns where appropriate.

For regulated workloads, anything in scope for PCI DSS, FCA SYSC 7, or DORA, ensure WAF logs are shipped to your central SIEM with a retention policy that meets your regulatory minimum. Twelve months is the common baseline I see for UK financial services clients.

---

## Multi-account governance with AWS Firewall Manager

If you manage more than one AWS account, managing web ACLs per account is operationally unsustainable. I have reviewed environments with forty-plus accounts where each team maintained their own web ACLs. The result is always the same: inconsistent rules, new resources that go unprotected because nobody remembered to associate the web ACL, and compliance gaps that show up at the worst possible time.

AWS Firewall Manager lets you define WAF policies once and automatically deploy them across all accounts in your AWS Organisation. New resources matching the policy scope receive WAF protection automatically, with no manual association required. Firewall Manager also routes WAF logs from all accounts to a single centralised destination.

For UK public sector and FCA-regulated firms, this centralised enforcement model maps directly to the NCSC CAF principle of protecting all attack surfaces consistently, not just the ones your most conscientious team happens to manage.

---

## Common pitfalls in AWS WAF configuration

These are patterns I see repeatedly in architecture reviews. Every one of them has produced either a production incident or a compliance finding.

Deploying a web ACL but forgetting to associate it is more common than it should be. An unassociated web ACL does nothing. Use the AWS Config rule `waf-regional-webacl-not-empty` to catch this automatically, because nobody catches it manually when they are busy.

Going straight to Block mode with new managed rules is the number one cause of self-inflicted 403 storms on legitimate users. Before deploying changes in your web ACL for production traffic, test and tune them in a staging environment first. Then run your updated rules in Count mode against production traffic for at least a week before switching to Block. One week of false-positive analysis is cheaper than one hour on an incident bridge.

Scoping Bot Control to all traffic is an expensive mistake. Bot Control is a paid managed rule group, and inspecting every request including `/static/logo.png` produces a large bill with zero security benefit. Limit the scope of inspection to sensitive URI paths and APIs, and exclude static content.

Ignoring WCU limits catches teams by surprise. Using more than 1,500 WCUs in a web ACL incurs costs beyond the basic web ACL price. Model your WCU consumption before stacking multiple managed rule groups and intelligent threat mitigation features on top of each other.

Setting arbitrary rate limits without traffic data leads to either excessive blocking or thresholds so high they provide no protection. Always derive your threshold from actual traffic using CloudWatch Logs Insights or Athena before switching a rate rule from Count to Block.

Ignoring CVE-2026-13763 on ALB deployments is a specific and time-sensitive risk right now. As covered above, this requires manual customer action on ALB target groups. It will not remediate itself.

Creating CloudFront web ACLs in the wrong region is an error that fails silently in some automation pipelines. CloudFront web ACLs must be created in `us-east-1`; regional resources use the resource's own region. Attempting to associate a `eu-west-2` web ACL with a CloudFront distribution will leave your distribution unprotected with no obvious error.

---

## Key takeaways

- Act on CVE-2026-13763 now if you run WAF with an ALB and HTTP/2 endpoints. Review and update target group attributes for WAF HTTP/2 traffic inspection behaviour. This is a customer-action required remediation, not an automatic fix.
- Extend your WAF configuration to AgentCore Gateway if you are deploying agentic AI workloads on Bedrock. The protection pack model means a single configuration covers all downstream tools and integrations behind the Gateway.
- Rule priority is both a security and a cost decision. Place cheap terminating rules (IP reputation, geo-blocking) at the lowest priority numbers so they eliminate traffic before it reaches paid managed rule groups like Bot Control.
- Never skip Count mode. Every new managed rule group or custom rule should run in Count mode against production traffic for at least a week before switching to Block.
- Automate logging enforcement. Default WAF behaviour is logging off. Use AWS Config remediation or a Firewall Manager policy to ensure every web ACL in every account ships logs to your SIEM from day one.
- Use Firewall Manager for anything beyond a single account. Inconsistent per-account WAF posture is a compliance liability under FCA SYSC, DORA, and NCSC CAF. Centralise rule management and log aggregation from the start.

---

## Related Guides

- [AWS Security Hub: A Practitioner's Guide](/guides/aws-security-hub-guide/) — Security Hub control WAF.11 and WAF.12 enforce WAF logging and metrics; centralise your WAF finding aggregation here.
- [Cloud Network Security](/guides/cloud-network-security/) — WAF sits at the application layer; this guide covers the network layer controls that sit beneath it.
- [Cloud Security Vulnerability Management](/guides/cloud-security-vulnerability-management/) — CVE-2026-13763 is a patching obligation; use this guide for the prioritisation framework to manage WAF-related CVEs alongside the rest of your estate.
- [Cloud Compliance Frameworks](/guides/cloud-compliance-frameworks/) — FCA SYSC 7, DORA, and NCSC CAF requirements that WAF logging and Firewall Manager policies help satisfy.
