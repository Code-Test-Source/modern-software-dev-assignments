# Multi-Agent Workflow with Git Worktree

A Warp Drive automation for running multiple concurrent agents on independent tasks.

## Purpose

Enable parallel development by running multiple agents in separate git worktrees, preventing conflicts and allowing concurrent work on independent features.

## Prerequisites

- Git repository
- Multiple independent tasks from TASKS.md

## Workflow Steps

### Step 1: Identify Independent Tasks

Select tasks that can be worked on independently without shared state or sequential dependencies.

Good candidates:
- Task 3 (Notes CRUD) - only modifies notes router
- Task 4 (Action items filters/bulk) - only modifies action_items router
- Task 8 (Pagination) - cross-cutting but isolated changes

### Step 2: Create Git Worktrees

```bash
# Create worktree for Task 3
git worktree add .claude/worktrees/task-3-notes-crud -b feature/notes-crud

# Create worktree for Task 4
git worktree add .claude/worktrees/task-4-action-filters -b feature/action-filters
```

### Step 3: Launch Concurrent Agents

In Warp terminal tabs:

**Tab 1 - Notes CRUD Agent:**
```
cd .claude/worktrees/task-3-notes-crud
# Implement PUT /notes/{id}, DELETE /notes/{id}
# Add optimistic UI updates
# Run tests
```

**Tab 2 - Action Items Agent:**
```
cd .claude/worktrees/task-4-action-filters
# Implement GET /action-items?completed=true|false
# Implement POST /action-items/bulk-complete
# Add filter UI and bulk action UI
# Run tests
```

### Step 4: Merge Results

```bash
# After both agents complete
git checkout master
git merge feature/notes-crud
git merge feature/action-filters

# Clean up worktrees
git worktree remove .claude/worktrees/task-3-notes-crud
git worktree remove .claude/worktrees/task-4-action-filters
```

## Coordination Strategy

1. **Shared contracts**: Define API schemas upfront in main branch
2. **File ownership**: Each agent owns specific files (routers, tests)
3. **Communication**: Use PR descriptions to document changes
4. **Conflict resolution**: Merge in order of task dependencies

## Benefits

- **Speed**: 2x faster with 2 concurrent agents
- **Isolation**: No conflicts between parallel work
- **Focus**: Each agent focuses on single task
- **Review**: Easier to review isolated changes

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Schema conflicts | Define shared schemas first |
| Test conflicts | Separate test files per feature |
| Merge conflicts | Use git worktree for isolation |
| Duplicate work | Clear task assignment |

## Example: Parallel Implementation

In this assignment, Task 3 (Notes CRUD) and Task 4 (Action Items) were implemented sequentially but could be parallelized:

- **Agent 1**: backend/app/routers/notes.py, backend/tests/test_notes.py
- **Agent 2**: backend/app/routers/action_items.py, backend/tests/test_action_items.py

Both agents share only `backend/app/schemas.py` - coordination needed only there.
