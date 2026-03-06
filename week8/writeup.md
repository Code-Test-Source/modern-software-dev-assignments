# Week 8 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Feiyang Zhou** \
SUNet ID: **TODO** \
Citations: **Claude Code (Opus 4.6) for code generation and documentation**

This assignment took me about **3** hours to do.


## App Concept
```
Developer Control Center - A productivity web application for managing notes and action items.

Main Features:
- Notes: Create, read, update, delete, and search notes with title and content
- Action Items: Create, track, complete, and delete action items with status management
- Real-time UI updates without page refresh
- Search and filter capabilities
- Persistent storage with SQLite database

This app provides a clean interface for developers to organize their thoughts (notes) and track
their tasks (action items) in a single, cohesive application.
```


## Version #1 Description
```
APP DETAILS:
===============
Folder name: django-app
AI app generation platform: None (built manually with Claude Code)
Tech Stack: Django 5.0 + Django REST Framework + SQLite
Persistence: SQLite database
Frameworks/Libraries Used: Django, djangorestframework, django-cors-headers
(Optional but recommended) Screenshots of core flows: N/A

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
   - Django's default project structure required manual setup of apps
   - Resolved by creating modular apps (notes, actionitems) with ViewSets

b. Prompting (e.g. what required additional guidance; what worked poorly/well):
   - N/A - built manually without AI app generator

c. Approximate time-to-first-run and time-to-feature metrics:
   - ~30 minutes to setup project structure
   - ~15 minutes per model/serializer/viewset
```


## Version #2 Description
```
APP DETAILS:
===============
Folder name: fastapi-app
AI app generation platform: None (built manually with Claude Code)
Tech Stack: FastAPI + SQLAlchemy + SQLite + Vanilla JS
Persistence: SQLite database with SQLAlchemy ORM
Frameworks/Libraries Used: FastAPI, SQLAlchemy, Pydantic, Uvicorn
(Optional but recommended) Screenshots of core flows: N/A

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
   - FastAPI requires explicit database setup compared to Django
   - Resolved by using SQLAlchemy's declarative base and session management

b. Prompting (e.g. what required additional guidance; what worked poorly/well):
   - N/A - built manually without AI app generator

c. Approximate time-to-first-run and time-to-feature metrics:
   - ~25 minutes to setup project structure
   - ~20 minutes for frontend integration
```


## Version #3 Description
```
APP DETAILS:
===============
Folder name: express-app
AI app generation platform: None (built manually with Claude Code)
Tech Stack: Node.js + Express + sql.js + Vanilla JS
Persistence: SQLite database via sql.js (in-memory with file persistence)
Frameworks/Libraries Used: Express, sql.js, cors
(Optional but recommended) Screenshots of core flows: N/A

REFLECTIONS:
===============
a. Issues encountered per stack and how you resolved them:
   - better-sqlite3 requires native compilation which is incompatible with Node.js 25
   - Resolved by switching to sql.js (WebAssembly-based SQLite) for pure-JS compatibility
   - Boolean handling in SQLite required explicit conversion (0/1 to true/false)

b. Prompting (e.g. what required additional guidance; what worked poorly/well):
   - N/A - built manually without AI app generator

c. Approximate time-to-first-run and time-to-feature metrics:
   - ~20 minutes to setup project structure
   - ~10 minutes per route group (notes, action items)
```


## Note on Bolt.new
Bolt.new was not available during development, so all three versions were built manually using Claude Code for code generation assistance. Each version demonstrates a distinct technology stack with the same functionality.
