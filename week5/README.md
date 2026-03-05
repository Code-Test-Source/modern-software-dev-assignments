# Week 5

Full‑stack application for experimenting with autonomous coding agents.

- FastAPI backend with SQLite (SQLAlchemy)
- React frontend with Vite (or static fallback)
- Comprehensive tests (pytest + Vitest)
- Pre-commit (black + ruff)
- Tasks to practice agent-driven workflows

## Features

- **Notes**: Full CRUD, search with pagination and sorting, tag support
- **Tags**: Create, delete, attach/detach from notes, filter notes by tag
- **Action Items**: Create, complete, filter by status, bulk complete
- **Extraction**: Parse `#hashtags` and `- [ ] tasks` from note content

## Quickstart

1) Activate your conda environment

```bash
conda activate cs146s
```

2) (Optional) Install pre-commit hooks

```bash
pre-commit install
```

3) Run the app (from `week5/`)

```bash
make run
```

Open `http://localhost:8000` for the frontend and `http://localhost:8000/docs` for the API docs.

## Structure

```
backend/                # FastAPI app
  app/
    routers/            # API endpoints
    services/           # Business logic
    models.py           # SQLAlchemy models
    schemas.py          # Pydantic schemas
    main.py             # FastAPI app
  tests/                # pytest tests
frontend/
  index.html            # Static fallback UI
  app.js                # Static fallback JS
  ui/                   # React + Vite app
  dist/                 # Built React app (created by make run)
data/                   # SQLite DB
docs/                   # TASKS for agent-driven workflows
api/                    # Vercel serverless function
```

## Available Commands

```bash
make run          # Start the server (builds React if needed)
make test         # Run backend tests
make web-test     # Run React component tests
make format       # Format code with black and ruff
make lint         # Lint code with ruff
make web-install  # Install React dependencies
make web-dev      # Start React dev server with proxy
make web-build    # Build React app for production
```

## Tests

```bash
make test         # Backend tests (79 tests)
make web-test     # React tests (20 tests)
```

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Connect the repository to Vercel
3. Deploy - Vercel will auto-detect the configuration

The app is configured for serverless deployment:
- `api/index.py` - Serverless FastAPI function
- `frontend/ui/` - React app built by Vercel
- `vercel.json` - Routing configuration

### Environment Variables

- `DATABASE_URL` - SQLite database path (optional, defaults to `data/app.db`)
- `VITE_API_BASE_URL` - API URL for React app (optional, for external API)

## API Endpoints

### Notes
- `GET /notes` - List notes (paginated, filterable by tag)
- `GET /notes/search` - Search notes with pagination and sorting
- `POST /notes` - Create note
- `GET /notes/{id}` - Get note
- `PUT /notes/{id}` - Update note
- `DELETE /notes/{id}` - Delete note
- `POST /notes/{id}/extract` - Extract hashtags and action items
- `POST /notes/{id}/tags` - Attach tags to note
- `DELETE /notes/{id}/tags/{tag_id}` - Detach tag from note

### Tags
- `GET /tags` - List tags
- `POST /tags` - Create tag
- `DELETE /tags/{id}` - Delete tag

### Action Items
- `GET /action-items` - List items (paginated, filterable by completion)
- `POST /action-items` - Create item
- `PUT /action-items/{id}/complete` - Complete item
- `POST /action-items/bulk-complete` - Bulk complete items

## Configuration

Copy `.env.example` to `.env` (in `week5/`) to override defaults like the database path.
