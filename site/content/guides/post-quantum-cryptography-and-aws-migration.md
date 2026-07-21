---
title: "Post-Quantum Cryptography and AWS Migration: A Practitioner's Guide"
date: 2026-07-21
description: "A technical guide to post-quantum cryptography and AWS migration covering NIST standards, AWS services, NCSC timelines, and common pitfalls for UK security architects."
tags: ["post-quantum cryptography", "aws security", "cryptography", "aws kms", "ncsc", "quantum computing"]
slug: "post-quantum-cryptography-and-aws-migration"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2222
draft: false
---

# Post-Quantum Cryptography and AWS migration: a practitioner's guide

Post-quantum cryptography migration is no longer a theoretical exercise reserved for government cryptographers and academic papers. It is an active engineering programme with real deadlines, live AWS service releases, and regulatory consequences for UK financial services and critical national infrastructure. If you run workloads on AWS that involve long-lived sensitive data, digital signatures, or PKI, this guide is for you. I will walk through the standards landscape, what AWS has already shipped, where your responsibilities lie under the shared responsibility model, and the practical steps needed to avoid being caught flat-footed when the 2028 NCSC checkpoint arrives.

---

## Why the urgency is real: "harvest now, decrypt later"

The argument for acting before quantum computers exist is straightforward and uncomfortable.

State-level adversaries almost certainly have collection programmes running against high-value targets right now. Any data encrypted with classical asymmetric algorithms today -- TLS key exchange, SFTP file transfers, certificate issuance -- is potentially stockpiled for future decryption. The NCSC has explicitly warned that organisations must assume sensitive encrypted data is already being collected and will eventually be decrypted. That statement, from the UK's premier technical security authority, should be the opening slide of every PQC board briefing you give.

For UK financial services firms, the stakes are particularly high. The sector relies heavily on public-key cryptography, faces strong regulatory alignment through DORA, and carries significant harvest-now-decrypt-later exposure. In January 2024 the FCA and the World Economic Forum published a joint white paper on quantum security for the financial sector, and GDPR's accountability principle means you need to demonstrate that you have assessed and mitigated this risk -- not just noted it in a risk register.

<!-- INTERNAL_LINK: AWS compliance and governance overview | aws-compliance-and-governance -->

---

## The standards foundation: NIST FIPS 203, 204, and 205

The cryptographic community now has firm ground to stand on. On 13 August 2024, NIST finalised three post-quantum cryptographic algorithms as Federal Information Processing Standards, the culmination of a standardisation process that began in 2016.

The three standards are:

- FIPS 203 (ML-KEM), a module lattice-based key-encapsulation mechanism originally submitted as CRYSTALS-Kyber. This is the primary algorithm for protecting data in transit.
- FIPS 204 (ML-DSA), a module lattice-based digital signature algorithm originally submitted as CRYSTALS-Dilithium. This replaces ECDSA and RSA signatures.
- FIPS 205 (SLH-DSA), a stateless hash-based signature scheme that began as SPHINCS+. This provides a conservative, lattice-independent fallback for signatures.

NIST also selected HQC for standardisation in 2025, with further signature algorithms in the pipeline for specific use cases.

NIST's IR 8547 (IPD) targets deprecation of traditional asymmetric algorithms by 2030 and disallows them after 2035. That is a hard stop on RSA and ECC, not a suggestion.

<!-- INTERNAL_LINK: Cloud compliance frameworks guide | cloud-compliance-frameworks -->

---

## The NCSC migration roadmap for UK organisations

The UK National Cyber Security Centre published comprehensive post-quantum cryptography migration guidance in March 2025, setting a three-phase roadmap for organisations to transition to quantum-resistant encryption by 2035.

The three phases are:

- To 2028: identify cryptographic services needing upgrades and build a migration plan.
- 2028 to 2031: execute high-priority upgrades and refine plans as PQC evolves.
- 2031 to 2035: complete migration to PQC for all systems, services, and products.

The 2028 checkpoint is the one that demands immediate attention. The NCSC's November 2023 white paper was clear: organisations should be beginning or continuing their preparation for migration now.

