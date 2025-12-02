# OSS SLU Mouser Project – CI/CD Environment Investigation and Build Stabilization

## Status  
Completed

---

## 1. Context  
The **OSS SLU Mouser Project** is a Python-based application used within SLU’s Open Source community for hardware communication and audio processing tasks. During this sprint, the project faced several **environment, dependency, and CI/CD challenges** that prevented consistent testing, installation, and `.exe` build generation.

### Key Issues Identified  
- Python version inconsistencies (project built for Python 3.9; contributors using 3.11–3.13+).  
- The package **`playsound` failed to build** on newer Python versions.  
- Test failures were due to **import path issues**, not faulty logic.  
- No existing workflow generated installable **Windows executables**.  
- Maintainers required a **safe, non-production-impact** CI workflow for experimentation.

---

## 2. Decision  

### 2.1 CI/CD Workflow Enhancements  
A new **sandbox workflow** was introduced to safely test `.exe` builds without impacting production.

#### Sandbox Workflow Features  
- New file: `.github/workflows/build-windows-sandbox.yml`  
- Runs on **Windows runners only**, isolated from production branches.  
- Uses Python **3.11** for broader compatibility.  
- Builds using **PyInstaller** with metadata and resource bundling.  
- Uploads `.zip` artifacts for maintainers to download.  
- Gracefully bypasses `playsound` install errors using `playsound3`.

#### Purpose of the Sandbox Workflow  
- Prevent breaking production code.  
- Allow maintainers to experiment with installer builds.  
- Provide downloadable artifacts for manual validation.

---

### 2.2 Environment Investigation  
A thorough audit of the development environment revealed:

- **`playsound` is incompatible** with Python 3.13 (fails to build wheels).  
- Replacing it with **`playsound3`** resolves installation failures.  
- All other libraries installed correctly (`pyaudio`, `customtkinter`, `CTkMessageBox`, etc.).  
- Test failures stemmed from **relative import paths**, not application bugs.  
- Application launches successfully using `python main.py` 


All findings were documented in `docs/env_investigation.md`.

---

### 2.3 Workflow Integration  
Two workflow files now manage CI:

#### `build-windows.yml`  
- Production-oriented workflow  
- Uses maintainers' reusable workflow (`build-reusable.yml`)  
- Validates builds on PRs and pushes  

#### `build-windows-sandbox.yml`  
- Safely tests installer builds  
- Uploads artifacts without affecting production  
- Useful for iterative debugging and experimentation  

---

## 3. Implementation Summary  

### Key Updates Made  
- Added **playsound3** to `requirements.txt` to replace legacy `playsound`.  
- Created a **sandbox CI workflow** for safe Windows build testing.  
- Configured PyInstaller with  
- `--onedir` packaging  
- image/sound data collection (`shared/images`, `shared/sounds`)  
- metadata handling for dependencies (`tqdm`, `regex`, `sacremoses`, etc.)  
- Implemented artifact upload for `.zip` builds.  
- Documented all environment findings and reproducible steps.

---

## 4. Results and Impact  

### Positive Results  
- CI/CD now safely attempts Windows installer builds without affecting production code.  
- Dependency installation is stable after switching to `playsound3`.  
- Contributors can use the sandbox workflow to **download build artifacts** for validation.  
- Documentation clarifies environment expectations (Python versions, imports, etc.).  
- Template serves as a reusable pattern for other SLU OSS projects.

### Remaining Limitations  
- `.exe` builds still require manual validation.  
- PyInstaller paths may need OS-specific refactoring.  
- Sandbox workflow does not yet upload full logs for release-style debugging.

---

## 5. Future Recommendations  

To achieve a fully stable and production-ready installer pipeline, follow-up work should include:

- Creating a **production-tier Windows installer workflow** with versioning.  
- Adding **post-build smoke tests**, such as launching the `.exe` and verifying dependencies.  
- Introducing automated pre-checks for import path validity.  
- Adding Linux/macOS builds for cross-platform packaging.  
- Refactoring dependency management to a **locked environment** using  
- `requirements.freeze.txt`, or  
- `pip-tools` / `uv`  
- Integrating with the OSS CI/CD reusable workflows across SLU.

---

## 6. References  

- **Workflows:**  
- `.github/workflows/build-windows.yml`  
- `.github/workflows/build-windows-sandbox.yml`  

- **Documentation:**  
- `docs/env_investigation.md`  
- `README.md`  

- **External Resources:**  
- PyInstaller – https://pyinstaller.org  
- GitHub Actions Artifacts – https://docs.github.com/en/actions  
- playsound3 – https://pypi.org/project/playsound3/  

---

