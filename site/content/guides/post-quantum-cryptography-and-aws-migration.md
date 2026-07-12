---
title: "Post-Quantum Cryptography and AWS Migration: A Practitioner's Guide"
date: 2026-07-12
description: "A technical guide to post-quantum cryptography and AWS migration for cloud security architects — covering NIST standards, NCSC timelines, ML-KEM, and crypto-agility."
tags: ["post-quantum cryptography", "aws security", "cryptography", "cloud security", "encryption", "NCSC", "KMS"]
slug: "post-quantum-cryptography-aws-migration"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 1834
draft: false
---

# Post-Quantum cryptography and AWS migration: what you need to do now

If you are responsible for cloud security in a UK financial services firm, government body, or enterprise running regulated workloads on AWS, post-quantum cryptography migration is no longer something you can defer. It became an active programme of work the moment NIST finalised its first three PQC standards in August 2024, releasing FIPS 203, FIPS 204, and FIPS 205. The threat model is real and the regulatory clock is running. This guide covers what those standards mean for your AWS workloads, what AWS has already done under the shared responsibility model, and what remains your problem to solve.

<!-- INTERNAL_LINK: AWS KMS key management best practices | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: AWS compliance and governance fundamentals | aws-compliance-and-governance -->

---

## Why the quantum threat is already operational

The common misconception is that quantum risk only materialises when a cryptographically relevant quantum computer exists. That is wrong.

The priority threat is "harvest now, decrypt later" (HNDL): a well-resourced adversary captures encrypted traffic today and holds it until a quantum computer exists to break it. For a UK financial services firm under FCA oversight, or a government supplier handling OFFICIAL-SENSITIVE data, this means API calls, key exchange material, and authentication tokens in transit right now could be in someone's archive waiting for that day. The NCSC has said explicitly that organisations must assume sensitive encrypted data is already being collected.

The algorithms at risk are RSA, ECDH, and ECDSA. Your AES-256 symmetric keys are not in scope. Properly implemented symmetric encryption is considered quantum-resistant; asymmetric cryptography is not. That distinction matters enormously for how you triage your migration effort.

---

## The NIST standards you are actually migrating to

Three algorithms are now standardised:

- CRYSTALS-Kyber is standardised as ML-KEM (Module Lattice KEM) under FIPS 203
- CRYSTALS-Dilithium is standardised as ML-DSA (Module Lattice Digital Signature Algorithm) under FIPS 204
- SPHINCS+ is standardised as SLH-DSA (Stateless Hash-based DSA) under FIPS 205

For most AWS workloads, the two you will encounter first are ML-KEM and ML-DSA. ML-KEM handles quantum-safe key encapsulation in TLS handshakes, replacing ECDH, and is the primary defence against HNDL attacks on data in transit. ML-DSA covers digital signatures, replacing RSA and ECDSA in certificate chains, code signing, and long-lived roots of trust.

NIST's position is that organisations should begin applying these standards now. That is not a future recommendation.

---

## The NCSC's three-phase timeline

In March 2025, the NCSC published its migration guidance with a concrete roadmap across three phases: identify cryptographic services needing upgrades and build a migration plan by 2028; execute high-priority upgrades and refine plans as PQC evolves between 2028 and 2031; complete migration to PQC for all systems, services, and products by 2035.

If you are in Phase 1 right now, as most UK organisations should be, your deliverable is a cryptographic asset inventory and a prioritised migration plan. Full migration is not yet the expectation. The NCSC is explicit that regulated sectors including banking, financial services, and telecoms, and those with predominantly internet-facing services, should target earlier migration for high-priority systems.

The NCSC endorsed the NIST quantum-safe algorithms in its 'Next steps in preparing for post-quantum cryptography' white paper, updated in August 2024 to reflect NIST's finalised standards. The FCA has also been active here, collaborating with the World Economic Forum on a January 2024 white paper covering quantum security in the financial sector.

On cryptographic agility, the NCSC's position is straightforward: traditional public-key cryptography and PQC will need to coexist during the transition. Introducing PQC will create interoperability and compatibility challenges, so the NCSC advises choosing solutions that support cryptographic agility and can switch between algorithm suites without architectural rewrites. That lets you phase out legacy algorithms on a workload-by-workload basis as readiness allows.

