+++
title = "Kubernetes Security Best Practices"
date = "2026-06-08T09:29:27Z"
slug = "kubernetes-security-best-practices"
description = "Defence-in-depth Kubernetes security for EKS, GKE, and AKS: RBAC hardening, network policies, pod security standards, secrets management, and runtime image scanning aligned with CKS exam domains."
keywords = ["Kubernetes", "K8s security", "container security", "RBAC", "CKS"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

Securing Kubernetes requires a defence-in-depth approach across the control plane, workload configuration, and runtime environment. The most impactful controls are RBAC hardening, network policy enforcement, pod security standards, proper secrets management, and continuous image scanning — the same domains tested in the CKS exam and exploited most frequently in real-world incidents. This guide covers each layer with practical guidance for teams running managed clusters on EKS, GKE, or AKS.

---

## RBAC: Least Privilege at the API Layer

Role-Based Access Control is the primary authorisation mechanism in Kubernetes, and misconfigured RBAC remains one of the most common paths to cluster compromise. The default service account token mounted into every pod, combined with overly permissive ClusterRoleBindings, gives attackers a trivial lateral movement vector.

**What to audit immediately:**

- Run `kubectl get clusterrolebindings -o wide` and identify anything bound to `system:anonymous` or `system:unauthenticated`
- Look for subjects with `cluster-admin` that aren't break-glass service accounts
- Use tools like [rbac-police](https://github.com/PaloAltoNetworks/rbac-police) or Fairwinds Insights to map effective permissions

**Hardening principles:**

- Create scoped Roles (namespace-level) rather than ClusterRoles wherever possible
- Disable automounting of service account tokens with `automountServiceAccountToken: false` in the pod spec unless the workload explicitly requires API access
- Use Workload Identity (GKE), IAM Roles for Service Accounts (EKS), or Azure Workload Identity (AKS) instead of long-lived credentials in secrets
- Never grant `get`/`list`/`watch` on secrets cluster-wide — this is equivalent to reading every password in the cluster

K8s security testing should include impersonating service accounts with `kubectl auth can-i --as=system:serviceaccount:default:myapp --list` to validate least privilege before deploying to production.

---

## Network Policies: Zero Trust Between Pods

By default, Kubernetes allows all pod-to-pod communication across namespaces. Without network policies, a compromised workload can freely reach databases, the metadata API, or internal microservices.

Network policies are enforced by the CNI plugin, not Kubernetes itself — so you need a policy-aware CNI. Cilium and Calico are the most capable options. AWS VPC CNI supports basic network policies from EKS 1.25+ with the `--enable-network-policy` flag, but Cilium provides far richer L7 controls and observability.

**Practical baseline:**

Start with a default-deny policy in every namespace:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

Then layer explicit allow rules per service. Egress policies are frequently overlooked — without them, a compromised pod can exfiltrate data or reach a C2 server via the internet.

For teams on GKE, Dataplane V2 (powered by Cilium eBPF) provides network policy logging and FQDN-based egress filtering without deploying a separate CNI. On AKS, Azure CNI with Calico is the recommended combination.

---

## Pod Security Standards: Removing Host-Level Access

The Pod Security Admission (PSA) controller, stable since Kubernetes 1.25, replaces the deprecated PodSecurityPolicy. It enforces one of three built-in profiles — `privileged`, `baseline`, or `restricted` — at the namespace level using labels.

The `restricted` profile enforces:

- Non-root user and group
- Read-only root filesystem (recommended, not required)
- Dropped all capabilities, optionally add specific ones back
- No privilege escalation
- Seccomp profile set to `RuntimeDefault` or `Localhost`

Apply it:

```bash
kubectl label namespace production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=latest
```

For brownfield clusters, use `warn` and `audit` modes first to surface violations without blocking deployments. GKE Autopilot enforces `restricted` by default, which is worth factoring into architectural decisions.

OPA/Gatekeeper or Kyverno can extend this further with custom policies — for example, enforcing that all images come from a specific registry, or that resource limits are always set.

---

## Secrets Management: Don't Store Secrets in etcd

Kubernetes Secrets are base64-encoded, not encrypted, by default in etcd. Anyone with read access to etcd — or an overly permissive RBAC role — can retrieve plaintext credentials.

**Encryption at rest** is table stakes. On managed platforms this is typically enabled by default (GKE, AKS) but verify it. On EKS, configure envelope encryption with a KMS key at cluster creation:

```bash
aws eks create-cluster \
  --encryption-config '[{"resources":["secrets"],"provider":{"keyArn":"arn:aws:kms:..."}}]'
```

**External secrets are better than native secrets for sensitive material.** The External Secrets Operator (ESO) syncs secrets from AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager into Kubernetes Secrets while keeping the source of truth outside the cluster. This means secret rotation happens in one place, and audit trails are cleaner.

For the most sensitive credentials, consider using the Secrets Store CSI Driver to mount secrets directly as volumes from the vault, bypassing Kubernetes Secrets entirely. Combined with Workload Identity, no persistent credential touches the cluster.

**Never commit Kubernetes manifests with Secret values to Git** — use Sealed Secrets, SOPS, or ESO alongside GitOps pipelines to manage this safely.

---

## Image Security: Shift Left and Enforce at Admission

Container security starts before runtime. A secure base image and a clean build pipeline prevent entire classes of vulnerability.

**Build-time:**

- Use distroless or minimal base images (Google distroless, Chainguard images) to reduce attack surface
- Pin image digests (`image@sha256:...`) in production manifests rather than mutable tags
- Scan images in CI with Trivy, Grype, or Snyk — fail builds on critical CVEs

**Admission-time enforcement:**

Use an admission controller to prevent unsigned or unscanned images from reaching the cluster. Cosign with Sigstore enables keyless signing in CI. Policy engines like Kyverno can verify signatures at admission:

```yaml
verifyImages:
  - imageReferences: ["registry.example.com/*"]
    attestors:
      - entries:
          - keyless:
              issuer: "https://accounts.google.com"
              subject: "ci@project.iam.gserviceaccount.com"
```

On GKE, Binary Authorization provides a managed equivalent with audit and enforcement modes. AKS supports similar controls via Azure Policy and Defender for Containers.

---

## Runtime Security: Detect What Slips Through

Even with everything above in place, assume breach. Runtime security tooling monitors for anomalous behaviour inside running containers — unexpected processes, suspicious syscalls, file writes to sensitive paths.

**Falco** is the de facto open-source runtime security tool for Kubernetes. It uses eBPF or a kernel module to detect threats based on configurable rules — for example, alerting when a shell is spawned inside a container or when credentials are read from `/proc`. Deploy it as a DaemonSet and route alerts to your SIEM.

Commercial options like Aqua Security, Sysdig Secure, and Prisma Cloud provide richer policy management, compliance reporting, and deeper integrations with managed cluster platforms.

**Audit logging** at the API server level is equally critical. Enable audit logs on all managed clusters and forward them to a centralised SIEM. Look for:

- `exec` into pods (legitimate debugging or active intrusion?)
- Secrets access outside expected service accounts
- ClusterRoleBinding creation events

---

## What Architects Should Do: Practical Checklist

- **Enable PSA restricted mode** on all non-system namespaces; use warn/audit first in existing clusters
- **Audit RBAC** quarterly; automate detection of over-privileged bindings with rbac-police or OPA
- **Deploy default-deny NetworkPolicies** in all namespaces as a baseline; use Cilium for L7 visibility
- **Use External Secrets Operator or CSI driver** rather than native secrets for any credential that rotates or is shared
- **Enable KMS envelope encryption** for etcd on all clusters where you control the option
- **Scan images in CI and enforce signatures** at admission with Kyverno or Binary Authorization
- **Run Falco** as a DaemonSet and integrate with your SOC alerting pipeline
- **Forward API audit logs** to your SIEM and define detection rules for privileged escalation paths
- **Pin image digests** in production Helm values and automate digest updates via Renovate or Dependabot

---

## Key Takeaways

Kubernetes security is not a single control — it's a stack of overlapping defences that collectively reduce blast radius at each layer. RBAC and pod security standards address configuration risk; network policies limit lateral movement; proper secrets management protects credentials even if the cluster is breached; image scanning and admission control stop vulnerable workloads reaching production; and runtime tooling catches what everything else misses. For teams preparing for the CKS exam, this maps directly to the exam domains — but more importantly, each of these controls addresses a real attack vector seen in production incidents. Managed platforms like EKS, GKE, and AKS handle some of this by default, but never all of it: responsibility for RBAC, network policy, and runtime detection remains firmly with the platform team.


## Related Guides

- [Zero Trust Architecture](/guides/what-is-zero-trust-architecture/) — Kubernetes is one of the most complex environments in which to implement Zero Trust. This guide explains the principles; the Kubernetes guide explains the practice.
- [AWS IAM Security Best Practices](/guides/aws-iam-security-best-practices/) — IAM Roles for Service Accounts (IRSA) and EKS Pod Identity connect AWS IAM controls directly into Kubernetes workload security.
- [Cloud Security Posture Management (CSPM)](/guides/what-is-cspm-cloud-security-posture-management/) — CSPM tools with Kubernetes support continuously assess cluster configuration against CIS benchmarks and cloud provider best practices.
- [Cloud Infrastructure Entitlement Management (CIEM)](/guides/what-is-ciem-cloud-infrastructure-entitlement-management/) — Kubernetes RBAC and service account entitlements are a growing focus for CIEM tooling.
- [Securing AI Agents in Cloud Infrastructure](/guides/securing-ai-agents-cloud-infrastructure/) — AI agents increasingly run as containerised workloads in Kubernetes. The security controls in this guide apply directly to agentic deployments.
- [Cross-Cloud Security Services Comparison](/guides/aws-azure-gcp-security-service-comparison/) — Compare AKS, EKS, and GKE security capabilities including built-in admission controllers, network policy, and workload identity.
