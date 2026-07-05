---
title: "Recent Cloud Security CVEs: What Practitioners Need to Patch Right Now (July 2026)"
date: 2026-07-05
description: "A practitioner's breakdown of recent cloud security CVEs including Bad Epoll, PHP OpenSSL, and Azure flaws — with triage advice and detection code."
tags: ["cloud security", "CVE", "vulnerability management", "Linux kernel", "AWS", "Azure", "patch management"]
slug: "recent-cloud-security-cves"
author: "Steve Harrison & AI - Principal Security Architect"
word_count: 2307
draft: false
---

# Recent cloud security CVEs: what practitioners need to patch right now

Summer 2026 is not a quiet patch cycle. Linux kernels, PHP runtimes, Azure managed services -- the vulnerabilities landing right now sit in infrastructure that underpins real production workloads, and triage discipline matters as much as remediation speed. Mandiant's M-Trends 2026 puts the mean time to exploit at negative seven days: exploitation is routinely happening before a patch exists. You cannot patch your way out of that reactively. You need a clear view of what matters, why it matters specifically in cloud environments, and what to do about it this week.

This guide covers three high-impact CVEs disclosed in July 2026, explains the cloud-specific blast radius of each, and closes with the mistakes that leave teams exposed long after patches are available.

<!-- INTERNAL_LINK: cloud vulnerability management programme | cloud-security-vulnerability-management -->

---

## The vulnerability landscape right now

The macro context matters before looking at individual CVEs.

The public CVE programme published 48,185 new vulnerabilities in 2025, a 20.6% increase on the prior year. The CISA Known Exploited Vulnerabilities catalogue grew 20% to 1,484 entries, with 245 added across the year. If FIRST's predictions hold, 2026 will be the first year to exceed 50,000 published CVEs.

That works out to roughly 131 new CVEs per day, with a median time to exploit now under five days. The question for security teams is no longer whether vulnerabilities will be targeted. It is whether the right ones are being fixed fast enough.

In cloud environments this is made worse by the shared responsibility model. Some vulnerabilities are patched transparently by your cloud provider. Others land squarely in your court. Knowing which is which, immediately, is the difference between a non-event and a notification to the ICO.

<!-- INTERNAL_LINK: shared responsibility model explainer | shared-responsibility-model-cloud-security -->

---

## CVE-2026-46242 — "Bad Epoll": Linux kernel privilege escalation

This is the one dominating the security community's attention this week, and for good reason.

### What it is

Bad Epoll lets an ordinary user with no special access take full control of a machine as root. It affects Linux desktops, servers, and Android. A fix is out.

The vulnerability lives in the Linux kernel's epoll subsystem, the core I/O event notification mechanism that applications rely on to monitor multiple file descriptors simultaneously. Because epoll is central to how Linux handles concurrent I/O, it is embedded in virtually every Linux-based environment, from enterprise cloud infrastructure to Android devices.

The bug itself is a use-after-free. Two parts of the kernel attempt to clean up the same internal object at the same time. One frees the memory while the other is still writing into it. That brief collision lets an attacker corrupt kernel memory and escalate from a normal account to root.

### Why the exploit reliability is alarming

The exploit loops until it lands without ever crashing the kernel, and it hits root roughly 99% of the time on a vulnerable machine. This is not a theoretical primitive. It is a reliable, weaponised attack chain.

The flaw affects mainline Linux from version 6.4 onwards, plus the backport ranges distributions maintain on older long-term-support branches. On Android, devices running 6.6-series kernels and newer are confirmed vulnerable, including current Pixel hardware.

There is also a browser-chaining risk. The proof-of-concept can be triggered from inside Chrome's sandboxed renderer process. An attacker who already has renderer code execution, through a separate browser bug, could chain Bad Epoll with that access to break out of the sandbox entirely.

### Cloud-specific blast radius

