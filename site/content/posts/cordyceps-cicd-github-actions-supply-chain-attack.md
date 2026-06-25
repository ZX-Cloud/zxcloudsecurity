+++
title = "Cordyceps CI/CD Flaw Hits 300+ GitHub Repos"
date = "2026-06-24T12:48:11Z"
publishDate = "2026-06-24T12:48:11Z"
slug = "cordyceps-cicd-github-actions-supply-chain-attack"
description = "The Cordyceps vulnerability class exposes 300+ GitHub repositories to supply-chain attacks, allowing full workflow hijack at orgs including Microsoft and G"
categories = ["general"]
tags = ["github", "github-actions", "ci-cd", "supply-chain", "workflow-hijack", "open-source-security", "devops-security"]
severity = "Critical"
source = "The Hacker News"
source_url = "https://thehackernews.com/2026/06/cordyceps-cicd-flaws-expose-300-github.html"
weight = 10
draft = false
+++

🔴 **Critical** &nbsp;|&nbsp; **Source:** [The Hacker News](https://thehackernews.com/2026/06/cordyceps-cicd-flaws-expose-300-github.html)

---

A newly identified class of CI/CD vulnerability, dubbed 'Cordyceps' by Novee Security, allows attackers to hijack GitHub Actions workflows and gain full control of repositories belonging to major organisations including Microsoft, Google, and Apache. Over 300 repositories have been identified as exposed, making this a significant supply-chain risk. Because CI/CD pipelines often hold privileged credentials and publish trusted software artefacts, a successful exploit could enable attackers to inject malicious code into widely used open-source packages.


> **Security Architect's Take:** Audit all GitHub Actions workflows across your organisation immediately for write permissions granted to pull request triggers (e.g. pull_request_target with checkout of untrusted code), restrict GITHUB_TOKEN permissions to least-privilege, and enforce branch protection rules requiring signed commits and mandatory reviewers before any workflow executes with elevated access.


**Original advisory:** [Cordyceps CI/CD Flaws Expose 300+ GitHub Repositories to Supply-Chain Attacks](https://thehackernews.com/2026/06/cordyceps-cicd-flaws-expose-300-github.html)
