+++
title = "Kubernetes Security Best Practices"
date = "2026-06-07T14:22:17Z"
slug = "kubernetes-security-best-practices"
description = "Kubernetes Security Best Practices — a practical guide for cloud security architects."
keywords = ["Kubernetes", "K8s security", "container security", "RBAC", "CKS"]
draft = false
+++

Securing Kubernetes requires a defence-in-depth approach spanning identity and access control, network segmentation, workload hardening, secrets hygiene, and runtime threat detection. A single misconfigured admission webhook or overly permissive ClusterRole can expose your entire cluster. The guidance below reflects current best practice for production clusters on EKS, GKE, and AKS, and maps closely to the CNCF Certified Kubernetes Security Specialist (CKS) curriculum.

---

## RBAC: Least Privilege at Every Layer

Role-Based Access Control is the cornerstone of K8s security, yet it remains one of the most commonly misconfigured areas in enterprise clusters. The default service account in every namespace has token auto-mounting enabled — a foothold that lateral movement exploits routinely abuse.

**Key principles:**

- Never bind `cluster-admin` to user identities or service accounts outside break-glass scenarios. Audit existing ClusterRoleBindings with `kubectl get clusterrolebindings -o json | jq '.items[] | select(.subjects[]?.name=="system:unauthenticated")'`.
- Prefer Roles scoped to a namespace over ClusterRoles wherever possible.
- Disable automatic service account token mounting with `automountServiceAccountToken: false` in pod specs and ServiceAccount manifests unless the pod genuinely needs API server access.
- Use projected service account tokens (OIDC-based, audience-scoped, time-limited) rather than long-lived static tokens. EKS IRSA, GKE Workload Identity, and AKS Workload Identity all provide cloud-native implementations.
- Regularly audit RBAC with tools such as `rbac-tool`, `kubectl-who-can`, or the open-source Polaris dashboard to surface wildcard verbs (`*`), access to `secrets` resources, and `exec` or `portforward` permissions.

On managed services, integrate your cloud IAM with Kubernetes RBAC. On EKS, `aws-auth` ConfigMap (now superseded by EKS Access Entries in newer clusters) maps IAM roles to Kubernetes groups. Misconfigured mappings are a frequent source of privilege escalation.

---

## Network Policies: Zero-Trust Inside the Cluster

By default, Kubernetes allows unrestricted pod-to-pod communication across namespaces. Implementing NetworkPolicy resources enforces zero-trust micro-segmentation at layer 3/4.

Start with a default-deny baseline in every namespace:

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

Then layer explicit allow rules for known traffic flows. Ensure your CNI plugin actually enforces NetworkPolicy — vanilla kubenet on AKS does not. Use Calico, Cilium, or Azure NPM. Cilium's eBPF-based enforcement extends policies to layer 7 (HTTP methods, DNS FQDNs), which is significantly more expressive than standard NetworkPolicy for controlling egress to external APIs.

For EKS, consider Amazon VPC CNI with Network Policy support (GA since 2023), which provides native VPC-level enforcement. On GKE, Dataplane V2 (Cilium-based) is the recommended path for policy enforcement.

---

## Pod Security Standards: Replacing PSPs

Pod Security Policies were deprecated in Kubernetes 1.21 and removed in 1.25. The replacement is Pod Security Standards (PSS), enforced via the built-in Pod Security Admission controller.

Three profiles are defined: `privileged`, `baseline`, and `restricted`. In practice:

- Label namespaces to enforce `restricted` for all application workloads: `pod-security.kubernetes.io/enforce: restricted`
- Use `warn` and `audit` modes during migration to identify violations without breaking deployments.
- The `restricted` profile prohibits privilege escalation, requires non-root users, drops all Linux capabilities, and mandates a read-only root filesystem.

For more granular policy, consider OPA/Gatekeeper or Kyverno. Kyverno is particularly popular on managed services due to its Kubernetes-native policy language and mutating admission capabilities — for example, automatically injecting `securityContext` defaults or stripping `hostPath` volumes.

---

## Secrets Management: Don't Trust etcd Alone

Kubernetes Secrets are base64-encoded by default, not encrypted. Etcd at-rest encryption should be enabled on self-managed clusters, but even then it relies on a locally managed key. The robust approach uses an external KMS provider.

