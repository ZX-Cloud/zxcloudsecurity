+++
title = "AWS IoT Device Management MQTT Session Data API"
date = "2026-06-03T21:15:00Z"
slug = "aws-iot-device-management-mqtt-session-connectivity-api"
description = "AWS IoT Device Management adds MQTT session and socket data to its connectivity API. Learn the IAM controls and security implications for IoT fleets."
categories = ["aws"]
tags = ["aws", "iot", "aws-iot-device-management", "mqtt", "iam", "network-visibility", "audit-logging", "fleet-security"]
severity = "Low"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/05/aws-iot-device-management-mqtt/"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/05/aws-iot-device-management-mqtt/)

---

AWS IoT Device Management has enhanced its connectivity status API to include detailed MQTT session data, such as session timeout and expiry values, plus optional socket-level details including IP addresses, ports, and VPC endpoint IDs. Unlike the IoT Core GetConnection API, which only retains data for 30 minutes post-disconnect, this API stores connection history indefinitely. This is useful for security auditing, forensic investigation of disconnect events, and monitoring connection patterns across large IoT fleets.


> **Architect's Take:** Review and tighten IAM policies controlling access to the new socket-level details (source/destination IPs, ports, VPC endpoint IDs), as this data could aid lateral movement reconnaissance if exposed to over-privileged roles. Use the indefinite data retention capability to feed IoT connectivity logs into your SIEM for anomaly detection and post-incident forensics.


**Original advisory:** [AWS IoT Device Management adds MQTT session data to connectivity status API](https://aws.amazon.com/about-aws/whats-new/2026/05/aws-iot-device-management-mqtt/)
