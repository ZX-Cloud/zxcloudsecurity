---
title: "Recent Cloud Security CVEs: July 2026 Threat Briefing for AWS Practitioners"
date: 2026-07-09
description: "A deep-dive into the most critical recent cloud security CVEs of mid-2026, covering Apache Airflow, AWS RES, and Esri ArcGIS — with detection and remediation guidance."
tags: ["cloud security", "CVE", "Apache Airflow", "AWS", "vulnerability management"]
slug: "recent-cloud-security-cves"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2184
draft: false
---

# Recent cloud security CVEs: July 2026 threat briefing for AWS practitioners

If you are responsible for cloud security posture, the CVEs published on 7 July 2026 deserve immediate attention. Three ecosystems -- Apache Airflow, AWS Research and Engineering Studio (RES), and Esri Portal for ArcGIS -- produced a cluster of disclosures ranging from critical remote code execution to information disclosure vulnerabilities that quietly undermine access controls your teams have spent months building. At least one carries a CVSS score of 9.8. Another has already drawn active exploitation reports. None have backported fixes available at the time of writing.

For each CVE below, I will tell you what is actually exploitable, what the realistic blast radius looks like in an AWS environment, and what to do about it today.

<!-- INTERNAL_LINK: cloud security vulnerability management programme | cloud-security-vulnerability-management -->

---

## The NVD context problem

Before getting into the individual vulnerabilities, there is a structural issue affecting how you receive CVE intelligence.

On 15 April 2026, NIST announced a fundamental change to the National Vulnerability Database (NVD). CVE disclosure volumes essentially tripled over a five-year span, and NIST is now transitioning to a heavily constrained, risk-based model for vulnerability enrichment. In practice, your scanner will increasingly ingest CVEs without CVSS metadata. Most vulnerabilities will now enter the CVE ecosystem without the enrichment data that automated downstream tooling needs to prioritise them.

Scanners that depend on NVD-supplied CVSS scores are now flying partially blind. Without enrichment, tools will report systems as secure when they are not.

For UK financial services and regulated cloud environments, do not rely solely on your CSPM scanner's severity rating to triage this week's disclosures. Supplement NVD with vendor security advisories, CISA's Known Exploited Vulnerabilities (KEV) catalogue, and feeds such as FIRST's EPSS scores. CISA maintains the authoritative record of vulnerabilities actively exploited in the wild, and the KEV catalogue should be a direct input to your prioritisation framework.

<!-- INTERNAL_LINK: AWS Security Hub for automated CVE triage | aws-security-hub-guide -->
<!-- INTERNAL_LINK: AWS Inspector for vulnerability management | aws-inspector-vulnerability-management -->

---

## CVE-2026-33264: critical Apache Airflow RCE (CVSS 9.8)

This is the headline. If you run Apache Airflow -- on Amazon MWAA, self-hosted on EKS, or via any managed Airflow service -- and you have not already upgraded to 3.3.0, stop reading and go patch.

### What it does

A bug in `BaseSerialization.deserialize()` allowed unrestricted `import_string()` of attacker-controlled class paths when the Scheduler or API Server loaded a serialised DAG. A DAG author could embed a malicious trigger to gain remote code execution on the API Server or Scheduler process, crossing the trust boundary that exists precisely to prevent DAG-author code from executing in those privileged processes.

The violation here is architectural, not merely technical. The Airflow security model explicitly defines that boundary. This deserialization flaw lets an attacker with network access and no privileges achieve complete system compromise, with full impact to confidentiality, integrity, and availability.

### Why it matters in an AWS context

In a typical AWS deployment, the Airflow Scheduler process carries an IAM role with broad permissions: access to S3 data lakes, Secrets Manager, RDS, and often cross-account roles for data pipelines. RCE on the Scheduler means an attacker inherits that IAM role. In regulated environments under FCA SYSC obligations or GDPR data governance requirements, the blast radius extends well beyond the Airflow cluster itself.

### Fix and workaround

Upgrade to `apache-airflow` 3.3.0 or later. As a defence-in-depth mitigation, restrict the `[core] allowed_deserialization_classes` config to a narrow allowlist on deployments where DAG-author trust is limited.

Set this in your `airflow.cfg` or as an environment variable on MWAA:

```ini
[core]
allowed_deserialization_classes = airflow\..*
```

This restricts deserialisation to the `airflow.*` class namespace only, preventing an attacker-controlled class path from being loaded. On Amazon MWAA, you will need to push this via a custom `airflow_local_settings.py` configuration override or wait for AWS to release an updated MWAA engine version. Check the AWS Health Dashboard and MWAA release notes daily until a patched version is available.

