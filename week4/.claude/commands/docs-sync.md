# API Documentation Sync

Synchronize API documentation with the current OpenAPI specification from the running server.

## Usage
```
/docs-sync
```

## Prerequisites
- Server must be running at http://localhost:8000
- Run `make run` first if server is not running

## Steps

1. **Fetch OpenAPI Spec**: Get the current spec from `/openapi.json`:
   ```bash
   curl -s http://localhost:8000/openapi.json
   ```

2. **Parse Endpoints**: Extract all routes, methods, request bodies, and response schemas from the spec.

3. **Check for Existing Docs**: Look for `docs/API.md` file.

4. **Generate/Update Documentation**: Create or update `docs/API.md` with:
   - All endpoints grouped by router (notes, action-items)
   - HTTP method and path
   - Request body schema
   - Response schema
   - Status codes

5. **Detect Changes**: Compare with previous documentation (if exists) and report:
   - New endpoints added
   - Endpoints removed
   - Endpoints modified

## Output Format

```
## API Documentation Sync Report

### Endpoints Found (X total)

#### Notes (/notes)
- GET /notes/ - List all notes
- POST /notes/ - Create a note
- GET /notes/search/ - Search notes
- GET /notes/{note_id} - Get single note

#### Action Items (/action-items)
- GET /action-items/ - List all action items
- POST /action-items/ - Create an action item
- PUT /action-items/{item_id}/complete - Mark as complete

### Changes Detected
- [+] New: POST /notes/extract
- [~] Modified: GET /notes/search/ (added query param)
- [-] Removed: None

### Documentation Updated
- File: docs/API.md
- Status: Created/Updated

### TODOs
- [ ] Add example requests/responses
- [ ] Document error codes
```

## Safety Notes
- Read-only operation on the server
- Creates/updates only `docs/API.md`
- Original spec from `/openapi.json` is untouched
