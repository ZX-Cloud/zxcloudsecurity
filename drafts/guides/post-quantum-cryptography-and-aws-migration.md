---
title: "Post-Quantum Cryptography and AWS Migration: A Practical Guide for Cloud Security Architects"
date: 2026-07-12
description: "A practitioner's guide to post-quantum cryptography and AWS migration — covering NIST standards, NCSC timelines, hybrid TLS, and the pitfalls to avoid."
tags: ["post-quantum cryptography", "aws security", "encryption", "cloud security", "kms", "tls", "ncsc", "crypto agility"]
slug: "post-quantum-cryptography-aws-migration"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2173
draft: false
---

# Post-Quantum cryptography and AWS migration: what UK cloud security architects need to do now

If you work in regulated cloud environments -- financial services, government, healthcare -- post-quantum cryptography is no longer a research topic. It belongs on your security roadmap today. NIST finalised its first three post-quantum cryptographic (PQC) standards in August 2024. The NCSC published its migration timelines in March 2025. AWS has already deployed hybrid post-quantum TLS across KMS, ACM, and Secrets Manager. The standards are settled. The clock is running. What most organisations lack is a clear-eyed view of what they actually need to do on their side of the shared responsibility model, and the practical steps to get there.

This guide covers the threat model, the current AWS capability landscape, what crypto agility actually demands of your architecture, and the pitfalls that will stall your programme before it gets moving.

---

## Why this is not a 2030 problem

The instinct to defer is understandable. There is no evidence that a quantum computer powerful enough to break the public-key cryptography in use throughout AWS exists today. So why act now?

The answer is harvest now, decrypt later (HNDL). Adversaries are collecting encrypted communications today to decrypt once quantum computers mature -- estimated somewhere between 2030 and 2035. The NCSC has warned UK organisations that sensitive encrypted data should be assumed already collected.

For FCA-regulated firms and UK government agencies processing data that must remain confidential for a decade or more -- legal documents, M&A communications, patient records, national security material -- this is not theoretical. If that traffic is being recorded now, the algorithm protecting it today is on a countdown timer.

Cryptographic migrations have historically taken far longer than anyone expects. SHA-1 deprecation took more than a decade from the first practical collision attack in 2005 until major browsers finally rejected it in 2017. MD5, 3DES, and RC4 all followed the same pattern: clear technical consensus, slow organisational response. PQC migration will be no different unless you build a programme with teeth today.

---

## The standard landscape: what has actually been agreed

NIST released the final versions of FIPS 203, 204, and 205 in August 2024, concluding an eight-year standardisation process that began in 2016.

The three primary standards are:

- ML-KEM (FIPS 203), derived from CRYSTALS-Kyber, specifies a module-lattice-based key encapsulation mechanism providing IND-CCA2 security under the Module Learning With Errors hardness assumption. This is the primary algorithm for securing key exchange in TLS.
- ML-DSA (FIPS 204), derived from CRYSTALS-Dilithium, provides a lattice-based digital signature scheme.
- SLH-DSA (FIPS 205), derived from SPHINCS+, provides a stateless hash-based signature scheme whose security rests solely on hash function properties. SLH-DSA is a useful hedge -- if lattice-based assumptions are broken, your signature infrastructure has a fallback.

The NCSC endorses all three. One thing worth being clear on: properly implemented symmetric encryption is considered quantum-resistant. It is asymmetric cryptography that faces the quantum threat. Your AES-256 envelope encryption is fine. Your RSA and ECDH key exchange is what needs replacing.

### NCSC migration timelines for UK organisations

The NCSC outlines three phases: to 2028, identify cryptographic services needing upgrades and build a migration plan; from 2028 to 2031, execute high-priority upgrades and refine plans as PQC evolves; from 2031 to 2035, complete migration to PQC for all systems and services.

Regulated sectors -- banking, financial services, telecoms -- should prioritise early migration. If you are under FCA supervision or handle CNI, the 2028 deadline for a completed migration plan is the one your board needs to understand.

---

## Where AWS is today under the shared responsibility model

AWS is migrating to post-quantum cryptography and helping customers do the same, but the shared responsibility model applies here as clearly as it does anywhere else. Some PQC capability is being rolled out transparently on the AWS side. Much of the client-side work falls to you.

The transition is starting with systems that communicate over untrusted networks. AWS's workstreams prioritise encryption in transit first, and that is what has been delivered so far.

### Services with live PQC support

AWS KMS, AWS Certificate Manager, and AWS Secrets Manager endpoints now support ML-KEM for hybrid post-quantum key agreement on non-FIPS endpoints across all AWS Regions in the `aws` partition.

AWS KMS and AWS Private CA also support quantum-resistant signatures and roots of trust with ML-DSA.

