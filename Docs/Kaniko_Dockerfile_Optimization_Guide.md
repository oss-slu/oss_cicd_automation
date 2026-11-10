# Multi-Stage Dockerfile Optimization Guide for In-Cluster Kaniko Builds

- **Authored by:** DevSecOps & Tech Lead Team
- **Date:** November 2026
- **Project:** OSS CI/CD Automation
- **Target repository:** `oss-slu/oss_cicd_automation`

## Table of Contents

- [Technical Mechanism: Kaniko vs. Docker/BuildKit](#technical-mechanism-kaniko-vs-dockerbuildkit)
- [Core Rules for Multi-Stage Dockerfiles](#core-rules-for-multi-stage-dockerfiles)
- [Practical Case Studies](#practical-case-studies)
- [Standardized Starter Templates](#standardized-starter-templates)
- [Checklist for In-Cluster Kaniko Readiness](#checklist-for-in-cluster-kaniko-readiness)

---

## Technical Mechanism: Kaniko vs. Docker/BuildKit

When building container images inside the bare-metal SLU Kubernetes cluster (`k8s-manifests/harbor-build`), builds are executed with **Kaniko** rather than a standard Docker or BuildKit engine.

Understanding how Kaniko processes multi-stage Dockerfiles is critical to preventing broken builds and cluster resource bloat:

- **Docker/BuildKit (target tree pruning):** Modern Docker engines evaluate multi-stage Dockerfiles lazily. When a `--target` flag is passed, BuildKit analyzes the stage dependency graph and skips unreferenced or sibling build stages.
- **Kaniko (sequential layer execution):** Kaniko executes instructions across **all preceding and sibling stages in sequential order**, regardless of whether `--target` is specified. If an early or unused stage in a monolithic Dockerfile fails or pulls heavy dependencies, the entire build fails.

This behavior directly caused build failures in `rpc-mesh` (where an unreferenced audio stage broke the text-only worker build) and storage bloat in `mdma` and `shelter-volunteers`.

> [!NOTE]
> Recent Kaniko releases offer an opt-in `--skip-unused-stages` flag. Do not rely on it unless the cluster's build configuration enables it. The rules below keep builds safe either way.

---

## Core Rules for Multi-Stage Dockerfiles

### 1. Maintain a Strict Linear Hierarchy

Avoid branching or parallel stages where unused branches contain heavy, native, or fragile system dependencies. Structure stages so that each stage directly feeds the next in a single, predictable linear chain.

### 2. Prefer Dedicated Single-Target Dockerfiles

When client and server (or worker and API) dependencies diverge significantly, **do not write a monolithic multi-target Dockerfile**. Create separate, focused Dockerfiles instead (for example, `client.Dockerfile` and `server.Dockerfile`).

### 3. Minimize Base Layer Dependencies

Avoid generic heavy images such as `ubuntu:latest` or the standard `python:3.12`. Standardize on minimal distributions such as `python:3.12-slim` or `node:lts-alpine` to reduce the attack surface and prevent node-local storage bloat.

### 4. Standardize the Build-to-Production Pattern

Strictly isolate compile-time tooling (`build-essential`, `g++`, `npm`, full SDKs) in intermediate build stages. Copy only compiled binaries, assets, or wheel artifacts into the clean production runtime stage.

---

## Practical Case Studies

### Case Study 1: `rpc-mesh` Multi-Stage Refactoring

- **Problem:** The original Dockerfile contained a non-linear stage installing `ffmpeg` and 150+ heavy audio/multimodal packages. When building the text-only GPU worker with `--target text-worker`, Kaniko still executed the audio stage and failed on missing multimedia headers.
- **Solution:** The unused audio stages were moved into a dedicated `audio-worker.Dockerfile`, which shortened text-worker build times and removed 150+ unnecessary system packages.

### Case Study 2: `mdma` Monolith Split

- **Problem:** A monolithic `Dockerfile` defined both Node.js frontend asset compilation and Python/FastAPI backend stages. Kaniko pulled both Node and Python base images for every build target.
- **Solution:** The file was split into `apps/web/Dockerfile` and `apps/api/Dockerfile`, allowing Kaniko to build each image independently without cross-contaminating cache layers.

---

## Standardized Starter Templates

### Template A: Python / FastAPI Backend

```dockerfile
# Stage 1: Build stage for dependency compilation
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Minimal production runtime
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/install/bin:${PATH}" \
    PYTHONPATH="/install/lib/python3.12/site-packages"

COPY --from=builder /install /install
COPY . .

USER nobody

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Template B: Node.js / React Frontend

```dockerfile
# Stage 1: Dependency installation and build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Unprivileged Nginx production runtime
FROM nginxinc/nginx-unprivileged:alpine AS runner

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# nginx.conf must listen on 8080 (non-root users cannot bind to port 80)
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
```

> [!IMPORTANT]
> The unprivileged Nginx image listens on port `8080`. Update your `nginx.conf` (`listen 8080;`) and any Kubernetes Service or Ingress `targetPort` accordingly.

---

## Checklist for In-Cluster Kaniko Readiness

Copy this checklist into your pull request description.

- [ ] **Stage structure:** Dockerfile follows a strict linear build sequence with no unreferenced branches.
- [ ] **Separation:** Diverging app components use dedicated Dockerfiles (`client.Dockerfile`, `server.Dockerfile`).
- [ ] **Base images:** Minimal base images (`python:3.12-slim`, `node:lts-alpine`) are used.
- [ ] **Build isolation:** Heavy build tools (`build-essential`, `npm`) are excluded from the final image stage.
- [ ] **Security:** Final runtime layer runs as a non-root user (`USER nobody` or equivalent).