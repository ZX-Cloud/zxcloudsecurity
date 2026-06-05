+++
title = "AWS IoT Core Adds Auth & Ping Logs in CloudWatch"
date = "2026-06-03T07:00:00Z"
slug = "aws-iot-core-cloudwatch-ping-authn-error-logs"
description = "AWS IoT Core now offers Ping and Connection.AuthNError CloudWatch log types to help detect connectivity failures and authentication errors across IoT fleet"
categories = ["aws"]
tags = ["aws", "iot-core", "cloudwatch", "authentication", "logging", "mqtt", "iot-security", "observability"]
severity = "Low"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/06/aws-iot-core-ping-auth-logs/"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-iot-core-ping-auth-logs/)

---

AWS IoT Core has introduced two new CloudWatch log event types: Ping logs for MQTT Keep-alive messages and Connection.AuthNError logs for failed authentication attempts. These logs help operators identify devices struggling to maintain connections and quickly diagnose certificate or credential failures across IoT fleets. This is an observability improvement rather than a security fix, but it meaningfully strengthens the ability to detect and respond to authentication anomalies.


> **Architect's Take:** Enable these new log event types in your AWS IoT Core logging configuration and consider creating CloudWatch Metric Filters or alarms on Connection.AuthNError events to surface potential credential misuse or certificate expiry issues proactively — particularly useful in large-scale fleets where silent authentication failures are easy to miss.


**Original advisory:** [AWS IoT Core adds new logs to troubleshoot connectivity and authentication](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-iot-core-ping-auth-logs/)
