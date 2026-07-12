---
title: "Post-Quantum Cryptography and AWS Migration: A Practitioner's Guide"
date: 2025-07-12
description: "A practitioner's guide to post-quantum cryptography and AWS migration — covering NIST standards, AWS PQC services, NCSC timelines, and common pitfalls to avoid."
tags: ["post-quantum cryptography", "aws security", "cryptography", "kms", "encryption", "ncsc", "compliance"]
slug: "post-quantum-cryptography-and-aws-migration"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2336
draft: false
---

# Post-quantum cryptography and AWS migration: what every cloud security architect needs to know now

If you work in UK financial services, government, or any enterprise sector that handles long-lived sensitive data, post-quantum cryptography and AWS migration is no longer a research topic you can defer to next year's roadmap. The regulatory clock is ticking, adversaries are harvesting encrypted traffic today, and AWS is actively retiring legacy pre-standard algorithms in favour of NIST-finalised replacements. This guide gives you a practical, opinionated view of what you need to do, why it matters, and where teams typically go wrong.

<!-- INTERNAL_LINK: AWS KMS and encryption key management | aws-iam-security-best-practices -->
<!-- INTERNAL_LINK: AWS compliance and governance posture | aws-compliance-and-governance -->

---

## Why this is not a future problem

The threat model here is asymmetric and time-sensitive. The top priority for PQC is addressing the "harvest now, decrypt later" (HNDL) risk, where long-lived sensitive data in transit over public networks can be captured today and decrypted by future quantum computers. This is not hypothetical. Estimated timelines for sufficiently powerful quantum computers sit in the 2030-2035 range, and the NCSC has warned UK organisations that sensitive encrypted data should be assumed already collected.

Historically, cryptographic migrations have taken far longer than you might expect. The deprecation of SHA-1 took roughly a dozen years from the first published collision attacks in 2005 until major browsers finally rejected it in 2017. MD5, 3DES, and RC4 all followed the same pattern of slow organisational response despite clear technical consensus that migration was overdue.

The lesson is clear: starting late is expensive. Organisations that treat PQC as a 2029 problem will find themselves in a compliance crisis with compressed timelines and diminished options.

---

## The standards landscape: what NIST actually published

NIST released the final versions of FIPS 203, 204, and 205 in August 2024, concluding an eight-year standardisation process that began in 2016. These are the algorithms you should be building around:

- ML-KEM (FIPS 203), derived from CRYSTALS-Kyber, specifies a module-lattice-based key encapsulation mechanism providing IND-CCA2 security under the Module Learning With Errors (MLWE) hardness assumption. This is your primary replacement for RSA and ECDH key exchange.
- ML-DSA (FIPS 204), derived from CRYSTALS-Dilithium, provides a lattice-based digital signature scheme.
- SLH-DSA (FIPS 205), derived from SPHINCS+, provides a stateless hash-based signature scheme whose security rests solely on hash function properties. Treat this as your conservative fallback if lattice-based assumptions ever come under question.

One point that regularly trips teams up: properly implemented symmetric encryption is already considered quantum-resistant. Asymmetric cryptography is where the quantum threat sits. Your AES-256 data at rest is not the urgent problem. Your TLS key exchange and digital signatures are.

<!-- INTERNAL_LINK: Data security posture and encryption coverage | what-is-dspm-data-security-posture-management -->

---

## The UK regulatory context: NCSC timelines you cannot ignore

The UK National Cyber Security Centre has been telling organisations to prepare for this transition since its 2023 white paper, "Next steps in preparing for post-quantum cryptography". In March 2025 it followed up with its "Timelines for migration to post-quantum cryptography" guidance, setting a three-phase roadmap for organisations to transition to quantum-resistant encryption by 2035. For FCA-regulated firms and operators of critical national infrastructure, this is not optional reading.

The three phases are concrete. To 2028: identify cryptographic services needing upgrades and build a migration plan. From 2028 to 2031: execute high-priority upgrades and refine plans as PQC evolves. From 2031 to 2035: complete migration to PQC for all systems, services and products.

