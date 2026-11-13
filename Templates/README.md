# 🧩 Templates

This directory provides **reusable GitHub Action workflow templates**, configuration checklists, and reference setups used across the OSS CI/CD automation project.

These templates ensure every workflow follows consistent standards for reliability, security, and maintainability.

---

## 🪄 What This Folder Is For

- Creating and maintaining **reusable GitHub Actions workflows**  
- Providing **checklists** for validating new or updated workflows  
- Storing **reference configurations** (naming, triggers, environments, and secrets)  
- Simplifying onboarding and enforcing CI/CD best practices  

---

## 📁 Files in This Folder

- **`workflowChecklist.md`** — A structured checklist to verify your workflow’s configuration.  
  Use it before submitting or reviewing a new GitHub Actions workflow to ensure:
  - Triggers, environments, and job definitions are correct  
  - Steps are named clearly  
  - Security and secret management follow best practices  

- *(Add more templates here as needed)*  
  For example:  
  - `build-attest/slsa-build-attest-caller.yml` → Drop-in caller template for SLSA Level 3 container builds, Syft SBOM generation, cryptographic provenance attestation, Harbor dual-push, and Trivy scan reporting.
  - `branch-sync/sync-staging-main.yml` → Drop-in workflow for automated reconciliation of `main` into `staging` to prevent branch drift in GitOps environments.
  - `reusable-test.yml` → A base test workflow using reusable actions  
  - `deploy-template.yml` → Standardized deployment pipeline template  
  - `security/secret-scan-caller.yml` → Reusable workflow caller template for pre-merge Gitleaks secret detection.
  - `link-check/reusable-link-check-caller.yml` → Reusable workflow caller template for automated Markdown link verification using Lychee (pre-merge internal relative-link checks and weekly external URL audits). 
  - `git-hooks/.pre-commit-config-general.yml` → Drop-in pre-commit base template for repo hygiene and Gitleaks secret scanning — suitable for any repo.
  - `git-hooks/.pre-commit-config-python.yml` → Drop-in pre-commit template for Python repos using Ruff (linter + formatter).
  - `git-hooks/.pre-commit-config-js-ts.yml` → Drop-in pre-commit template for JavaScript/TypeScript repos using ESLint and Prettier.
  - `git-hooks/.pre-commit-config-rust.yml` → Drop-in pre-commit template for Rust repos using cargo fmt and cargo clippy.
  - `dependencies/dependabot-actions.yml` → Drop-in Dependabot template for GitHub Actions updates, grouped by minor+patch to reduce PR noise.
  - `dependencies/dependabot-python.yml` → Drop-in Dependabot template for Python (pip/poetry/uv) dependency updates with grouping configuration.
  - `dependencies/dependabot-node.yml` → Drop-in Dependabot template for Node.js (npm/yarn/pnpm) dependency updates with grouping configuration.
  - `dependencies/dependabot-docker.yml` → Drop-in Dependabot template for Docker base image updates.
  - `labeler/labeler.yml` → Sample path-based label configuration for `actions/labeler`; copy to `.github/labeler.yml` and customize globs to match your repository structure.
  - `labeler/pr-labeler-caller.yml` → Caller workflow template for automated PR size labeling (`size/XS` through `size/XL`) and path-based area labeling (`area/frontend`, `area/backend`, `area/docs`, `area/ci`).
  - `testing/coverage-python-caller.yml` → Caller template for Python pytest-cov coverage reporting and PR comment posting.
  - `testing/coverage-jest-caller.yml` → Caller template for Jest/Node.js lcov coverage reporting and PR comment posting.
  - `testing/coverage-go-caller.yml` → Caller template for Go coverage reporting and PR comment posting.


---

## 🧠 Usage

When adding or editing a workflow:
1. Reference `workflowChecklist.md` to confirm compliance.  
2. Follow the recommended naming, branching, and trigger conventions.  
3. Store sensitive data only in **GitHub Secrets**.  
4. Keep workflows modular and version-pinned (e.g., `actions/checkout@v4`).

Example:
```bash
Templates/workflowChecklist.md
🚀 Best Practices
Use workflow_call to define reusable workflows.

Pin all third-party action versions for build stability.

Cache dependencies to reduce CI/CD execution time.

Avoid hardcoding tokens, credentials, or secrets.

Keep logs readable and step names descriptive.

Maintainer: OSS Automation Team
Last Updated: October 2025
