+++
title = "AWS Cognito New Lambda Trigger for Federated Sign-In"
date = "2026-06-04T15:49:15Z"
slug = "aws-cognito-lambda-trigger-federated-sign-in"
description = "AWS adds a new Cognito Lambda trigger enabling custom logic during federated sign-in via SAML, OIDC, and social providers. Here's what architects need to k"
categories = ["aws"]
tags = ["aws", "amazon-cognito", "lambda", "identity-federation", "saml", "oidc", "authentication", "iam"]
severity = "Low"
source = "AWS Security Blog"
source_url = "https://aws.amazon.com/blogs/security/customize-federated-sign-in-with-new-amazon-cognito-lambda-trigger/"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS Security Blog](https://aws.amazon.com/blogs/security/customize-federated-sign-in-with-new-amazon-cognito-lambda-trigger/)

---

AWS has introduced a new Lambda trigger for Amazon Cognito that allows developers to customise the federated sign-in process when users authenticate via external identity providers such as SAML, OIDC, or social logins. This enables teams to intercept and modify authentication flows at key points, such as attribute mapping or access decisions, without altering core Cognito configuration. The feature improves flexibility for organisations with complex identity federation requirements.


> **Architect's Take:** Review any existing custom authentication workarounds in your Cognito-integrated applications and assess whether this new trigger can consolidate or replace them — pay particular attention to how federated user attributes are mapped and validated, as improper handling here is a common source of privilege misassignment.


**Original advisory:** [Customize federated sign-in with new Amazon Cognito Lambda trigger](https://aws.amazon.com/blogs/security/customize-federated-sign-in-with-new-amazon-cognito-lambda-trigger/)
