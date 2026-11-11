# Automated Dependency Updates Guide

This guide explains how to adopt the Dependabot configuration templates from
`Templates/dependencies/` to automatically keep your project's dependencies
and GitHub Actions up to date.

## What is Dependabot?

Dependabot is a GitHub-native tool that automatically detects outdated
dependencies and opens pull requests with version updates. It runs on a
schedule you define and can optionally auto-merge safe updates.

## Adoption steps

1. **Identify your package manager** — determine which ecosystems your project
   uses:
   - GitHub Actions (every project)
   - Python (pip, poetry, uv)
   - Node.js (npm, yarn, pnpm)
   - Docker (base images in Dockerfiles)

2. **Copy the template** — copy the relevant template(s) to your repository:

   ```bash
   # For example, a Python project with GitHub Actions
   cp Templates/dependencies/dependabot-actions.yml .github/dependabot.yml
   cp Templates/dependencies/dependabot-python.yml .github/dependabot.yml
