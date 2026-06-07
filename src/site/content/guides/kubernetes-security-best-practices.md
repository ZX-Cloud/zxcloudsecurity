+++
title = "Kubernetes Security Best Practices"
date = "2026-06-07T13:52:17Z"
slug = "kubernetes-security-best-practices"
description = "Kubernetes Security Best Practices — a practical guide for cloud security architects."
keywords = ["Kubernetes", "K8s security", "container security", "RBAC", "CKS"]
type = "guides"
draft = false
+++

Securing Kubernetes requires a defence-in-depth approach across identity, network, workload, and supply chain layers. The core controls — RBAC, network policies, pod security standards, secrets management, image scanning, and runtime monitoring — map directly to what the CKS exam tests and what production EKS, GKE, and AKS clusters demand. Get these right, and you substantially reduce your blast radius when something inevitably goes wrong.

---

## RBAC: Least Privilege Is Non-Negotiable

Role-Based Access Control is the cornerstone of K8s security, yet misconfigured RBAC remains one of the most exploited attack vectors in real-world Kubernetes breaches. The problem is usually over-permissive bindings — `cluster-admin` handed to service accounts that only need to read ConfigMaps, or wildcard verb grants on sensitive resources.

**What to tighten:**

- Audit all `ClusterRoleBindings` and `RoleBindings` regularly. Tools like `kubectl-who-can` and Fairwinds Insights make this tractable at scale.
- Never bind `cluster-admin` to user-facing service accounts. If a workload needs cross-namespace access, scope it precisely with a `ClusterRole` limited to the exact resources and verbs required.
- Avoid `*` (wildcard) verbs or resources in roles. Be explicit: `get`, `list`, `watch` for read-only consumers.
- Use separate service accounts per workload. The default service account in every namespace should have no bound roles — add an explicit `automountServiceAccountToken: false` to the namespace's default service account.
- On EKS, map IAM roles to K8s RBAC groups via the `aws-auth` ConfigMap (or the newer access entries API), keeping the IAM boundary and the K8s RBAC boundary aligned.

---

## Network Policies: Zero Trust Within the Cluster

By default, all pods in a Kubernetes cluster can communicate with all other pods across all namespaces. This is a flat network model that should never reach production.

NetworkPolicy objects enforce ingress and egress rules at the pod level, but they require a CNI plugin that actually implements the spec — Calico, Cilium, and Weave Net do; the default VPC CNI on EKS does not enforce policies alone without the Calico add-on or switching to Cilium.

**Practical implementation:**

- Start with a default-deny posture per namespace. Apply a NetworkPolicy that selects all pods and denies all ingress and egress, then explicitly allow only what's needed.
- Use namespace selectors with labels (`namespaceSelector: matchLabels: team: payments`) rather than relying solely on pod selectors, so policies remain meaningful as namespaces scale.
- On GKE, enable Dataplane V2 (based on Cilium/eBPF) to get native NetworkPolicy enforcement plus deeper visibility. On AKS, Azure CNI with Calico or Azure Network Policy is the supported path.
- Enforce egress restrictions to external endpoints — many breaches involve compromised workloads exfiltrating data to attacker-controlled infrastructure. Limit egress by IP block or FQDN (Cilium supports FQDN-based egress policies natively).

---

## Pod Security Standards: Replacing PodSecurityPolicy

PodSecurityPolicy was deprecated in Kubernetes 1.21 and removed in 1.25. Its replacement, Pod Security Standards (PSS), operates via the Pod Security Admission controller and defines three policy levels: `privileged`, `baseline`, and `restricted`.

For production workloads, `restricted` is the target. It enforces:

- No privilege escalation (`allowPrivilegeEscalation: false`)
- Non-root user enforcement (`runAsNonRoot: true`)
- Dropping all Linux capabilities (`capabilities: drop: [ALL]`)
- Seccomp profile set to `RuntimeDefault` or `Localhost`
- No host namespace sharing (hostPID, hostIPC, hostNetwork all false)
- Read-only root filesystems where feasible

Apply PSS via namespace labels:

```yaml
labels:
  pod-security.kubernetes.io/enforce: restricted
  pod-security.kubernetes.io/enforce-version: latest
  pod-security.kubernetes.io/warn: restricted
  pod-security.kubernetes.io/audit: restricted
```

Use `warn` and `audit` labels in lower environments before enforcing in production — they surface violations without blocking deployments, giving teams time to remediate.

