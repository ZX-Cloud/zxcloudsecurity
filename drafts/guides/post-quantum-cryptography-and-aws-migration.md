---
title: "Post-Quantum Cryptography and AWS Migration: A Practitioner's Guide for 2025–2035"
date: 2026-07-07
description: "A practical guide to post-quantum cryptography and AWS migration covering NIST standards, NCSC timelines, ML-KEM, ML-DSA, and common pitfalls for UK cloud teams."
tags: ["post-quantum cryptography", "aws security", "cryptography", "cloud security", "ncsc", "aws kms"]
slug: "post-quantum-cryptography-aws-migration"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2276
draft: false
---

# Post-Quantum cryptography and AWS migration: a practitioner's guide for 2025-2035

The regulatory and threat environment around post-quantum cryptography has shifted meaningfully in the past twelve months, and if you are a cloud security architect in UK financial services or government, the window for comfortable, unhurried planning is closing. France's ANSSI announced it will stop certifying security products that lack quantum-resistant encryption from 2027, with businesses expected to purchase only quantum-safe products by 2030. ANSSI approval is required for use in French government agencies and critical infrastructure, making this a de facto phase-out of older encryption. The UK's NCSC is not far behind. This guide tells you what decisions to make right now inside AWS.

<!-- INTERNAL_LINK: AWS compliance and governance overview | aws-compliance-and-governance -->

---

## Why the urgency is real, not theoretical

The classic objection is that quantum computers powerful enough to break RSA do not exist yet, so there is time. That argument misunderstands the threat model.

The concern is "harvest now, decrypt later": adversaries collect encrypted data today expecting future quantum computers to unlock it. For UK financial services firms holding customer data under long GDPR retention periods, or government agencies managing multi-decade classified records, data encrypted today with RSA-2048 or ECDH P-256 is potentially already being collected by nation-state adversaries. The NCSC has explicitly warned that organisations must assume sensitive encrypted data is already being collected and will eventually be decrypted. That is not hedged language from a standards body. It is a direct operational warning.

On the standards side, the foundation is now solid. On 13 August 2024, NIST published three post-quantum cryptographic algorithms as Federal Information Processing Standards, concluding a standardisation process begun in 2016. Those three standards are:

- FIPS 203 (ML-KEM, Module-Lattice-Based Key-Encapsulation Mechanism): the primary standard for key exchange, replacing ECDH and RSA key transport.
- FIPS 204 (ML-DSA, Module-Lattice-Based Digital Signature Standard): replacement for ECDSA and RSA signatures.
- FIPS 205 (SLH-DSA, Stateless Hash-Based Digital Signature Standard): a conservative, hash-based signature option that does not rely on lattice hardness assumptions.

In August 2024, the NCSC updated their PQC white paper to endorse the NIST quantum-safe algorithms. The UK was the first major regulatory jurisdiction to reflect NIST's algorithms and embed them within national guidance.

<!-- INTERNAL_LINK: What is Zero Trust Architecture | what-is-zero-trust-architecture -->

---

## The NCSC migration timeline you need to know

Migration to post-quantum cryptography is a multi-year programme. In March 2025, the NCSC published guidance setting timelines for key migration activities across three phases:

Phase 1 runs to 2028 and covers identifying cryptographic services that need upgrading and building a migration plan. Phase 2 runs from 2028 to 2031 and covers executing high-priority upgrades while refining plans as PQC evolves. Phase 3 runs from 2031 to 2035 and requires completing migration to PQC across all systems, services, and products.

For AWS-centric organisations, Phase 1 is largely discovery and inventory work: knowing which workloads rely on public-key cryptography, which data has long-lived sensitivity, and which SDK and TLS client versions are in use. The NCSC guidance specifically calls out regulated sectors including banking, financial services, and telecoms as priorities for early migration. If you are under FCA oversight, treat Phase 2 milestones as constraints on your security roadmap, not aspirations.

The Financial Conduct Authority has been collaborating within the World Economic Forum on quantum security in financial services. Expect FCA Dear CEO letters referencing PQC readiness within the next 12 to 18 months.

---

## What AWS is actually doing (and what it is not doing)

AWS's PQC migration covers three workstreams: protecting data in transit, establishing quantum-resistant roots of trust, and authenticating identities in a post-quantum world. Understanding which side of the shared responsibility line you sit on is the most important mental model shift for AWS teams.

### Data in transit: ML-KEM hybrid TLS

AWS has deployed hybrid post-quantum key agreement for TLS across AWS KMS, AWS Certificate Manager, and AWS Secrets Manager endpoints. These now support ML-KEM for hybrid post-quantum key agreement on non-FIPS endpoints.