<!-- INTERNAL_LINK: AWS Well-Architected Security Pillar overview | aws-well-architected-security -->

---

## What AWS has already done (and what it has not)

AWS operates a four-workstream PQC migration plan and is progressively enabling quantum-safe protections under the shared responsibility model. Some features are being enabled transparently for all customers; others are options you need to switch on yourself.

### What AWS has already delivered

AWS KMS, ACM, and Secrets Manager endpoints now support ML-KEM for hybrid post-quantum key agreement on non-FIPS endpoints. AWS KMS also supports quantum-resistant digital signatures using ML-DSA. At the foundation is AWS-LC, the FIPS-140-3-validated cryptographic library, which AWS states was the first open-source cryptographic module to include ML-KEM in a FIPS 140-3 validation.

For SFTP workloads, AWS Transfer Family has upgraded its hybrid quantum-resistant key exchange support from Kyber to ML-KEM (FIPS 203). The SSH security policies that support post-quantum key exchange with ML-KEM are `TransferSecurityPolicy-2025-03` and `TransferSecurityPolicy-FIPS-2025-03`.

### What is still your responsibility

AWS will negotiate ML-KEM when a client offers it. If your SDK is outdated and does not offer ML-KEM during the TLS handshake, the connection falls back to classical-only key exchange. You are unprotected regardless of what AWS has deployed server-side.

Also worth flagging: support for pre-standard CRYSTALS-Kyber continues through 2025 but will be removed across all AWS service endpoints in 2026 in favour of ML-KEM. If you have clients still using the pre-standard Kyber implementation, migration to ML-KEM is urgent.

<!-- INTERNAL_LINK: AWS CloudTrail configuration for security monitoring | aws-cloudtrail-configuration-best-practices -->

---

## Enabling hybrid PQ-TLS for AWS KMS: practical example

The hybrid approach is the correct posture during migration. It combines classical ECDH with ML-KEM so that security holds as long as either algorithm remains unbroken. Here is how to configure the AWS SDK for Java 2.x to use hybrid post-quantum TLS when calling AWS KMS.

```java
import software.amazon.awssdk.http.async.SdkAsyncHttpClient;
import software.amazon.awssdk.http.crt.AwsCrtAsyncHttpClient;
import software.amazon.awssdk.services.kms.KmsAsyncClient;

// Requires: AWS SDK for Java v2 >= 2.30.22 on Linux
// and the aws-crt runtime dependency

SdkAsyncHttpClient awsCrtHttpClient = AwsCrtAsyncHttpClient.builder()
    .postQuantumTlsEnabled(true)  // Prefer ECDH + ML-KEM-768 hybrid
    .build();

KmsAsyncClient kmsClient = KmsAsyncClient.builder()
    .httpClient(awsCrtHttpClient)
    .build();

// All KMS API calls (GenerateDataKey, Decrypt, Sign, etc.)
// now use hybrid post-quantum TLS in transit.
// Note: this secures the TLS channel — KMS still uses
// AES-256-GCM (quantum-resistant) for data-at-rest operations.
```

A few caveats architects frequently miss:

Hybrid cipher suite support in s2n-tls is currently available only on Linux. Windows-based workloads need a different approach. These cipher suites are also only supported in SDKs that include the AWS Common Runtime, such as the AWS SDK for Java 2.x.

The handshake overhead is real but small. In AWS's published benchmarks, switching from classical to hybrid post-quantum key agreement added approximately 1,600 bytes per TLS handshake and around 80 to 150 microseconds of additional compute. That is a one-time connection startup cost, amortised over the lifetime of the TLS session. With TLS connection reuse enabled, AWS measured only a 0.05 per cent decrease in maximum transactions per second when calling `GenerateDataKey`. Negligible in practice, though these are AWS's benchmark figures for a specific test workload — validate against your own.

For AWS Transfer Family SFTP endpoints, apply the updated security policy via the CLI:

```bash
aws transfer update-server \
  --server-id s-xxxxxxxxxxxxxxxxx \
  --security-policy-name TransferSecurityPolicy-2025-03
```

Starting in 2025, all new AWS Transfer Family security policies include post-quantum support using hybrid key exchange. If you are running older policies, check them now.

