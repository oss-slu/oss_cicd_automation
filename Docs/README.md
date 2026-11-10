# Documentation

This folder contains written documentation related to the CI/CD work completed throughout the project. It includes guidance, audits, and reference materials that support maintainers and contributors.

## Contents
- **ADR / Audit Reports** – Analysis of existing project workflows, CI/CD readiness, and recommended improvements.
- **Setup Guides** – Instructions for configuring testing frameworks, linters, or development environments.
- **Process Documentation** – Relevant notes that explain technical decisions, debugging steps, and CI/CD practices.
- **[Supply Chain Security Baseline](Supply_Chain_Security_Baseline.md)** – Comprehensive standard and reference workflows for automated SBOM generation, artifact preservation, and build provenance attestations across OSS-SLU projects.
- **[Secret Scanning Workflow Guide](Secret_Scanning_Workflow.md)** – Instructions for integrating Gitleaks pre-merge checks, configuring `.gitleaksignore`, and executing leak remediation.
- **[Kaniko Dockerfile Optimization Guide](Kaniko_Dockerfile_Optimization_Guide.md)** – Technical guide detailing Docker/BuildKit vs. Kaniko execution mechanisms, linear hierarchy rules, and multi-stage container optimization for in-cluster builds.
- **[Pre-Commit Hook Setup Guide](Pre_Commit_Setup_Guide.md)** – Instructions for installing and enabling the standardized pre-commit hook templates, skipping hooks with `--no-verify`, and troubleshooting common issues.

All documentation is written to support long-term maintainability, knowledge transfer, and onboarding for future contributors.

