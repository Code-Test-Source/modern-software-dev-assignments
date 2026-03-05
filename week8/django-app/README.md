# Developer Control Center - Django Version

A Django REST Framework application for managing notes and action items.

## Tech Stack
- **Backend:** Django 5.0+ with Django REST Framework
- **Database:** SQLite
- **API:** RESTful API with ViewSets

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

# Run migrations
python manage.py migrate

# (Optional) Create superuser for admin access
python manage.py createsuperuser
```

## Running the App

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/notes/` | GET, POST | List/create notes |
| `/api/notes/{id}/` | GET, PUT, PATCH, DELETE | Retrieve/update/delete note |
| `/api/action-items/` | GET, POST | List/create action items |
| `/api/action-items/{id}/` | GET, PUT, PATCH, DELETE | Retrieve/update/delete action item |
| `/api/action-items/{id}/complete/` | PUT | Mark action item as complete |

## Data Models

### Note
- `title` (string, max 200 chars)
- `content` (text)
- `created_at` (datetime, auto)
- `updated_at` (datetime, auto)

### ActionItem
- `description` (text)
- `completed` (boolean, default false)
- `created_at` (datetime, auto)

## Notes
- Built manually without AI app generators
- Uses Django REST Framework's ViewSet pattern for clean CRUD operations
- CORS enabled for frontend integration
