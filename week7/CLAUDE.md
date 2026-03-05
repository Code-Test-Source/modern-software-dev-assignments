# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
make run     # Start dev server at localhost:8000 (API docs at /docs)
make test    # Run pytest tests
make format  # Format with black + ruff --fix
make lint    # Run ruff linter
make seed    # Apply seed.sql to database
```

Run a single test:
```bash
PYTHONPATH=. pytest -q backend/tests/test_notes.py::test_create_note -v
```

## Architecture

**FastAPI + SQLAlchemy (SQLite)** backend with static frontend served by the same app.

### Backend Structure
```
backend/
├── app/
│   ├── main.py       # FastAPI app, static file mounting, router inclusion
│   ├── db.py         # SQLAlchemy engine, SessionLocal, get_db() dependency
│   ├── models.py     # Note, ActionItem models with TimestampMixin
│   ├── schemas.py    # Pydantic schemas: Create, Read, Patch for each model
│   ├── routers/      # API endpoints by domain (notes, action_items)
│   └── services/     # Business logic (extract.py for action item extraction)
└── tests/
    └── conftest.py   # TestClient with temp SQLite database
```

### Key Patterns

- **Database sessions**: Use `get_db()` dependency injection. Sessions auto-commit on success, rollback on exception.
- **Schemas**: Three schemas per model: `ModelCreate`, `ModelRead`, `ModelPatch` (partial updates).
- **List endpoints**: Support `skip`/`limit` pagination, `sort` field with `-` prefix for descending, optional filters.
- **PATCH endpoints**: Only update fields that are not None in payload.

### Models

- **Note**: id, title, content, created_at, updated_at
- **ActionItem**: id, description, completed, created_at, updated_at

## Assignment Tasks

See `docs/TASKS.md` for the four tasks to implement:
1. Add more endpoints and validations
2. Extend extraction logic
3. Add new model and relationships
4. Improve tests for pagination and sorting

Each task should be implemented on a separate branch with a PR including Graphite Diamond AI review.
