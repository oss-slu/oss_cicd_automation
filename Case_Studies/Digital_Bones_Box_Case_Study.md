# Case Study: Establishing foundational CI/CD infrastructure for the Digital Bones Box project

## 1. Overview
The **Digital Bone Box project** is a web-based anatomy study tool designed to provide students with quick, mobile-friendly access to annotated bone images originally created in a PowerPoint-based resource by Prof. Brian Elliott. The project is built using **Node.js**, **HTMX**, **HTML**, and **CSS**, with a monorepo structure containing both frontend and backend components.

As part of the OSS-SLU CI/CD team, our task was to audit, modernize, and lay the groundwork for a maintainable CI/CD pipeline. The project previously lacked foundational testing, structured automation, or security checks. This case study documents our investigation, improvements, and next steps.

---

## 2. Problem Statement
The Digital Bone Box repository initially had:

- No automated tests (unit, integration, or end-to-end).
- Only one GitHub Action, a basic linting workflow.
- No test framework, meaning changes could not be validated automatically.
- No CI/CD structure to ensure reliability, prevent regressions, or guide contributors.
- Existing test-like files (templates/test.js) that were incompatible with Jest or Node environments.
- Missing containerization, security scanning, dependency monitoring, and deployment workflows.

These gaps made it difficult for contributors to ensure code quality, detect breakages early, or participate in structured DevOps practices.

---

## 3. Investigation
### Steps Taken
- **Repository Audit**: Reviewed project structure, scripts, GitHub workflows, folders, and existing test files.
Identified major CI/CD gaps and documented them in an ADR-formatted audit report.
- **Cloning and Local Testing**: Cloned the repo locally and ran the backend to understand the API routes, helper methods, and server structure.
- **Test Environment review**: Located a legacy `templates/test.js` file containing browser-dependent tests, which repeatedly failed under Jest.
- **Workflow Analysis**: Studied existing GitHub Actions workflows and validated their behavior (e.g., lint.yml).

### Root Causes Identified
1. No testing framework (e.g., Jest, Mocha).
2. No `tests/` directory or testing conventions.
3. No build or deployment workflows.
4. Legacy test files incompatible with Node/Jest.
5. Mixed ES module and CommonJS syntax in the frontend/JS code.
6. Linting existed but was limited to a single workflow and lacked formatting enforcement. 

---

## 4. Actions Taken
### CI/CD Foundation
- Installed and configured **Jest** as the testing framework.
- Added a structured `tests/` directory with a sample test to confirm CI pipeline execution.
- Updated package.json to include Jest scripts. 

### GitHub Actions Improvements
Extended the existing `lint.yml` workflow to:

- Install dependencies
- Run ESLint
- Run Jest tests

Ensured the workflow successfully executes on push and pull_request events to main. 

### Code Quality Fixes
- Corrected ESLint errors in server and test files (e.g., quote style, missing semicolons).
- Added a test-safe server startup pattern using `if (require.main === module)`.

### Documentation
Created an **ADR-style audit report** outlining:

- Current CI/CD gaps
- Recommended next steps
- Long-term testing and automation roadmap 

---

## 5. Results & Impact
- Automated testing now works across CI via **Jest + GitHub Actions**.
- Linting and testing run automatically on each PR, ensuring code quality.
- Sample tests verify the framework for future contributors.
- Legacy test failures are now isolated, documented, and no longer block CI foundation work.
- A CI/CD roadmap now exists for future developers to expand upon.

These changes transform the project from **manual-only** to **automation-ready**, enabling sustainable development and cleaner collaboration.

---

## 6. Challenges Faced
- Legacy DOM-based tests `templates/test.js` failed under Jest; they require a browser-like environment.
- Merge conflicts in server.js caused by upstream code changes required careful resolution.
- Determining which helper functions still existed or were removed required reviewing evolution of backend code.
- Ensuring tests could run without starting the live server required restructuring Express initialization

---

## 7. Lessons Learned
- CI/CD must be built iteratively: lint → test → security → deployment.
- Legacy code may not fit modern testing frameworks, requiring phased refactoring.
- Clear documentation accelerates collaboration, especially with multiple maintainers.
- Testable server design (exporting app without starting the server) is essential for backend test automation.

---

## 8. Conclusion
Through systematic auditing, automation setup, documentation, and code-quality improvements, this sprint delivered a strong CI/CD foundation for the Digital Bone Box project.
Although full test coverage, integration tests, and security workflows remain future goals, the essential groundwork is now in place.

This case study demonstrates how strategic CI/CD enhancements can significantly improve reliability and maintainability even without altering core application logic, reinforcing the value of DevOps practices in academic and open-source environments.