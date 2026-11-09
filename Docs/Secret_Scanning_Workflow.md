# Secret & Credential Leak Scanning Guide

To comply with **Risk R-01** of the OSS-SLU Security Risk Register, all candidate projects must enforce automated pre-merge secret scanning. Accidental exposure of API tokens, cloud keys, database connection strings, or environment credentials poses severe operational and security risks to both individual project repositories and shared cluster infrastructure.

This repository provides a centralized, reusable GitHub Actions workflow based on [Gitleaks](https://github.com/gitleaks/gitleaks) that catches credential leaks in pull request commit diffs _before_ they are merged into the main git history.

## Table of Contents

- [1. Onboarding & Integration](#1-onboarding--integration)
- [2. Configurable Workflow Parameters](#2-configurable-workflow-parameters)
- [3. Handling Legitimate Test Fixtures](#3-handling-legitimate-test-fixtures)
- [4. Leak Remediation & History Rewriting](#4-leak-remediation--history-rewriting)
- [5. Local Pre-Commit Validation (Optional)](#5-local-pre-commit-validation-optional)

---

## 1. Onboarding & Integration

To enable pre-merge secret scanning in your repository, add a workflow file (for example, `.github/workflows/secret-scan.yml`) that references the reusable workflow from `oss_cicd_automation`.

### Automated Setup

From your repository root, run:

```bash
mkdir -p .github/workflows
curl -o .github/workflows/secret-scan.yml \
  https://raw.githubusercontent.com/oss-slu/oss_cicd_automation/main/Templates/security/secret-scan-caller.yml
```

### Manual Configuration

Create `.github/workflows/secret-scan.yml` with the following contents:

```yaml
name: Security Secret Scan

on:
  pull_request:
    branches:
      - main
      - develop
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  secret-scan:
    name: Call Reusable Secret Scan
    uses: oss-slu/oss_cicd_automation/.github/workflows/reusable-secret-scan.yml@main
    with:
      fetch-depth: 0
      fail-on-leak: true
    secrets: inherit
```

## 2. Configurable Workflow Parameters

The reusable workflow accepts the following inputs:

| Input          | Type      | Default | Description                                                                    |
| -------------- | --------- | ------- | ------------------------------------------------------------------------------ |
| `fetch-depth`  | `number`  | `0`     | Depth of git history to fetch. Use `0` for full PR history diff inspection.    |
| `config-path`  | `string`  | `""`    | Optional relative path to a custom `.gitleaks.toml` ruleset in your repo.      |
| `fail-on-leak` | `boolean` | `true`  | Whether the workflow fails the PR build when a leak is detected.               |

## 3. Handling Legitimate Test Fixtures

Student projects often require dummy keys, mock tokens, or sample credentials inside unit tests and documentation examples. To prevent false positives from blocking your build, use one of the two mechanisms below.

### Option A: `.gitleaksignore` (specific findings)

Add a `.gitleaksignore` file to the root of your repository. Each line is the **fingerprint** of a single finding, which Gitleaks prints in its report output.

```text
# Mock AWS key in unit test fixture
a1b2c3d4e5f6:tests/fixtures/mock_aws_credentials.json:aws-access-token:3

# Sample JWT in README documentation example
a1b2c3d4e5f6:docs/api_examples.md:jwt:42
```

### Option B: `.gitleaks.toml` allowlist (whole paths)

To exclude entire files or directories, define an allowlist in a custom ruleset and point the workflow at it with the `config-path` input.

```toml
[extend]
useDefault = true

[allowlist]
description = "Synthetic test data and public documentation samples"
paths = [
  '''tests/fixtures/.*''',
  '''docs/api_examples\.md''',
]
```

```yaml
jobs:
  secret-scan:
    uses: oss-slu/oss_cicd_automation/.github/workflows/reusable-secret-scan.yml@main
    with:
      config-path: .gitleaks.toml
    secrets: inherit
```

> [!NOTE]
> Use these mechanisms strictly for synthetic test data or public sample templates. Never ignore files containing production or live operational credentials.

## 4. Leak Remediation & History Rewriting

If Gitleaks flags a real secret in your pull request, **pushing a new commit that deletes the secret is not sufficient**. The secret remains fully accessible in your branch's commit history.

Follow these steps in order.

### Step 1: Remove the Credential from History

Use an amend or an interactive rebase to erase the credential from your commit history.

If the secret was introduced in the most recent commit:

```bash
git add <filename>
git commit --amend --no-edit
```

If the secret was introduced several commits ago:

```bash
git rebase -i HEAD~n  # Replace 'n' with the number of commits to go back
```

Mark the offending commit as `edit`, remove the secret, stage the change, and then run:

```bash
git rebase --continue
```

### Step 2: Force-Push Cleaned Commits

Push the rewritten history to your remote branch:

```bash
git push origin <your-feature-branch> --force-with-lease
```

### Step 3: Rotate the Compromised Secret Immediately

Any secret pushed to a remote repository, even temporarily, must be treated as fully compromised.

1. Revoke or delete the key in the relevant provider or service dashboard (for example, AWS IAM, OpenAI, GitHub Developer Portal, or Postgres).
2. Issue a new replacement credential.
3. Store the new credential only in your local environment file (`.env`) or in GitHub Repository Secrets.

> [!WARNING]
> Rewriting history does not undo exposure. Rotation (Step 3) is mandatory even if the force-push succeeds.

## 5. Local Pre-Commit Validation (Optional)

To catch credential leaks on your workstation before pushing to GitHub, install and run Gitleaks locally:

```bash
# Install Gitleaks via Homebrew (macOS/Linux)
brew install gitleaks

# Scan the git history of the current repository
gitleaks git --verbose .
```

> [!TIP]
> On older Gitleaks versions (before v8.19), use `gitleaks detect --source . --verbose` instead.