<!-- INTERNAL_LINK: Kubernetes security controls for self-hosted Airflow | kubernetes-security-best-practices -->

---

## CVE-2026-48828: Apache Airflow secrets redaction bypass in bulk variables API

Scored at Medium, with CVSS not yet NVD-enriched at time of writing. Do not let that lull you into complacency. This is a data leakage issue that will bypass teams not paying attention to their Airflow variable naming conventions.

### What it does

The Bulk Variables API called the redactor without passing the variable's key, so the key-based `should_hide_value_for_key` check -- which triggers on secret-suffixed key names like `*_password`, `*_token`, and `*_secret` -- could not fire for JSON-decodable variable values. An authenticated UI or API user with bulk Variable read permission could retrieve plaintext values from JSON variables whose key would otherwise trigger redaction.

This affects deployments that store sensitive values in JSON-typed Airflow Variables under secret-suffixed key names. There is no 3.2.x backport; upgrade to 3.3.0.

If your pipelines use Airflow Variables to store database credentials, API keys, or AWS access keys (a common anti-pattern, but widespread in practice), any user with Variable read access can exfiltrate those secrets through the bulk API endpoint.

---

## CVE-2026-48892: Apache Airflow secrets backend credentials exposed via config API

Closely related to CVE-2026-48828, but targeting the Config API rather than Variables. This one specifically affects teams using HashiCorp Vault or AWS Secrets Manager as a secrets backend via environment variable overrides.

### What it does

The Config API surfaced per-key secrets-backend overrides -- environment variables like `AIRFLOW__SECRETS__BACKEND_KWARG__SECRET_ID` and `AIRFLOW__WORKERS__SECRETS_BACKEND_KWARG__SECRET_ID` -- as synthetic config options whose option names were not in `sensitive_config_values`. The masker therefore did not redact them. An authenticated UI or API user with Config read permission could retrieve plaintext secrets-backend credentials (Vault `role_id` and `secret_id`, for example) directly from the Config API response.

This is a serious miscategorisation in Airflow's masking logic. If your Airflow deployment authenticates to HashiCorp Vault using a `role_id` and `secret_id` passed as environment variable overrides -- a very common pattern for AWS-hosted Airflow deployments -- those credentials are visible to any user who can reach the Config API. Upgrade to 3.3.0.

---

## CVE-2026-49296: Apache Airflow DAG source disclosure across team boundaries

The least severe of the Airflow cluster at CVSS 6.5, but worth understanding if you operate a multi-team deployment where DAG source code is considered proprietary or sensitive.

### What it does

Before `apache-airflow` 3.3.0, a user authorised to read one DAG could disclose the source of other DAGs co-located in the same source file. `GET /api/v2/dagSources/{dag_id}` -- and the equivalent DAG-source view in the UI -- returned the entire source file without redacting DAGs the caller was not authorised to read, bypassing per-DAG read authorisation. Deployments that co-locate multiple DAGs in a single file and rely on per-DAG access control to limit source visibility are affected. Single-DAG-per-file deployments are not.

The remediation is either upgrading to 3.3.0 or restructuring your DAG files to adopt a one-DAG-per-file convention. The latter is good practice regardless.

---

## CVE-2026-13020: Esri Portal for ArcGIS weak password recovery (CVSS 8.1)

Not every critical cloud workload runs on AWS-native services. ArcGIS Portal is widespread in UK public sector environments -- local government, emergency services, NHS trusts -- and this one is worth flagging for any team running geospatial or mapping workloads.

### What it does

A weak password recovery mechanism exists in Esri Portal for ArcGIS versions 12.1 and earlier on Windows, Linux, and Kubernetes. A remote, unauthenticated attacker can assume ownership of a user's account by manipulating this mechanism.

The recommended mitigation is to configure an email server with ArcGIS Enterprise to force user self-service password recovery through a properly validated email flow, rather than relying on the vulnerable mechanism. Apply this immediately and wait for a vendor patch.

For UK government deployments running ArcGIS on AWS infrastructure, verify your account recovery configuration now and review CloudTrail for any anomalous password reset activity.

<!-- INTERNAL_LINK: AWS CloudTrail configuration for audit logging | aws-cloudtrail-configuration-best-practices -->

---

## AWS RES symlink arbitrary file read

Not one of the five headline CVEs, but worth flagging for teams running HPC or scientific computing workloads on AWS Research and Engineering Studio (RES).

An improper link resolution issue (CWE-59) in the `Auth.GetUserPrivateKey` API means an authenticated remote user can read arbitrary files on the cluster-manager EC2 instance by replacing their SSH private key file with a symbolic link targeting any file on the host. Because the cluster-manager process runs as root, any file readable by root is exposed, including other users' SSH private keys and application configuration secrets.