According to the NCSC, regulated sectors in the UK -- such as banking, financial services, and telecoms companies, and those with predominantly internet-facing services -- should prioritise an early migration to PQC, aligning these efforts with global partners and rolling out the transition as soon as well-implemented PQC solutions become available.

Since introducing PQC will likely give rise to interoperability or compatibility challenges, the NCSC advises that you choose solutions that offer cryptographic agility and can readily support alternative suites of cryptographic algorithms, allowing you to determine on a case-by-case basis when to phase out legacy algorithms.

The phrase "crypto-agility" appears throughout NCSC guidance for good reason. Build your architecture to swap algorithms, not to hardcode them.

---

## Where AWS is in its own migration

AWS is migrating to post-quantum cryptography and helping customers do the same under a shared responsibility model. Understanding precisely what that means in practice is critical, because it determines what you have to do yourself.

This transition is happening in phases, starting with systems that communicate over untrusted networks such as the internet. AWS has structured its work into four workstreams: inventory and standards development, PQ key exchange for data in transit (Workstream 2), PQ signing algorithms for long-lived roots of trust (Workstream 3), and PQ signatures for session-based authentication such as TLS certificates (Workstream 4).

AWS has already deployed post-quantum cryptography across several services. AWS KMS, AWS Certificate Manager (ACM), and AWS Secrets Manager have implemented post-quantum hybrid key establishment combining ECDH with ML-KEM to protect against harvest now, decrypt later attacks. AWS KMS and AWS Private CA support quantum-resistant signatures and roots of trust with ML-DSA.

The critical nuance on shared responsibility: AWS customers must update their TLS clients and SDKs to offer ML-KEM when connecting to AWS service HTTPS endpoints. AWS upgrades the server side; you own the client side. Do not assume that because you are using a managed service, you are automatically protected.

### The CRYSTALS-Kyber deprecation deadline

Teams that piloted PQC using the pre-standard CRYSTALS-Kyber implementation need to act. Support for CRYSTALS-Kyber will continue through 2025, but will be removed across all AWS service endpoints in 2026 in favour of ML-KEM. If you have any workloads or SDK configurations that explicitly target Kyber, update them now.

<!-- INTERNAL_LINK: AWS Security Hub for posture monitoring | aws-security-hub-guide -->

---

## Enabling hybrid post-quantum TLS: practical implementation

The hybrid approach is the right one for this migration window. Hybrid post-quantum TLS establishes connections by combining traditional cryptography (such as X25519) with post-quantum algorithms (ML-KEM), protecting your secrets against both current classical attacks and future quantum computer threats.

### AWS SDK for Java v2: enabling ML-KEM for KMS

The most straightforward entry point for most enterprise workloads is enabling PQ TLS at the SDK level. For AWS KMS calls using the AWS SDK for Java v2 with the Common Runtime HTTP client:

```java
import software.amazon.awssdk.http.crt.AwsCrtAsyncHttpClient;
import software.amazon.awssdk.http.async.SdkAsyncHttpClient;
import software.amazon.awssdk.services.kms.KmsAsyncClient;
import software.amazon.awssdk.regions.Region;

// Build an HTTP client with hybrid post-quantum TLS (ML-KEM) enabled
SdkAsyncHttpClient awsCrtHttpClient = AwsCrtAsyncHttpClient.builder()
    .postQuantumTlsEnabled(true)
    .build();

// Attach it to your KMS async client
KmsAsyncClient kmsClient = KmsAsyncClient.builder()
    .region(Region.EU_WEST_2)  // London region
    .httpClient(awsCrtHttpClient)
    .build();

// All GenerateDataKey, Decrypt, etc. calls now use hybrid PQ TLS
// Verify by inspecting CloudTrail tlsDetails.keyExchange for "X25519MLKEM768"
```

