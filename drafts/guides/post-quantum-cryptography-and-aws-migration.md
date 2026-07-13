---
title: "Post-Quantum Cryptography and AWS Migration: A Practitioner's Guide"
date: 2025-07-13
description: "A practical guide to post-quantum cryptography and AWS migration covering NCSC timelines, ML-KEM, ML-DSA, shared responsibility, and common pitfalls."
tags: ["post-quantum cryptography", "aws security", "cryptography", "kms", "ncsc", "cloud security"]
slug: "post-quantum-cryptography-and-aws-migration"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2224
draft: false
---

# Post-quantum cryptography and AWS migration: what you actually need to do now

The question I get most often from CTOs and security leads at UK financial services firms right now is: "Is post-quantum cryptography something we need to worry about yet?" The answer is unambiguous: yes, and the window for comfortable planning is closing. Post-quantum cryptography migration is no longer a theoretical future-state exercise. There is no evidence that a quantum computer powerful enough to break public-key cryptography exists today, but AWS is not waiting, and neither should you. The posture every organisation handling sensitive data should adopt is to put protections in place now. This guide covers the threat model, the UK regulatory context, what AWS has already built, and the concrete steps your team needs to take, including the pitfalls I see teams fall into repeatedly.

---

## The threat model: why "harvest now, decrypt later" changes everything

The quantum threat is not about an adversary breaking your encryption today. It is about data being exfiltrated and stockpiled right now, to be decrypted once a sufficiently powerful quantum machine exists.

The top priority for PQC is addressing this "harvest now, decrypt later" (HNDL) risk. Long-lived sensitive data in transit over public networks can be captured today and decrypted by future quantum computers. For UK financial institutions, where transaction records, client data, and regulatory filings carry multi-decade retention obligations under GDPR and FCA rules, this is not a distant risk. The NCSC has explicitly warned that organisations must assume sensitive encrypted data is already being collected and will eventually be decrypted.

The threat a cryptographically relevant quantum computer poses is its potential to break the public-key cryptographic algorithms in use today, the algorithms underpinning most communication protocols and digital signature schemes. Symmetric encryption, AES-256 for instance, is not meaningfully threatened. The exposure sits entirely in asymmetric cryptography: RSA, ECDH, ECDSA, the foundations of TLS, code signing, certificate authorities, and key exchange.

<!-- INTERNAL_LINK: understanding zero trust architecture | what-is-zero-trust-architecture -->

---

## The UK regulatory landscape

In March 2025, the UK National Cyber Security Centre published its guidance "Timelines for migration to post-quantum cryptography", setting a three-phase roadmap for organisations to transition to quantum-resistant encryption by 2035.

The three phases are concrete and, for regulated sectors, non-negotiable:

- Phase 1 (to 2028): identify cryptographic services needing upgrades and build a migration plan
- Phase 2 (2028-2031): execute high-priority upgrades and refine plans as PQC standards evolve
- Phase 3 (2031-2035): complete migration to PQC for all systems, services, and products

That timelines guidance builds on an earlier NCSC white paper, published in November 2023 and titled "Next steps in preparing for post-quantum cryptography", with minor updates in August 2024 to reflect NIST's publication of three algorithm standards. The core message was that organisations should be beginning or continuing their preparation for migration to PQC now.

On the algorithm side, NIST published FIPS 203, 204, and 205 in August 2024, standardising the first post-quantum cryptographic algorithms: ML-KEM, ML-DSA, and SLH-DSA. These are the standards you should be building against. NIST's IR 8547 (IPD) provides a transition roadmap draft targeting deprecation of traditional asymmetric algorithms by 2030 and disallowing them after 2035.

For FCA-regulated firms, the picture is moving. UK securities agencies are showing growing focus on the topic, with the Financial Conduct Authority collaborating within the World Economic Forum to publish a white paper on quantum security within the financial sector. Treat this as early signal of eventual binding guidance and get ahead of it now.

<!-- INTERNAL_LINK: AWS compliance and governance overview | aws-compliance-and-governance -->

---

## What AWS has already done (and what it has not)

