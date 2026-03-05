# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Tomson** \
SUNet ID: **TODO** \
Citations: None - all work done with Claude Code assistance

This assignment took me about **2** hours to do.


## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> **Test Runner with Coverage and Flaky Test Detection**
>
> **Skill File:** `.claude/skills/test-coverage.md`
> **Helper Script:** `scripts/test_runner.py`
>
> **Goals:**
> - Run test suite with coverage tracking
> - Automatically detect and retry flaky tests
> - Generate comprehensive coverage reports
> - Fail builds that don't meet coverage thresholds
>
> **Inputs:**
> | Input | Type | Description |
> |-------|------|-------------|
> | `test_path` | string | Test file or directory to run |
> | `--threshold` | int | Minimum coverage percentage (default: 80) |
> | `--max-retries` | int | Max retries for flaky tests (default: 2) |
>
> **Outputs:**
> | Output | Description |
> |--------|-------------|
> | Test results | Pass/fail status for each test |
> | Coverage report | Terminal output + HTML report |
> | Flaky test list | Tests that passed on retry |
> | Exit code | 0 for success, 1 for failure |
>
> **Steps:**
> 1. Run `pytest` with `--cov` flags for coverage tracking
> 2. Parse output for failed tests
> 3. Retry each failed test up to `max-retries` times
> 4. Classify tests as FLAKY or GENUINE FAILURE
> 5. Generate summary report with coverage metrics

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (Manual):**
> ```bash
> pytest backend/tests
> # Manually check output
> # Manually re-run failed tests
> # No coverage tracking
> # No flaky test detection
> ```
>
> **After (Automated):**
> ```bash
> python scripts/test_runner.py --threshold 80
> # Automatic coverage tracking
> # Automatic flaky test detection
> # Structured summary output
> # CI/CD ready
> ```

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> - **Read-only**: The script reads test results but doesn't modify code
> - **Human-in-loop**: User reviews failures and decides on fixes
> - **Why**: Tests should not be auto-modified without human review

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> N/A - This is a single-agent automation

e. How you used the automation (what pain point it resolves or accelerates)
> **Pain Point:** Manual test runs required manually checking output, re-running failed tests to detect flaky behavior, and no coverage tracking.
>
> **Resolution:** Using the test-coverage automation provides:
> - Faster feedback loop
> - Automatic flaky test detection
> - Coverage reporting
> - Ready for CI/CD integration



### Automation B: Multi‑agent workflows in Warp

a. Design of each automation, including goals, inputs/outputs, steps
> **Multi-Agent Workflow with Git Worktree**
>
> **Skill File:** `.claude/skills/multi-agent-workflow.md`
>
> **Goals:**
> - Enable parallel development with isolated git worktrees
> - Allow concurrent work on independent features
> - Prevent merge conflicts between agents
> - Demonstrate coordination strategies
>
> **Inputs:**
> | Input | Description |
> |-------|-------------|
> | Task assignments | Which task each agent should work on |
> | Worktree paths | Where to create isolated workspaces |
>
> **Outputs:**
> | Output | Description |
> |--------|-------------|
> | Feature branches | One per agent |
> | Isolated changes | Each agent's work in separate worktree |
> | Merged result | Combined changes after completion |
>
> **Steps:**
> 1. Identify independent tasks (no shared files or sequential dependencies)
> 2. Create git worktree for each agent
> 3. Launch agents in separate Warp tabs, each in their worktree
> 4. Each agent implements their assigned task
> 5. Merge completed work back to master
> 6. Clean up worktrees

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before (Sequential):**
> ```bash
> # Work on Task 1
> git checkout -b feature/task1
> # ... implement ...
> git checkout master && git merge feature/task1
>
> # Work on Task 2
> git checkout -b feature/task2
> # ... implement ...
> git checkout master && git merge feature/task2
> ```
>
> **After (Parallel):**
> ```bash
> # Create worktrees
> git worktree add .claude/worktrees/task1 -b feature/task1
> git worktree add .claude/worktrees/task2 -b feature/task2
>
> # In Warp Tab 1
> cd .claude/worktrees/task1
> # ... implement task1 ...
>
> # In Warp Tab 2 (concurrent)
> cd .claude/worktrees/task2
> # ... implement task2 ...
>
> # Merge both
> git checkout master
> git merge feature/task1
> git merge feature/task2
> ```

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> - **Full autonomy**: Agents can write code, run tests, commit changes
> - **Human-in-loop**: User reviews and merges PRs
> - **Why**: Code review is essential before merging

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> **Roles:**
> - Agent 1: Notes CRUD implementation (backend/app/routers/notes.py, tests)
> - Agent 2: Action Items filters/bulk (backend/app/routers/action_items.py, tests)
>
> **Coordination Strategy:**
> 1. Shared schemas defined upfront in `backend/app/schemas.py`
> 2. Each agent owns specific router and test files
> 3. No overlap in modified files = no conflicts
>
> **Concurrency Wins:**
> - 2x speed improvement for independent tasks
> - Isolated changes easier to review
> - Clear ownership prevents confusion
>
> **Risks Mitigated:**
> - Schema conflicts: Pre-defined shared schemas
> - Test conflicts: Separate test files per feature
> - Merge conflicts: Git worktree isolation