This is particularly consequential in shared infrastructure: multi-tenant cloud VMs, container escape scenarios where a process runs as a low-privileged host user, developer workstations, and CI/CD build runners. Any environment where untrusted or semi-trusted code executes under a non-root account is in scope.

AWS customers running EC2 Linux instances on kernel 6.4+ are affected. AKS clusters on Ubuntu 22.04 and 24.04 nodes are in scope. EKS node groups using AL2023 or Ubuntu need verification against the specific kernel version. The shared responsibility model gives you the OS layer. Patch it.

### Remediation

Check whether your distribution has backported the upstream fix (commit `a6dc643c6931`) and prioritise the update. There is no configuration change or module you can disable to mitigate this one. Patching is the only path.

```bash
# Check your kernel version — anything >= 6.4 is potentially in scope
uname -r

# On Ubuntu/Debian, apply the latest kernel security update
sudo apt-get update && sudo apt-get install --only-upgrade linux-image-$(uname -r)

# Verify the fix commit is present (upstream reference)
# Commit: a6dc643c6931 - "epoll: fix use-after-free in ep_remove()"
sudo dmesg | grep -i "epoll" | tail -20

# On Amazon Linux 2023, use dnf
sudo dnf update kernel -y && sudo reboot

# Detection: hunt for anomalous privilege escalation patterns
# Query your CloudTrail/auditd logs for unexpected root process spawning
ausearch -m execve -ts recent | grep -E "(uid=0|euid=0)" | head -50
```

For detection in AWS environments, ship your instance `auditd` logs to CloudWatch Logs and alert on unexpected `setuid` execution or rapid UID changes. AWS Security Hub combined with Amazon Inspector will surface unpatched kernel versions across your EC2 fleet.

<!-- INTERNAL_LINK: AWS Security Hub configuration guide | aws-security-hub-guide -->

### GDPR and UK regulatory angle

GDPR Article 32 requires organisations to implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk. A known, unpatched kernel vulnerability that allows root access fails that standard categorically. A successful exploit of CVE-2026-46242 in a production environment grants an attacker unrestricted access to everything processed on that system, including personal data subject to GDPR protections. UK organisations subject to UK GDPR post-Brexit face the same obligation. FCA-regulated firms should treat unpatched systems processing customer data as a material control failure.

---

## CVE-2026-14355 — PHP OpenSSL AES-WRAP-PAD buffer overflow

Less headline-grabbing than Bad Epoll, but potentially more relevant to cloud application teams running PHP on Lambda, Elastic Beanstalk, App Service, or containerised workloads.

### What it is

CVE-2026-14355 affects PHP versions 8.2.x before 8.2.32, 8.3.x before 8.3.32, 8.4.x before 8.4.23, and 8.5.x before 8.5.8. The AES-WRAP-PAD algorithm implementation in the OpenSSL extension contains a buffer allocation flaw. The output buffer for the AES key-wrap-with-padding operation is sized from the plaintext length without accounting for RFC 5649 expansion. This causes OpenSSL to write beyond allocated memory, corrupting heap metadata and triggering application abort.

The CVSS score is 5.6 (Medium), which might tempt teams to defer it. That would be a mistake. Heap corruption in a cryptographic code path has a history of being escalated through further research into something considerably worse, and the fix is trivially applied.

### Cloud-specific impact

Any PHP application using `openssl_encrypt()` with `AES-WRAP-PAD` mode is in scope. In cloud contexts that includes:

- AWS Lambda PHP runtimes (Bref, custom runtime layers)
- AWS Elastic Beanstalk PHP platform environments
- Containerised PHP on ECS, EKS, or GKE
- Azure App Service PHP stacks

The exploitability is conditional on an attacker being able to influence the plaintext fed to the key-wrap operation. In multi-tenant SaaS applications, or anywhere user input touches cryptographic operations, that bar is lower than it might appear.

### Remediation

