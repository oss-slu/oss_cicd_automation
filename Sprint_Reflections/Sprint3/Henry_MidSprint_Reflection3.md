# Work Description:
During this sprint, I focused on developing a tool, Slack2Canvas, to automate the verification of Slack workspace users against Canvas course rosters. The goal was to identify possible missing students that is not in the Slack workspace, supporting more efficient onboarding and reducing manual errors. Originally, the project plan involved fully integrating Microsoft Graph API for automatic invites and utilizing Canvas and Slack APIs for live data access. However, due to limited access to certain administrative API tokens, the implementation was adapted to a CSV based approach that compares existing Canvas roster data with Slack users and generates a report of possible mismatches.

# Individual Efforts:
I designed and implemented the full Python script to handle the implementation. This included:

- Fetching and normalizing Canvas and Slack user data.

- Implementing custom scoring rules for matching: assigning scores of 10 for same names with @slu.edu emails, 50 for same names with other domain emails, and using fuzzy string matching for all other cases.

- Generating a CSV report with the results, including columns for the Canvas user name, email, best match score, and reason for the score.

- Ensuring configurability through environment variables, including Canvas CSV path, Slack token, and output directory.

Technical decisions, such as using fuzzywuzzy for string similarity and Python’s slack_sdk for Slack API integration, were made to ensure both accuracy and maintainability.

# Collaboration:
I engaged with team members by requesting code reviews and documenting my pull request (#30) for transparency. Discussions included verification of scoring logic, potential edge cases with duplicate or missing emails, and best practices for organizing output files. Feedback was incorporated to improve readability, CSV formatting, and handling of unusual scenarios, such as non-@slu.edu email addresses.

# Challenges:
A primary challenge was the inability to access required administrative tokens for Canvas to automatically retrieve the csv and Microsoft Graph to send the missing students on slack an invitation link, this prevented the originally planned live integration and automatic invitation workflow. To address this, I adapted the project to rely on CSV input, allowing testing and validation without live API calls. Additionally, edge cases in matching logic, such as duplicate names with different emails, required careful handling to ensure that scores reflected the intended significance of each match scenario.

# Professional Growth:
This sprint strengthened my skills in Python scripting, API integration, and designing robust data processing pipelines. I gained experience in adapting project plans when ideal conditions (full API access) are not available, emphasizing flexibility and delivering functional value despite constraints. I also enhanced my ability to document technical work clearly for reviewers and teammates, a critical skill for collaborative software development. Overall, the experience improved my proficiency in problem solving, project adaptation, and professional communication within a team setting.