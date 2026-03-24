# Linting Automation Script

## Overview

CI workflows kept failing on PRs because of basic lint errors — wrong formatting, import order, spacing issues. Most of these don't need a human, they just need a formatter to run. This script handles that automatically before builds or tests run, so contributors aren't chasing down style errors manually.

It runs the appropriate linting tools for whatever languages are in the repo, applies fixes where it can, and only fails the workflow when something genuinely needs a human to look at it — like an undefined variable, an ambiguous name, or logic that a formatter can't safely touch.

## Supported languages and tools

| Language | Tools |
|---|---|
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

def   add(x,y):
    return x+y

unused=42
result=add(1,2)
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