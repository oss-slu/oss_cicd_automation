# **Speech Transcription – End of Sprint Reflection**

### **Work Accomplished**
During this sprint, my primary contribution involved improving the **CI/CD infrastructure** for the Speech Transcription project. My main task was to investigate why the **Windows `.exe` file was crashing** for the Saltify application, even though it worked on macOS. I reproduced the issue locally, performed step-by-step debugging, and documented all findings in a structured case study. I also supported **dependency management** by updating the `requirements.txt` file and adding comments explaining why certain packages were needed.

### **Collaboration**
Collaboration played a major role in this sprint. Along with our scheduled Monday capstone classes, our team held additional meetings every Tuesday and Friday to track progress and share updates. Our Tech Lead helped distribute work efficiently:  
- I focused on diagnosing and reproducing the `.exe` crash  
- My teammate worked on logging and workflow updates  

This parallel work allowed us to make steady progress. A key lesson I learned was the importance of following **team version control practices**—specifically, adding reviewers to pull requests. I initially forgot to tag my Tech Lead as a reviewer, which reminded me that collaboration isn’t just about writing code—it also includes maintaining good communication and accountability within the development workflow.

### **Technical Growth**
This sprint significantly expanded my technical skill set:
- Gaining hands-on experience with **CI/CD debugging**
- Learning how **PyInstaller** packages Python applications into executables
- Understanding how missing dependencies, DLLs, or resource files cause `.exe` failures
- Installing and bundling missing components manually
- Creating a reproducible debugging workflow
- Writing clear developer documentation and case-study style explanations

Before this sprint, I had limited experience with pull requests, merge requests, structured documentation, or diagnosing packaging issues. By the end, I was able to rebuild the `.exe` from scratch and successfully launch it, demonstrating clear progress in problem-solving and CI/CD understanding.

### **Challenges**
The biggest challenge was that **the `.exe` file crashed silently** with no visible error message. To address this, I:
1. Checked Windows Event Viewer logs
2. Ran the application through the terminal to surface Python runtime errors
3. Installed missing third-party dependencies
4. Installed Microsoft Build Tools when required
5. Repackaged the executable using PyInstaller with the appropriate resource folders included

This systematic approach turned a vague error into a solvable engineering task.

### **Professional Development**
From a professional standpoint, this sprint improved my:
- **Time management**, by breaking a long debugging task into manageable steps
- **Communication skills**, through writing clear documentation and presenting results to the Tech Lead
- **Confidence** working with real-world CI/CD issues and GitHub workflows

Overall, this sprint was extremely valuable. I not only fixed the immediate issue but also created documentation that will help future contributors understand how to diagnose `.exe` failures and dependency issues. It reinforced the importance of teamwork, communication, and structured debugging, resulting in a successful and productive sprint.