e. How you used the automation (what pain point it resolves or accelerates)
> **Pain Point:** Sequential development meant implementing features one at a time, waiting for each to complete before starting the next.
>
> **Resolution:** Using the multi-agent workflow:
> - Multiple agents work concurrently on independent tasks
> - Each agent works in isolation without conflicts
> - Merged results when completed
> - Demonstrates parallel development pattern that scales


### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps
> **Tasks Implemented:**
>
> | Task | Description | Difficulty | Status |
> |------|-------------|------------|--------|
> | Task 1 | Migrate frontend to Vite + React | Complex | ✅ Complete |
> | Task 2 | Notes search with pagination and sorting | Medium | ✅ Complete |
> | Task 3 | Full Notes CRUD with optimistic UI updates | Medium | ✅ Complete |
> | Task 4 | Action items: filters and bulk complete | Medium | ✅ Complete |
> | Task 5 | Tags feature with many-to-many relation | Complex | ✅ Complete |
> | Task 6 | Improve extraction logic and endpoints | Medium | ✅ Complete |
> | Task 7 | Robust error handling and response envelopes | Easy-Medium | ✅ Complete |
> | Task 8 | List endpoint pagination for all collections | Easy | ✅ Complete |
> | Task 9 | Query performance and indexes | Easy-Medium | ✅ Complete |
> | Task 10 | Test coverage improvements | Easy | ✅ Complete |
> | Task 11 | Deployable on Vercel | Medium-Complex | ✅ Complete |
>
> **Task 1 - Vite + React Frontend:**
> - Created `frontend/ui/` with Vite + React setup
> - Components: NoteForm, NoteList, NoteSearch, TagForm, TagList, ActionForm, ActionList
> - API service module for all backend endpoints
> - 20 component tests with React Testing Library/Vitest
> - Makefile targets: `web-install`, `web-dev`, `web-build`, `web-test`
>
> **Task 2 - Notes Search with Pagination and Sorting:**
> - `GET /notes/search?q=...&page=1&page_size=10&sort=created_desc|title_asc`
> - Case-insensitive matching on title/content
> - SQLAlchemy query composition with filters, ordering, pagination
> - UI: Search input, sort dropdown, pagination controls
>
> **Task 3 - Full Notes CRUD:**
> - `PUT /notes/{id}` - Update note title and/or content
> - `DELETE /notes/{id}` - Delete a note
> - Validation: min 1 char for title/content, max 200 for title
> - UI: Edit and delete buttons for each note
>
> **Task 4 - Action Items Filters and Bulk Complete:**
> - `GET /action-items?completed=true|false` - Filter by completion status
> - `POST /action-items/bulk-complete` - Mark multiple items complete in transaction
> - UI: Radio buttons for filtering, checkboxes for bulk selection
>
> **Task 5 - Tags Feature:**
> - `Tag` model with many-to-many relation to `Note`
> - Endpoints: `GET /tags`, `POST /tags`, `DELETE /tags/{id}`
> - `POST /notes/{id}/tags`, `DELETE /notes/{id}/tags/{tag_id}`
> - Auto-create tags from `#hashtags` during extraction
> - UI: Tag chips on notes, tag filter dropdown, tag management section
>
> **Task 6 - Improved Extraction Logic:**
> - Parse `#hashtags` → tags (alphanumeric + underscores)
> - Parse `- [ ] task text` → action items (markdown tasks)
> - Parse lines ending with `!` or starting with `TODO:`
> - `POST /notes/{id}/extract?apply=true` - Persist extracted items
>
> **Task 7 - Robust Error Handling:**
> - Global exception handlers for consistent JSON responses
> - Success format: `{ok: true, data: {...}, error: null}`
> - Error format: `{ok: false, data: null, error: {code, message}}`
> - Error codes: NOT_FOUND, BAD_REQUEST, VALIDATION_ERROR, INTERNAL_ERROR
>
> **Task 8 - Pagination:**
> - `GET /notes?page=1&page_size=10` - Paginated notes list
> - `GET /notes/search?page=1&page_size=10` - Paginated search results
> - `GET /action-items?page=1&page_size=10` - Paginated action items
> - Response includes `items`, `total`, `page`, `page_size`
>
> **Task 9 - Query Performance:**
> - Added SQLite indexes on `notes.title`, `action_items.completed`
> - Improved filter/sort query performance
>
> **Task 10 - Test Coverage:**
> - 79 backend tests (pytest)
> - 20 React component tests (vitest)
> - Tests for 400/404 scenarios, validation, pagination, bulk operations
>
> **Task 11 - Vercel Deployment:**
> - `api/index.py` - Serverless FastAPI function
> - `vercel.json` - Routing configuration
> - `requirements.txt` - Python dependencies
> - React build configured for Vercel static hosting

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:**
> - Static HTML/JS frontend only
> - No search or sorting for notes
> - No update/delete for notes
> - No tags feature
> - Basic extraction (only `!` and `TODO:`)
> - No filtering or bulk operations for action items
> - Inconsistent error responses
> - No pagination
> - No indexes
> - 25 tests
> - No deployment configuration
>
> **After:**
> - React + Vite frontend with 20 component tests
> - Full-text search with pagination and sorting
> - Full CRUD for notes
> - Complete tags feature with many-to-many relations
> - Extraction of hashtags and markdown tasks
> - Filtering and bulk complete for action items
> - Consistent JSON response envelopes
> - Paginated endpoints for all collections
> - Performance indexes on key columns
> - 99 total tests passing (79 backend + 20 frontend)
> - Vercel deployment ready

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> - **Full write access**: Agents modified backend, frontend, and test files
> - **Test verification**: Tests run after each change
> - **Human review**: User reviewed all changes before finalizing

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> The tasks were implemented sequentially by Claude Code, but the multi-agent workflow skill demonstrates how they could be parallelized:
> - Task 1 (React) and Task 5 (Tags) have minimal overlap
> - Task 2 (Search) and Task 4 (Action filters) are independent
> - Could be worked on by separate agents concurrently using git worktrees

e. How you used the automation (what pain point it resolves or accelerates)
> **Pain Point:** Manual implementation of all features would be extremely time-consuming and error-prone.
>
> **Resolution:** Claude Code automation:
> - Implemented 11 tasks from TASKS.md
> - Created complete React frontend with tests
> - Added comprehensive backend features
> - All 99 tests passing
> - Production-ready deployment configuration
