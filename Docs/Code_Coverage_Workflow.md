# Code Coverage PR Reporter Workflow

This guide explains how to adopt the reusable code coverage workflow from
`Templates/testing/` to automatically post coverage summaries as comments
on pull requests.

## What it does

The workflow runs your test suite with coverage enabled, parses the coverage
output file, and posts a formatted comment on the PR:

| Metric | Value |
|--------|-------|
| Coverage | 85.23% |
| Lines Covered | 1234 |
| Total Lines | 1448 |

The comment updates idempotently — subsequent pushes to the same PR update
the existing comment rather than creating new ones.

## Supported Coverage Formats

| Format | Package Manager | Output File | Template |
|--------|----------------|-------------|----------|
| Cobertura XML | Python (pytest-cov) | `coverage.xml` | `coverage-python-caller.yml` |
| lcov.info | Node.js (Jest) | `lcov.info` | `coverage-jest-caller.yml` |
| Go coverage | Go | `coverage.out` | `coverage-go-caller.yml` |

## Adoption steps

### Python (pytest-cov)

1. Install pytest-cov:

   ```bash
   pip install pytest-cov
   ```

2. Copy the template:

   ```bash
   cp Templates/testing/coverage-python-caller.yml .github/workflows/coverage.yml
   ```

3. Adjust the test command if needed (e.g., add specific test paths).

### JavaScript / TypeScript (Jest)

1. Ensure Jest is configured in your project:

   ```bash
   npm install --save-dev jest
   ```

2. Add a test script to `package.json`:

   ```json
   "scripts": {
     "test": "jest --coverage --coverageReporters=lcov"
   }
   ```

3. Copy the template:

   ```bash
   cp Templates/testing/coverage-jest-caller.yml .github/workflows/coverage.yml
   ```

### Go

1. Copy the template:

   ```bash
   cp Templates/testing/coverage-go-caller.yml .github/workflows/coverage.yml
   ```

2. The workflow automatically runs `go test -coverprofile`.

## Customizing the workflow

### Change the coverage file path

If your coverage file is in a different location, edit the `coverage_file` input:

```yaml
with:
  coverage_file: reports/coverage.xml
```

### Change the comment header

```yaml
with:
  comment_header: "## My Custom Coverage Report"
```

### Run on specific paths only

The templates already include path filters. To customize:

```yaml
on:
  pull_request:
    paths:
      - 'src/**'
      - 'tests/**'
```

## Security notes

- The workflow uses `permissions: contents: read` and `pull-requests: write`
  (least privilege).
- All actions are pinned to immutable commit SHAs.
- No external tokens are required — uses the built-in `GITHUB_TOKEN`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Comment not posting | Check that `pull-requests: write` is set in permissions. |
| Coverage shows 0% | Verify the coverage file exists at the specified path. |
| Multiple comments appearing | Ensure the reusable workflow uses the same `header` value so sticky-comment updates the existing one. |