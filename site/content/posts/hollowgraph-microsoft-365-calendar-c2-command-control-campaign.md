+++
title = "HOLLOWGRAPH: M365 Calendars Used as C2 Drop Boxes"
date = "2025-07-20T14:59:00Z"
publishDate = "2026-07-20T14:59:00Z"
slug = "hollowgraph-microsoft-365-calendar-c2-command-control-campaign"
description = "The HOLLOWGRAPH campaign abuses Microsoft 365 calendar invites to hide malware commands, using Microsoft's own cloud as a covert C2 channel."
categories = ["general"]
tags = ["azure", "microsoft-365", "microsoft-graph-api", "command-and-control", "living-off-the-land", "defender-for-cloud-apps", "calendar-abuse", "apt"]
severity = "High"
source = "The Register — Security"
source_url = "https://www.theregister.com/security/2026/07/20/microsoft-365-calendars-become-spy-drop-boxes-in-hollowgraph-campaign/5274982"
weight = 20
draft = false
+++

🟠 **High** &nbsp;|&nbsp; **Source:** [The Register — Security](https://www.theregister.com/security/2026/07/20/microsoft-365-calendars-become-spy-drop-boxes-in-hollowgraph-campaign/5274982)

---

A threat campaign dubbed HOLLOWGRAPH is abusing Microsoft 365 calendar invitations to deliver and relay malware commands, with attackers embedding instructions inside appointments dated as far ahead as 2050 to evade detection. The malware uses Microsoft's own cloud infrastructure as its command-and-control channel, making malicious traffic extremely difficult to distinguish from legitimate Microsoft 365 communications. This living-off-the-land approach significantly reduces the effectiveness of traditional network-based detection controls.


> **Security Architect's Take:** Review Microsoft 365 audit logs and Defender for Cloud Apps policies for anomalous calendar API activity, particularly calendar items with far-future dates or unusual creation patterns from non-interactive service principals. Consider implementing Conditional Access policies and Microsoft Graph API monitoring to flag atypical programmatic access to calendar endpoints.


**Original advisory:** [Microsoft 365 calendars become spy drop boxes in HOLLOWGRAPH campaign](https://www.theregister.com/security/2026/07/20/microsoft-365-calendars-become-spy-drop-boxes-in-hollowgraph-campaign/5274982)
