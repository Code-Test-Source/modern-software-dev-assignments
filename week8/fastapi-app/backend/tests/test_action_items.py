def test_create_and_complete_action_item(client):
    response = client.post("/action-items/", json={"description": "Do something"})
    assert response.status_code == 201
    item_id = response.json()["id"]

    response = client.put(f"/action-items/{item_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True