Understanding the AWS shared responsibility model for PQC matters here. AWS is not doing this for you wholesale. There is meaningful customer-side work required.

As AWS delivers post-quantum cryptography capabilities, some PQC features will be transparently enabled for all customers while others will be options that customers can choose to implement to meet their own requirements.

### What AWS has delivered

AWS pioneered a mechanism called hybrid post-quantum key agreement, which combines Elliptic-Curve Diffie-Hellman (ECDH) with a post-quantum key encapsulation method such as ML-KEM. The two resulting keys are combined to establish session communication keys that encrypt network traffic. An adversary would need to break both ECDH and ML-KEM to break the confidentiality of that exchange.

Services including AWS KMS, Amazon S3, and Amazon CloudFront have implemented this hybrid key establishment to protect against harvest-now-decrypt-later attacks. On the signatures side, AWS has integrated FIPS 204 (ML-DSA) into AWS KMS, allowing customers to create and use ML-DSA keys through the same KMS APIs they use today for digital signatures: CreateKey, Sign, and Verify. All ML-DSA keys and signature operations are protected in FIPS 140-3 Security Level 3 validated hardware security modules.

For Secrets Manager specifically, the Workload Credentials Provider (v2.0.0 or later), the AWS Lambda extension (v19 or later), and the Secrets Manager CSI Driver (v2.0.0 or later) now enable and prefer post-quantum TLS when connecting to Secrets Manager.

### What you still own

AWS customers must update their TLS clients and SDKs to offer ML-KEM when connecting to AWS service HTTPS endpoints. That is your responsibility. PQ-ready clients are backwards compatible, so you can begin client-side updates even if some services you connect to have not yet launched PQ support. There is no good reason to delay.

The performance overhead is real but modest. AWS's own measurements put the cost of moving from ECDH-only key agreement to an ECDH+ML-KEM hybrid at approximately 1,600 additional bytes in the TLS handshake and around 80-150 microseconds of additional compute time for ML-KEM operations, though the exact overhead varies with the ML-KEM parameter set and implementation in use. For high-frequency microservice meshes this warrants profiling, but for most workloads it is negligible.

<!-- INTERNAL_LINK: AWS KMS and IAM security best practices | aws-iam-security-best-practices -->

---

## Creating an ML-DSA key and signing with AWS KMS

The following example demonstrates creating a post-quantum ML-DSA-65 signing key in AWS KMS using the AWS CLI and Python boto3 SDK. AWS KMS offers three new key specs: `ML_DSA_44`, `ML_DSA_65`, and `ML_DSA_87`.

ML-DSA-44 is suitable for applications requiring security comparable to classical 128-bit encryption, while ML-DSA-65 and ML-DSA-87 provide progressively stronger security levels equivalent to classical 192-bit and 256-bit encryption respectively.

Step 1: create the key via CLI:

```bash
# Create an asymmetric ML-DSA-65 key pair for signing
aws kms create-key \
  --key-spec ML_DSA_65 \
  --key-usage SIGN_VERIFY \
  --description "Post-quantum signing key (ML-DSA-65) - FIPS 204" \
  --tags TagKey=Purpose,TagValue=PQC-Signing \
       TagKey=Environment,TagValue=Production
```

Step 2: sign and verify a message with Python (boto3):

