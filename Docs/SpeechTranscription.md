# Use Local Windows Build Workflow & Refactor PyInstaller Steps

## Status
Accepted

## Context
- The original release workflow called the Windows build via a fixed external branch (`oss-slu/SpeechTranscription/.github/workflows/windows-build.yml@build_fixes_copy`), which made iteration and debugging difficult.  
- The Windows build workflow (`windows-build.yml`) had outdated Python installation steps, redundant package installs, and manual file moves.  
- Several dependencies required explicit installation, and crash logs for the GUI were not fully captured in a structured way.  
- The previous PyInstaller command was less modular and relied on multiple separate `--copy-metadata` and `--collect-data` options with redundant manual folder operations.

## Decision
- Update `release.yml` to use the **local `windows-build.yml`** instead of referencing an external repository branch.  
- Refactor `windows-build.yml` to:
  - Use `workflow_call` for reusable workflows.  
  - Simplify Python setup and caching.  
  - Install system dependencies (e.g., ffmpeg, PyAudio) cleanly.  
  - Initialize Git submodules correctly.  
  - Remove obsolete `typing` package gracefully.  
  - Consolidate PyInstaller options, including `--add-data` and `--collect-data`, and specify `--hidden-import` for necessary packages.  
  - Run the GUI headless to capture logs and upload logs as artifacts (`SpeechTranscription_windows_logs`).  
- Preserve release workflow steps for packaging artifacts (`.zip`) and creating GitHub releases.

**Alternative options considered but not chosen:**
- Continue referencing the external branch for Windows builds (harder to maintain, slower iteration).  
- Keep manual post-build copying and artifact handling (less robust, error-prone).  

## Consequences
**Positive outcomes (benefits):**
- Simplifies CI/CD workflow by making Windows build workflow self-contained.  
- Easier debugging with headless GUI logs uploaded as artifacts.  
- More robust PyInstaller packaging with proper inclusion of dependencies.  
- Reusable workflow via `workflow_call` in future pipelines.  
- Reduces risk of inconsistent builds from external branches.  

**Negative trade-offs or risks:**
- Local workflow must be maintained; errors here affect all future releases.  

## References
- Pull Request #269: [https://github.com/oss-slu/SpeechTranscription/pull/269](https://github.com/oss-slu/SpeechTranscription/pull/269)
- GitHub release workflow: `release.yml`  
- Windows build workflow: `windows-build.yml`  
- PyInstaller documentation: [https://pyinstaller.org](https://pyinstaller.org)  
- GitHub Actions workflow_call: [https://docs.github.com/en/actions/using-workflows/reusing-workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
