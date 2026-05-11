# Kubernetes Deployment Infrastructure for PAO Surgery Simulator

**Project:** PAO Surgery Simulator (`oss-slu/pao_surgery_simulator`)  
**Author:** Justin Duong
**Last Updated:** May 10, 2026

---

## Overview

This document describes the Kubernetes deployment infrastructure created for the PAO Surgery Simulator web application. The work covers the containerization of both application components, the creation of Kubernetes manifests following existing `oss-slu` conventions, and the implementation of a GitHub Actions workflow that automates the full build and deployment pipeline on every push to `main`.

---

## Background

PAO Surgery Simulator is a web application consisting of a React frontend and a Python Flask backend API, backed by a PostgreSQL database. Prior to this work, neither the frontend nor backend had been configured for deployment to a Kubernetes cluster.

---

## Dockerfiles

Two Dockerfiles were created to containerize the application components.

**`frontend/Dockerfile`** packages the React frontend using a multi-stage build. The first stage installs dependencies and runs `npm run build` to compile the application. The second stage copies only the compiled output into a clean image and serves it via `http-server` on port 3000. A multi-stage build is used here — unlike the DigitalBoneBox frontend — because React requires a build step before the static assets can be served.

**`backend/Dockerfile`** packages the Flask API. It uses a `python:3.11-slim` base image, installs dependencies from `requirements.txt`, and runs `app.py` on port 5000. The build context is scoped to the `backend/` directory, which is self-contained with its own requirements and entrypoint.

---

## Kubernetes Manifests

**`frontend-deployment.yaml`** defines a Deployment running one replica of the frontend container and a ClusterIP Service exposing it on port 3000 within the cluster.

**`backend-deployment.yaml`** defines a Deployment running one replica of the backend container and a ClusterIP Service exposing it on port 5000 within the cluster.

**`postgres-statefulset.yaml`** defines a Deployment running one replica of the `postgres:14` image and a ClusterIP Service exposing it on port 5432 within the cluster. Unlike the frontend and backend, Postgres uses the public Docker Hub image and does not require an image pull secret.

All manifests use `ghcr-secret` as the image pull secret where applicable, set `imagePullPolicy: Always` to ensure the latest pushed image is used on each pod restart, and deploy into the `pao-surgery-simulator` namespace.

---

## GitHub Actions Workflow

A single `build.yml` workflow was created in `.github/workflows/` to handle the full build and deployment pipeline. It runs on every push to `main` and consists of two jobs.

The **`build` job** uses a matrix strategy to build and push both Docker images to GHCR in parallel. Each image is tagged with a short SHA (`sha-a1b2c3d`), a `latest` floating tag pointing to the most recent `main` build, and a version tag on git tag pushes. Building in parallel via the matrix reduces total workflow time compared to sequential builds.

The **`update-manifests` job** runs after both matrix builds succeed. It checks out `oss-slu/k8s-manifests`, patches the image tag in both the frontend and backend manifest files to the current commit's short SHA using `sed`, and commits the change back. This keeps the manifests repository in sync with what was built, maintaining a GitOps record of exactly what is running in the cluster. Postgres is not patched here as it uses a fixed public image tag rather than a build artifact.

---

## Docker Compose

A `docker-compose.yml` is included at the repo root to support local development. It builds and runs all three services — frontend, backend, and Postgres — using the same Dockerfiles, with the frontend depending on the backend and the backend depending on the database. This mirrors the behaviour of running the services manually and allows contributors to test the fully containerized application locally without needing access to the cluster.

---

## Outstanding Items

One item must be configured before the workflow can run end-to-end: a `K8S_MANIFESTS_TOKEN` GitHub Personal Access Token with write access to `oss-slu/k8s-manifests` must be added to the repository secrets. This is required by the `update-manifests` job to commit image tag changes back to the manifests repository. A `KUBECONFIG` secret is also required for any direct `kubectl` operations against the cluster.