Upgrade PHP to 8.2.32, 8.3.32, 8.4.23, or 8.5.8 depending on your branch. For containerised workloads, rebuild your base images and redeploy. For Lambda layers, update the Bref layer or your custom runtime.

```bash
# Check current PHP version in any Linux environment
php -v

# Check specifically for the vulnerable OpenSSL extension
php -r "echo openssl_get_md_methods() ? 'OpenSSL loaded' : 'No OpenSSL';"

# For Bref Lambda layers, pin to a patched version in serverless.yml
# layers:
#   - ${bref:layer.php-84}   # Ensure >= 8.4.23 equivalent layer

# Docker: rebuild with pinned patched version
# FROM php:8.3.32-fpm-alpine
# Rebuild and push to ECR
docker build --no-cache -t myapp:8.3.32 .
aws ecr get-login-password --region eu-west-2 | \
  docker login --username AWS --password-stdin \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com
docker tag myapp:8.3.32 \
  123456789012.dkr.ecr.eu-west-2.amazonaws.com/myapp:8.3.32
docker push 123456789012.dkr.ecr.eu-west-2.amazonaws.com/myapp:8.3.32
```

Amazon Inspector detects outdated PHP versions in EC2 instances and ECR container images natively. Enable it and make sure it is scanning your ECR repositories. It catches exactly this class of issue, and it is free for the first 15 days on a new account.

---

## CVE-2026-32193 — Azure Kubernetes Service container escape (RCE, CVSS 8.8)

For teams running AKS, this one warrants immediate attention. It was patched in Microsoft's June 2026 Patch Tuesday cycle but deserves examination given the scope change it enables.

### What it is

CVE-2026-32193 is a critical RCE vulnerability in Azure Kubernetes Service with a CVSS score of 8.8. A path traversal flaw (CWE-22) allows a low-privileged local attacker to execute code with no user interaction and low attack complexity. An attacker running an untrusted container configured with `hostNetwork` can send crafted requests to a host-level service not intended for unauthenticated access, break out of the container, and gain control of the AKS worker node. Successful exploitation has a changed scope, meaning impact can extend beyond the container to resources managed by a different security authority.

The attack vector is `hostNetwork: true`. If your Kubernetes workloads, including third-party Helm charts you may have deployed without scrutinising the pod spec, use host networking, an attacker with container execution can reach host-level services and escalate.

### Remediation and mitigation

Upgrade your AKS node image to the patched version and apply the node image upgrade to all node pools.

Beyond patching, enforce a Pod Security Admission policy that prohibits `hostNetwork: true` for anything except explicitly approved system workloads. This is a compensating control that blocks the attack vector even before patching is complete.

```yaml
# PodSecurity admission — enforce 'restricted' at namespace level
# Apply to workload namespaces to block hostNetwork
apiVersion: v1
kind: Namespace
metadata:
  name: production-workloads
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
---
# Kyverno policy: deny hostNetwork in non-system namespaces
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: deny-host-network
spec:
  validationFailureAction: Enforce
  rules:
    - name: deny-host-network
      match:
        resources:
          kinds:
            - Pod
      exclude:
        resources:
          namespaces:
            - kube-system
            - azure-arc
      validate:
        message: "hostNetwork is not allowed for non-system workloads."
        pattern:
          spec:
            =(hostNetwork): "false"
```

<!-- INTERNAL_LINK: Kubernetes security best practices | kubernetes-security-best-practices -->

---

## Common mistakes teams make with CVE triage

### 1. Treating CVSS score as the only triage signal

With 131 new CVEs per day, CVSS-only triage does not hold up. The score does not reflect exploitability in your environment, how exposed the asset is, or how critical it is to your business. CVE-2026-14355 scores 5.6 but sits in your cryptographic stack. CVE-2026-46242 scores 7.8 but has a 99%-reliable public exploit already circulating. CVSS does not tell you either of those things adequately.

Use EPSS scores alongside CVSS. Check the CISA KEV catalogue first. A CVE in KEV is not theoretical -- it is being used against organisations right now.