This single configuration change routes all KMS API calls over a TLS connection that combines X25519 (classical) with ML-KEM-768 (post-quantum), providing protection against both current and future adversaries.

### Verifying PQ TLS is active via CloudTrail

Do not assume the handshake is negotiating correctly. Verification is a two-step process: fetch a secret using your Secrets Manager client to generate an API call, then confirm in AWS CloudTrail that the call negotiated hybrid post-quantum key exchange. In CloudTrail, look for the `tlsDetails` field:

```json
{
  "tlsDetails": {
    "tlsVersion": "TLSv1.3",
    "cipherSuite": "TLS_AES_256_GCM_SHA384",
    "clientProvidedHostHeader": "kms.eu-west-2.amazonaws.com",
    "keyExchange": "X25519MLKEM768"
  }
}
```

If it shows a traditional algorithm such as X25519, the client is not advertising ML-KEM support. Check the client version and configuration.

### Performance overhead: honest numbers

Switching from a classical to a hybrid post-quantum key agreement transfers approximately 1,600 additional bytes during the TLS handshake and requires more compute time for ML-KEM cryptographic operations — AWS's April 2025 Security Blog announcement of ML-KEM support in KMS, ACM, and Secrets Manager put this at approximately 80-150 microseconds, though your figures will vary with hardware, environment, and the ML-KEM parameter set negotiated. Either way, this is a one-time TLS connection startup cost, amortised over the lifetime of the connection across all HTTP requests sent over it.

In practice, if your workloads reuse TLS connections (which they should be doing anyway) this overhead is negligible. If you have applications that create a new TLS connection per API call, fix that first.

<!-- INTERNAL_LINK: CloudTrail configuration for security auditing | aws-cloudtrail-configuration-best-practices -->

---

## AWS Transfer Family and SSH post-quantum support

PQC migration extends beyond HTTPS. AWS Transfer Family has upgraded its support of hybrid quantum-resistant key exchanges from Kyber to ML-KEM, standardised by NIST in FIPS 203. The SSH policy names that support post-quantum key exchange with ML-KEM are `TransferSecurityPolicy-2025-03` and `TransferSecurityPolicy-FIPS-2025-03`. If you use AWS Transfer Family for SFTP workloads (common in financial services data exchange pipelines) update your security policies.

---

## Common mistakes and pitfalls

This is where most organisations lose time and money. Based on patterns I see repeatedly across enterprise AWS environments, these are the errors that will set your programme back by 12-18 months.

### 1. Assuming managed services handle everything automatically

Some PQC features will be transparently enabled for all customers while others are options that customers choose to implement. Managed service encryption at rest (S3 SSE, RDS, Secrets Manager) is largely already handled. TLS client behaviour is your responsibility. Organisations that discover this distinction after an audit have a rude awakening.

### 2. Hardcoding cipher suites and pinning specific algorithms

Systems running custom TLS libraries or hardcoded cipher suites need to be flagged early. If your Lambda functions or EC2 workloads are pinning specific TLS cipher suites, you will silently fall back to classical key exchange without any warning. Audit your TLS configuration as part of discovery.

### 3. Skipping the cryptographic inventory phase

Understanding where cryptography underpins business processes (customer authentication, supply chain communications, cloud connectivity, regulatory data retention) is essential for managing quantum risk effectively. Teams that jump straight to enabling ML-KEM on KMS without cataloguing their full cryptographic surface area typically discover, six months later, that their API gateway mutual TLS, their inter-VPC private certificate authority, and their document signing workflow are all still classical. Do the discovery work first.

### 4. Confusing transit protection with at-rest protection

One of the important decisions AWS itself made was to focus more on encryption in transit and less on encryption at rest. This is the right prioritisation, yet many teams invert it. When AWS KMS encrypts your data under KMS keys, it uses symmetric cryptography with 256-bit keys and AES-GCM, which is already quantum resistant. Spending six months auditing your S3 encryption instead of securing your TLS handshakes is a category error.

