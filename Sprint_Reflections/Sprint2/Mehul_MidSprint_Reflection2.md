# Work Description
During the second sprint, I was assigned with the Digital Bones Box Project in which I had audit the repository to ensure its readiness for CI/CD and testing. This web-based application lacked structural testing mechanisms and automation, which are essential for reliability and maintainability. The first thing I did was cloning the repository locally, and investigating the components which were present and the ones which were missing. After an analysis of the project's workflows, I observed that only linting was set up, specifically in the lint.yml file, and there were no unit, static, integration, security or end-to-end tests and workflows with regards to deployment. I summarized these findings in a concise and descriptive audit report which I submitted in our CI/CD repository as a pull request that recommends a phased approach towards CI/CD.

# Individual efforts
My main contribution was drafting the audit report, which I organized into the documentation folder of the CI/CD repository. I proposed specific tests such as creating a /tests folder with Jest, extending the existing GitHub Actions workflow to install dependencies, run dependencies and run tests while also writing atleast one unit test before the sprint closes.

# Collaboration
With regards to collaboration, I held a Google Meet with the Project's Tech Lead, who clarified my thoughts and expectations for this project. She was instrumental in helping me realize that the current project lacked a complete CI/CD setup, and that only linting was done at the moment. She said that she didn't expect me to deliver a complete pipeline, but even if the progress shows promise compared to what was existent before, it was good work.

# Challenges
She told me that the project lacked unit tests, static tests, integration tests, end to end tests, security tests and automation. It was also not containerized (there was no Docker file which would potentially help the project to be deployed). After this meeting and refining some of my doubts, I decided to create an audit report as a good first step in helping their team.

# Professional Growth
Overall, this sprint helped me to systematically analyze an unfamiliar codebase, identify gaps (with regards to missing tests and workflows) and to translate findings into actionable improvements. I was able to enhance my technical writing by creating an audit document, something which I had never done beforehand, and include relevant information while providing technically accurate feedback in an ADR format. Thus, I came to appreciate the importance of incremental improvements in engineering complex systems, without having to figure out and solve everything at once.
