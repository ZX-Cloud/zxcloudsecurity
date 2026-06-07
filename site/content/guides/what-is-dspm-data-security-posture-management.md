+++
title = "What is DSPM (Data Security Posture Management)?"
date = "2026-06-07T14:20:33Z"
slug = "what-is-dspm-data-security-posture-management"
description = "What is DSPM (Data Security Posture Management)? — a practical guide for cloud security architects."
keywords = ["DSPM", "data security posture management", "data discovery", "classification"]
draft = false
+++

Data security posture management (DSPM) is a category of security tooling and practice focused on continuously discovering, classifying, and monitoring sensitive data across cloud environments to identify and remediate exposure risks. Unlike perimeter-centric controls, DSPM starts with the data itself — where it lives, who can access it, and whether its protection posture matches its sensitivity. As organisations distribute data across multi-cloud storage, data lakes, SaaS platforms, and managed databases, DSPM has become a foundational discipline for cloud security programmes.

---

## Why DSPM Has Emerged Now

Cloud adoption fundamentally changed the data risk calculus. In on-premises environments, sensitive data had relatively predictable boundaries — a DBA could enumerate most datastores. In cloud environments, an S3 bucket can be created in seconds, a Snowflake share can expose a dataset to an external account without touching a firewall rule, and a developer can snapshot a production RDS instance into a personal AWS account for debugging purposes.

The result is **data sprawl**: sensitive data duplicated, moved, and forgotten across hundreds of services and accounts. Traditional data loss prevention (DLP) tools were built for egress monitoring at defined control points — they cannot inventory what they cannot see. DSPM addresses this gap by treating discovery as a continuous, cloud-native process rather than a periodic scan.

Regulatory pressure has compounded the urgency. GDPR, the UK Data Protection Act 2018, PCI DSS v4.0, and sector-specific frameworks such as DORA all impose obligations to know where sensitive data resides and demonstrate that appropriate controls are applied. An inability to locate personal data is itself a compliance failure under UK GDPR Article 30 (records of processing).

---

## What DSPM Actually Does

A mature DSPM capability typically covers four interconnected functions:

### 1. Data Discovery

DSPM tools connect to cloud environments — AWS, Azure, GCP, Snowflake, Databricks, Microsoft 365, and others — using read-only API access or agentless scanning to enumerate datastores. This includes object storage, relational and NoSQL databases, data warehouses, file shares, and increasingly SaaS application datastores. The output is a living inventory of where data assets exist across your estate.

Discovery must be continuous, not point-in-time. A quarterly scan misses the bucket created last Tuesday that already contains exported customer records.

### 2. Classification

Once datastores are discovered, DSPM applies classification to understand what types of data they contain. This uses a combination of structural pattern matching (regular expressions for formats such as NI numbers, IBANs, passport numbers), machine learning models trained on data types, and metadata inference (column names, table schemas, file naming conventions).

Classification outputs are typically mapped to sensitivity labels — public, internal, confidential, highly confidential — and to regulatory categories such as PII, PHI, PCI cardholder data, or credentials. The quality of classification logic directly determines the signal-to-noise ratio; poorly tuned tools generate enough false positives to make triage unworkable.

### 3. Posture Assessment

With data located and classified, DSPM assesses the security posture of each datastore: Is the S3 bucket publicly accessible? Does this Snowflake database have MFA enforcement on service accounts? Are RDS snapshots encrypted? Is this BigQuery dataset shared outside the organisation? Is there excessive IAM access — identities that have SELECT permissions but have never queried the table?

This is where DSPM diverges from generic cloud security posture management (CSPM). CSPM evaluates infrastructure configuration in isolation; it can tell you a bucket's ACL is overly permissive without knowing whether that bucket contains anything sensitive. DSPM contextualises configuration findings against data sensitivity. A misconfigured bucket containing log files is a different risk profile from a misconfigured bucket containing UK resident health records.

### 4. Risk Prioritisation and Remediation Guidance

The most actionable DSPM platforms combine discovery, classification, and posture findings into a risk-ranked view. They surface "toxic combinations" — for example, a datastore containing PII that is publicly accessible, lacks encryption at rest, and has not been accessed in six months (suggesting it may be a forgotten data shadow). Remediation guidance is typically mapped to specific API calls, IaC changes, or native console steps.

