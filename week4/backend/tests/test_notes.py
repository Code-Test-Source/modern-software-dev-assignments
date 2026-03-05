def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_update_note(client):
    # Create a note
    payload = {"title": "Original Title", "content": "Original content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Update the note
    update_payload = {"title": "Updated Title", "content": "Updated content"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"


def test_update_note_partial(client):
    # Create a note
    payload = {"title": "Original Title", "content": "Original content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Update only the title
    r = client.put(f"/notes/{note_id}", json={"title": "New Title"})
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "New Title"
    assert data["content"] == "Original content"  # Unchanged


def test_update_note_not_found(client):
    r = client.put("/notes/9999", json={"title": "New Title"})
    assert r.status_code == 404


def test_delete_note(client):
    # Create a note
    payload = {"title": "To Delete", "content": "This will be deleted"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    # Delete the note
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    # Verify it's deleted
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_note_not_found(client):
    r = client.delete("/notes/9999")
    assert r.status_code == 404
