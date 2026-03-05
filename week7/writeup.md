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
> Commit: https://code.techutopia.cn/tomson/modern-software-dev-assignments/commit/2fa310c

b. PR Description
> https://code.techutopia.cn/tomson/modern-software-dev-assignments/pulls/2
> - Added GET/DELETE/PATCH endpoints for notes and action items
> - Implemented input validation (title length, content validation)
> - Added proper 404 error handling
> - Comprehensive test coverage added

c. Graphite Diamond generated code review
> TODO: Add Graphite Diamond review comments after review

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> Commit: https://code.techutopia.cn/tomson/modern-software-dev-assignments/commit/c5df790

b. PR Description
> https://code.techutopia.cn/tomson/modern-software-dev-assignments/pulls/1
> - Extended action markers: FIXME, BUG, HACK, NOTE
> - Added `ActionItemMatch` dataclass with metadata extraction
> - Priority extraction from `(priority)` or `[priority]` syntax
> - Assignee extraction from `@mentions`
> - Due date hint extraction from `by <date>` patterns
> - 22 comprehensive tests added

c. Graphite Diamond generated code review
> TODO: Add Graphite Diamond review comments after review

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> Commit: https://code.techutopia.cn/tomson/modern-software-dev-assignments/commit/eb324f0

b. PR Description
> https://code.techutopia.cn/tomson/modern-software-dev-assignments/pulls/3
> - Added Tag model with name (unique) and color fields
> - Created many-to-many relationship between Notes and Tags
> - Full CRUD endpoints for tags
> - Notes can be filtered by tag name
> - 18 comprehensive tests added

c. Graphite Diamond generated code review
> TODO: Add Graphite Diamond review comments after review

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> TODO

b. PR Description
> TODO

c. Graphite Diamond generated code review
> TODO

## Brief Reflection
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> TODO

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> TODO

c. When the AI reviews were better/worse than yours (cite specific examples)
> TODO

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
>TODO