- **EKS**: Enable envelope encryption with AWS KMS. Configure via `--encryption-provider-config` or through the EKS console/API at cluster creation.
- **GKE**: Application-layer secrets encryption with Cloud KMS is available on all cluster tiers.
- **AKS**: Etcd encryption with Azure Key Vault-managed keys using the KMS plugin.

Beyond etcd encryption, prefer externalising secrets entirely using the Secrets Store CSI Driver with provider plugins for AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager. This mounts secrets as ephemeral volumes and supports automatic rotation without redeploying pods.

Avoid injecting secrets as environment variables where possible — they are visible in `kubectl describe pod` output and process listings. Volume mounts reduce exposure surface.

---

## Image Security: Shifting Left and Enforcing at Admission

Container security begins in CI/CD, not at runtime. Integrate image scanning into your pipeline using Trivy, Grype, or managed services like AWS Inspector (ECR), GCP Artifact Analysis, or Microsoft Defender for Containers.

Enforce image policies at admission:

- Use admission webhooks (via Kyverno or Gatekeeper) to block images not pulled from approved registries or lacking a valid cosign signature.
- Implement image signing with Sigstore/cosign and enforce signature verification using policy engines. GKE Binary Authorization and AWS Signer provide managed signing workflows.
- Set `imagePullPolicy: Always` for mutable tags (though preferring immutable digests — `image: myapp@sha256:abc123` — is the correct long-term approach).
- Minimise base image attack surface: use distroless or scratch-based images. An image without a shell eliminates an entire class of post-exploitation techniques.

---

## Runtime Security: Detecting Threats in Running Workloads

Static policies and pre-deployment scanning cannot catch everything. Runtime security monitors syscall behaviour and detects anomalies indicative of exploitation, cryptomining, or data exfiltration.

**Falco** is the de facto standard for Kubernetes runtime security. It uses eBPF or a kernel module to capture syscall events and evaluate them against rules. Default rules flag shell spawning inside containers, sensitive file reads (`/etc/shadow`, `/proc/*/mem`), unexpected outbound connections, and privilege escalation attempts.

Deploy Falco as a DaemonSet, ship alerts to your SIEM (Elastic, Splunk, or a managed service like Amazon Security Lake), and integrate with incident response workflows via Falcosidekick.

Managed equivalents include GKE Threat Detection, Microsoft Defender for Containers, and Amazon GuardDuty for EKS (which analyses EKS audit logs and runtime agent telemetry).

Complement Falco with audit log analysis. Kubernetes audit logs capture every API server interaction — ensure they are enabled with an appropriate policy, shipped off-cluster immediately, and monitored for patterns such as anonymous requests, high-frequency secret reads, or `exec` into pods.

---

## What Architects Should Do: Practical Checklist

- **RBAC**: Enumerate and remediate wildcard ClusterRoles; disable service account token auto-mounting cluster-wide; implement cloud Workload Identity for pod IAM.
- **Network policies**: Deploy default-deny in all namespaces; validate CNI enforces policies; consider Cilium for L7 visibility.
- **Pod security**: Enforce `restricted` PSS on application namespaces; deploy Kyverno for mutation and additional custom policies.
- **Secrets**: Enable KMS envelope encryption or use Secrets Store CSI; avoid environment variable injection for sensitive values.
- **Images**: Scan in CI with Trivy; enforce registry allowlisting and cosign verification at admission; pin to immutable digests.
- **Runtime**: Deploy Falco with eBPF driver; enable Kubernetes audit logging; integrate with your SIEM and alerting pipelines.
- **CKS preparation**: The exam tests hands-on cluster hardening — practice with `kubeadm` clusters and work through scenarios involving audit policy configuration, AppArmor/Seccomp profiles, and Falco rule writing.

---

## Key Takeaways

Kubernetes security is not a product you buy — it is a series of deliberate controls applied at every layer of the stack. RBAC and network policies limit blast radius; pod security standards and admission controllers prevent misconfigured workloads reaching production; secrets management protects credentials at rest and in use; image scanning and signing enforce supply chain integrity; and runtime security provides the detection capability when preventive controls fail. Managed services like EKS, GKE, and AKS reduce operational overhead for many of these controls, but the architectural decisions — least privilege, default-deny, zero-trust — remain your responsibility regardless of where the cluster runs.