Upgrade to RES version 2026.06 to remediate.

<!-- INTERNAL_LINK: AWS IAM best practices for EC2 instance profiles | aws-iam-security-best-practices -->

---

## Detection: CloudTrail and CloudWatch queries for rapid triage

For the Airflow-family CVEs, detection focuses on identifying unusual access patterns to the affected API endpoints. If you are running Airflow behind an AWS ALB with access logs enabled, use the following Athena query against your ALB logs to identify suspicious Config API and Bulk Variables API calls:

```sql
SELECT
  time,
  client_ip,
  request_verb,
  request_url,
  response_processing_time,
  elb_status_code
FROM alb_logs
WHERE
  (request_url LIKE '%/api/v2/config%'
    OR request_url LIKE '%/api/v2/variables%'
    OR request_url LIKE '%/api/v2/dagSources%')
  AND elb_status_code = 200
  AND time > current_timestamp - interval '7' day
ORDER BY time DESC;
```

For the AWS RES symlink vulnerability, review CloudTrail for `GetUserPrivateKey` API calls originating from user identities that do not match expected cluster-manager service accounts:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=GetUserPrivateKey \
  --start-time $(date -d '7 days ago' --utc +%Y-%m-%dT%H:%M:%SZ) \
  --query 'Events[*].{Time:EventTime,User:Username,Source:EventSource}' \
  --output table
```

Alert on any results. Legitimate cluster-manager operations should not generate user-facing `GetUserPrivateKey` events outside of expected key rotation windows.

<!-- INTERNAL_LINK: cloud incident response playbook | cloud-incident-response -->

---

## Common mistakes when responding to this CVE cluster

Assuming MWAA is automatically patched. Amazon MWAA manages the Airflow installation, but it does not instantly adopt new Airflow versions. You remain on your chosen engine version until AWS releases and you opt into the updated version. Check the MWAA release notes and AWS Health Dashboard for your account proactively.

Conflating "authenticated attacker" with "low risk." Several of these CVEs require authentication. In the context of an internal tool like Airflow or ArcGIS, "authenticated" often means any employee with an SSO account. In a post-breach scenario where an attacker has compromised a developer laptop, authenticated APIs are trivially accessible.

Treating CVSS Medium as a "next sprint" problem. CVE-2026-48892 exposes your HashiCorp Vault or AWS Secrets Manager authentication credentials in plaintext over an API. That is not a Medium-priority remediation regardless of the base score. Apply business context to every CVE, not just the raw CVSS number.

Missing the NVD enrichment gap. If your vulnerability management process gates remediation SLAs purely on NVD-sourced severity, you need to revisit that process now. The combination of CISA KEV, vendor bulletins, and EPSS gives you a more reliable signal than NVD alone at this point.

Forgetting forked or customised deployments. Teams that maintain custom Airflow operators or RES extensions must audit their own code separately. A vendor patch does not cover your fork.

<!-- INTERNAL_LINK: what is CSPM and how it supports CVE triage | what-is-cspm-cloud-security-posture-management -->
<!-- INTERNAL_LINK: AWS IAM Identity Centre for controlling Airflow access | aws-iam-identity-centre -->
<!-- INTERNAL_LINK: zero trust architecture to reduce blast radius | what-is-zero-trust-architecture -->

---

## Summary

Upgrade Apache Airflow to 3.3.0 immediately. CVE-2026-33264 (CVSS 9.8) enables DAG-author RCE on the Scheduler process. There is no 3.2.x backport. This is a fundamental security boundary violation, not an edge-case bug.

Audit your Airflow Variable and Config API access controls now. CVE-2026-48828 and CVE-2026-48892 expose secrets via the bulk Variables and Config APIs to any authenticated user with read permission, including Vault credentials and Secrets Manager keys.

Stop gating remediation SLAs solely on NVD CVSS scores. NIST's April 2026 NVD policy change means many CVEs arrive without enriched metadata. Supplement with CISA KEV, vendor bulletins, and EPSS to triage accurately.

Patch AWS RES to 2026.06 if you run scientific or HPC workloads. The symlink vulnerability in the `Auth.GetUserPrivateKey` API exposes arbitrary root-readable files on the cluster-manager EC2 instance.

Review ArcGIS Portal password recovery configuration for all UK public sector or government deployments running versions 12.1 or earlier, and enforce email-validated recovery flows immediately.

Use CloudTrail and ALB access logs now. The queries above will tell you whether any of these endpoints have already been accessed abnormally. Do not wait for a vendor-supplied IOC list; look at the evidence you already have.