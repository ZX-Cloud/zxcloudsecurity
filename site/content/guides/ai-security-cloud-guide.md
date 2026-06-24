+++
title = "AI Security in the Cloud: A Practitioner's Guide"
date = "2026-06-24T07:00:00Z"
slug = "ai-security-cloud-guide"
description = "AI security for cloud architects: the threat model for LLMs, AI agents, and ML pipelines — prompt injection, data exfiltration, model abuse, and the controls that defend against them."
keywords = ["AI security", "LLM security", "AI cloud security", "prompt injection", "AI agents security", "machine learning security", "AWS Bedrock security", "generative AI security"]
type = "guides"
draft = false
author = "Steve Harrison, Principal Security Architect"
+++

AI systems running in cloud environments introduce a threat model that most security teams are not yet equipped to handle. The underlying risk is not that AI is inherently dangerous — it is that AI components are being wired into cloud infrastructure with the same access patterns as any other service, without the same scrutiny applied to the novel attack surfaces they introduce. An LLM with access to a database, a file system, or a set of API credentials is a new kind of principal with new kinds of attack vectors. Security architects who understand cloud IAM, network controls, and vulnerability management need to extend that understanding to cover AI-specific threats before organisations learn about them the hard way.

This guide covers the AI threat model relevant to cloud environments, the attack categories that matter in practice, the security controls available today, and how to architect AI workloads defensibly.

---

## Why AI Changes the Cloud Threat Model

Traditional cloud workloads operate deterministically. Given the same input, a well-written application produces the same output and makes the same API calls. Security controls — IAM policies, network rules, secret management, input validation — are designed around this predictability.

AI systems, and large language models in particular, are non-deterministic. Their behaviour depends on the content of their inputs, their context window, the instructions in their system prompt, and the outputs of previous reasoning steps. This non-determinism has direct security implications:

- An LLM processing user-controlled input can be manipulated into ignoring its system prompt, extracting sensitive context, or taking actions its operator did not intend — without any code change, purely through the content of the input.
- An AI agent with tool access — the ability to call APIs, write files, query databases, browse the web, or invoke other AI systems — can be manipulated into using those tools in ways that cause real damage.
- AI systems trained on datasets can inadvertently encode sensitive information that can be extracted through targeted querying, or can be manipulated if the training data was poisoned.

These are not theoretical risks. Prompt injection attacks against AI agents have been demonstrated repeatedly in research settings and in deployed production systems. As AI components become more capable and more deeply integrated into cloud infrastructure, the security implications become more consequential.

---

## The AI Attack Surface in Cloud Environments

### Large Language Models and Generative AI APIs

Organisations deploying LLMs — whether through AWS Bedrock, Azure OpenAI Service, GCP Vertex AI, or direct API calls to foundation model providers — introduce a new category of externally-queryable endpoint. The attack surface includes:

**Prompt injection** is the AI equivalent of SQL injection: attacker-controlled content in the LLM's input context causes the model to behave contrary to the operator's instructions. Direct prompt injection attacks the system prompt or model configuration. Indirect prompt injection embeds malicious instructions in data the model will process — a document, a web page, a database record, an email — with the expectation that when the model reads that content, it will follow the embedded instructions rather than its original system prompt. Indirect injection is particularly dangerous in agentic systems that autonomously browse the web, process user-provided files, or read from external data sources.

**Sensitive data extraction** occurs when an LLM's training data, context window, or retrieved documents contain sensitive information that can be extracted through carefully crafted queries. Models with retrieval augmented generation (RAG) systems that pull documents from internal knowledge bases are a common source: an attacker who can influence what queries reach the RAG system, or who has access to the LLM interface, may be able to extract documents they should not have access to.

**Model abuse and denial of service** — using AI APIs in ways that incur excessive cost, generate harmful content that violates acceptable use policies, or consume resources that degrade availability for legitimate users — is a relevant concern for systems where the LLM interface is externally accessible.

### AI Agents and Agentic Frameworks

AI agents extend LLM risk significantly. An agent with tool access — function calling, computer use, or integration with external APIs — can take real-world actions: send emails, query databases, write files, make API calls, create cloud resources. If an agent is manipulated into taking unauthorised actions, the damage is real.