A successful migration depends on good asset management, clear visibility into your systems and infrastructure, and actively managed supply chains. If you are not investing in cryptographic inventory tooling today, you will not meet the 2028 discovery deadline.

The NCSC also makes a practical point about coexistence: except for the simplest systems, traditional public-key cryptography and PQC will need to run in parallel for a period. Organisations should therefore seek solutions that support cryptographic agility -- the ability to switch between algorithm suites without architectural surgery.

<!-- INTERNAL_LINK: AWS Well-Architected security pillar | aws-well-architected-security -->

---

## What AWS has already shipped

This is where AWS workloads have a genuine advantage over on-premises infrastructure. Workloads that rely heavily on AWS managed services generally face the least effort for PQC migration. Here is the current state of play.

### Data in transit: hybrid post-quantum TLS with ML-KEM

AWS KMS, Amazon S3, and Amazon CloudFront have implemented post-quantum hybrid key establishment combining Elliptic Curve Diffie-Hellman (ECDH) with ML-KEM. The hybrid approach means the handshake remains protected as long as either the classical or the post-quantum component holds -- genuine defence in depth against harvest-now-decrypt-later attacks.

AWS KMS, AWS Certificate Manager (ACM), and AWS Secrets Manager endpoints all support ML-KEM for hybrid post-quantum key agreement. The underlying library is AWS-LC, AWS's FIPS-140-3-validated cryptographic module, which was the first open-source module to include ML-KEM in its FIPS validation.

### Digital signatures: ML-DSA in AWS KMS

AWS KMS now supports FIPS 204 ML-DSA signing. All ML-DSA keys and signing operations run inside FIPS 140-3 Security Level 3 validated hardware security modules.

Three key specs are available. ML-DSA-44 targets security comparable to classical 128-bit encryption. ML-DSA-65 and ML-DSA-87 provide progressively stronger security equivalent to classical 192-bit and 256-bit encryption respectively.

ML-DSA is particularly useful for code signing and firmware signing, where cryptographic signatures may be embedded in devices that cannot be easily updated after deployment, and for any use case where signatures need to remain valid for several years.

### PKI: AWS Private CA with ML-DSA

Following the ML-DSA support in AWS KMS, AWS added post-quantum ML-DSA signature support to AWS Private Certificate Authority. You can now establish quantum-resistant roots of trust for code signing, device authentication, workload authentication with AWS IAM Roles Anywhere, and communication tunnels such as IKEv2/IPsec or mutual TLS using private PKI.

### SFTP file transfers: AWS Transfer Family

AWS Transfer Family supports ML-KEM (FIPS-203) for SFTP file transfers. The two security policy names that include post-quantum key exchange are `TransferSecurityPolicy-2025-03` and `TransferSecurityPolicy-FIPS-2025-03`. The supported post-quantum SSH key exchange methods in these policies are `mlkem768nistp256-sha256`, `mlkem1024nistp384-sha384`, and `mlkem768x25519-sha256`.

<!-- INTERNAL_LINK: AWS CloudTrail configuration best practices | aws-cloudtrail-configuration-best-practices -->

---

## Your side of the shared responsibility model

AWS handles the server-side migration. The customer is responsible for using clients that enable the new algorithms and for configuring those clients to negotiate only the cipher suites you trust.

In practice, this means four things.

First, update your AWS SDKs. PQ TLS support varies by language and runtime. The AWS SDK for Python (Boto3) relies on system libssl/libcrypto -- to use PQ TLS, you need an OS distribution with at least OpenSSL 3.5 installed. The Java v2 SDK requires the AWS CRT client with `postQuantumTlsEnabled(true)`.

Second, update Transfer Family security policies. If you run SFTP endpoints, migrate from any pre-2025 or experimental Kyber policies to `TransferSecurityPolicy-2025-03`. All new Transfer Family security policies issued from 2025 onwards include post-quantum support using hybrid key exchange algorithms.

