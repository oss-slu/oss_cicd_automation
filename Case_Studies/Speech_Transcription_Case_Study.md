# Case Study: Debugging and Improving the Windows Build of OSS SLU Speech Transcription Project

## 1. Overview
The **Speech Transcription Project** at SLU provides an open-source tool for transcribing speech audio into text to identify errors in children's speech.
As part of our role as internal CI/CD developers, we investigated and resolved recurring issues with the **Windows executable (.exe) build**.  
These failures prevented maintainers and contributors from reliably running the application outside of a development environment.

---

## 2. Problem Statement
The packaged `.exe` consistently crashed on Windows, while the application ran successfully using `python GUI.py` in development.  
This indicated the problem was **not with the core application code**, but with packaging, dependencies, and runtime environment setup.

---

## 3. Investigation
### Steps Taken
- **Windows Event Viewer**: Initial logs contained unrelated DCOM noise (ContentDeliveryManager).  
- **Command Prompt Execution**: Running the `.exe` directly revealed Python runtime/DLL errors and missing resource files.  
- **Local Reproduction**: Verified the app works in development mode and confirmed that the issue was specific to **PyInstaller builds**.

### Root Causes Identified
1. **Missing runtime data files**  
   - Packages like `pattern` and `lightning_fabric` depend on non-Python resources (e.g., `pattern/text/en/en-model.slp`, `lightning_fabric/version.info`) that PyInstaller did not bundle.  

2. **Mismatched Python DLLs**  
   - The packaged build sometimes looked for `python3x.dll` not present on the target system.  

3. **Native compilation issues**  
   - Packages like `webrtcvad` require MS Visual C++ Build Tools.  

4. **Missing FFmpeg**  
   - `pydub` raised warnings when `ffmpeg` was not found in `PATH`.  

---

## 4. Actions Taken
### Dependency Updates
- **requirements.txt**:  
  - Added inline comments for complex packages (`pattern`, `lightning_fabric`).  
  - Removed `wave`, which caused dependency conflicts with `mysql_python`.  

### Documentation Improvements
- **README.md**:  
  - Added a **“Known Issues and Packaging Notes”** section explaining why `.exe` builds fail on Windows and how to mitigate.  

### Build Process Fixes
- Created a clean Python 3.9 virtual environment (`venv39`).  
- Installed critical dependencies directly from GitHub when PyPI was outdated.  
- For `webrtcvad`, documented the need for Visual C++ Build Tools.  
- Rebuilt the `.exe` using **PyInstaller** with explicit `--add-data` commands for missing runtime files (pattern models, torch, torchaudio, etc.).  

### Logging & CI/CD Enhancements
- **GUI.py**: Added logging to write errors and runtime information to `app.log`.  
- **GitHub Actions Workflow**:  
  - Run the GUI and redirect output to `app.log`.  
  - Upload `app.log` as an artifact after each CI/CD run for easier debugging.  

---

## 5. Results & Impact
- **Debugging Simplified**: Maintainers can now review crash logs (`app.log`) from GitHub Actions without running the app locally.  
- **Stabilized Builds**: Dependency conflicts (e.g., `wave` → `mysql_python`) were resolved, improving `requirements.txt` reliability.  
- **Cross-Platform Notes**: Developers now have clear documentation for handling missing files, DLL mismatches, and package build requirements.  
- **Reproducibility**: Step-by-step setup instructions ensure future contributors can replicate our environment and fixes.

---

## 6. Challenges Faced
- Aligning PyInstaller with non-Python runtime resources.  
- Cross-platform differences (Windows requires `;` in `--add-data`, Linux/Mac use `:`).  
- Balancing automation with transparency: ensuring CI/CD logs provide enough detail without overwhelming contributors.

---

## 7. Lessons Learned
- **Logging is essential**: Capturing errors into `app.log` dramatically improved traceability.  
- **Dependencies must be curated**: Blindly packaging all requirements can introduce hidden conflicts.  
- **Documentation saves time**: Recording known issues and reproducible steps will help future contributors avoid repeating the same troubleshooting cycle.

---

## 8. Conclusion
Through systematic investigation, dependency management, logging improvements, and CI/CD workflow updates, we stabilized the Windows build process for this project.  
This case study demonstrates the importance of DevOps practices — even when core application logic remains unchanged, **a strong CI/CD pipeline ensures reliability, traceability, and accessibility for all contributors.**