```python
import boto3
import hashlib

def create_mldsa_key(region: str = "eu-west-1") -> str:
    """Create an ML-DSA-65 signing key in AWS KMS."""
    kms = boto3.client("kms", region_name=region)
    response = kms.create_key(
        KeySpec="ML_DSA_65",
        KeyUsage="SIGN_VERIFY",
        Origin="AWS_KMS",
        Description="PQC signing key — ML-DSA-65 (FIPS 204)",
    )
    key_id = response["KeyMetadata"]["KeyId"]
    print(f"Created ML-DSA key: {key_id}")
    return key_id


def sign_message(key_id: str, message: bytes, region: str = "eu-west-1") -> bytes:
    """Sign a message using ML-DSA via AWS KMS.
    
    Messages larger than 4 KB must use EXTERNAL_MU pre-processing.
    For demonstration, this example signs a <=4 KB raw message.
    """
    kms = boto3.client("kms", region_name=region)
    response = kms.sign(
        KeyId=key_id,
        Message=message,
        MessageType="RAW",             # Use EXTERNAL_MU for messages > 4 KB
        SigningAlgorithm="ML_DSA_SHAKE_256",
    )
    return response["Signature"]


def verify_signature(
    key_id: str,
    message: bytes,
    signature: bytes,
    region: str = "eu-west-1",
) -> bool:
    """Verify an ML-DSA signature via AWS KMS."""
    kms = boto3.client("kms", region_name=region)
    response = kms.verify(
        KeyId=key_id,
        Message=message,
        MessageType="RAW",
        SigningAlgorithm="ML_DSA_SHAKE_256",
        Signature=signature,
    )
    return response["SignatureValid"]


if __name__ == "__main__":
    region = "eu-west-1"                   # ML-DSA is rolling out region-by-region
    payload = b"Firmware build v2.4.1"     # Keep under 4 KB for RAW mode

    key_id = create_mldsa_key(region)
    sig = sign_message(key_id, payload, region)
    valid = verify_signature(key_id, payload, sig, region)
    print(f"Signature valid: {valid}")
```

A few notes on this code. AWS KMS supports asymmetric key signatures for messages up to 4 KB using the RAW message type. For larger messages, you must externally compute the 64-byte message representation used in ML-DSA signing as defined in NIST FIPS 204 section 6.2. The ML-DSA keys work with the existing KMS CreateKey and Sign APIs, so your established automation processes, IAM and KMS key policies, auditing, and tagging workflows carry over without changes. For code signing with a full PKI chain, combine this with AWS Private CA, which now supports post-quantum ML-DSA signature hierarchies.

<!-- INTERNAL_LINK: AWS Security Hub posture monitoring | aws-security-hub-guide -->

---

## Building crypto-agility: the architecture principle that matters most

Deploying ML-KEM today is not the end of this story. Standards will evolve, algorithms will be refined, and your architecture needs to be able to rotate cryptographic primitives without a full rewrite.

Your goal should extend beyond deploying PQC once. Build the organisational muscle to rotate protocols, algorithms, and key lengths as standards evolve, because cryptographic migration will be a recurring operational requirement.

In practice, crypto-agility on AWS means four things.

First, centralise all signing and key-exchange operations through AWS KMS and never hardcode algorithm choices in application code. Call the KMS API and let the key spec define the algorithm.

Second, use AWS Certificate Manager and Private CA for all certificate issuance. This gives you a single control plane to rotate certificate algorithms when standards change.

Third, specify TLS policies explicitly in your infrastructure-as-code wherever you create or update customer-configurable resources. If the TLS policy is implicit, it will drift.

Fourth, use AWS Config rules to detect that drift. Config can continuously monitor PQC configurations across AWS services, correlating ML-KEM and ML-DSA compatibility attributes from KMS, Transfer Family, ACM, and other cryptographic endpoints, and flagging when deployed configurations deviate from approved quantum-safe baselines.

<!-- INTERNAL_LINK: AWS CloudTrail configuration and audit logging | aws-cloudtrail-configuration-best-practices -->

---

## Your cryptographic inventory: the work that cannot be skipped

One of the clearest lessons from real-world deployments is that you cannot migrate cryptography you cannot see.

In most organisations, the cryptographic inventory is incomplete. Encryption is embedded across enterprise infrastructure, including TLS certificates, firmware, boot processes, applications, and hardware systems, often distributed and not centrally tracked. Discovery is the first step in any migration effort.

On AWS, start your inventory with four things:

- AWS Certificate Manager: list all issued certificates, note algorithm types, expiry dates, and issuing CAs
- AWS KMS: enumerate all asymmetric key pairs and identify any still using RSA or ECC for long-lived operations
- AWS CloudTrail: query for `kms:Sign` and `kms:GenerateDataKeyPair` calls to surface where asymmetric crypto is actively in use
- AWS Config: use managed rules and custom Config rules to flag resources using deprecated TLS policies