### 5. Ignoring proxy and firewall interference

Depending on the network path your request takes, you may find that intermediate hosts, proxies, or firewalls with deep packet inspection (DPI) block the request. If this happens, you will need to work with your security team or IT administrators to update firewalls to permit these new TLS algorithms. This is particularly common in heavily regulated environments with inline TLS inspection. ML-KEM key shares are significantly larger than classical ones, and some legacy DPI appliances drop connections they cannot parse. Test from your actual network paths, not just from a developer laptop.

### 6. Treating CRYSTALS-Kyber as equivalent to ML-KEM

They are related but distinct. AWS services previously deployed support for CRYSTALS-Kyber, the predecessor of ML-KEM. Support for CRYSTALS-Kyber continues through 2025 but will be removed across all AWS service endpoints in 2026 in favour of ML-KEM. Any workload that is only advertising Kyber support (not ML-KEM) will break when the retirement happens. Audit your SDK versions against the minimum version matrix published by AWS.

### 7. Neglecting supply chain and third-party dependencies

Firms should consider incorporating requirements for PQC into new contracts and service-level agreements to ensure all vendor relationships are accounted for in their quantum risk management strategy. If your payment processor, data analytics vendor, or managed SOC provider communicates with your AWS environment over TLS connections they control, their client-side upgrade is outside your direct control. Raise it now, before procurement renewals give you leverage.

---

## Your practical migration roadmap

Given the NCSC's Phase 1 deadline of 2028, here is a prioritised sequence that makes sense for most UK enterprise AWS environments:

1. Complete cryptographic discovery: map all services, SDKs, and dependencies that use asymmetric cryptography. Focus on internet-facing and cross-VPC TLS first.
2. Update SDK dependencies: upgrade to the minimum SDK versions required for ML-KEM support. Start with services that have the highest HNDL exposure (KMS, Secrets Manager, ACM).
3. Verify via CloudTrail: confirm `keyExchange: X25519MLKEM768` is appearing in `tlsDetails` for your critical API calls.
4. Test proxy and DPI compatibility: run hybrid TLS handshakes from all network segments, including on-premises connections via Direct Connect or VPN.
5. Migrate AWS Transfer Family policies: update SFTP security policies to `TransferSecurityPolicy-2025-03` where applicable.
6. Build crypto-agility into your CI/CD: make SDK version and cipher suite configuration a pipeline parameter, not a hardcoded value.
7. Draft your NCSC Phase 1 migration plan: document scope, priorities, and a delivery timeline against the 2028 milestone.

<!-- INTERNAL_LINK: Well-Architected security pillar alignment | aws-well-architected-security -->
<!-- INTERNAL_LINK: Cloud incident response planning | cloud-incident-response -->

---

## Key takeaways

- HNDL is the most urgent threat. The harvest now, decrypt later risk (where sensitive data in transit today can be decrypted by future quantum computers) is the top priority for PQC migration, not encryption at rest.
- The NCSC has given you a deadline. UK organisations must complete discovery and a migration plan by 2028, execute high-priority migrations by 2031, and achieve full PQC coverage by 2035.
- AWS shared responsibility applies. Some PQC features are transparently enabled; others require explicit customer action, particularly on the TLS client side. Enabling ML-KEM in your AWS SDKs is your responsibility.
- CRYSTALS-Kyber is being retired. AWS is removing support for the pre-standard Kyber implementation across all service endpoints in 2026 in favour of ML-KEM. Audit your SDK versions and configurations before this deadline.
- The performance overhead is minimal. Hybrid PQ TLS adds approximately 1,600 bytes per new TLS handshake plus a small amount of compute (roughly 80-150 microseconds per AWS's published figures, varying by environment), a one-time cost amortised across the connection lifetime. There is no credible performance argument against enabling it.
- Crypto-agility is the real goal. Build the organisational capability to rotate protocols, algorithms, and key lengths as standards evolve. Cryptographic migration will be a recurring operational requirement, not a one-time project.