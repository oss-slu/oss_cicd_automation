# Documentation Link Verification Workflow

This repository verifies links in its Markdown documentation automatically
using [Lychee](https://github.com/lycheeverse/lychee), run via
[lycheeverse/lychee-action](https://github.com/lycheeverse/lychee-action).

Link checking is split into two modes so pull request checks stay fast and
deterministic while external link health is still monitored over time.

## How it works

### 1. Pre-merge PR checks (internal, blocking)

Any pull request that changes a `*.md` file triggers the internal link check,
which runs Lychee in **offline** mode (`--offline`). Offline mode makes no
network requests, so:

- Broken relative links (e.g. a renamed doc file) **fail the check** and block merge.
- Broken in-page anchors (`#section` that no longer exists) **fail the check**.
- External `http(s)://` links are **not** checked, so transient network errors or
  rate-limiting never block a contributor.
- Pull requests that do **not** modify any Markdown file skip the check entirely
  (path filter on the `pull_request` trigger).

### 2. Scheduled external audit (weekly, non-blocking)

A weekly scheduled job runs Lychee against all Markdown files and **also**
checks external URLs. This job never fails the workflow run and never blocks a
merge — its results are written to the GitHub job summary and the
`lychee-report.md` job output for review. Known rate-limited or bot-protected
domains, listed in `.lycheeignore`, are skipped during this audit.

## Files

| File | Purpose |
| --- | --- |
| `.github/workflows/reusable-link-check.yml` | Reusable workflow (the engine). Accepts a `mode` input (`internal` or `all`) and runs Lychee accordingly. |
| `.github/workflows/link-check.yml` | Caller workflow for **this** repo. Triggers the internal check on PRs and the weekly external audit on a schedule. |
| `Templates/linting/reusable-link-check-caller.yml` | Example caller for **other** OSS-SLU repos that want to reuse the link checker. |
| `.lycheeignore` | Regular expressions (one per line) for external domains to skip during the weekly audit. |

## Security conventions

- `lycheeverse/lychee-action` is pinned to an immutable commit SHA.
- `actions/checkout` and `actions/cache` are pinned to immutable commit SHAs.
- The workflow runs with least privilege: `permissions: contents: read`.

## Adding exclusions

To stop a URL (or set of URLs) from being reported by the weekly audit, add a
line to `.lycheeignore` at the repository root. Each line is a regular
expression matched against the **full URL, including the scheme**. Anchor with
`^https?://` to target a domain, for example:

```
# Skip all SonarCloud links (rate-limited / requires auth)
^https?://.*\.sonarcloud\.io
```

Lines starting with `#` are comments. Keep exclusions narrow and review them
periodically so genuine breakage is still caught.

## Running locally

Reproduce the PR check on your machine:

```bash
lychee --offline --no-progress './**/*.md'
```

Reproduce the full external audit:

```bash
lychee --cache --max-cache-age 1d --no-progress './**/*.md'
```
