def test_create_and_list_notes(client):
    response = client.post("/notes/", json={"title": "Test", "content": "Content"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test"

    response = client.get("/notes/")
    assert len(response.json()) == 1