The hybrid approach combines traditional cryptography such as X25519 with ML-KEM, protecting connections against both classical attacks today and quantum attacks in future. This is the right engineering approach. A pure PQC migration without hybrid fallback would create compatibility problems in enterprise environments with diverse TLS client stacks.

Amazon S3 now supports post-quantum TLS key exchange on regional S3, S3 Tables, and S3 Express One Zone endpoints.

The critical point: AWS enabling PQC on service endpoints does not mean your workloads are using it. You must update your TLS clients and SDKs to advertise ML-KEM when connecting to AWS service HTTPS endpoints. If your Java Lambda functions are running AWS SDK for Java v1, or your Rust workloads are on an older crate, you are falling back to classical TLS even though the endpoint supports ML-KEM.

### Digital signatures: ML-DSA in AWS KMS

AWS KMS supports ML-DSA for post-quantum cryptographic signatures under FIPS 204. All ML-DSA keys and signature operations are created and protected in FIPS 140-3 Security Level 3 validated hardware security modules.

AWS Private CA and AWS KMS together support post-quantum code signing. Consumers of signed code pre-provisioned with post-quantum PKI roots can be confident the software could not have been forged by an adversary with a cryptographically relevant quantum computer. For UK organisations signing software artefacts destined for government or critical infrastructure use, this is a capability you should be adopting in your CI/CD pipelines now, not at Phase 2.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->

---

## Enabling hybrid post-quantum TLS with the AWS SDK for Java v2

The following snippet enables hybrid ML-KEM post-quantum TLS for calls to AWS KMS using the AWS Common Runtime HTTP client. With s2n-tls, configuring an HTTP client to prefer post-quantum TLS places ECDH with ML-KEM first in the preference list, with classic key exchange algorithms included for compatibility but ranked lower.

```java
import software.amazon.awssdk.http.crt.AwsCrtHttpClient;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.kms.KmsClient;

// AWS SDK for Java v2 + AWS CRT HTTP client
// Requires: software.amazon.awssdk:aws-crt-client (2.21.x or later)
// The CRT client negotiates ML-KEM hybrid TLS by default when supported.

KmsClient kmsClient = KmsClient.builder()
    .region(Region.EU_WEST_2)   // London region
    .httpClientBuilder(
        AwsCrtHttpClient.builder()
            // postQuantumTlsEnabled() is set to PREFERRED by default
            // in recent CRT HTTP client versions; set explicitly for clarity.
            .postQuantumTlsEnabled(true)
    )
    .build();

// All KMS API calls via this client will now negotiate
// ECDH + ML-KEM-768 hybrid key exchange where the endpoint supports it,
// falling back to classical ECDH if not (e.g. FIPS endpoints).
```

> Note on FIPS endpoints: the hybrid ML-KEM cipher suites are currently available on non-FIPS KMS endpoints. These cipher suites protect data in transit between your client and the AWS KMS endpoint. They do not affect how KMS encrypts key material at rest. Your at-rest key material under AES-256-GCM is already quantum-resistant. The hybrid TLS is specifically mitigating the harvest-now-decrypt-later risk on the wire.

Migrating from ECDH-only to ECDH+ML-KEM hybrid key agreement adds roughly 1,600 bytes to the TLS handshake and 80 to 150 microseconds of additional compute time for ML-KEM operations. In practice, this overhead is negligible for nearly all workloads. Do not let micro-benchmarking block your PQC adoption.

---

## Building a cryptographic inventory on AWS

You cannot migrate what you cannot see. Before touching a single SDK version or TLS policy, you need a cryptographic inventory across your AWS estate. Focus on these four areas:

First, TLS termination points: Application Load Balancers, API Gateway, and CloudFront distributions. Check your TLS security policies. The `ELBSecurityPolicy-TLS13-1-2-2021-06` policy does not include ML-KEM. AWS has released updated TLS policies that support ML-KEM for ALBs, but switching to a PQ-enabled policy is your responsibility under the shared responsibility model.

Second, SDK versions in Lambda, ECS/Fargate, and EC2. Run a Config rule or use Systems Manager Inventory to catalogue runtime SDK versions. Any Java workload on SDK v1 needs uplift.

Third, long-lived data assets. S3 buckets holding customer PII, financial records, or IP with retention periods beyond 2030 are your highest-priority harvest-now-decrypt-later targets. Tag workloads based on sensitivity, exposure, and data lifespan to focus effort where the risk is greatest.

