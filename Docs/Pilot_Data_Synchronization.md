Audited by: Thomas Pautler  Date: March 19, 2026

Project: PilotDataSynchronization  Repository: `oss-slu/PilotDataSynchronization`

## Workflow Overview

There are two workflows in `.github/workflows/` — `meson-build.yml` and `super-linter.yml`.

`meson-build.yml` handles the C++ build for `xplane_plugin` on Windows. It sets up Python, installs meson and ninja from `ci_requirements.txt`, then runs `meson setup` and `meson compile`. It triggers on push and pull request to any branch, plus `workflow_dispatch`. There are path filters for `.cpp` and `.h` files but they're commented out, so the workflow runs on every push regardless of what changed. A test step and artifact upload are also in the file but commented out — the infrastructure is there, it just isn't running.

`super-linter.yml` runs on push and pull request to `main`. It validates C++ formatting with clang-format, checks GitHub Actions YAML syntax, and validates YAML files. Auto-fix is enabled for clang-format and it commits fixes back using `stefanzweifel/git-auto-commit-action`. There are commented-out entries for Markdown and YAML Prettier — a note in the file says the team still needs to discuss those.

What's currently running in CI:
* Windows C++ build (Meson + Ninja)
* C++ formatting checks with auto-fix (clang-format)
* GitHub Actions and YAML validation
* `workflow_dispatch` on both workflows
* Auto-commit of lint fixes

What isn't covered:
* No Rust CI at all — `relay` is never built or tested
* Tests exist but don't run — the meson test step is commented out
* Only Windows builds — Ubuntu and macOS jobs are commented out in `meson-build.yml`
* No dependency caching (pip or Cargo)
* No artifact upload when builds fail
* No Dependabot or dependency scanning
* No branch protection requiring CI to pass before merge

## Workflow Template Compliance Checklist

| Category | Criteria | Status | Notes |
|---|---|---|---|
| General Setup | Workflow exists in `.github/workflows/` | ✅ Implemented | 2 workflows found |
| General Setup | Workflow triggers (`on:`) defined | ✅ Implemented | push, pull_request, workflow_dispatch on both |
| General Setup | Branch filters configured | ⚠️ Partial | super-linter targets main; meson-build has no branch filter; path filters commented out |
| General Setup | Manual trigger (`workflow_dispatch`) | ✅ Implemented | Both workflows |
| Jobs | Jobs have descriptive names | ✅ Implemented | "Build and Test on Windows with Meson" |
| Jobs | Runner environment defined | ✅ Implemented | windows-latest / ubuntu-latest |
| Jobs | Job dependencies (`needs:`) | ❌ Missing | No job sequencing |
| Steps | Repository checkout included | ✅ Implemented | actions/checkout@v4 in both |
| Steps | Runtime setup (Python) | ✅ Implemented | actions/setup-python@v5 in meson-build |
| Steps | Runtime setup (Rust) | ❌ Missing | No Rust setup anywhere; relay not in CI |
| Steps | Dependencies installed | ✅ Implemented | pip install -r ci_requirements.txt |
| Steps | Build executed | ✅ Implemented | meson setup + meson compile on Windows |
| Steps | Tests executed | ❌ Missing | Test step commented out; no cargo test |
| Steps | Dependency caching | ❌ Missing | Nothing cached |
| Steps | Artifact upload on failure | ❌ Missing | Commented out in meson-build.yml |
| Linting | C++ formatting (clang-format) | ✅ Implemented | Auto-fix on |
| Linting | Rust linting (clippy / rustfmt) | ❌ Missing | Not in either workflow |
| Linting | YAML and GitHub Actions | ✅ Implemented | VALIDATE_YAML and VALIDATE_GITHUB_ACTIONS enabled |
| Linting | Markdown / YAML Prettier | ⚠️ Partial | Commented out, pending team discussion |
| Error Handling | Fail-fast and logging | ⚠️ Partial | No explicit configuration |
| Error Handling | Test log upload on failure | ❌ Missing | Commented out |
| Security | Dependency scanning | ❌ Missing | No cargo audit or equivalent |
| Security | Dependabot | ❌ Missing | No dependabot.yml |
| Build & Deployment | Multi-platform build | ⚠️ Partial | Windows only; Ubuntu and macOS commented out |
| Build & Deployment | Release / artifact generation | ❌ Missing | No release workflow |
| Documentation | CI documentation | ⚠️ Partial | README covers supported versions but no CI guide |
| Documentation | Inline workflow comments | ✅ Implemented | Both files have notes and TODOs |
| Documentation | CONTRIBUTING.md | ✅ Implemented | Present and thorough |

