# Pre-Commit Hook Setup Guide

Pre-commit hooks run checks locally before a commit is created, catching
formatting errors, secrets, and syntax issues before they ever reach CI.
This guide covers installing and enabling the hook templates provided in
`Templates/git-hooks/`.

## Available templates

| Template file | Purpose |
| --- | --- |
| `.pre-commit-config-general.yml` | Repo hygiene (trailing whitespace, end-of-file newlines, YAML/JSON validation) + Gitleaks secret scanning — base for any repo. |
| `.pre-commit-config-python.yml` | Ruff linting and formatting for Python repos. |
| `.pre-commit-config-js-ts.yml` | ESLint and Prettier for JavaScript / TypeScript repos. |
| `.pre-commit-config-rust.yml` | cargo fmt and cargo clippy for Rust repos. |

You can use the general template standalone, or combine it with a language-specific
template by merging their `repos` lists into a single `.pre-commit-config.yaml`
in your repository root.

## Installation

1. Install pre-commit (requires Python ≥ 3.9):

   ```bash
   pip install pre-commit
   ```

2. Copy the template(s) you need to your repo root:

   ```bash
   # Base hygiene + secrets for any repo
   cp Templates/git-hooks/.pre-commit-config-general.yml .pre-commit-config.yaml

   # Python repo
   cp Templates/git-hooks/.pre-commit-config-python.yml .pre-commit-config.yaml

   # JavaScript / TypeScript repo
   cp Templates/git-hooks/.pre-commit-config-js-ts.yml .pre-commit-config.yaml

   # Rust repo
   cp Templates/git-hooks/.pre-commit-config-rust.yml .pre-commit-config.yaml
   ```

3. Install the hooks into your local `.git/hooks/`:

   ```bash
   pre-commit install
   ```

   From this point on, the hooks run automatically on every `git commit`.

4. (Optional) Run all hooks against your entire repo right now to catch
   any existing issues:

   ```bash
   pre-commit run --all-files
   ```

## Combining templates

To use the general base alongside a language-specific template, merge their
`repos` lists into one file. Example for a Python repo:

```yaml
repos:
  # --- from .pre-commit-config-general.yml ---
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1
    hooks:
      - id: gitleaks

  # --- from .pre-commit-config-python.yml ---
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.17.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

## JavaScript / TypeScript repos — extra step

The JS/TS template uses a `local` Prettier hook that calls your project's
own `node_modules`. Make sure Prettier and ESLint are installed first:

```bash
npm install --save-dev prettier eslint
```

## Rust repos — extra step

The Rust template uses `language: system` hooks that call `cargo` directly.
Make sure the Rust toolchain is installed:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Skipping hooks

If you need to bypass hooks for a specific commit (e.g. a WIP commit):

```bash
git commit --no-verify -m "wip: skip hooks this once"
```

Use `--no-verify` sparingly. The reusable CI workflows will still catch issues
on your PR even if hooks were skipped locally.

## Suppressing Gitleaks false positives

Add the flagged line's SHA to `.gitleaksignore` in your repo root. For full
details on the format and remediation steps, see
[`Secret_Scanning_Workflow.md`](Secret_Scanning_Workflow.md).

## Updating hook versions

To update all hook versions to their latest releases:

```bash
pre-commit autoupdate
```

Review the resulting diff before committing — a new hook version may
introduce new violations in existing code.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `pre-commit: command not found` | Re-run `pip install pre-commit` and check that your Python scripts dir is on `PATH`. |
| Hook passes locally but fails in CI | Confirm the `rev` tags in your `.pre-commit-config.yaml` match the versions used in the reusable CI workflows. |
| Ruff auto-fixes break other hooks | Run `pre-commit run --all-files` a second time — Ruff's fixes may need to be re-validated. |
| `cargo clippy` fails on warnings | Add `#[allow(clippy::...)]` for intentional patterns, or remove `-D warnings` from the hook entry. |
| `gitleaks: exit code 1` on a test fixture | Add a `.gitleaksignore` entry for that file/line. See `Secret_Scanning_Workflow.md`. |
