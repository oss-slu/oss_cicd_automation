# **Mouser – Mid-Sprint Reflection**

## **Work Accomplished**
For this sprint, I selected the **OSS Mouser project** and focused on a **CI/CD environment investigation**. My primary mid-sprint objective was to verify whether tests ran consistently across development environments and provide maintainers with clear documentation for future improvements.  
So far, my work ensures that contributors can **reproduce a stable development setup** without altering production code, which is key for CI/CD readiness.

To begin, I forked the repository, cloned it locally, created a feature branch, and set up a Python virtual environment. I then installed dependencies from the `requirements.txt` file using `pip install -r requirements.txt`.  
During installation, I discovered that every package installed correctly **except `playsound`**, which failed to build a wheel under **Python 3.13**. Since Mouser was originally written when Python 3.9 was common, this compatibility gap explained the issue. To avoid altering my system Python version, I proceeded with all dependencies **except playsound** and verified that the remaining application still executed correctly.

Next, I ran the project’s existing tests using **pytest** and **unittest**, which revealed **import-path errors**. These errors confirmed that the failures were **environment-based**, not logic flaws within the code.

---

## **Collaboration**
Although this was mostly an individual effort, I communicated with my Tech Lead before beginning work to clarify expectations. This helped guide my tasks and ensured alignment with sprint goals.  
Due to a career trek in Cincinnati during fall break, my available working time was limited, but I resumed progress immediately afterward. I recognize that collaboration could have been stronger during this phase, and I plan to increase communication with both my Tech Lead and teammate as we move into the second half of the sprint.

---

## **Technical Growth**
This sprint improved my skills in:

- Setting up Python virtual environments  
- Handling dependency installation failures  
- Understanding cross-version compatibility issues (Python 3.9 vs. 3.13)
- Running and diagnosing **pytest** and **unittest** based test suites
- Identifying when failures are caused by **environment configuration rather than code logic**

It also strengthened my ability to analyze how **CI/CD pipelines depend on reproducible builds**, clean dependency management, and a consistent testing environment.

---

## **Professional Development**
Through this sprint, I gained practical insight into:

- How to communicate findings clearly and professionally
- Balancing school responsibilities with project deadlines
- Structured debugging — reproducing issues, documenting causes, and validating fixes
- The importance of reliable documentation so other contributors can reproduce results without confusion

Even without major code changes, this investigative work provides value to maintainers by reducing uncertainty and laying the groundwork for automated CI pipelines.

---

## **Summary**
Up to this mid-sprint checkpoint, I have:

- Set up a clean Python virtual environment  
- Installed and analyzed project dependencies  
- Identified Python-version incompatibilities with `playsound`  
- Executed tests and documented import-path failures  
- Ensured that application components run correctly without modifying production code  

This work forms a solid foundation for CI/CD integration and testing improvements in the upcoming sprint.

