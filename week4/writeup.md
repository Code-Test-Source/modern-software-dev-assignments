# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Tomson**
SUNet ID: **tomson**
Citations:
- Claude Code Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
- SubAgents Overview: https://docs.anthropic.com/en/docs/claude-code/sub-agents

This assignment took me about **2** hours to do.


## YOUR RESPONSES
### Automation #1: CLAUDE.md Repository Guidance File

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by the "CLAUDE.md guidance files" section in the assignment and the Claude Code best practices documentation. The best practices doc emphasizes: "Keep commands focused, use $ARGUMENTS, and prefer idempotent steps." I applied this philosophy to create a guidance file that provides clear, actionable context for working with the codebase.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal**: Provide Claude Code with repository-specific context to understand the project structure, conventions, and workflows without manual explanation each time.
>
> **Contents**:
> - Project overview and purpose
> - How to run the app, tests, and linting
> - Project structure with file descriptions
> - Key conventions for adding endpoints and database changes
> - Safety notes for development workflow
> - List of available slash commands
>
> **Inputs**: None (automatically read by Claude Code when starting in the directory)
> **Outputs**: Claude has context about the project structure and conventions

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run**: No explicit command needed. Claude Code automatically reads `CLAUDE.md` when starting a conversation in the directory.
>
> **Expected output**: Claude will understand:
> - How to run tests (`make test`)
> - How to format code (`make format`)
> - Where routers, models, and tests live
> - The workflow for adding new endpoints
>
> **Rollback**: Simply delete or rename `CLAUDE.md` to remove the guidance.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before**: Each new Claude session required manually explaining:
> - How to run the app and tests
> - Where to find specific files
> - What conventions to follow
> - Which commands are safe to run
>
> **After**: Claude automatically has all this context, reducing onboarding time and ensuring consistent behavior across sessions.

e. How you used the automation to enhance the starter application
> The CLAUDE.md file was essential for guiding the implementation of new features. With the context provided, I was able to:
> - Add `PUT /notes/{id}` and `DELETE /notes/{id}` endpoints following the documented workflow
> - Extend the `extract.py` service with tag extraction
> - Update the frontend with edit/delete buttons
> - All while following the project's conventions for testing and formatting


### Automation #2: `/tests` Slash Command

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by the "Test runner with coverage" example in the assignment and the Claude Code best practices which recommend: "Keep commands focused, use $ARGUMENTS, and prefer idempotent steps." The command follows the pattern of running tests first, then coverage only if tests pass.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal**: Provide a reusable workflow for running tests with coverage analysis and actionable feedback.
>
> **Inputs**: Optional `$ARGUMENTS` for specific test marker or path (e.g., "notes" or "backend/tests/test_notes.py")
>
> **Steps**:
> 1. Run pytest with the provided arguments or all tests
> 2. Analyze results and summarize failures
> 3. If tests pass, run coverage analysis
> 4. Report total tests, coverage percentage, and files with low coverage
>
> **Output**: Structured report with:
> - Test results (passed/failed)
> - Failure details with suggestions
> - Coverage percentage
> - Files below 80% coverage with missing lines

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run**:
> ```
> /tests                          # Run all tests
> /tests test_notes.py            # Run specific test file
> /tests backend/tests/test_notes.py -v  # With additional options
> ```
>
> **Expected output**: A structured markdown report with test results and coverage analysis.
>
> **Safety notes**:
> - Tests run in isolation with temp databases
> - No changes to production database
> - Can be run safely at any time

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before**: Running tests required:
> 1. Remembering the exact pytest command with PYTHONPATH
> 2. Manually checking for failures
> 3. Separately running coverage
> 4. Interpreting coverage output manually
>
> **After**: Single `/tests` command runs everything and provides a structured summary with actionable next steps.

e. How you used the automation to enhance the starter application
> Used the `/tests` command workflow to verify all new features:
> - Ran tests after adding the `extract_tags()` function
> - Verified PUT and DELETE endpoints work correctly
> - Confirmed all 12 tests pass after implementing the new endpoints
> - The command helped ensure no regressions were introduced


### Automation #3: `/docs-sync` Slash Command

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by the "Docs sync" example in the assignment. The Claude Code best practices recommend keeping documentation in sync with code changes automatically.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal**: Synchronize API documentation with the current OpenAPI specification from the running server.
>
> **Prerequisites**: Server must be running at http://localhost:8000
>
> **Steps**:
> 1. Fetch OpenAPI spec from `/openapi.json`
> 2. Parse all routes, methods, request bodies, and response schemas
> 3. Check for existing `docs/API.md`
> 4. Generate/update documentation with endpoints grouped by router
> 5. Detect and report changes (new, modified, removed endpoints)
>
> **Output**: Structured report with:
> - All endpoints found
> - Changes detected (added/modified/removed)
> - Documentation file status
> - TODOs for improvements

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **How to run**:
> 1. Start server: `make run`
> 2. Run command: `/docs-sync`
>
> **Expected output**: Creates/updates `docs/API.md` with current API documentation.
>
> **Safety notes**:
> - Read-only operation on the server
> - Only creates/updates `docs/API.md`
> - Original OpenAPI spec is untouched

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before**: Updating API docs required:
> 1. Manually checking each endpoint
> 2. Reading router files to understand request/response schemas
> 3. Writing documentation by hand
> 4. Easy to miss changes or make errors
>
> **After**: Single `/docs-sync` command fetches the actual API spec and generates accurate documentation.

e. How you used the automation to enhance the starter application
> Used the `/docs-sync` workflow to:
> - Generate initial `docs/API.md` documentation
> - Update documentation after adding PUT and DELETE endpoints for notes
> - Ensure documentation stays accurate with the actual API implementation
> - The documentation now includes all 7 endpoints with their schemas