Third, maintain a cryptographic inventory. Keep an up-to-date record of every place traditional public-key cryptography is used across your environment -- not just AWS services, but third-party integrations and supply chain dependencies too.

Fourth, transition digital signatures to ML-DSA. For any long-lived signing use case -- firmware, code signing, certificate issuance -- migrate to ML-DSA keys in AWS KMS.

---

## Practical implementation: creating an ML-DSA key in AWS KMS

The following AWS CLI and Boto3 snippets cover the key operations for adopting ML-DSA signatures. ML-DSA keys work with the existing KMS `CreateKey` and `Sign` APIs, so your existing IAM and key policies, CloudTrail auditing, and tagging workflows carry over without changes.

### Create an ML-DSA-65 signing key

```bash
# Create a quantum-resistant asymmetric key for signing
aws kms create-key \
  --key-spec ML_DSA_65 \
  --key-usage SIGN_VERIFY \
  --description "Post-quantum code signing key (ML-DSA-65)" \
  --tags TagKey=Environment,TagValue=Production \
            TagKey=PQC-Ready,TagValue=true
```

### Sign an artefact (message up to 4KB)

```bash
# Sign a message (base64-encoded) — RAW MessageType for payloads ≤4096 bytes
KEY_ID="arn:aws:kms:eu-west-2:123456789012:key/mrk-abc123"
MESSAGE=$(echo -n "release-v2.3.1-sha256:abc123" | base64)

aws kms sign \
  --key-id "$KEY_ID" \
  --message "$MESSAGE" \
  --message-type RAW \
  --signing-algorithm ML_DSA_SHAKE_256 \
  --output json \
  | jq -r '.Signature'
```

### Verify a signature

```bash
# Verify the signature — integrates with existing IAM policies and CloudTrail
aws kms verify \
  --key-id "$KEY_ID" \
  --message "$MESSAGE" \
  --message-type RAW \
  --signing-algorithm ML_DSA_SHAKE_256 \
  --signature file://signature.b64
```

### Enable hybrid PQ-TLS in Java (AWS SDK v2)

```java
// Require hybrid post-quantum TLS for all KMS API calls
SdkAsyncHttpClient awsCrtHttpClient = AwsCrtAsyncHttpClient.builder()
    .postQuantumTlsEnabled(true)
    .build();

KmsAsyncClient kmsClient = KmsAsyncClient.builder()
    .httpClient(awsCrtHttpClient)
    .region(Region.EU_WEST_2)
    .build();
```

