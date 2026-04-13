# OSS-SLU Reusable Docker CI Template

---

## Overview

This repository provides a **reusable GitHub Actions workflow template** for building and pushing Docker images across OSS-SLU projects.

The goal of this template is to eliminate duplicated CI/CD logic and provide a standardized, scalable Docker build pipeline that can be reused across multiple repositories.

The workflow supports:
- Docker image builds using Buildx
- Automated publishing to GitHub Container Registry (GHCR)
- Parameterized configuration for flexible usage across repositories
- Reusable invocation via GitHub Actions `workflow_call`

---

## What This Template Does

This reusable workflow handles the full Docker CI pipeline:

### Core Functions
- Builds Docker images using Docker Buildx
- Authenticates with GitHub Container Registry (GHCR)
- Tags images automatically (SHA-based + latest tag)
- Pushes built images to `ghcr.io`
- Supports configurable Dockerfile paths and build contexts
- Enables reuse across multiple repositories without duplication

---

## How to Use This Template

### 1. Add the reusable workflow to your CI templates repository

The workflow should be stored in a central repository under:

.github/workflows/docker-build-push.ymlS