The critical security property for AI agents is the **principle of least privilege**, applied to both the tools available to the agent and the actions those tools can perform. An agent that needs to read from a database should not be able to write to it. An agent that needs to query an API should not hold credentials that allow it to delete resources. An agent that processes user-provided content should not be able to make outbound network calls that can exfiltrate data.

**Tool call manipulation** is a specific attack pattern: if an agent invokes tools based on the content of its input or the output of previous reasoning steps, an attacker who can influence that content can attempt to trigger unintended tool calls. Defences include validating tool call parameters independently of the LLM's reasoning, requiring human confirmation for high-impact actions, and logging all tool calls for audit.

### Machine Learning Pipelines

Beyond inference, organisations running ML training pipelines have additional exposure:

**Training data poisoning** introduces malicious examples into a training dataset with the goal of creating backdoored or biased model behaviour in the resulting model. For organisations that fine-tune models on proprietary data, the integrity of that data and the pipeline that processes it is a security property.

**Model theft and extraction** — reconstructing a proprietary model's capabilities through systematic querying — is a concern for organisations where the model represents competitive value.

**Supply chain attacks** on ML dependencies — the Python packages, pre-trained model weights, datasets, and pipeline tooling that ML teams rely on — follow the same patterns as general software supply chain attacks, with the additional risk that malicious behaviour embedded in a model weight file may not be detectable through normal code review.

---

## Cloud AI Platform Security

### AWS Bedrock

Amazon Bedrock provides access to foundation models (Claude, Llama, Titan, Mistral) through a fully managed API within your AWS account. Security controls available:

- **IAM for Bedrock** — `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` permissions control which principals can call which models. Apply resource-based conditions to restrict to specific model ARNs. Avoid granting access to all models where a subset is needed.
- **VPC endpoints** — Bedrock supports VPC endpoints (AWS PrivateLink), keeping API traffic within your network and off the public internet. Use these for any production deployment.
- **AWS CloudTrail** logs all Bedrock API calls, including model invocations, enabling audit of who invoked what model with what parameters. Enable Bedrock data events in CloudTrail if you need per-invocation logging.
- **Guardrails for Amazon Bedrock** — configurable content filters, topic denial policies (preventing the model from discussing specified topics), grounding checks (comparing model responses against source documents to detect hallucination), and sensitive information redaction. Evaluate which guardrails are appropriate for your use case.
- **Knowledge Bases** — when using Bedrock Knowledge Bases for RAG, control access to the underlying data source (typically S3) using S3 bucket policies and IAM, and audit retrieval queries through CloudTrail.

### Azure OpenAI Service

Azure OpenAI integrates with Entra ID for authentication, supports private endpoints, and logs requests through Azure Monitor. Azure AI Content Safety provides content filtering. Azure Managed Identity is the correct authentication mechanism for applications calling Azure OpenAI — no API keys in application code.

Azure AI Studio's prompt flow feature includes built-in evaluation for content safety and groundedness. For production deployments, enable diagnostic settings to route Azure OpenAI logs to a central Log Analytics workspace.

### GCP Vertex AI

Vertex AI integrates with GCP IAM — service accounts with Workload Identity are the correct authentication model for applications invoking models. Vertex AI supports VPC Service Controls, which restrict API access to specified network perimeters. Cloud Audit Logs record all Vertex AI API calls.

---

## Security Controls for AI Workloads

### Input and Output Validation

The LLM is not the last line of defence. Every user input that reaches an LLM should pass through validation:

- Strip or sanitise known prompt injection patterns — explicit instruction overrides (`Ignore all previous instructions`), system prompt override attempts, or role-play framings designed to bypass restrictions
- Validate the structure of LLM outputs before acting on them — if an agent is expected to return a JSON object with a specific schema, validate it; do not execute tool calls based on malformed or unexpected LLM output
- Implement output content filtering, independently of the model's own safeguards, for any external-facing application

These validations should be implemented in code outside the LLM, not delegated to the model itself. Telling the model "always validate your output" does not constitute a security control.

### Least Privilege for AI Principals

Every AI component — an agent, a Bedrock-calling Lambda, a model serving endpoint — is an IAM principal and should be scoped accordingly:

- Grant the minimum Bedrock model permissions needed — specific model ARNs, specific inference actions
- If an agent uses tools, grant the IAM permissions those tools require, and no more — a tool that reads an S3 object needs `s3:GetObject` on that specific prefix, not `s3:*` on `*`
- Do not run AI workloads with administrator-level permissions — the blast radius of a successful prompt injection is bounded by the IAM permissions of the compromised principal

