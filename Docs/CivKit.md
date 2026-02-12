# CivKit — CI/CD Workflow Audit Report  
**Audited by:** Thomas (CI/CD Development Team)  
**Date:** February 9, 2026

**Project:** CivKit
**Repository:** `oss-slu/oss_cicd_automation`  
**Issue:** [#89 — CivKit CI/CD Workflow implementation and audi](https://github.com/oss-slu/oss_cicd_automation/issues/89)


## Workflow Overview
There is 0 automation in the repository, meaning that we will need to build from scratch. there is no extisting dependences to audit at the time, this audit only contains ideas that the Civkit team and I have proposed adding.

## Proposed ideas 
over this sprint I have colaborated witht the civkit team, these are some of the things they want to tackle reguarding CI/CD implementation on thier project.  

-database testing, need an isolated database for testing purposes. We are
using prisma
    user authentication
    checking passwords are correctly hashed
    json token correctly created
    json token doesnʼt last too long
    test login with inappropriate credentials
    issue creation, issue retrieval by id, issue retrieval by
    nearby(longitude/latitude credentials)
- want to run in under 30 seconds
- easy to run locally through npm test
- tests are deterministic
- Jest configuration file ( jest.config.js )
- Test setup file ( jest.setup.js )
- Testing utilities file ( tests/helpers.ts )
-Example test file demonstrating patterns:
    Unit test example (service or utility function)
    API endpoint test example (with Supertest)
    Database test example (with Prisma)
- Updated package.json with test scripts and dependencies
- .env.test template
-Documentation: backend/tests/README.md explaining:
    How to run tests locally
    How to write new tests
    How to mock dependencies
    Best practices
-Future 
    testing upvote functionality, that it is created attached to an issue when an issue is created and initialized to 0, that people can only upvote once, and only if they are a registered user, that people can remove their upvote, and that if an issue is deleted, the upvote variable is deleted as well.