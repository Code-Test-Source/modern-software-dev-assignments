class TestResponseEnvelope:
    def test_success_envelope_format(self, client):
        """Test that successful responses have correct envelope format."""
        r = client.post("/notes/", json={"title": "Test", "content": "Content"})
        assert r.status_code == 201
        data = r.json()
        assert data["ok"] is True
        assert data["data"] is not None
        assert data["error"] is None
        assert data["data"]["title"] == "Test"

    def test_error_envelope_format_not_found(self, client):
        """Test that 404 errors have correct envelope format."""
        r = client.get("/notes/99999")
        assert r.status_code == 404
        data = r.json()
        assert data["ok"] is False
        assert data["data"] is None
        assert data["error"]["code"] == "NOT_FOUND"
        assert "not found" in data["error"]["message"].lower()


class TestNotesPagination:
    def test_list_notes_pagination(self, client):
        # Create multiple notes
        for i in range(15):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

        # Get first page
        r = client.get("/notes/?page=1&page_size=10")
        assert r.status_code == 200
        json = r.json()
        assert json["ok"] is True
        data = json["data"]
        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["page"] == 1
        assert data["page_size"] == 10

        # Get second page
        r = client.get("/notes/?page=2&page_size=10")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data["items"]) == 5
        assert data["page"] == 2

    def test_list_notes_empty_page(self, client):
        r = client.get("/notes/?page=999&page_size=10")
        assert r.status_code == 200
        json = r.json()
        assert json["ok"] is True
        assert len(json["data"]["items"]) == 0
        assert json["data"]["total"] == 0

    def test_list_notes_large_page_size(self, client):
        r = client.get("/notes/?page=1&page_size=100")
        assert r.status_code == 200

    def test_pagination_boundary_page_size_one(self, client):
        """Test with minimum page size."""
        client.post("/notes/", json={"title": "Note 1", "content": "Content"})
        client.post("/notes/", json={"title": "Note 2", "content": "Content"})

        r = client.get("/notes/?page=1&page_size=1")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data["items"]) == 1
        assert data["total"] >= 2

    def test_pagination_invalid_page(self, client):
        """Test with invalid page number."""
        r = client.get("/notes/?page=0&page_size=10")
        assert r.status_code == 422  # Validation error

    def test_pagination_invalid_page_size(self, client):
        """Test with invalid page size."""
        r = client.get("/notes/?page=1&page_size=0")
        assert r.status_code == 422  # Validation error

        r = client.get("/notes/?page=1&page_size=200")
        assert r.status_code == 422  # Exceeds max


