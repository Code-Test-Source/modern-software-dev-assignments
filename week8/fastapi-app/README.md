# Developer Control Center - FastAPI Version

A FastAPI application with vanilla JS frontend for managing notes and action items.

## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** Vanilla JavaScript
- **API:** RESTful with Pydantic validation

## Prerequisites
- Python 3.10+
- pip

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the App

```bash
# From the fastapi-app directory
uvicorn backend.app.main:app --reload
```

The app will be available at `http://localhost:8000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/notes/` | GET, POST | List/create notes |
| `/notes/{id}` | GET, PATCH, DELETE | Retrieve/update/delete note |
| `/action-items/` | GET, POST | List/create action items |
| `/action-items/{id}` | GET, PATCH, DELETE | Retrieve/update/delete action item |
| `/action-items/{id}/complete` | PUT | Mark action item as complete |

## Running Tests

```bash
pytest backend/tests/
```

## Data Models

### Note
- `title` (string, required)
- `content` (text, optional)
- `created_at`, `updated_at` (datetime, auto)

### ActionItem
- `description` (text, required)
- `completed` (boolean, default false)
- `created_at` (datetime, auto)

## Notes
- Built manually without AI app generators
- Uses SQLAlchemy ORM with SQLite
- CORS enabled for development
