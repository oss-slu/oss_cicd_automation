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
  - `reusable-test.yml` → A base test workflow using reusable actions  
  - `deploy-template.yml` → Standardized deployment pipeline template  

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