---

## DSPM vs CSPM: Understanding the Distinction

This comparison is worth being precise about because the two are frequently conflated in vendor marketing.

| Dimension | CSPM | DSPM |
|---|---|---|
| Primary focus | Infrastructure configuration | Data assets and their protection |
| What it inventories | Resources (compute, storage, network) | Datastores and their contents |
| Risk context | Config deviation from baselines | Sensitivity of data at risk |
| Key question answered | "Is this resource misconfigured?" | "Is this sensitive data exposed?" |

In practice, the two are complementary. CSPM is strong at detecting misconfigured security groups, missing logging, and IAM policy anomalies at scale. DSPM is strong at answering "of all our misconfigurations, which ones actually put sensitive data at risk right now?" Security programmes that have CSPM deployed and are drowning in findings often find that DSPM integration allows them to triage effectively by anchoring remediation priority to data sensitivity.

Some CSPM vendors have extended their platforms to include DSPM capabilities; purpose-built DSPM vendors include Cyera, Varonis, Securiti, BigID, and Dig Security (now part of Palo Alto). Evaluation should focus on breadth of datastore connectors, classification accuracy, and the quality of the risk-scoring model rather than on category label.

---

## What Architects Should Do: Practical Steps

**Establish a continuous data inventory before anything else.** You cannot protect what you cannot see. Deploy DSPM discovery across all cloud accounts and SaaS integrations, not just production. Shadow data frequently originates in non-production environments where controls are relaxed.

**Define classification taxonomies that align to your regulatory obligations.** Work with your data protection officer to agree on sensitivity tiers and the specific data types that trigger each tier. Build these into DSPM policy rather than accepting vendor defaults — a fintech will care about cardholder data; an NHS supplier will prioritise NHS numbers and clinical data.

**Integrate DSPM findings with your CSPM and SIEM.** Risk scoring is only useful if it feeds existing workflows. Map high-severity DSPM findings to your ticketing system with defined SLAs. A publicly exposed datastore containing PII should trigger P1 remediation; an internal datastore with stale access permissions might be P3.

**Use DSPM output to drive IaC remediation, not just reactive fixes.** When DSPM identifies a recurring misconfiguration pattern — for example, RDS instances in a specific account consistently lack deletion protection on snapshots — that is a signal to update your Terraform modules and enforce policy via OPA or AWS Config rules.

**Audit access paths, not just bucket policies.** DSPM should assess effective permissions including IAM roles, resource-based policies, VPC endpoint policies, and service control policies together. A bucket policy that looks restrictive may be wide open when IAM role trust relationships are considered. Prioritise datastores where the set of identities with access is unexpectedly large relative to data sensitivity.

**Address data minimisation alongside posture.** Discovery often reveals data that should not exist — production PII copied to development environments, retained beyond its legal basis, or duplicated across regions without justification. DSPM creates the evidence base for data minimisation programmes that reduce your attack surface fundamentally rather than just hardening controls around unnecessary exposure.

**Run DSPM against your SaaS estate, not just IaaS.** A significant proportion of sensitive data in most enterprises now lives in Salesforce, ServiceNow, Google Workspace, or Microsoft 365. Modern DSPM platforms provide SaaS connectors; neglecting these leaves a substantial blind spot.

---

## Key Takeaways

- **DSPM discovers and classifies sensitive data continuously** across cloud and SaaS environments, giving security teams an accurate picture of where sensitive data lives and how it is protected.
- **The discipline is data-centric, not infrastructure-centric** — it contextualises configuration risk against actual data sensitivity, enabling meaningful prioritisation.
- **DSPM and CSPM are complementary**, not competing: CSPM finds misconfigurations at scale; DSPM identifies which of those misconfigurations actually matter because sensitive data is involved.
- **Classification quality and connector breadth** are the most important evaluation criteria when selecting tooling.
- **Effective DSPM programmes go beyond alerting** — findings should drive IaC remediation, data minimisation, and access governance improvements that reduce long-term data exposure risk.