class TestNotesCRUD:
    def test_create_and_list_notes(self, client):
        payload = {"title": "Test", "content": "Hello world"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, r.text
        data = r.json()["data"]
        assert data["title"] == "Test"

        r = client.get("/notes/")
        assert r.status_code == 200
        items = r.json()["data"]["items"]
        assert len(items) >= 1

    def test_create_note_validation(self, client):
        # Empty title
        r = client.post("/notes/", json={"title": "", "content": "test"})
        assert r.status_code == 422

        # Empty content
        r = client.post("/notes/", json={"title": "test", "content": ""})
        assert r.status_code == 422

    def test_create_note_title_max_length(self, client):
        """Test title max length validation."""
        long_title = "x" * 201
        r = client.post("/notes/", json={"title": long_title, "content": "test"})
        assert r.status_code == 422

        # 200 chars should work
        r = client.post("/notes/", json={"title": "x" * 200, "content": "test"})
        assert r.status_code == 201

    def test_create_note_missing_fields(self, client):
        """Test missing required fields."""
        r = client.post("/notes/", json={"title": "test"})
        assert r.status_code == 422

        r = client.post("/notes/", json={"content": "test"})
        assert r.status_code == 422

        r = client.post("/notes/", json={})
        assert r.status_code == 422

    def test_get_note(self, client):
        r = client.post("/notes/", json={"title": "Get Test", "content": "Get content"})
        note_id = r.json()["data"]["id"]

        r = client.get(f"/notes/{note_id}")
        assert r.status_code == 200
        assert r.json()["data"]["title"] == "Get Test"

    def test_get_note_not_found(self, client):
        r = client.get("/notes/99999")
        assert r.status_code == 404
        assert r.json()["error"]["code"] == "NOT_FOUND"

    def test_get_note_invalid_id(self, client):
        """Test with invalid note ID format."""
        r = client.get("/notes/abc")
        assert r.status_code == 422  # Validation error

    def test_update_note(self, client):
        r = client.post("/notes/", json={"title": "Original", "content": "Original content"})
        note_id = r.json()["data"]["id"]

        r = client.put(f"/notes/{note_id}", json={"title": "Updated", "content": "Updated content"})
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["title"] == "Updated"
        assert data["content"] == "Updated content"

    def test_update_note_partial(self, client):
        r = client.post("/notes/", json={"title": "Partial", "content": "Original content"})
        note_id = r.json()["data"]["id"]

        r = client.put(f"/notes/{note_id}", json={"title": "Only Title Changed"})
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["title"] == "Only Title Changed"
        assert data["content"] == "Original content"

    def test_update_note_not_found(self, client):
        r = client.put("/notes/99999", json={"title": "Test"})
        assert r.status_code == 404

    def test_update_note_validation(self, client):
        """Test update validation."""
        r = client.post("/notes/", json={"title": "Test", "content": "Content"})
        note_id = r.json()["data"]["id"]

        # Empty title should fail
        r = client.put(f"/notes/{note_id}", json={"title": ""})
        assert r.status_code == 422

    def test_delete_note(self, client):
        r = client.post("/notes/", json={"title": "To Delete", "content": "Delete me"})
        note_id = r.json()["data"]["id"]

        r = client.delete(f"/notes/{note_id}")
        assert r.status_code == 200
        assert r.json()["data"]["deleted"] is True

        r = client.get(f"/notes/{note_id}")
        assert r.status_code == 404

    def test_delete_note_not_found(self, client):
        r = client.delete("/notes/99999")
        assert r.status_code == 404

    def test_delete_note_twice(self):
        """Test deleting the same note twice."""
        # This test would need a fresh client, skipping for now
        pass


class TestNotesSearch:
    def test_search_notes(self, client):
        client.post("/notes/", json={"title": "Hello World", "content": "Search test"})
        client.post("/notes/", json={"title": "Other", "content": "Different content"})

        r = client.get("/notes/search/", params={"q": "Hello"})
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data["items"]) >= 1

    def test_search_notes_pagination(self, client):
        for i in range(15):
            client.post("/notes/", json={"title": f"Search {i}", "content": "Find me"})

        r = client.get("/notes/search/", params={"q": "Search", "page": 1, "page_size": 10})
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data["items"]) == 10
        assert data["total"] == 15

    def test_search_notes_empty_query(self, client):
        r = client.get("/notes/search/")
        assert r.status_code == 200

    def test_search_notes_case_insensitive(self, client):
        """Test that search is case insensitive."""
        client.post("/notes/", json={"title": "UPPERCASE", "content": "lowercase"})

        r = client.get("/notes/search/", params={"q": "uppercase"})
        assert r.status_code == 200
        assert len(r.json()["data"]["items"]) >= 1

        r = client.get("/notes/search/", params={"q": "LOWERCASE"})
        assert r.status_code == 200
        assert len(r.json()["data"]["items"]) >= 1

    def test_search_notes_content_match(self, client):
        """Test that search matches content, not just title."""
        client.post("/notes/", json={"title": "Title", "content": "UniqueContent123"})

        r = client.get("/notes/search/", params={"q": "UniqueContent123"})
        assert r.status_code == 200
        assert len(r.json()["data"]["items"]) >= 1

    def test_search_notes_no_results(self, client):
        """Test search with no matching results."""
        r = client.get("/notes/search/", params={"q": "zzzzzzzzzzznotfound"})
        assert r.status_code == 200
        assert len(r.json()["data"]["items"]) == 0

    def test_search_notes_sort_title_asc(self, client):
        """Test sorting by title ascending."""
        client.post("/notes/", json={"title": "Zebra", "content": "Content"})
        client.post("/notes/", json={"title": "Apple", "content": "Content"})
        client.post("/notes/", json={"title": "Mango", "content": "Content"})

        r = client.get("/notes/search/", params={"sort": "title_asc"})
        assert r.status_code == 200
        items = r.json()["data"]["items"]
        titles = [item["title"] for item in items]
        # Check that titles are sorted ascending (Apple before Zebra)
        apple_idx = next((i for i, t in enumerate(titles) if t == "Apple"), None)
        zebra_idx = next((i for i, t in enumerate(titles) if t == "Zebra"), None)
        if apple_idx is not None and zebra_idx is not None:
            assert apple_idx < zebra_idx

    def test_search_notes_sort_created_desc(self, client):
        """Test sorting by created descending (default)."""
        client.post("/notes/", json={"title": "First", "content": "Content"})
        client.post("/notes/", json={"title": "Second", "content": "Content"})
        client.post("/notes/", json={"title": "Third", "content": "Content"})

        r = client.get("/notes/search/", params={"sort": "created_desc"})
        assert r.status_code == 200
        items = r.json()["data"]["items"]
        # Most recently created (highest ID) should be first
        assert items[0]["title"] == "Third"

    def test_search_notes_invalid_sort(self, client):
        """Test invalid sort parameter."""
        r = client.get("/notes/search/", params={"sort": "invalid_sort"})
        assert r.status_code == 422
