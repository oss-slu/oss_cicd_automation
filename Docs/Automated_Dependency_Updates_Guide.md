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

2. **Copy and combine the templates** — copy the relevant template(s) into a
   single `.github/dependabot.yml` file. Do NOT run sequential `cp` commands
   that overwrite each other. Instead, combine all ecosystem blocks under the
   single `updates:` key:

   ```bash
   # WRONG — this overwrites the file each time:
   cp Templates/dependencies/dependabot-actions.yml .github/dependabot.yml
   cp Templates/dependencies/dependabot-python.yml .github/dependabot.yml  # overwrites!

   # CORRECT — combine both under the updates: key manually
   ```

   The combined file should look like this:

   ```yaml
   version: 2
   updates:
     # --- GitHub Actions ---
     - package-ecosystem: github-actions
       directory: /
       schedule:
         interval: weekly
         day: monday
       groups:
         action-minor-patch:
           patterns:
             - "*"
           update-types:
             - minor
             - patch

     # --- Python (pip) ---
     - package-ecosystem: pip
       directory: /
       schedule:
         interval: weekly
         day: monday
       groups:
         python-minor-patch:
           patterns:
             - "*"
           update-types:
             - minor
             - patch
   ```

3. **Customize if needed** — edit `.github/dependabot.yml` to:
   - Uncomment the section matching your specific package manager (pip vs
     poetry vs uv; npm vs yarn vs pnpm)
   - Adjust the schedule (`day: monday` is the default)
   - Modify the `open-pull-requests-limit` if you want fewer concurrent PRs
   - Add or remove `update-types` based on your risk tolerance

4. **Commit and verify** — push the file and watch for the initial Dependabot
   PR within the next scheduled run.

## Understanding the grouping configuration

Each template includes a `groups:` section that bundles updates:

```yaml
groups:
  python-minor-patch:
    patterns:
      - "*"
    update-types:
      - minor
      - patch
```

| `update-types` | What gets grouped |
|----------------|-------------------|
| `minor` | 1.0.0 ? 1.1.0 |
| `patch` | 1.0.0 ? 1.0.1 |
| `major` | 1.0.0 ? 2.0.0 (always gets its own PR) |

**Why group?** Without grouping, a project with 15 outdated npm packages
generates 15 simultaneous PRs. With grouping, those 15 become 1 PR per
ecosystem per week. Major version bumps always get their own PR because
they may contain breaking changes.

## Handling Dependabot PRs

| PR type | Recommendation |
|---------|---------------|
| Grouped (minor+patch) | Review quickly — these are low-risk. Consider enabling auto-merge. |
| Major version | Review carefully — may contain breaking changes. Test locally first. |
| Security alerts | Review immediately — Dependabot detected a known CVE. |

### Auto-merge strategy

For low-risk projects, enable auto-merge on grouped PRs:

1. Go to your repo **Settings** ? **General** ? **Automatically delete head branches**
2. Enable **Allow auto-merge** in your repo settings
3. On a grouped PR, click **Approve** ? **Enable auto-merge**

Only auto-merge grouped PRs. Never auto-merge major version updates without
manual review.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| No PRs appear | Verify `.github/dependabot.yml` is valid YAML. Check the **Dependabot** tab in your repo. |
| Too many PRs at once | Lower `open-pull-requests-limit` or ensure `groups:` is configured. |
| Wrong ecosystem detected | Ensure `package-ecosystem` matches your lockfile (npm vs pip). |