# Linting Automation Script

## Overview

CI workflows kept failing on PRs because of basic lint errors — wrong formatting, import order, spacing issues. Most of these don't need a human, they just need a formatter to run. This script handles that automatically before builds or tests run, so contributors aren't chasing down style errors manually.

It runs the appropriate linting tools for whatever languages are in the repo, applies fixes where it can, and only fails the workflow when something genuinely needs a human to look at it — like an undefined variable, an ambiguous name, or logic that a formatter can't safely touch.

## Supported languages and tools

| Language | Tools |
| --- | --- |
| Python | ruff, isort |
| JavaScript / TypeScript | eslint, prettier |
| Go | gofmt |
| Rust | rustfmt |
| Markdown | markdownlint-cli2 |

If a tool isn't installed it gets skipped with a warning — the script won't fail just because a tool is missing.

## How it works

Languages are detected automatically from file extensions in the target directory. You can also pass them explicitly with `--langs`. For each language it runs the auto-fix command, then re-runs the linter to see if anything is still broken. If everything passes, it exits 0. If something is still flagged after fixing, it exits 1.

For Python the cycle looks like this:

```
ruff check --fix .   # fixes safe violations (unused imports, etc.)
ruff format .        # reformats spacing, line length, quotes
isort .              # sorts and groups imports
ruff check .         # re-checks — anything left needs manual review
```

## Setup

Install the tools for the languages you need:

```bash
# Python
pip install ruff isort

# JavaScript / TypeScript
npm install -g eslint prettier

# Rust
rustup component add rustfmt

# Markdown
npm install -g markdownlint-cli2

# Go — gofmt comes with Go, nothing extra needed
```

On Windows, ruff and isort may install but not be on your PATH. The script handles this automatically by falling back to `python -m ruff` and `python -m isort`.

## Usage

```bash
# run against the current directory (auto-detects languages)
python lint_fix.py

# target a specific directory
python lint_fix.py --path ./src

# only run Python linters
python lint_fix.py --langs python

# see what would be fixed without changing any files
python lint_fix.py --check-only

# show full output from each tool
python lint_fix.py -v
```

Exit codes:

- `0` — everything is clean
- `1` — unfixable issues remain, needs manual review
- `2` — bad argument or path doesn't exist

## Testing on a Real Repository

Before integrating the script into a CI workflow, it was validated against a real open source project by forking and cloning a repository and running the script against it.

### Test Environment

| Detail | Value |
| -------- | ------- |
| Repository tested | pao_surgery_simulator |
| Test directory | `C:\Users\user\pao_surgery_simulator_linting` |
| Script path | `C:\Users\user\Downloads\oss_cicd_automation\Tools&Utilities\lint.py` |
| Languages detected | JavaScript, Markdown, Python |

### Test Procedure

Run check-only first to review findings without making changes, then apply fixes and verify with git diff.

```cmd
# Step 1 — check only, no changes made
python "C:\...\lint.py" --check-only -v

# Step 2 — apply fixes
python "C:\...\lint.py" -v

# Step 3 — review what changed
git diff

# Step 4 — revert if needed
git checkout .
```

### Test Output

```
[INFO] Detected: javascript, markdown, python
[INFO] Running javascript...
[WARNING] eslint not found, skipping JS/TS
[WARNING] prettier not found, skipping JS/TS formatting
[INFO] Running markdown...
[WARNING] markdownlint-cli2 not found, skipping Markdown
[INFO] Running python...
F401 [*] `PIL.Image` imported but unused --> backend\app.py:7:17
F401 [*] `flask.send_file` imported but unused --> backend\app.py:10:44
F401 [*] `sqlalchemy.orm.declarative_base` imported but unused --> backend\db.py:3:42
F401 [*] `models` imported but unused --> backend\db.py:7:8
Found 4 errors. [*] 4 fixable with the `--fix` option.
[FAIL] Unfixable issues in: python — needs manual review
```

