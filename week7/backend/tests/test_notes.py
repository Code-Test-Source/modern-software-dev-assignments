def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_delete_note(client):
    # Create a note
    payload = {"title": "To Delete", "content": "This will be deleted"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Verify it exists
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200

    # Delete it
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    # Verify it's gone
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404

    # Delete non-existent note
    r = client.delete("/notes/99999")
    assert r.status_code == 404


def test_note_validation(client):
    # Empty title
    r = client.post("/notes/", json={"title": "", "content": "content"})
    assert r.status_code == 422

    # Whitespace-only title
    r = client.post("/notes/", json={"title": "   ", "content": "content"})
    assert r.status_code == 422

    # Empty content
    r = client.post("/notes/", json={"title": "title", "content": ""})
    assert r.status_code == 422

    # Title too long
    r = client.post("/notes/", json={"title": "x" * 201, "content": "content"})
    assert r.status_code == 422

    # Content too long
    r = client.post("/notes/", json={"title": "title", "content": "x" * 10001})
    assert r.status_code == 422

    # Valid note should work
    r = client.post("/notes/", json={"title": "Valid Title", "content": "Valid content"})
    assert r.status_code == 201


def test_put_note(client):
    # Create a note
    payload = {"title": "Original", "content": "Original content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Full update with PUT
    r = client.put(f"/notes/{note_id}", json={"title": "Replaced", "content": "Replaced content"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Replaced"
    assert data["content"] == "Replaced content"

    # PUT requires both fields
    r = client.put(f"/notes/{note_id}", json={"title": "Only title"})
    assert r.status_code == 422

    # PUT on non-existent note
    r = client.put("/notes/99999", json={"title": "New", "content": "New content"})
    assert r.status_code == 404


def test_notes_count(client):
    # Create multiple notes
    client.post("/notes/", json={"title": "Note 1", "content": "Content 1"})
    client.post("/notes/", json={"title": "Note 2", "content": "Content 2"})
    client.post("/notes/", json={"title": "Other", "content": "Content 3"})

    # Get count
    r = client.get("/notes/count")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 3

    # Get count with search filter
    r = client.get("/notes/count", params={"q": "Note"})
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 2


def test_negative_id_validation(client):
    # Negative note ID should return 400
    r = client.get("/notes/-1")
    assert r.status_code == 400

    r = client.patch("/notes/-1", json={"title": "Test"})
    assert r.status_code == 400

    r = client.delete("/notes/-1")
    assert r.status_code == 400


def test_pagination_validation(client):
    # Negative skip
    r = client.get("/notes/", params={"skip": -1})
    assert r.status_code == 422

    # Negative limit
    r = client.get("/notes/", params={"limit": -1})
    assert r.status_code == 422

    # Zero limit is valid but returns empty
    r = client.get("/notes/", params={"limit": 0})
    assert r.status_code == 200
    assert r.json() == []


def test_sort_field_validation(client):
    # Invalid sort field
    r = client.get("/notes/", params={"sort": "invalid_field"})
    assert r.status_code == 400

    # Valid sort fields
    r = client.get("/notes/", params={"sort": "title"})
    assert r.status_code == 200

    r = client.get("/notes/", params={"sort": "-updated_at"})
    assert r.status_code == 200