## Overall Assessment

The repo is in better shape than projects with no CI at all, but there are some real gaps. The biggest issue is that `relay` — the Rust crate that handles all the data transmission to iMotions — has zero CI coverage. It's never built or tested on any PR. If something breaks in there it won't surface until someone runs it locally.

The C++ side is partially covered but the test step is commented out. GoogleTest is already set up in `meson.build` and `test_threading_tools` is a defined target, so the tests exist — they just aren't running in CI. That's an easy fix.

Multi-platform is another gap. Only the Windows build job is active. The Ubuntu cross-compile job is in the file but commented out, and macOS isn't there at all. Given the plugin has a macOS source file (`pilotdatasync-xp11.macos.cpp`) this matters.

On the positive side, the linting setup is solid. clang-format auto-fix with auto-commit is a nice workflow for contributors. The contributor docs are detailed and the issue/PR templates are set up well.

Without resolving the gaps above:
* Regressions in `relay` won't be caught before merge
* C++ threading bugs can ship since tests never run
* No dependency updates or vulnerability alerts
* Merges to `main` can bypass any CI failure since there are no branch protection rules

## Recommended Enhancements

**1. Uncomment the Meson test step**

This is the lowest-effort change with immediate value. The test executable is already defined, GoogleTest is already a subproject, it just needs to be uncommented. Also uncomment the artifact upload so the test log is saved when things fail.

**2. Add a Rust CI job for `relay`**

This is the most important missing piece. A job that runs `cargo build`, `cargo test`, `cargo clippy`, and `cargo fmt --check` inside `relay/` would cover the entire Rust side. The `.rust-toolchain.toml` already pins stable so toolchain setup is one action step with `dtolnay/rust-toolchain@stable`.

**3. Add dependency caching**

`relay/Cargo.lock` is committed so Cargo cache keys are stable. Same for `ci_requirements.txt`. Adding `actions/cache@v4` for both would cut down build times noticeably, especially on the Cargo side.

**4. Restore the Ubuntu build job**

It's already written in `meson-build.yml`, just commented out. The `lin-to-win.ini` cross-file is in the repo. Restoring it makes the Windows plugin buildable on Linux, which is useful for contributors who aren't on Windows.

**5. Enable Dependabot**

`relay/Cargo.toml` has several wildcard version constraints (`iced = "*"`, `anyhow = "*"`) which makes it hard to reason about what's actually being pulled in. A `dependabot.yml` covering Cargo, pip, and GitHub Actions would at least surface updates.

**6. Set up branch protection on `main`**

Require the meson-build and super-linter checks to pass before merging. Once the Rust job is added, add that too. Right now nothing stops a PR from merging while CI is red.

**7. Enable Prettier for Markdown and YAML**

The super-linter workflow already has the variables for this, just commented out. Once the team agrees it's worth doing, it's four lines to uncomment.

## Final Evaluation

The project has working CI but it isn't covering the full codebase yet. The Rust side needs a job and the C++ tests need to be turned on — those two things would make a big difference. Everything else is incremental improvement.

Fine to include on the CI/CD dashboard, but should be marked as partial until at least the relay CI job and the test step are active.