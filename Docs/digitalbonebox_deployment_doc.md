# Kubernetes Deployment Infrastructure for DigitalBoneBox

**Project:** DigitalBoneBox (`oss-slu/DigitalBoneBox`)  
**Author:** Justin Duong
**Last Updated:** May 10, 2026

---

## Overview

This document describes the Kubernetes deployment infrastructure created for the DigitalBoneBox web application. The work covers the containerization of both application components, the creation of Kubernetes manifests following existing `oss-slu` conventions, and the implementation of a GitHub Actions workflow that automates the full build and deployment pipeline on every push to `main`.

---

## Background

DigitalBoneBox is a Node.js web application consisting of two components: a static HTML/HTMX frontend served by `http-server`, and a backend Express API (`boneset-api`). Prior to this work, neither component had been containerized or configured for deployment to a Kubernetes cluster.

---

## Dockerfiles

Two Dockerfiles were created to containerize the application components.

**`templates/Dockerfile`** packages the frontend. It installs dependencies from the root `package.json` — where `http-server` lives — and copies the `templates/` directory into the image, serving it on port 8080. The build context is the repo root rather than the `templates/` subdirectory because `http-server` is not a dependency scoped to that folder.

**`boneset-api/Dockerfile`** packages the API. Since `boneset-api/` is self-contained with its own `package.json` and `server.js` entrypoint, the build context is scoped to that directory alone. The container runs the Express server on port 3000.

---

## Kubernetes Manifests

**`frontend.yaml`** defines a Deployment running one replica of the frontend container and a ClusterIP Service exposing it on port 8080 within the cluster.

**`api.yaml`** defines a Deployment running one replica of the API container and a ClusterIP Service exposing it on port 3000 within the cluster.

Both manifests use `ghcr-secret` as the image pull secret, set `imagePullPolicy: Always` to ensure the latest pushed image is used on each pod restart, and deploy into the `digitalbonebox` namespace.

---

## GitHub Actions Workflow

A single `build.yml` workflow was created in `.github/workflows/` to replace the previously separate per-component build files. It runs on every push to `main` and consists of two jobs.

The **`build` job** uses a matrix strategy to build and push both Docker images to GHCR in parallel. Each image is tagged with a short SHA (`sha-a1b2c3d`), a `dev` floating tag pointing to the latest `main` build, and a version tag on git tag pushes. Building in parallel via the matrix reduces total workflow time compared to sequential builds.

The **`update-manifests` job** runs after both matrix builds succeed. It checks out `oss-slu/k8s-manifests`, patches the image tag in both manifest files to the current commit's short SHA using `sed`, and commits the change back. This keeps the manifests repository in sync with what was built, maintaining a GitOps record of exactly what is running in the cluster.

---

## Docker Compose

A `docker-compose.yml` was added at the repo root to support local development. It builds and runs both containers using the same Dockerfiles, with the frontend depending on the API starting first — mirroring the behaviour of `npm run dev`. This allows contributors to test the containerized application locally without needing access to the cluster.

---

## Outstanding Items

One item must be configured before the workflow can run end-to-end: a `K8S_MANIFESTS_TOKEN` GitHub Personal Access Token with write access to `oss-slu/k8s-manifests` must be added to the repository secrets. This is required by the `update-manifests` job to commit image tag changes back to the manifests repository. A `KUBECONFIG` secret is also required for any direct `kubectl` operations against the cluster.