For messages larger than 4KB, you must pre-process using the External Mu (µ) variant -- see the [AWS KMS ML-DSA documentation](https://docs.aws.amazon.com/kms/latest/developerguide/mldsa.html) for the EXTERNAL_MU signing workflow.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->

---

## Common pitfalls in PQC migration

After working through early-stage PQC readiness assessments with several clients, these are the mistakes I see repeatedly.

### 1. Confusing "quantum-safe at rest" with "quantum-safe in transit"

AES-256 is fine. Properly implemented symmetric encryption is considered quantum-resistant. The real exposure is in the asymmetric algorithms used to negotiate symmetric keys -- your TLS and SSH handshakes. Teams frequently close the wrong tickets because they conflate the two.

### 2. Running Kyber-era clients against ML-KEM endpoints

AWS has signalled that support for pre-standard CRYSTALS-Kyber is phasing out across its service endpoints during 2026 in favour of ML-KEM. Any application still using pre-standard Kyber SDKs at that point will silently fall back to classical-only TLS. There will be no error. You will just lose your HNDL protection without knowing it. Audit your Java SDK versions now.

### 3. Not testing hybrid TLS through your network stack

ML-KEM adds roughly 2.3KB to TLS handshakes. Intermediate proxies, firewalls with deep packet inspection, or anything that terminates and re-establishes TLS may block the new cipher suites -- either because of the ClientHello content or because of the larger key exchange messages. Old DPI appliances and path MTU issues are real blockers in enterprise environments. Test against every network choke point before you roll out.

### 4. Treating PQC migration as a one-time project

Cryptographic migration will be a recurring operational requirement. NIST is still standardising additional algorithms. The architecture needs to swap algorithms without a major engineering effort. Crypto agility -- not any specific algorithm -- is the actual deliverable. Teams with strong patching discipline, reliable CI/CD, and automated lifecycle management will handle the next migration too.

### 5. Skipping the cryptographic inventory step

The deprecation of SHA-1 took roughly a decade from its first publicly demonstrated cryptanalytic weaknesses in 2005 until major browsers completed rejecting SHA-1 certificates around 2017. You cannot migrate what you have not mapped. The NCSC's Phase 1 target of 2028 is a discovery deadline. Many organisations have no clear picture of how deeply RSA and ECDH are embedded across their estate, third-party integrations, and supply chain -- and that problem needs solving before anything else.

### 6. Ignoring the ML_DSA_EXTERNAL_MU requirement for large messages

AWS KMS supports ML-DSA signatures for messages up to 4KB using the RAW message type. For larger messages, you must externally compute the 64-byte message representation µ as defined in NIST FIPS 204. Developers used to RSA or ECDSA workflows hit this limit when signing SBOMs, container manifests, or Terraform state files, and the error messages are not always obvious about the cause.

<!-- INTERNAL_LINK: AWS Security Hub guide | aws-security-hub-guide -->
<!-- INTERNAL_LINK: What is CSPM | what-is-cspm-cloud-security-posture-management -->

---

## UK regulatory context: FCA, GDPR, and NCSC alignment

UK organisations face a convergence of pressures. The NCSC has set its 2028/2031/2035 phased timeline. In August 2024, the NCSC updated their PQC white paper to endorse the NIST quantum-safe algorithms -- the UK was the first major regulatory jurisdiction to reflect NIST's algorithms within national guidance. In January 2024, the FCA and the World Economic Forum jointly published a white paper setting out guiding principles for quantum security in the financial sector.

Under GDPR Article 32, organisations must implement "appropriate technical measures". A documented PQC migration programme -- with evidence of cryptographic inventory, risk assessment, and phased remediation -- is increasingly the expected standard of care. If you suffer a breach of long-retained, classically-encrypted personal data and you have done nothing despite the available NCSC guidance, arguing that your measures were "appropriate" will be difficult.

Some procurement frameworks are beginning to require evidence of PQC readiness for new contracts, with full migration timelines varying considerably by industry and geography. If you are procuring or renewing any cryptographic capability -- HSMs, PKI, secure messaging platforms -- post-quantum readiness should already be in your vendor requirements.

<!-- INTERNAL_LINK: Cloud identity and access management | cloud-identity-and-access-management -->
<!-- INTERNAL_LINK: What is zero trust architecture | what-is-zero-trust-architecture -->

---

## Summary

The threat is present-tense, not future-tense. Adversaries harvesting encrypted data today is the primary driver for acting now. Data with a ten-year sensitivity window is already at risk. Start with your highest-confidentiality data-in-transit workloads.

AWS has shipped real PQC capabilities. ML-KEM hybrid TLS is live across AWS KMS, ACM, Secrets Manager, S3, and CloudFront. ML-DSA signing is available in AWS KMS and Private CA. Workloads that rely heavily on managed services absorb most of the server-side migration automatically.

Your SDK and client versions are your responsibility. Post-quantum-ready clients are backwards-compatible, so you can start client-side updates now regardless of whether every service you use has launched PQ support.

The NCSC's 2028 Phase 1 deadline is a discovery and planning target, not a completion milestone. The full transition runs to 2035, with high-priority migration activities completing by 2031. If you have not started your cryptographic inventory, you are already behind.

Build for crypto agility, not a single migration. NIST is still standardising additional KEMs and signature schemes beyond ML-KEM, ML-DSA, and SLH-DSA. Your architecture needs to accommodate algorithm changes without a major engineering effort each time.

Kyber clients should be migrated ahead of 2026. AWS has signalled that CRYSTALS-Kyber support is phasing out across its service endpoints in favour of ML-KEM. Audit your Java SDK versions and any legacy PQ-experimental Transfer Family policies now.