### What the Test Confirmed

- Auto-detection works correctly from file extensions
- Missing tools are skipped gracefully — no crash, just a warning
- `FAIL` on `--check-only` with all `[*]` errors is expected behavior, not a bug
- Running without `--check-only` resolved all flagged Python issues automatically
- `git diff` after fixing showed only the removed unused imports — no unintended changes

## Integrating into CI

Add this step before your build or test steps. The script exits 1 on unfixable issues which fails the job, and silently fixes everything else.

```yaml
- name: Lint
  run: python .github/scripts/lint_fix.py --path . -v
```

To auto-commit fixes back to the branch:

```yaml
- name: Lint
  run: python .github/scripts/lint_fix.py --path .

- name: Commit fixes
  run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git add -A
    if ! git diff --cached --quiet; then
      git commit -m "chore: auto-fix lint issues [skip ci]"
      git push
    fi
```

## What gets fixed automatically

These are the kinds of issues the script resolves without any manual intervention:

```python
# Before
import os
import json
import sys


def add(x, y):
    return x + y


unused = 42
result = add(1, 2)
```

```python
# After — ruff and isort clean this up automatically
import json
import os
import sys


def add(x, y):
    return x + y


result = add(1, 2)
```

Specific things that get fixed: inconsistent spacing, import order, unused imports, line length, quote style, missing blank lines between functions.

## When the script still fails

Exit 1 means something is left that the tools won't touch, here is an example

**Undefined name** — ruff flags this but won't guess what you meant:

```python
def process(data):
    result = transform(data)  # 'transform' is not defined
    return result
```

**Complexity** — a function that's too deeply nested needs to be restructured, which requires understanding what it's supposed to do.

**Project-specific rules** — if your `.ruff.toml` or `.eslintrc` enforces conventions specific to your project, those won't be auto-fixed.

When CI fails for one of these reasons the output will show the file and line number. Fix it manually and push again.

---

## Reusable GitHub Actions Workflow (`reusable-lint.yml`)

For downstream repositories in **OSS-SLU**, static code linting and formatting can be automatically enforced using our central reusable workflow without copy-pasting complex CI configurations.

### Key Features

- **Automatic Stack Detection:** Automatically detects Python, Node.js/TypeScript, and Go manifests (`pyproject.toml`, `package.json`, `go.mod`, etc.) and executes only the required checks.
- **Non-Blocking Advisory Mode (Default):** Runs with `fail_on_error: false` by default. Warnings appear as inline GitHub PR annotations without failing status checks or blocking PR merges.
- **Polyglot Support:** Works seamlessly across single-language repositories and multi-language/monorepo setups.

---

### Quick Onboarding Setup

Add a workflow file named `.github/workflows/lint.yml` in your downstream repository with the following block:

```yaml
name: Lint & Format Checks

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  lint:
    uses: oss-slu/oss_cicd_automation/.github/workflows/reusable-lint.yml@main
    with:
      fail_on_error: false
```

---

### Configurable Parameters

| Input Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `fail_on_error` | Boolean | No | `false` | When `false`, linters run in advisory mode using PR annotations without failing the overall CI status check. |
| `python_version` | String | No | `"3.12"` | Python version for Ruff linting and formatting. |
| `node_version` | String | No | `"20"` | Node.js version for ESLint & Prettier checks. |
| `go_version` | String | No | `"1.22"` | Go version for `golangci-lint`. |

---

### Tools Used in Reusable Workflow

| Stack | Execution Criteria | Tooling Commands |
| --- | --- | --- |
| **Python** | `pyproject.toml`, `requirements.txt`, `setup.py`, or `*.py` files | `ruff check --output-format=github .` and `ruff format --check .` |
| **Node.js / TS** | `package.json` | `npm run lint` (or `npx eslint .`) + `npx prettier --check .` |
| **Go** | `go.mod` | `golangci/golangci-lint-action` |

---
