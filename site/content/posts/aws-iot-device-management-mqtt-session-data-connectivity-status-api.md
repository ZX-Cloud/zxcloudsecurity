+++
title = "AWS IoT Device Management: MQTT Session Data in API"
date = "2026-06-03T21:15:00Z"
slug = "aws-iot-device-management-mqtt-session-data-connectivity-status-api"
description = "AWS IoT Device Management adds MQTT session data to its connectivity status API, with indefinite retention and IAM-controlled socket-level access for IoT f"
categories = ["aws"]
tags = ["aws", "iot", "aws-iot-device-management", "mqtt", "iam", "network-visibility", "audit-logging", "access-control"]
severity = "Low"
source = "AWS What's New"
source_url = "https://aws.amazon.com/about-aws/whats-new/2026/05/aws-iot-device-management-mqtt/"
draft = false
+++

🟢 **Low** &nbsp;|&nbsp; **Source:** [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2026/05/aws-iot-device-management-mqtt/)

---

AWS IoT Device Management has enhanced its connectivity status API to include detailed MQTT session data, such as session timeout and expiry values, plus optional socket-level details including IP addresses, ports, and VPC endpoint IDs. Unlike the AWS IoT Core GetConnection API, which only retains data for 30 minutes post-disconnect, this API stores connection history indefinitely, improving long-term auditability. Access to sensitive socket-level information is controlled via IAM policies, allowing organisations to limit visibility to authorised teams.


> **Architect's Take:** Review and tighten IAM policies governing access to the connectivity status API, particularly the socket-level data permissions, to ensure only operations and security teams have visibility into source/destination IPs and VPC endpoint IDs. Additionally, consider integrating the indefinite data retention capability into your IoT incident response and audit workflows to leverage historical disconnect data for forensic investigations.


**Original advisory:** [AWS IoT Device Management adds MQTT session data to connectivity status API](https://aws.amazon.com/about-aws/whats-new/2026/05/aws-iot-device-management-mqtt/)