---

## Building your cryptographic asset inventory

Before you can migrate anything, you need to know what you have. This is the most underestimated task in any PQC programme. Without a clear inventory you cannot assess risk, prioritise systems, or coordinate updates across your infrastructure.

For AWS environments specifically, your inventory should cover:

TLS endpoints and cipher suites across ALBs, API Gateway, CloudFront distributions, and any custom TLS termination. CloudTrail events for AWS KMS and AWS Payment Cryptography now include `keyExchange` as a field in `tlsDetails`, which gives you visibility into what is actually being negotiated. Over time, service-specific logs will extend this to show the key exchange used during TLS session establishment.

Certificate chains issued by AWS Private CA or ACM that rely on RSA or ECDSA signatures.

Custom SDK integrations where service-to-service calls use hardcoded cipher suite configurations or pinned TLS libraries that bypass AWS-LC entirely.

Third-party and on-premises integrations, including VPN tunnels, inter-data-centre links, and partner API connections that terminate outside AWS.

Systems running custom TLS libraries or hardcoded cipher suites need to be flagged early. The fastest way to reduce your PQC surface area is to eliminate custom cryptographic stacks entirely. Workloads that use AWS managed services will generally need the least effort to migrate, which is a practical steer worth acting on: if you are running self-managed Nginx, HAProxy, or OpenSSL stacks, those are your priority targets for upgrade or re-platforming.

The inventory is not a one-time exercise. Your cryptographic estate changes every time a developer adds a dependency, a new service is deployed, or a third-party integration is updated. Build the process to repeat.

<!-- INTERNAL_LINK: AWS Security Hub for continuous compliance monitoring | aws-security-hub-guide -->
<!-- INTERNAL_LINK: Cloud security vulnerability management | cloud-security-vulnerability-management -->

---

## Common pitfalls in PQC migration on AWS

### Assuming AWS handles everything

The shared responsibility model applies here exactly as it does everywhere else. AWS secures the infrastructure; you own the client. If your application connects to AWS KMS using an SDK without ML-KEM support, the connection falls back to classical TLS regardless of what AWS has deployed server-side.

### Upgrading to Kyber and stopping there

Teams that implemented pre-standard Kyber during early testing and have not migrated to ML-KEM are facing a hard deadline. Support ends in 2026. Check your SDK versions now.

### Ignoring the signature migration

Most teams focus on key exchange (HNDL protection) and overlook digital signatures entirely. Long-lived certificates, firmware signing keys, and document signatures all need a migration plan. AWS uses ML-DSA for quantum-resistant roots of trust precisely because devices shipping today need to authenticate data for their entire operational lifetime.

### Treating the inventory as a one-off exercise

As infrastructure evolves and new dependencies are introduced, inventories go stale. Maintaining ongoing visibility is the only way to manage quantum security risk as migration deadlines approach.

### Failing to test through network appliances

Deep-packet inspection appliances that fingerprint TLS handshakes may block or corrupt hybrid post-quantum ClientHello messages. Your request can be denied by proxies or DPI firewalls depending on its network path. Test in a non-production environment before rolling out to production, and flag this to your network and firewall teams early.

### Conflating encryption at rest with encryption in transit

PQC migration for AWS workloads is overwhelmingly a transit problem today. AES-256, which KMS uses for data at rest, is already quantum-resistant. Effort should be proportionate to that reality.

### Underestimating the organisational timeline

The deprecation of SHA-1 took roughly twelve years from the first practical collision attacks in 2005 until major browsers finally rejected SHA-1 certificates in 2017. MD5, 3DES, and RC4 followed the same pattern of slow organisational response despite clear technical consensus. Do not let your PQC programme stall after the initial inventory phase.

---

## Key takeaways

The HNDL threat is active now. Adversaries may already be collecting your ciphertext. Waiting for a quantum computer to materialise before acting is the wrong posture. Both the NCSC and NIST say to start today.

NIST finalised the standards in August 2024. ML-KEM (FIPS 203) and ML-DSA (FIPS 204) are the primary algorithms you will implement. These are no longer experimental.

AWS covers the server side; you own the client. KMS, ACM, Secrets Manager, and Transfer Family already support ML-KEM. You must update