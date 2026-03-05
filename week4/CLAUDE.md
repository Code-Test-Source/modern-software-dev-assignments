# Week 4 Starter Application - Developer's Command Center

## Project Overview
A minimal full-stack "developer's command center" application with FastAPI backend, SQLite database, and static frontend.

## How to Run

```bash
# Activate conda environment first
conda activate cs146s

# Run the development server (from week4/ directory)
make run
# Access at http://localhost:8000
# API docs at http://localhost:8000/docs

# Run tests
make test

# Format and lint
make format   # runs black + ruff --fix
make lint     # runs ruff check only

# Seed database
make seed
```

## Project Structure

```
backend/
  app/
    main.py          # FastAPI app entry point
    db.py            # SQLAlchemy setup, session management
    models.py        # Note, ActionItem models
    schemas.py       # Pydantic request/response schemas
    routers/
      notes.py       # /notes/* endpoints
      action_items.py # /action-items/* endpoints
    services/
      extract.py     # Text extraction utilities
  tests/
    conftest.py      # pytest fixtures (TestClient, temp DB)
    test_*.py        # Test modules

frontend/
  index.html         # Main HTML page
  app.js             # Frontend logic (vanilla JS)
  styles.css         # Styling

data/
  app.db             # SQLite database (auto-created)
  seed.sql           # Initial seed data

docs/
  TASKS.md           # List of tasks/feature ideas to implement
```

## Key Conventions

### Adding a New Endpoint
1. Create/update Pydantic schemas in `schemas.py`
2. Add the route handler in the appropriate router (`routers/*.py`)
3. Write tests in `tests/test_*.py`
4. Run `make format && make test` to verify

### Database Changes
- Models are in `models.py`
- Migrations are not used; SQLite with auto-create on startup
- Seed data in `data/seed.sql`

### Testing
- Uses pytest with TestClient
- Each test gets a fresh temp database
- Run specific test: `PYTHONPATH=. pytest -q backend/tests/test_notes.py -v`

## Safety Notes
- Always run `make test` after making changes
- Run `make format` before committing
- Pre-commit hooks will run black and ruff

## Available Slash Commands
- `/tests` - Run tests with coverage and summarize results
- `/docs-sync` - Sync API documentation with OpenAPI spec
