# Action Item Extractor

A FastAPI + SQLite application that converts free-form notes into enumerated action items. Supports both heuristic-based and LLM-powered extraction via Ollama.

## Features

- Extract action items from notes using heuristic rules
- LLM-powered extraction using Ollama (structured JSON output)
- Save notes and track action item completion
- RESTful API with FastAPI
- Simple HTML frontend

## Tech Stack

- **Backend**: FastAPI, SQLite, Pydantic
- **LLM**: Ollama (local large language model)
- **Testing**: pytest

## Setup

1. Activate the conda environment:
```bash
conda activate cs146s
```

2. Ensure Ollama is installed and a model is available:
```bash
ollama pull llama3.2:1b
```

3. Initialize the database (automatic on first run):
```bash
```

## Running the Application

From the project root:
```bash
poetry run uvicorn week2.app.main:app --reload
```

Open http://127.0.0.1:8000/ in your browser.

## API Endpoints

### Action Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/action-items/extract` | Extract action items (heuristic) |
| POST | `/action-items/extract-llm` | Extract action items (LLM-powered) |
| GET | `/action-items` | List all action items |
| POST | `/action-items/{id}/done` | Mark action item as done |

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a new note |
| GET | `/notes` | List all notes |
| GET | `/notes/{id}` | Get a specific note |

## Running Tests

```bash
pytest week2/tests/
```

## Project Structure

```
week2/
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── db.py             # SQLite database layer
│   ├── schemas.py        # Pydantic request/response models
│   ├── routers/
│   │   ├── action_items.py
│   │   └── notes.py
│   └── services/
│       └── extract.py    # Action item extraction logic
├── tests/
│   └── test_extract.py
├── frontend/
│   └── index.html
└── data/
    └── app.db
```
