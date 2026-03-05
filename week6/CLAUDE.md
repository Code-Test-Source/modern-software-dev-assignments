# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Week 6 of Modern Software Development course - a FastAPI backend with vanilla JS frontend for demonstrating security scanning with Semgrep. The codebase intentionally contains vulnerabilities (SQL injection, XSS, hardcoded secrets, command injection, SSRF) for educational analysis.

## Commands

```bash
# Run the development server
make run
# Or: PYTHONPATH=. uvicorn backend.app.main:app --reload

# Run tests
make test
# Or: PYTHONPATH=. pytest -q backend/tests

# Run a single test file
PYTHONPATH=. pytest backend/tests/test_notes.py -v

# Run a single test
PYTHONPATH=. pytest backend/tests/test_notes.py::test_create_list_and_patch_notes -v

# Format and lint
make format  # runs black and ruff --fix
make lint    # runs ruff check

# Seed database
make seed

# Run Semgrep security scan (from repository root)
semgrep ci --subdir week6
```

## Architecture

```
week6/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, CORS, startup, routers
│   │   ├── db.py            # SQLite engine, session management
│   │   ├── models.py        # SQLAlchemy models (Note, ActionItem)
│   │   ├── schemas.py       # Pydantic request/response models
│   │   ├── routers/         # API endpoints
│   │   │   ├── notes.py     # /notes/* endpoints + debug endpoints
│   │   │   └── action_items.py
│   │   └── services/        # Business logic (extract.py)
│   └── tests/               # pytest tests with TestClient
├── frontend/                # Vanilla JS frontend
├── data/                    # SQLite database + seed.sql
└── Makefile
```

### Key Patterns

- **Database**: SQLite with SQLAlchemy ORM. Session via dependency injection (`get_db()`). Auto-commits on yield, rollback on exception.
- **Routers**: FastAPI routers with Pydantic schemas for validation. Patch endpoints use partial updates (only set provided fields).
- **Testing**: Uses `TestClient` with a temp SQLite database. `conftest.py` overrides the `get_db` dependency.
- **Frontend**: Served from `/static`, with `index.html` at root `/`. Uses `innerHTML` for rendering (intentional XSS vulnerability).

### Intentional Vulnerabilities (for Semgrep practice)

Located in `backend/app/routers/notes.py`:
- `/notes/unsafe-search` - SQL injection via f-string
- `/notes/debug/eval` - Arbitrary code execution via `eval()`
- `/notes/debug/run` - Command injection via `subprocess.run(shell=True)`
- `/notes/debug/fetch` - SSRF via `urlopen()`
- `/notes/debug/read` - Path traversal via `open(path)`
- `/notes/debug/hash-md5` - Weak hashing (MD5)

Located in `backend/app/services/extract.py`:
- Hardcoded API token on line 13

Located in `frontend/app.js`:
- XSS via `innerHTML` on line 14

## Dependencies

FastAPI 0.65.2, SQLAlchemy 1.3.23, Pydantic 1.5.1, uvicorn, requests, PyYAML. Uses pre-commit hooks with black and ruff.
