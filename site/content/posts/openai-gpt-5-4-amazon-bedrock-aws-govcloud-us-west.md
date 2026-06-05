+++
title = "OpenAI GPT-5.4 on AWS Bedrock GovCloud (US-West)"
date = "2026-06-03T19:58:00Z"
slug = "openai-gpt-5-4-amazon-bedrock-aws-govcloud-us-west"
description = "OpenAI GPT-5.4 is now available on Amazon Bedrock in AWS GovCloud (US-West), offering isolated inference for government and regulated-industry workloads."
categories = ["aws"]
tags = ["aws", "amazon-bedrock", "openai", "govcloud", "generative-ai", "data-residency", "compliance", "inference-security"]
severity = "Low"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/06/GPT54-available-in-aws-govcloud-us-west/"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/GPT54-available-in-aws-govcloud-us-west/)

---

OpenAI's GPT-5.4 model is now generally available on Amazon Bedrock within AWS GovCloud (US-West), extending access to government and regulated-industry customers. The deployment leverages Bedrock's isolated inference infrastructure, ensuring prompts and responses remain within the customer's AWS environment and are not used for model training. This expands the options available for sensitive workloads requiring complex reasoning and document analysis under strict compliance controls.


> **Architect's Take:** Evaluate data residency and access control policies before enabling GPT-5.4 for sensitive workloads — confirm that Bedrock resource policies, VPC endpoints, and CloudTrail logging are configured to meet your organisation's compliance requirements, particularly if handling OFFICIAL-SENSITIVE or equivalent data in GovCloud.


**Original advisory:** [OpenAI GPT-5.4 generally available on Amazon Bedrock in AWS GovCloud (US-West)](https://aws.amazon.com/about-aws/whats-new/2026/06/GPT54-available-in-aws-govcloud-us-west/)