### 2. Assuming your cloud provider has patched everything

The shared responsibility model catches teams out here repeatedly. Managed services like RDS or Lambda runtimes are patched by AWS. Your EC2 instances, ECS task containers, and EKS node images are your responsibility. For AKS Automatic, updates happen with less customer intervention because the cluster follows managed upgrade behaviour. For AKS Standard, you need to monitor and apply upgrades yourself. The same split applies across AWS managed versus self-managed Kubernetes.

### 3. Ignoring the patch-to-deployment gap

The Bad Epoll fix landed in the kernel mainline on 24 April, but many distributions had not shipped backports when the public writeup dropped 70 days later. Upstream patches do not automatically update your AMI, container base image, or node pool VHD. Automate image rebuilds on upstream patch availability, not on your quarterly release cadence.

### 4. Not scanning ECR and container images

Teams that scan their EC2 estate but ignore their container image registry are working with incomplete visibility. Amazon Inspector supports ECR scanning natively. Enable it. A vulnerable PHP version in a container is just as dangerous as on a bare instance. The frequency of container restarts does not equate to automatic patching.

<!-- INTERNAL_LINK: AWS IAM security best practices | aws-iam-security-best-practices -->

### 5. Conflating "no evidence of exploitation" with "low risk"

As of this writing, Bad Epoll is not on CISA's Known Exploited Vulnerabilities list and the only working code is the kernelCTF proof of concept. That status will change. The exploit code is public, reliable, and the technique is well understood. "Not yet in KEV" means you have a narrow window, not permanent safety.

### 6. Treating AI-assisted scanning as a complete safety net

The Bad Epoll story is instructive here. The flaw was found in the same stretch of kernel code where Anthropic's Mythos model recently found a different bug. The AI caught one flaw and missed this one. AI-assisted tooling is a force multiplier. It is not a substitute for defence-in-depth or human review.

<!-- INTERNAL_LINK: AI and LLM security guide | beginners-guide-ai-llm-security -->

---

## Key takeaways

CVE-2026-46242 (Bad Epoll) is a Linux kernel privilege escalation with a 99%-reliable public exploit affecting kernel 6.4+. There is no workaround. Patch your EC2 instances, EKS/AKS node pools, and container base images now. Apply upstream commit `a6dc643c6931` or wait for your distribution's backport, then verify.

CVE-2026-14355 is a Medium-severity PHP OpenSSL heap corruption bug affecting all active PHP 8.x branches before their respective July 2026 releases. Upgrade PHP across Lambda layers, container images, and Elastic Beanstalk environments. Enable Amazon Inspector ECR scanning to catch it automatically going forward.

CVE-2026-32193 is a critical AKS container escape with CVSS 8.8. Upgrade your AKS node images and enforce PodSecurity admission policies that prohibit `hostNetwork: true` in workload namespaces. The policy is a compensating control that blocks the attack vector even before patching is complete.

CVSS scores alone are an inadequate triage mechanism. Layer in EPSS scores, CISA KEV status, and your own asset-criticality data. A Medium-CVSS CVE in your cryptographic stack matters more than a High in a service you do not deploy.

The shared responsibility split is not static. Re-audit what is your responsibility versus your cloud provider's after every major CVE disclosure, particularly for managed Kubernetes, container runtimes, and serverless execution environments.

Build towards automated detection rather than reactive patching. Ship `auditd` logs to CloudWatch, enable Amazon Inspector across EC2 and ECR, and configure AWS Security Hub to surface unpatched findings automatically. With the median time to exploit under five days, your change management process cannot be the bottleneck.

<!-- INTERNAL_LINK: cloud incident response playbook | cloud-incident-response -->
<!-- INTERNAL_LINK: AWS CloudTrail configuration | aws-cloudtrail-configuration-best-practices -->
<!-- INTERNAL_LINK: what is CSPM | what-is-cspm-cloud-security-posture-management -->