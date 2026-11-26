# Stale Issue and PR Triage Guide

## Overview

In semester-based open source projects, issues and pull requests opened during previous academic terms can accumulate without active follow-up. Leaving abandoned items untriaged makes it harder for new student contributors and maintainers to identify actionable work.

This repository provides a centralized, reusable GitHub Actions workflow ([`.github/workflows/reusable-stale-triage.yml`](../.github/workflows/reusable-stale-triage.yml)) powered by [`actions/stale`](https://github.com/actions/stale) (pinned to an immutable commit SHA) to gently prompt inactive authors before closing abandoned items.

---

## Quick Start

1. **Copy the caller template** from [`Templates/maintenance/stale-caller.yml`](../Templates/maintenance/stale-caller.yml) into your repository at `.github/workflows/stale-triage.yml`.
2. **Verify exempt labels** in your repository (`pinned`, `security`, `accepted`, `Always Open`, `work-in-progress`) and apply them to any roadmap items or long-lived issues that should never auto-close.
3. **Run a dry run first** by temporarily setting `debug-only: true` and triggering the workflow manually from the **Actions > Stale Issue and PR Triage > Run workflow** button. Inspect the workflow logs to confirm which issues and PRs would be flagged.
4. **Enable live triage** by setting `debug-only: false` and committing the workflow to your default branch.

---

## Workflow Inputs

All inputs are optional and carry safe defaults in [`.github/workflows/reusable-stale-triage.yml`](../.github/workflows/reusable-stale-triage.yml):

| Input | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `days-before-stale` | `number` | `60` | Days of inactivity before marking an issue or PR as stale (`-1` to disable). |
| `days-before-close` | `number` | `7` | Days after being marked stale before closing (`-1` to mark stale without auto-closing). |
| `exempt-issue-labels` | `string` | `pinned,security,accepted,Always Open` | Comma-separated issue labels excluded from stale triage. |
| `exempt-pr-labels` | `string` | `pinned,security,work-in-progress,Always Open` | Comma-separated PR labels excluded from stale triage. |
| `stale-issue-label` | `string` | `stale` | Label applied when an issue is marked stale. |
| `stale-pr-label` | `string` | `stale` | Label applied when a PR is marked stale. |
| `stale-issue-message` | `string` | *(gentle prompt)* | Comment posted when an issue is marked stale. |
| `stale-pr-message` | `string` | *(gentle prompt)* | Comment posted when a PR is marked stale. |
| `close-issue-message` | `string` | *(gentle closing note)* | Comment posted when a stale issue is closed. |
| `close-pr-message` | `string` | *(gentle closing note)* | Comment posted when a stale PR is closed. |
| `exempt-all-milestones` | `boolean` | `false` | When `true`, exempts all issues and PRs assigned to a milestone. |
| `exempt-draft-pr` | `boolean` | `false` | When `true`, exempts draft PRs from stale triage. |
| `operations-per-run` | `number` | `30` | Maximum GitHub API operations per scheduled run to stay within rate limits. |
| `debug-only` | `boolean` | `false` | Dry-run mode; logs planned actions without modifying issues or PRs. |

---

## Gentle Triage Best Practices

Automated closing works best when it acts as a polite reminder rather than a surprise cutoff:

- **Dry-run before enabling:** Always validate with `debug-only: true` on repositories with an existing backlog so maintainers can label long-term issues before the first live sweep.
- **Protect active and evergreen work:** Use exempt labels (`pinned`, `security`, `accepted`, `Always Open`) for architectural proposals, tracking dashboards (such as FAIR compliance issues), and security advisories. If your project tracks active sprints via GitHub Milestones, set `exempt-all-milestones: true`.
- **Account for academic breaks:** The default `60` days of inactivity plus a `7`-day grace period balances responsiveness with short breaks. For slower-moving research repositories or summer breaks, raise `days-before-stale` to `90` or `120`.
- **Use label-only mode if preferred:** Setting `days-before-close: -1` flags inactive items with the `stale` label for human review without closing them automatically.
- **Clear, welcoming messages:** Explain clearly why the item was flagged and let contributors know that any comment or commit automatically removes the `stale` label (`remove-stale-when-updated: true` is enabled in the reusable workflow). Remind authors that closed items can always be reopened if work resumes.
- **Respect API rate limits:** Keep `operations-per-run` at `30` (the default) on a daily schedule so large backlogs are processed gradually over several days without exhausting `GITHUB_TOKEN` rate limits.

---

## Security & Permissions

- **Least-privilege permissions:** The reusable workflow and caller template restrict `GITHUB_TOKEN` strictly to `issues: write` and `pull-requests: write`. No repository code checkout (`contents: read`) or code execution is performed.
- **Immutable action pinning:** `actions/stale` is pinned to a full 40-character commit SHA (`v11.0.0`) to protect against supply-chain tag mutation.
