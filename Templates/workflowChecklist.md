# Workflow Template
- [ ] Workflow has a descriptive `name:` that explains its purpose
- [ ] Workflow triggers are defined under `on:` (push, pull_request, schedule, workflow_dispatch, etc.)
- [ ] Branch filters set appropriately (e.g., main, develop, feature branches)
- [ ] Optional: workflow can be manually triggered using `workflow_dispatch`

# Jobs
- [ ] At least one job exists with a clear, descriptive name
- [ ] Runner environment is defined (`ubuntu-latest`, `windows-latest`, `macos-latest`, or self-hosted)
- [ ] Optional: environment variables defined only if needed

# Steps
- [ ] Repository code is checked out (`actions/checkout`)
- [ ] Runtime setup included (Python, Node, .NET, Java, etc.)
- [ ] Dependencies installed (from `requirements.txt`, `package.json`, etc.)
- [ ] Optional: cache dependencies to speed up workflow (`actions/cache`)
- [ ] Tests or validation commands executed (unit tests, linting, security scan)
- [ ] Optional: build or compile artifacts created
- [ ] Optional: deploy or upload artifacts (`actions/upload-artifact`)

# Error Handling & Reliability
- [ ] Fail-fast behavior configured if needed (stop workflow on critical errors)
- [ ] Steps are clearly named to identify failures quickly in logs

# Secrets & Security
- [ ] Sensitive information stored in GitHub Secrets, not hardcoded
