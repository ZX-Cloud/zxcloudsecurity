+++
title = "AWS IoT Core Adds Auth & Ping Logs in CloudWatch"
date = "2026-06-03T07:00:00Z"
slug = "aws-iot-core-ping-authn-error-cloudwatch-logs"
description = "AWS IoT Core introduces Ping and Connection.AuthNError CloudWatch log types to help detect MQTT connectivity failures and authentication errors across IoT "
categories = ["aws"]
tags = ["aws", "iot-core", "cloudwatch", "authentication", "mqtt", "logging", "observability"]
severity = "Low"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/06/aws-iot-core-ping-auth-logs/"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-iot-core-ping-auth-logs/)

---

AWS IoT Core has introduced two new CloudWatch log event types: Ping logs for MQTT keep-alive messages and Connection.AuthNError logs for failed authentication attempts. These additions give security and operations teams better visibility into device connectivity failures and credential or certificate issues across IoT fleets. This is a positive observability improvement rather than a vulnerability disclosure.


> **Architect's Take:** Enable event-level logging in AWS IoT Core and opt into both new event types immediately — feed Connection.AuthNError logs into your SIEM or CloudWatch alarms to detect potential credential stuffing or certificate misconfiguration across your IoT fleet at scale.


**Original advisory:** [AWS IoT Core adds new logs to troubleshoot connectivity and authentication](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-iot-core-ping-auth-logs/)