Fourth, code signing and certificate chains. Any internally signed artefacts including container images, Lambda deployment packages, and AMIs using ECDSA are candidates for ML-DSA uplift via AWS Private CA.

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->
<!-- INTERNAL_LINK: Cloud security vulnerability management | cloud-security-vulnerability-management -->

---

## Common pitfalls in post-quantum cryptography and AWS migration

These are mistakes I see repeatedly when advising enterprise and public sector clients. They cost time, money, and occasionally create new vulnerabilities in the process of fixing old ones.

### 1. Assuming AWS does it all for you

AWS delivers PQC as part of the shared responsibility model. Some PQC features are transparently enabled for all customers. Others are options you must explicitly choose. Enabling PQC on an ALB listener requires a deliberate security policy change. Updating your SDK is your responsibility. Do not assume that because you run on AWS, you are covered.

### 2. Conflating at-rest and in-transit quantum risk

AES-256 symmetric encryption, used for S3, EBS, and RDS at rest via KMS, is considered quantum-resistant. Properly implemented symmetric encryption is not the problem. It is asymmetric cryptography that faces quantum threats. Do not waste Phase 1 effort trying to PQC-harden your AES-256 at-rest encryption. Focus on asymmetric key exchange and digital signatures.

### 3. Migrating away from CRYSTALS-Kyber too slowly

If your organisation ran early proof-of-concepts using CRYSTALS-Kyber, the pre-standardisation predecessor to ML-KEM, be aware it is being retired. AWS is phasing out CRYSTALS-Kyber support across endpoints in 2026. Clients on older SDK versions that advertise only CRYSTALS-Kyber will fall back to classical TLS rather than negotiate the deprecated algorithm. A graceful fallback to classical TLS is a silent loss of your PQC protection. You will not see an error, just unprotected connections.

### 4. Ignoring algorithm divergence between ANSSI and NIST

ANSSI has explicitly reserved the right to certify an algorithm set that does not exactly match NIST's selections. The agency names FrodoKEM, an unstructured-lattice scheme that trades performance for conservatism, as an acceptable alternative KEM. If your organisation operates or sells into the French government market, a pure ML-KEM implementation may be insufficient for ANSSI certification without a hybrid that also supports FrodoKEM. That is a harder engineering lift than simply adding a new algorithm to the stack.

### 5. Treating crypto-agility as an afterthought

The NCSC guidance notes that traditional and post-quantum cryptography will need to co-exist for some time, and that organisations should seek solutions offering cryptographic agility: the ability to support alternative suites of cryptographic algorithms and to determine when to end support for traditional algorithms. Hard-coding algorithm identifiers in application code rather than externalising them via KMS key aliases or ACM policy is the most common anti-pattern I encounter. It turns a future algorithm rotation into an application deployment event rather than a configuration change.

### 6. Skipping performance testing in production-like environments

The performance overhead of ML-KEM is modest at the TLS layer, but ML-DSA signatures are meaningfully larger than ECDSA signatures. SLH-DSA, the hash-based option, is substantially slower and produces very large signatures. Test your signing workloads, particularly those involving high-volume token issuance, JWT signing, or code-signing pipelines, before committing to an algorithm choice.

<!-- INTERNAL_LINK: AWS Well-Architected Security | aws-well-architected-security -->

---

## Key takeaways

Start the cryptographic discovery now, not at Phase 2. The NCSC timeline runs to 2035, but Phase 1 ends in 2028 and it fills up faster than it looks.

Your at-rest AES-256 encryption is not the problem. Focus PQC engineering effort on asymmetric key exchange via ML-KEM hybrid TLS and digital signatures via ML-DSA. Those are the components quantum computers will target.

Update your SDKs and TLS policies. AWS plans to deploy ML-KEM support to all AWS services with HTTPS endpoints, but you must update your TLS clients and SDKs to advertise ML-KEM when connecting. This is your side of the shared responsibility model.

Use AWS KMS ML-DSA for code signing in regulated workloads today. AWS KMS creates and protects all ML-DSA keys and signature operations in FIPS 140-3 Security Level 3 validated hardware security modules. That is a production-grade, auditable control you can reference in FCA and NCSC audit responses right now.

Build for crypto-agility, not a one-time migration. NIST is already standardising additional candidates. Externalise algorithm selection into KMS key policies and ACM certificate configurations so future rotations do not require application code changes.

The regulatory clock is independent of Q-Day. Regulators, certification bodies, and procurement authorities are setting their own quantum deadlines, and those deadlines are binding regardless of when a cryptographically relevant quantum computer actually exists. Your board needs to understand this: PQC migration is a compliance deadline, not a future security investment that can wait.