AWS Transfer Family has upgraded its hybrid quantum-resistant key exchange support to ML-KEM (FIPS 203). The SSH policy names that support post-quantum key exchange are `TransferSecurityPolicy-2025-03` and `TransferSecurityPolicy-FIPS-2025-03`.

The underlying cryptographic foundation is AWS-LC, their FIPS-140-3-validated cryptographic library, which was the first open-source cryptographic module to include ML-KEM in its FIPS validation.

### What AWS does not handle for you

AWS customers must update their TLS clients and SDKs to offer ML-KEM when connecting to AWS service HTTPS endpoints. That includes your Lambda functions, EC2-based services, ECS containers, and anything using an AWS SDK to call KMS or Secrets Manager.

TLS policy updates on customer-owned resources -- ALBs, NLBs -- require manual intervention. That is on your side of the shared responsibility model.

There is also a hard deadline to be aware of. AWS committed to supporting CRYSTALS-Kyber only through the end of 2025, and it is being removed across all AWS service endpoints during 2026 in favour of ML-KEM. Customers currently negotiating CRYSTALS-Kyber who do not upgrade their AWS Java SDK v2 clients before then will see their clients fall back gracefully to classical key agreement. "Graceful fallback to classical" sounds benign until you realise it means your HNDL protection silently disappears.

---

## Enabling hybrid post-quantum TLS: a practical starting point

The hybrid approach combines classical ECDH with ML-KEM, establishing TLS connections that protect against both current classical attacks and future quantum threats. This is the right approach for now -- it does not require you to trust that ML-KEM alone is sufficient, and it maintains compatibility with classical-only peers.

### AWS SDK for Java v2

```java
import software.amazon.awssdk.http.crt.AwsCrtAsyncHttpClient;
import software.amazon.awssdk.services.kms.KmsAsyncClient;

AwsCrtAsyncHttpClient httpClient = AwsCrtAsyncHttpClient.builder()
    .postQuantumTlsEnabled(true)
    .build();

KmsAsyncClient kmsClient = KmsAsyncClient.builder()
    .httpClient(httpClient)
    .build();

// All KMS calls now use X25519MLKEM768 hybrid key exchange
// Verify by checking TLS handshake negotiated group in CloudWatch / VPC Flow Logs
```

### AWS SDK for Rust

```toml
# Cargo.toml
[dependencies]
aws-sdk-kms = "1"
aws-smithy-runtime = { version = "1", features = ["prefer-post-quantum"] }
```

### Verifying your connection

If the `keyExchange` field in your TLS session metadata shows `X25519MLKEM768`, hybrid post-quantum key exchange is active. If it shows `X25519`, the client is not advertising ML-KEM support. Check the client version and configuration.

You can verify at the OS level using OpenSSL `s_client` or by inspecting TLS session metadata in your application logs. Build this check into your CI pipeline as a regression gate. Silent fallback to classical TLS is a real risk in heterogeneous environments, and you will not catch it without an automated check.

### Performance impact

According to AWS's published measurements, switching from classical to hybrid post-quantum key agreement transfers approximately 1,600 additional bytes during the TLS handshake and requires roughly 80 to 150 microseconds more compute time for the ML-KEM operations. This is a one-time connection startup cost, amortised over the lifetime of the TLS session.

In practice, AWS measurements showed only a 0.05 percent decrease in maximum transactions per second when calling KMS GenerateDataKey with hybrid PQC enabled. If TLS connection reuse is properly configured, the overhead is negligible. There is no credible performance argument for deferring.

---

## Building a cryptographic inventory for your AWS estate

Before you can migrate anything, you need to know what you have. A sound quantum-safe transformation starts with assessing existing cryptographic use and classifying data and systems based on sensitivity and longevity.

For an AWS estate, that means cataloguing:

- All SDK calls performing asymmetric key operations (KMS `Decrypt`, `GenerateDataKey`, `Sign`)
- Custom TLS implementations in Lambda layers, container base images, and EC2 AMIs
- SSH connectivity to AWS services via Transfer Family or Systems Manager
- VPN and Direct Connect configurations using IKE/IPsec
- Certificate authorities managed via ACM Private CA and any third-party PKI
- Third-party SaaS and vendor integrations using API keys or mutual TLS

<!-- INTERNAL_LINK: managing secrets and credentials across your estate | aws-iam-security-best-practices -->

For custom applications where you cannot delegate cryptography to AWS, the goal is crypto agility -- the ability to update cryptographic algorithms and protocols without a major rearchitecture. That means maintaining current software versions, implementing automated update processes, and designing systems that can absorb algorithm changes.

Use AWS Config rules and Security Hub findings to surface services still using deprecated TLS versions. TLS 1.2 is a prerequisite concern -- TLS 1.3 is required for PQC support, and it is worth getting your estate onto 1.3 before worrying about ML-KEM.