### Human-in-the-Loop for High-Impact Actions

For any agentic system capable of taking irreversible or high-impact actions — sending emails, deleting resources, making financial transactions, modifying security configurations — require human confirmation before execution. This is a simple but powerful control: even a successfully injected agent cannot take an action autonomously if the action requires human approval.

Define the category of actions requiring human approval in terms of reversibility and blast radius, not just action type. Writing a file is low-risk if overwriting is recoverable; deleting a database is not.

### Audit Logging for AI Operations

Log every AI-related event at a level that supports investigation:

- All model invocations: which model, which principal, timestamp, input token count (not necessarily content, depending on data classification requirements)
- All tool calls made by agents: tool name, parameters, outcome
- All document retrievals from RAG systems: query, retrieved document identifiers, model that issued the retrieval
- All guardrail interventions: blocked content categories, invocation context

These logs are the evidence trail for investigating AI-assisted incidents. Without them, reconstructing what an agent did and why is extremely difficult.

### Secrets Management

AI applications frequently need credentials to call external APIs, query databases, or interact with other services. These credentials must not appear in system prompts, model configuration, or anywhere in the LLM's context window. A successful prompt injection attack that causes the model to reveal its context window would expose any credentials present there.

Use AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager. Inject credentials into the application layer, not the AI layer. If tool execution requires credentials, pass them directly to the tool implementation code, not through the model.

---

## What Architects Should Do

- **Treat every AI component as an IAM principal** — scope its permissions as you would any other workload, starting from zero and adding only what is needed
- **Implement input and output validation outside the model** — never rely on the model's own guardrails as your only defence; they can be bypassed
- **Require human confirmation for irreversible actions in agentic systems** — the blast radius of a successful prompt injection is bounded by what the agent can do autonomously
- **Log all model invocations and tool calls** — without this audit trail, AI-assisted incidents are nearly impossible to investigate
- **Use VPC endpoints and private networking for AI API calls** — Bedrock, Azure OpenAI, and Vertex AI all support private endpoints; use them for production
- **Audit your RAG data sources** — a knowledge base populated with sensitive data is a target; ensure that retrieval access controls match the sensitivity of the underlying content
- **Apply supply chain controls to ML dependencies** — model weights, datasets, and Python packages used in ML pipelines deserve the same scrutiny as any other software dependency

---

## Key Takeaways

- **AI components are IAM principals** — they need to be governed with the same least-privilege discipline as any other workload, with the additional consideration that they may be manipulated into misusing their permissions
- **Prompt injection is the primary runtime attack vector** — especially in agentic systems that process external content; validation controls outside the model are required
- **The blast radius of AI compromise is bounded by IAM permissions** — tight scoping is the single most effective control on the impact of a successful attack
- **Human-in-the-loop is a pragmatic defence for agentic systems** — irreversible actions should require confirmation; this stops injection-driven autonomous damage even when other controls fail
- **Audit logging for AI operations is a gap in most environments** — without it, neither detection nor investigation is possible

---

## Related Guides

- [A Beginner's Guide to AI and LLM Security](/guides/beginners-guide-ai-llm-security/) — How LLMs work, how they fail, and the foundational security risks architects must understand before deploying them.
- [Securing AI Agents with Cloud Infrastructure Access](/guides/securing-ai-agents-cloud-infrastructure/) — Deep dive into the threat model for agentic AI systems with tool access to cloud infrastructure.
- [Social Engineering Attacks Against AI Agents](/guides/social-engineering-ai-agents/) — How attackers adapt social engineering techniques to manipulate AI agents and what defences apply.
- [Cloud Identity and Access Management](/guides/cloud-identity-and-access-management/) — Least privilege and IAM controls apply directly to AI principals; this guide covers the underlying IAM architecture.
- [Cloud Threat Detection](/guides/cloud-threat-detection/) — AI-related incidents leave traces in CloudTrail and model API logs; detection requires instrumenting these signals specifically.
- [What is DSPM?](/guides/what-is-dspm-data-security-posture-management/) — RAG knowledge bases often contain sensitive data; DSPM tooling helps discover and classify it before it reaches an AI system.
