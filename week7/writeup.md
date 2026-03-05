# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do.


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> Commit: https://code.techutopia.cn/tomson/modern-software-dev-assignments/commit/d7ca84e
> GitHub Mirror PR: https://github.com/Code-Test-Source/modern-software-dev-assignments/pull/1

b. PR Description
> https://code.techutopia.cn/tomson/modern-software-dev-assignments/pulls/2
> - Added GET/DELETE/PATCH endpoints for notes and action items
> - Implemented input validation (title length 1-200 chars, content validation)
> - Added proper 404 error handling for missing resources
> - Added validation for item_id (must be positive integer)
> - Comprehensive test coverage added

c. Graphite Diamond generated code review
> **GitHub Copilot Review (8 comments):**
> - Reviewed 7 files: notes.py, action_items.py, schemas.py, extract.py, test_notes.py, test_action_items.py, test_extract.py
> - Noted that the PR adds `/count`, GET-by-id, DELETE, and PUT endpoints with schema-level validation
> - Identified that extract.py changes "removes structured extraction and reduces supported marker patterns"
>
> **Graphite Diamond Review:** Not triggered on this PR (only GitHub Copilot reviewed).

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> Commit: https://code.techutopia.cn/tomson/modern-software-dev-assignments/commit/d17df98
> GitHub Mirror PR: https://github.com/Code-Test-Source/modern-software-dev-assignments/pull/2

b. PR Description
> https://code.techutopia.cn/tomson/modern-software-dev-assignments/pulls/1
> - Extended action markers: FIXME, BUG, HACK, NOTE (in addition to TODO)
> - Added `ActionItemMatch` dataclass with metadata extraction
> - Priority extraction from `(priority)` or `[priority]` syntax
> - Assignee extraction from `@mentions`
> - Due date hint extraction from `by <date>` patterns
> - Backward compatible: `extract_action_items()` returns strings, `extract_action_items_structured()` returns rich objects
> - 22 comprehensive tests added

c. Graphite Diamond generated code review
> **GitHub Copilot Review (6 comments):**
> - Reviewed 2 files: extract.py, test_extract.py
> - Noted expanded marker support and structured extraction API
>
> **Graphite Diamond Review (7 detailed comments):**
> 1. **Inconsistent marker detection:** `MARKER_PATTERN` doesn't require a colon, but `extract_action_items()` requires a colon. This breaks backward compatibility - `TODO fix this` (no colon) returns empty list from basic extraction but a match from structured extraction.
> 2. **Priority syntax not supported in basic extraction:** `TODO(high): ...` won't be returned by the backward-compatible API because the colon check doesn't account for priority qualifiers.
> 3. **Duplicated logic:** Both extraction functions duplicate line-normalization logic. Suggested extracting to a shared helper.
> 4. **Misleading test name:** `test_multiple_items_same_line` tests items on separate lines, not same line.
> 5. **Missing length assertion:** Test indexes `items[0]` and `items[1]` without first asserting length.
> 6. **DUE_PATTERN not end-anchored:** Will match "by..." anywhere in description, causing false positives.
> 7. **Suggested regex fix:** `MARKER_PATTERN = r"^(TODO|ACTION|FIXME|BUG|HACK|NOTE):"` to ensure consistency.

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> Commit: https://code.techutopia.cn/tomson/modern-software-dev-assignments/commit/561e2da
> GitHub Mirror PR: https://github.com/Code-Test-Source/modern-software-dev-assignments/pull/3

b. PR Description
> https://code.techutopia.cn/tomson/modern-software-dev-assignments/pulls/3
> - Added Tag model with name (unique) and color fields
> - Created many-to-many relationship between Notes and Tags
> - Full CRUD endpoints for tags (GET, POST, PATCH, DELETE)
> - Notes can be filtered by tag name via `?tag=<tag_name>` query parameter
> - 18 comprehensive tests added

c. Graphite Diamond generated code review
> **GitHub Copilot Review (11 comments):**
> - Reviewed 7 files: writeup.md, test_tags.py, schemas.py, tags.py, notes.py, models.py, main.py
> - Noted the addition of Tag model, many-to-many relationship, and tag CRUD endpoints
> - Identified note filtering by tag and tag assignment on create/patch
>
> **Graphite Diamond Review:** Not triggered on this PR (only GitHub Copilot reviewed).

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> Commit: https://code.techutopia.cn/tomson/modern-software-dev-assignments/commit/a8b07a8
> GitHub Mirror PR: https://github.com/Code-Test-Source/modern-software-dev-assignments/pull/4

b. PR Description
> https://code.techutopia.cn/tomson/modern-software-dev-assignments/pulls/4
> - Comprehensive pagination tests (skip/limit combinations)
> - Sorting tests (ascending/descending by various fields: id, title, created_at, updated_at)
> - Combined pagination + sorting + filtering tests
> - Edge case tests (skip beyond available data, limit validation)
> - Invalid sort field error handling tests
> - 37 total tests covering all scenarios

c. Graphite Diamond generated code review
> **GitHub Copilot Review (7 comments):**
> - Reviewed 3 files: writeup.md, test_notes.py, test_action_items.py
> - Noted expanded test suite for pagination, sorting, and combined query behavior
> - Identified class-based test organization and edge case coverage
>
> **Graphite Diamond Review:** Not triggered on this PR (only GitHub Copilot reviewed).

## Brief Reflection
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> My manual reviews typically focused on:
> - **Correctness**: Verifying logic and edge cases are handled properly
> - **Test gaps**: Ensuring adequate test coverage for new features
> - **API shape**: Reviewing endpoint design and request/response schemas
> - **Naming**: Checking variable and function naming conventions
> - **Error handling**: Ensuring proper error responses and validation

b. A comparison of **your** comments vs. **Graphite's** AI-generated comments for each PR.
> **GitHub Copilot** provided high-level summaries of changes and file-by-file breakdowns, but the comments were more descriptive than actionable.
>
> **Graphite Diamond** (Task 2 only) provided much more detailed, actionable feedback:
> - Identified specific code inconsistencies (marker detection between basic and structured extraction)
> - Suggested concrete code fixes with regex patterns
> - Found potential bugs (DUE_PATTERN false positives)
> - Noted test quality issues (misleading test names, missing assertions)
>
> The Diamond review was notably more thorough and provided specific code suggestions rather than just descriptions.

c. When the AI reviews were better/worse than yours (cite specific examples)
> **AI reviews were better:**
> - Diamond caught the subtle backward compatibility issue between `MARKER_PATTERN` and `extract_action_items()` that I missed during manual review
> - Diamond identified that `DUE_PATTERN` would match "by" anywhere in text, not just at end of line - a potential bug I hadn't considered
> - Suggested specific regex fix: `MARKER_PATTERN = r"^(TODO|ACTION|FIXME|BUG|HACK|NOTE):"`
>
> **My reviews were better:**
> - I had more context about the assignment requirements and overall architecture
> - I could verify that tests actually pass and meet the assignment criteria
> - I understood the trade-offs made (e.g., simplifying extraction for Task 1 was intentional)

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
> **Comfort level: Moderate-High**
>
> **When to rely on AI reviews:**
> - For catching edge cases and potential bugs in logic
> - For identifying inconsistencies between related code paths
> - For suggesting code improvements and patterns
> - As a first pass before manual review
>
> **When to verify manually:**
> - When reviewing architecture decisions that require domain knowledge
> - For understanding trade-offs and intentional simplifications
> - For verifying that code meets specific requirements
> - When security-sensitive code is involved
