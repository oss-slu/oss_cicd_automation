# DroneWorld Project – Full CI/CD, Environment, and Docker Updates

## Status
**Proposed**

## Context
The DroneWorld project faced several issues during local and CI/CD builds:

- Backend Mac builds were failing, while Windows builds worked.
- Docker builds required proper Python/Node versions.
- Backend required AirSim settings.json, which needed a Google service account key.json.
- Frontend required Node ≥ 20.19.0 for Cesium/Resium compatibility.
- CI/CD pipelines were Windows-only and lacked Docker integration.
- Environment changes led to hardcoded modifications in ReportDashboard.jsx and Home.jsx to point to local AirSim URLs.

## Decision

### 1. Workflow / CI/CD Changes

**Backend CI:**

- Matrix OS support: ubuntu-latest and macos-latest.
- Python version explicitly set to "3.10" to prevent defaulting to 3.1.
- OS-specific system dependencies: apt-get for Ubuntu, brew for MacOS.
- Linting & formatting using flake8, black, autoflake; auto-fix enabled on push.
- Docker build and push to ghcr.io/imjusthenry/droneworld/backend:latest (Ubuntu only).
- GHCR permissions set to allow pushing packages.

**Frontend CI:**

- Matrix OS support: ubuntu-latest and macos-latest.
- Node.js version updated to 20.19.0.
- Ensured package-lock.json exists.
- Lint & formatting using eslint and prettier; auto-fix enabled on push.
- Docker build and push to ghcr.io/imjusthenry/droneworld/frontend:latest (Ubuntu only).

### 2. Docker / Local Development Changes

Backend:
Terminal command for windows to get docker backend to run. (replace the directory path with your own)
```
docker run -d --name droneworld-backend --network droneworld-net -p 5000:5000 \
  -v "C:/Users/{Name}/Documents/AirSim/settings.json:/root/Documents/AirSim/settings.json" \
  -v "C:/Users/{Name}/Documents/AirSim/key.json:/app/key.json" \
  ghcr.io/imjusthenry/droneworld/backend:latest
```
Frontend:
Terminal command for windows to get docker frontend to run. 
```
docker run -d --name droneworld-frontend --network droneworld-net -p 3000:80 droneworld-frontend
Docker ensures local builds match CI builds, providing consistency across environments.
```

### 3. Environment Changes
Added Google service account:

Created in GCP, downloaded key.json, and placed in AirSim folder.

Necessary for AirSim backend to generate settings.json and function correctly.

Hardcoded modifications in frontend for development:

ReportDashboard.jsx → points to local backend URL.

Home.jsx → points to local backend URL.

Environment version enforcement:

Ensured Python and Node versions explicitly match CI/CD configurations.

### 4. Key Benefits / Consequences
Positive outcomes:

Multi-OS CI/CD workflow ensures builds work on Ubuntu and Mac.

Dockerized backend and frontend simplifies local setup and deployment.

Linting and formatting checks improve code quality.

Explicit environment configuration prevents version mismatches.

Google service account integration enables AirSim to function.

Negative trade-offs / risks:

Docker builds limited to Ubuntu in CI; Mac only lint/format/test.

GHCR authentication required for Docker pushes.

Auto-fix and lint steps increase CI runtime slightly.

Hardcoding local URLs in frontend is temporary for development; may need refactoring for production.

## References
GitHub Actions workflows: .github/workflows/backend.yml, .github/workflows/frontend.yml

Docker documentation: https://docs.docker.com/get-started/

Google service account guide: https://cloud.google.com/iam/docs/creating-managing-service-accounts

GHCR push guide: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
