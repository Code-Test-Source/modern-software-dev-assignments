# API Documentation

Auto-generated from OpenAPI specification. Last synced: 2026-03-04

## Endpoints

### Root

#### `GET /`
Root endpoint serving the frontend HTML.

**Response**: `200` - HTML page

---

## Notes

### `GET /notes/`
List all notes.

**Response**: `200` - Array of [`NoteRead`](#noteread)

### `POST /notes/`
Create a new note.

**Request Body**: [`NoteCreate`](#notecreate)

**Response**: `201` - [`NoteRead`](#noteread)

**Errors**: `422` - Validation Error

### `GET /notes/search/`
Search notes by query.

**Query Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| q | string | No | Search query (case-insensitive) |

**Response**: `200` - Array of [`NoteRead`](#noteread)

**Errors**: `422` - Validation Error

### `GET /notes/{note_id}`
Get a single note by ID.

**Path Parameters**:
| Name | Type | Required |
|------|------|----------|
| note_id | integer | Yes |

**Response**: `200` - [`NoteRead`](#noteread)

**Errors**:
- `404` - Note not found
- `422` - Validation Error

### `PUT /notes/{note_id}`
Update a note (partial update supported).

**Path Parameters**:
| Name | Type | Required |
|------|------|----------|
| note_id | integer | Yes |

**Request Body**: [`NoteUpdate`](#noteupdate)

**Response**: `200` - [`NoteRead`](#noteread)

**Errors**:
- `404` - Note not found
- `422` - Validation Error

### `DELETE /notes/{note_id}`
Delete a note.

**Path Parameters**:
| Name | Type | Required |
|------|------|----------|
| note_id | integer | Yes |

**Response**: `204` - No content

**Errors**:
- `404` - Note not found
- `422` - Validation Error

---

## Action Items

### `GET /action-items/`
List all action items.

**Response**: `200` - Array of [`ActionItemRead`](#actionitemread)

### `POST /action-items/`
Create a new action item.

**Request Body**: [`ActionItemCreate`](#actionitemcreate)

**Response**: `201` - [`ActionItemRead`](#actionitemread)

**Errors**: `422` - Validation Error

### `PUT /action-items/{item_id}/complete`
Mark an action item as complete.

**Path Parameters**:
| Name | Type | Required |
|------|------|----------|
| item_id | integer | Yes |

**Response**: `200` - [`ActionItemRead`](#actionitemread)

**Errors**:
- `404` - Action item not found
- `422` - Validation Error

---

## Schemas

### NoteCreate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Note title |
| content | string | Yes | Note content |

### NoteUpdate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | No | Note title |
| content | string | No | Note content |

### NoteRead
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | Yes | Note ID |
| title | string | Yes | Note title |
| content | string | Yes | Note content |

### ActionItemCreate
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| description | string | Yes | Action item description |

### ActionItemRead
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | Yes | Action item ID |
| description | string | Yes | Action item description |
| completed | boolean | Yes | Completion status |

### HTTPValidationError
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| detail | array[ValidationError] | No | Validation error details |

### ValidationError
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| loc | array[string\|integer] | Yes | Location of the error |
| msg | string | Yes | Error message |
| type | string | Yes | Error type |
