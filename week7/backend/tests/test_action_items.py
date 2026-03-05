def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_delete_action_item(client):
    # Create an action item
    payload = {"description": "To delete"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201
    item_id = r.json()["id"]

    # Verify it exists
    r = client.get(f"/action-items/{item_id}")
    assert r.status_code == 200

    # Delete it
    r = client.delete(f"/action-items/{item_id}")
    assert r.status_code == 204

    # Verify it's gone
    r = client.get(f"/action-items/{item_id}")
    assert r.status_code == 404

    # Delete non-existent item
    r = client.delete("/action-items/99999")
    assert r.status_code == 404


def test_action_item_validation(client):
    # Empty description
    r = client.post("/action-items/", json={"description": ""})
    assert r.status_code == 422

    # Whitespace-only description
    r = client.post("/action-items/", json={"description": "   "})
    assert r.status_code == 422

    # Description too long
    r = client.post("/action-items/", json={"description": "x" * 1001})
    assert r.status_code == 422

    # Valid item should work
    r = client.post("/action-items/", json={"description": "Valid description"})
    assert r.status_code == 201


def test_get_action_item_by_id(client):
    # Create an action item
    payload = {"description": "Find me"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201
    item_id = r.json()["id"]

    # Get by ID
    r = client.get(f"/action-items/{item_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["description"] == "Find me"
    assert data["completed"] is False

    # Get non-existent item
    r = client.get("/action-items/99999")
    assert r.status_code == 404


def test_uncomplete_action_item(client):
    # Create and complete an action item
    r = client.post("/action-items/", json={"description": "Task to uncomplete"})
    assert r.status_code == 201
    item_id = r.json()["id"]

    # Complete it
    r = client.put(f"/action-items/{item_id}/complete")
    assert r.status_code == 200
    assert r.json()["completed"] is True

    # Uncomplete it
    r = client.put(f"/action-items/{item_id}/uncomplete")
    assert r.status_code == 200
    data = r.json()
    assert data["completed"] is False
    assert data["description"] == "Task to uncomplete"

    # Uncomplete non-existent item
    r = client.put("/action-items/99999/uncomplete")
    assert r.status_code == 404


def test_action_items_count(client):
    # Create multiple items
    client.post("/action-items/", json={"description": "Task 1"})
    client.post("/action-items/", json={"description": "Task 2"})
    client.post("/action-items/", json={"description": "Task 3"})

    # Complete one
    r = client.get("/action-items/")
    items = r.json()
    if items:
        client.put(f"/action-items/{items[0]['id']}/complete")

    # Get total count
    r = client.get("/action-items/count")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 3

    # Get count of completed items
    r = client.get("/action-items/count", params={"completed": True})
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 1

    # Get count of pending items
    r = client.get("/action-items/count", params={"completed": False})
    assert r.status_code == 200
    data = r.json()
    assert data["count"] >= 2


def test_action_item_negative_id_validation(client):
    # Negative action item ID should return 400
    r = client.get("/action-items/-1")
    assert r.status_code == 400

    r = client.patch("/action-items/-1", json={"description": "Test"})
    assert r.status_code == 400

    r = client.delete("/action-items/-1")
    assert r.status_code == 400

    r = client.put("/action-items/-1/complete")
    assert r.status_code == 400

    r = client.put("/action-items/-1/uncomplete")
    assert r.status_code == 400


def test_action_items_pagination_validation(client):
    # Negative skip
    r = client.get("/action-items/", params={"skip": -1})
    assert r.status_code == 422

    # Negative limit
    r = client.get("/action-items/", params={"limit": -1})
    assert r.status_code == 422


def test_action_items_sort_field_validation(client):
    # Invalid sort field
    r = client.get("/action-items/", params={"sort": "invalid_field"})
    assert r.status_code == 400

    # Valid sort fields
    r = client.get("/action-items/", params={"sort": "description"})
    assert r.status_code == 200

    r = client.get("/action-items/", params={"sort": "-completed"})
    assert r.status_code == 200
