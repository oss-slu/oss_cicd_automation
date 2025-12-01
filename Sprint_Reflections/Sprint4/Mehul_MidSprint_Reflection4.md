# Work Description
For this sprint, I decided to choose the OSS Mouser project and to conduct a CI/CD environment investigation. One of my goals for this mid-sprint check-in was to verify that the tests were running consistently across development environments and provide maintainers with clear guidance for future work. So far, I believe that my contribution sets the stage for continuous integration and that contributors can reproduce a stable local setup without breaking production code.

# Individual efforts
I began this project by forking the repository, cloning it, creating a new branch and starting with my work on this new branch. I created and activated a Python virtual environment and installed all the dependencies listed in "requirements.txt" file. This installation helped me find out that every library was installed successfully except for "playsound", which failed to build a wheel under Python 3.13. This was the latest version on my system and I believe that Mouser was created a time only when Python 3.9 was available. Despite this limitation, and not wanting to change my system to use Python 3.9 instead of Python 3.13, I installed all dependencies except for playsound and verified that the remainder of the application executed correctly. Furthermore, I also ran the project's existing tests using pytest and unittest and documented the import-path issues which resulted in test errors, confirming that these are environmental rather than logic faults.

# Collaboration
Although this was mostly an individual effort, I ensured to contact my tech lead regarding the work needed to be done. In the earlier class, we had discussed what we were going to do and this provided me with the guidance that I needed to accomplish my tasks for mid-sprint. 

# Challenges
In terms of logistics, during the fall break I visited Cincinnati as part of a career trek which was organized by SLU's Career Services Center. Since we were in Cincinnati for 2 days and we had programs planned for 2 days, I wasn't able to work on this project but immediately after coming back I got back on track to complete my work. I believe I should have collaborated more with my tech lead and my team mate for this project, but since we have the rest of the sprint remaining, this is something I will ensure to incorporate to deliver substantive work through collaboration and guidance.

# Professional Growth
Overall, this sprint strengthened my DevOps, testing and diagnostic skills, helping me understand how CI/CD pipelines rely on local builds, environment isolation and precise documentation.