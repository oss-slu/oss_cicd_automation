# PR Size and Component Labeler Guide

This guide explains how to adopt the automated PR labeling workflow from
`Templates/labeler/` to automatically apply size and area labels to pull
requests in your repository.

## How it works

Two independent jobs run on every PR open, update, or reopen event:

| Job | Action | What it does |
| --- | --- | --- |
| Area labeler | `actions/labeler@v7` | Applies `area/*` labels based on which file paths changed, using globs defined in `.github/labeler.yml`. |
| Size labeler | `codelytv/pr-size-labeler@v1.12.0` | Applies a `size/*` label based on total lines added + deleted. Never blocks a PR. |

## Size label thresholds

| Label | Line change range |
| --- | --- |
| `size/XS` | 0 – 10 lines |
| `size/S` | 11 – 50 lines |
| `size/M` | 51 – 200 lines |
| `size/L` | 201 – 500 lines |
| `size/XL` | 500+ lines |

Thresholds are configurable via the `xs_max_size`, `s_max_size`, `m_max_size`,
and `l_max_size` inputs in `pr-labeler-caller.yml`.

## Adoption steps

1. **Create the labels** in your repository's Labels settings page
   (`github.com/<org>/<repo>/labels`) before running the workflow.
   Required labels: `area/frontend`, `area/backend`, `area/docs`, `area/ci`,
   `size/XS`, `size/S`, `size/M`, `size/L`, `size/XL`.

2. **Copy the caller workflow** into your repo:

   ```bash
   cp Templates/labeler/pr-labeler-caller.yml .github/workflows/pr-labeler.yml
   ```

3. **Copy and customize the labeler config**:

   ```bash
   cp Templates/labeler/labeler.yml .github/labeler.yml
   ```

   Open `.github/labeler.yml` and adjust the path globs to match your
   repository's directory structure.

4. **Commit both files** and open a test PR to verify labels are applied.

## Customizing area labels

Add or rename labels in `.github/labeler.yml` by following the same pattern:

```yaml
area/tests:
  - changed-files:
    - any-glob-to-any-file:
      - 'tests/**'
      - '**/*.test.ts'
      - '**/*.spec.py'
```

The key (e.g. `area/tests`) must exactly match a label that exists in your
repository. The `any-glob-to-any-file` rule applies the label if **any**
changed file matches **any** of the listed globs.

## Customizing size thresholds

Edit the `xs_max_size`, `s_max_size`, `m_max_size`, `l_max_size` inputs in
`.github/workflows/pr-labeler.yml`:

```yaml
with:
  xs_max_size: 20    # raise XS ceiling to 20 lines
  s_max_size: 100
  m_max_size: 400
  l_max_size: 800
```

## Security note

The workflow uses `pull_request_target` so it has write access to apply labels
even on fork PRs. Both actions are pinned to immutable commit SHAs and run
with `permissions: contents: read` + `pull-requests: write` (least privilege).
Never add `actions/checkout` with `ref: ${{ github.event.pull_request.head.sha }}`
to this workflow — that would expose the write token to untrusted code.
