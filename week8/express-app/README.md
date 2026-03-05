# Developer Control Center - Express Version

A Node.js Express application with SQLite for managing notes and action items.

## Tech Stack
- **Backend:** Node.js + Express
- **Database:** SQLite (better-sqlite3)
- **Frontend:** Vanilla JavaScript
- **API:** RESTful

## Prerequisites
- Node.js 18+
- npm

## Installation

```bash
cd express-app
npm install
```

## Running the App

```bash
npm start
```

The app will be available at `http://localhost:3000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/notes` | GET, POST | List/create notes |
| `/api/notes/:id` | GET, PATCH, DELETE | Retrieve/update/delete note |
| `/api/action-items` | GET, POST | List/create action items |
| `/api/action-items/:id` | GET, PATCH, DELETE | Retrieve/update/delete action item |
| `/api/action-items/:id/complete` | PUT | Mark action item as complete |

## Data Models

### Note
- `id` (integer, auto)
- `title` (string, required)
- `content` (text, optional)
- `created_at`, `updated_at` (datetime, auto)

### ActionItem
- `id` (integer, auto)
- `description` (text, required)
- `completed` (boolean, default false)
- `created_at` (datetime, auto)

## Notes
- Built manually without AI app generators
- Uses better-sqlite3 for synchronous SQLite operations
- Database file `devcenter.db` created automatically on first run
- CORS enabled for development