<!-- INTERNAL_LINK: auditing your AWS environment configuration | aws-security-hub-guide -->

---

## Common pitfalls and how to avoid them

These are the failure modes I see most often when organisations attempt cryptographic migrations.

### 1. Treating this as a pure engineering task

The technical changes are not the hard part. The hard part is driving coordinated change across a large, complex organisation where asymmetric cryptography is embedded in every protocol, every vendor dependency, and every legacy system that quietly handles key exchange or digital signatures. Assigning this to the platform team without executive sponsorship and a cross-functional programme structure is how it stalls after the first quarterly review.

### 2. Confusing "AWS handled it" with "we're done"

AWS secures the managed service endpoints. Your Lambda, your EC2, your containerised microservice, your on-premises to AWS VPN -- those are your responsibility. Customers configure clients that negotiate cryptographic ciphers when connecting to AWS. Which ciphers get negotiated is down to you.

### 3. Thinking library swaps constitute a migration

Swapping an RSA call for an ML-KEM call is a real operation that must happen. It is also approximately 5% of the actual work of a PQC migration, and it is the easiest 5%. The hard work is certificate chains, PKI, HSM compatibility, vendor dependencies, and the third-party integrations your organisation has accumulated over the last decade.

### 4. Ignoring middle-box failures

ML-KEM's large public key and ciphertext sizes can cause fragmented TLS Client Hello packets. Deep packet inspection appliances, legacy firewalls, and SSL-inspection proxies frequently strip or reject cipher suites they do not recognise. Test your network path end-to-end before rolling out to production. If intermediate hosts or proxies block the new TLS algorithms, you will need to work with your network security team to update firewall rules before any application change will succeed.

### 5. Neglecting vendor dependency mapping

Each provider makes its own cryptographic choices on its own timeline. If your identity provider does not support PQC signing for SAML or OAuth tokens, your authentication infrastructure cannot migrate regardless of what you do internally. Map your third-party cryptographic dependencies -- identity providers, payment processors, HSM vendors, SaaS platforms -- and require PQC roadmap commitments in new procurement. GDPR's data protection by design principle gives you leverage here.

<!-- INTERNAL_LINK: governing third-party risk in your AWS environment | aws-compliance-and-governance -->

### 6. Abandoning crypto agility as a goal

Cryptographic standards will continue to evolve. NIST selected HQC for standardisation in 2025, and further algorithms for digital signatures with specific properties are in the pipeline. A migration that replaces one hard-coded algorithm with another has achieved nothing architectural. Build your systems to swap primitives, maintain a living cryptographic bill of materials (CBOM), and treat algorithm rotation as a routine operational capability rather than a dedicated programme.

<!-- INTERNAL_LINK: well-architected security principles for cloud workloads | aws-well-architected-security -->

---

## Key takeaways

- The HNDL threat is active now. Adversaries are harvesting encrypted traffic today. For UK financial services, government, and healthcare organisations holding long-lived sensitive data, the case for beginning migration work immediately is not speculative -- it is risk management.

- NIST standards are final; NCSC timelines are set. ML-KEM (FIPS 203), ML-DSA (FIPS 204), and SLH-DSA (FIPS 205) are the algorithms to implement. The NCSC's three-phase roadmap sets the planning horizon to 2035. Regulated sectors should target the 2028 milestone for a completed migration plan.

- AWS has delivered hybrid PQC on KMS, ACM, Secrets Manager, and Transfer Family. Update your SDKs and explicitly enable `.postQuantumTlsEnabled(true)` in Java or the `prefer-post-quantum` feature flag in Rust. Verify with TLS handshake inspection -- do not assume fallback will be caught.

- Client-side SDK upgrades, TLS policy updates on ALBs and NLBs, and firewall rule reviews are your responsibility. AWS secures the managed endpoint. You own the client, the network path, and the custom workload.

- Crypto agility is the durable outcome. A migration that replaces one hard-coded algorithm with another has solved nothing at the architectural level. Build configuration-driven cryptographic primitives, maintain an up-to-date CBOM, and treat algorithm rotation as a routine operational capability.

- Start with a cryptographic inventory before writing a line of migration code. You cannot prioritise what you cannot see. Catalogue every asymmetric operation in your estate -- SDK calls, certificates, VPN endpoints, HSMs, and third-party integrations -- before deciding where to focus first.

<!-- INTERNAL_LINK: managing and rotating secrets in AWS workloads | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: detecting and responding to security events across your AWS estate | cloud-incident-response -->
<!-- INTERNAL_LINK: posture management tooling to surface cryptographic drift | what-is-cspm-cloud-security-posture-management -->