AWS suggests using CloudTrail, Config, Lambda, or custom scripts to automate part of this discovery process. This is not a one-off exercise. Maintaining an updated cryptographic inventory across your broader environment, to identify other uses of traditional public-key cryptography that will require migration, is an ongoing operational responsibility.

<!-- INTERNAL_LINK: cloud security vulnerability management | cloud-security-vulnerability-management -->

---

## Common pitfalls in PQC migration on AWS

These are the mistakes I see most frequently, and they are all avoidable.

### 1. Assuming AWS handles everything for you

The shared responsibility model applies here as much as anywhere. AWS is migrating its managed service endpoints, but your client-side SDKs, your application TLS configurations, your ALB security policies, and your own PKI are your problem. Do not conflate "AWS supports ML-KEM" with "my workloads are post-quantum ready."

### 2. Still running CRYSTALS-Kyber in production

Support for CRYSTALS-Kyber will continue through 2025 but will be removed across all AWS service endpoints in 2026 in favour of ML-KEM. If you are running AWS SDK versions that negotiate Kyber rather than ML-KEM, you will fall back to classical key agreement silently when Kyber is withdrawn. AWS's ML-KEM launch announcement notes that customers currently negotiating CRYSTALS-Kyber on older AWS Java SDK versions will see their clients gracefully fall back to a classical key agreement once Kyber is removed from AWS service HTTPS endpoints. "Graceful fallback" is not the outcome you want.

### 3. Treating inventory as a prerequisite to starting

Trying to perfect the inventory before starting migration is a trap. Discovery should accelerate migration, not postpone it. Run your TLS endpoint migration and your inventory discovery as concurrent workstreams, not sequential ones.

### 4. Ignoring the data lifespan question

Not all data carries the same HNDL risk. Data with a sensitivity window of two years and data that must remain confidential for thirty years are entirely different threat profiles. AWS recommends using a data sensitivity, data lifespan, and threat exposure model to prioritise which assets should migrate first. Financial client records, M&A documentation, classified government data, and personal health information all warrant top priority. Ephemeral API responses do not.

### 5. Hardcoding algorithm choices in application code

If your application specifies `RSA_2048` or `ECDSA_SHA_256` as string literals in config files or code, every future algorithm rotation becomes a code-change-and-deploy cycle. Abstract all cryptographic operations behind KMS calls or a centralised crypto service. This is not just good PQC hygiene, it is good software architecture.

### 6. Neglecting third-party and supply chain exposure

Your AWS workloads may be PQC-ready whilst your VPN appliance, HSM vendor, or SaaS identity provider is running cryptography from 2019. Asymmetric cryptography is embedded in every protocol, every vendor dependency, and every legacy system that quietly handles key exchange or digital signatures. Contractually require PQC roadmap disclosure from all security-critical vendors.

<!-- INTERNAL_LINK: cloud incident response planning | cloud-incident-response -->

---

## Key takeaways

- The harvest-now-decrypt-later threat is active today. Sensitive data in transit over public networks can be captured now and decrypted by future quantum computers, making TLS key exchange the highest-priority item to address.

- The NCSC has set firm UK timelines. Complete your cryptographic discovery and migration plan by 2028, complete high-priority migrations by 2031, and complete all system migration by 2035. FCA-regulated firms should treat the 2028 discovery deadline as a compliance obligation, not a suggestion.

- Workloads that rely heavily on AWS managed services generally require the least effort for PQC migration. The more you use KMS, ACM, ALB, and CloudFront rather than self-managed crypto, the more AWS can handle transparently on your behalf.

- Update your AWS SDKs now. PQ-ready clients are backwards compatible, so there is no downside risk to upgrading today.

- Build crypto-agility into your architecture. Centralise all cryptographic operations through AWS KMS, declare TLS policies explicitly in IaC, and use AWS Config to detect drift. Treat algorithm rotation as a routine operational capability, not a crisis response.

- Post-quantum migration is not a single upgrade. It is an operational transformation affecting infrastructure, certificates, PKI, hardware, and long-term system design. Staff it, budget it, and govern it as a multi-year programme.