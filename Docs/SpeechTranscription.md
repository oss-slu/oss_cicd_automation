# SPEECH TRANSCRIPTION 

## Project Repository
[OSS Speech Transcription Repo](https://github.com/oss-slu/SpeechTranscription)

## Project Overview:

The Speech Transcription application titled "Saltify", developed as part of Open Source at SLU, seeks to transcribe an audio sample into a written format which is 
accepted by SALT software. This SALT software analyzes the speech of children and scores it according to their respective metrics. Saltify can currently transcribe 
audio samples of a conversation between a child and an adult into text. Since children naturally produce errors in speech and language, the app will transcribe
errors and features that are auto-corrected in currently available speech-to-text programs. It also offers suggestions in terms of coding the sample.

## Setup Instructions:

1. Use the given link to download the .exe files: [Download .exe files](https://github.com/oss-slu/SpeechTranscription/releases) Please select the correct executable
   based on your Operating System (Windows/Mac/Linux)
2. Once downloaded locally, open the .exe file and launch the application. You can record live or upload an audio sample from your computer, which will be transcribed
   to a text output and you will receive suggestions on fixing incorrect speech. The output results can be downloaded as a .docx format which can be saved locally on
   your machine.

## Dependencies:

All dependencies can be installed via `pip install -r requirements.txt`

### Audio Processing
pyaudio, wave, ffmpeg, ffprobe, ffprobe-python, ffmpeg-python, pydub, pyannote.audio, simple_diarizer

### NLP / Text
nltk, language-tool-python, python-docx

### AI / ML
Whisper, pyannote.audio, lightning_fabric, Resemblyzer (optional)

### GUI
sv_ttk, customtkinter

### Utilities
matplotlib, numpy, python-dotenv, pillow

### Testing
pytest

### Optional / Future
spectralcluster, Resemblyzer

## Files and Workflows:

- **`GUI.py`**  
Added logging to capture errors and runtime information into `app.log`.  
This improves debugging and allows maintainers to track issues without running the GUI locally.

- **`.github/workflows/<workflow>.yml`**  
Updated the GitHub Actions workflow to:  
  - Run the GUI and redirect output to `app.log`  
  - Upload `app.log` as an artifact after each run  
This ensures crash logs are available for each automated build.

- **`requirements.txt`**  
Updated to remove `wave`, which was causing EXE launch failures due to a conflicting dependency (`mysql_python`).  
This fixes package installation issues for automated builds.

## Developer Setup & Executable Access:

### Development Environment
For full details, see [Developer Guide](https://github.com/oss-slu/SpeechTranscription/blob/main/DEVELOPER_GUIDE.md).  
Key steps to get started:
- Clone the repository
- Install dependencies via `pip install -r requirements.txt`
- Set environment variables as needed

### Executable Access
Executables are automatically generated using GitHub Actions.

**Windows:**
1. Go to the 'Actions' tab on GitHub
2. Under 'Workflows', select `.github/workflows/create-executable.yml`
3. Find the desired version (check title & branch) and click it
4. Scroll to the 'Artifacts' section and download the Windows executable

**MacOS:**
- Follow the first 4:10 of [this tutorial](https://youtu.be/5Z_G6QG7xxg?si=zg5MozBv6WrYJtIQ)
- Run the steps in a Windows VM as described above to access the Mac executable

**Manual Build:**  
- Executable can also be created manually using `pyinstaller`. Check the GitHub Actions workflow for exact commands.