On managed platforms, EKS supports PSS natively from 1.25+. GKE Autopilot enforces `restricted` by default. AKS supports PSS from 1.25 and offers Azure Policy integration to enforce it at the admission layer.

---

## Secrets Management: Don't Store Secrets in etcd in Plaintext

By default, Kubernetes Secrets are base64-encoded — not encrypted — in etcd. Any attacker with etcd access (or a backup) gets your credentials in seconds.

**Mitigations:**

- Enable encryption at rest for etcd using an `EncryptionConfiguration` with an AES-GCM or KMS provider. All managed platforms support envelope encryption backed by their respective KMS services: AWS KMS for EKS, Cloud KMS for GKE, Azure Key Vault for AKS.
- Use external secrets operators to fetch secrets from your cloud KMS or secrets manager at runtime: External Secrets Operator (ESO) with AWS Secrets Manager/Parameter Store, GCP Secret Manager, or Azure Key Vault is the de facto pattern.
- Restrict `get` and `list` on the `secrets` resource in RBAC. Many operators grant broad Secret access unnecessarily — audit this specifically.
- Avoid mounting Secrets as environment variables where possible; use volume mounts so secrets aren't exposed in process inspection tools. Better still, use the Secrets Store CSI Driver to mount external secrets directly.

---

## Image Scanning and Supply Chain Security

Container security starts before the container runs. A runtime compromise often exploits a vulnerable package baked into the image at build time.

- Integrate image scanning into CI pipelines using Trivy, Grype, or Snyk Container. Fail builds on critical/high CVEs with known fixes — don't fail on everything or engineers will start ignoring alerts.
- Use signed images and enforce signature verification at admission time. Sigstore/Cosign is the emerging standard; pair it with a policy engine (OPA Gatekeeper or Kyverno) to reject unsigned images from untrusted registries.
- Restrict image registries via admission policy — workloads should only pull from your internal registry or approved public registries, never arbitrary Docker Hub images.
- Use distroless or minimal base images (Google Distroless, Chainguard Images) to reduce attack surface. Fewer packages mean fewer CVEs and less to scan.
- Implement a Software Bill of Materials (SBOM) process — generate SBOMs at build time and store them alongside images for compliance and incident response.

---

## Runtime Security: Detect What You Can't Prevent

Even with every preventive control in place, assuming breach is sound security architecture. Runtime security gives you visibility into what's actually happening inside your containers.

Falco is the dominant open-source tool here. It uses eBPF or kernel module hooks to detect anomalous syscalls — a shell spawning inside a container, outbound connections to unexpected IPs, `/etc/passwd` being read. Deploy Falco as a DaemonSet and route alerts to your SIEM.

Managed equivalents: AWS GuardDuty has EKS Runtime Monitoring (eBPF-based agent). Microsoft Defender for Containers provides runtime threat detection on AKS. GKE has Container Threat Detection built into Security Command Center.

Enable audit logging for the Kubernetes API server and ship those logs to your SIEM. API server audit logs capture every API call — who did what, when — and are invaluable for incident response.

---

## What Architects Should Do

- **Audit RBAC quarterly** using `kubectl-who-can` and automated policy-as-code checks in your CI pipeline (OPA Gatekeeper or Kyverno policies as tests).
- **Enforce PSS `restricted`** on all application namespaces; use `baseline` only for specific infrastructure workloads with documented exceptions.
- **Enable envelope encryption** for etcd Secrets on day one — retrofitting it later causes etcd rewrites that can destabilise clusters.
- **Deploy External Secrets Operator** and migrate away from native K8s Secrets for any credentials, API keys, or certificates within the first sprint.
- **Require signed images** in production environments and maintain a registry allowlist enforced by admission control.
- **Deploy Falco or the managed runtime detection equivalent** for your platform, and ensure alerts are actionable (tuned to reduce noise) and routed to your SOC.
- **Run CIS Kubernetes Benchmark** via kube-bench on node bootstrapping and in periodic compliance checks.

---

## Key Takeaways

- RBAC misconfigurations and overly permissive pod specs are the most commonly exploited Kubernetes weaknesses — fix these first.
- Network policies should default-deny; most production clusters run years without them, creating a flat internal network that aids lateral movement.
- Native K8s Secrets are not encrypted at rest by default — envelope encryption with your cloud KMS is table stakes on managed platforms.
- Runtime detection with Falco or a managed equivalent is essential for threat detection that preventive controls alone cannot provide.
- The CKS exam covers all of these domains for good reason: they represent the genuine attack surface of production Kubernetes clusters.
