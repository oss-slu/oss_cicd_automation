# DigitalBoneBox Audit Report

## Status
Proposed

## Context
- The **DigitalBoneBox** project is a web-based study tool for human anatomy, originally adapted from a PowerPoint resource.  
- The project stack includes **Node.js, HTMX, HTML, CSS**.  
- Current repository state:  
  - **CI/CD**: Only a `lint.yml` GitHub Actions workflow exists; no build/test/deploy workflows.  
  - **Testing**: No structured `tests/` folder; a single `templates/test.js` exists but is not connected to any framework. No unit, integration, security, or end-to-end tests.  
  - **Linting/Static Analysis**: `eslint.config.js` exists; linting workflow present but limited.  
  - **Security**: No dependency scanning (`npm audit`, Dependabot) or CodeQL.  
  - **Deployment**: No Dockerfile, docker-compose, or deployment workflows.  
  - **Docs**: CONTRIBUTING.md and GitHub issue/PR templates exist.  
  - **Other Observations**: Monorepo-style setup with `boneset-api` (backend) and frontend together, run concurrently with `npm start`.  

Constraints & Challenges:  
- Sprint #2 closes on **Oct 6**, so only limited time is available.  
- Full test coverage, containerization, and deployment are valuable but may be out of scope for this sprint.  

## Decision
We will begin by introducing **foundational CI/CD improvements** in this sprint:  
1. Add a `tests/` folder and configure **Jest** as the test framework.  
2. Write at least one **sample unit test** to validate the setup.  
3. Extend the existing GitHub Actions workflow to:  
   - Install dependencies  
   - Run linting  
   - Run tests  
4. Deliver this work on or before Oct 6 (sprint close).  

Alternative options considered:  
- Adding integration/E2E tests immediately — deprioritized due to time constraints.  
- Containerization and deployment — postponed to future sprints.  
- Security scans (Dependabot, CodeQL) — postponed to future sprints.  

## Consequences
**Positive Outcomes**  
- Establishes a testing foundation that future contributors can build upon.  
- Expands CI/CD from “lint-only” to “lint + tests,” improving reliability.  
- Provides immediate, demonstrable progress for Sprint #2 deliverables.  

**Negative Trade-offs / Risks**  
- Limited test coverage initially (only 1–2 sample tests).  
- Security, deployment, and broader developer experience improvements remain unaddressed until later sprints.  

## References
- Project repository: [DigitalBoneBox](https://github.com/oss-slu/DigitalBonesBox)  
- Sprint #2 deadline: Oct 6  
- Tools referenced: Jest (testing), ESLint (linting), GitHub Actions (CI/CD), Dependabot/CodeQL (future security scanning)  
