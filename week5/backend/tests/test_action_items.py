class TestResponseEnvelope:
    def test_success_envelope_format(self, client):
        """Test that successful responses have correct envelope format."""
        r = client.post("/action-items/", json={"description": "Test item"})
        assert r.status_code == 201
        data = r.json()
        assert data["ok"] is True
        assert data["data"] is not None
        assert data["error"] is None
        assert data["data"]["description"] == "Test item"

    def test_error_envelope_format_not_found(self, client):
        """Test that 404 errors have correct envelope format."""
        r = client.put("/action-items/99999/complete")
        assert r.status_code == 404
        data = r.json()
        assert data["ok"] is False
        assert data["data"] is None
        assert data["error"]["code"] == "NOT_FOUND"


class TestActionItemsPagination:
    def test_list_items_pagination(self, client):
        # Create multiple items
        for i in range(15):
            client.post("/action-items/", json={"description": f"Item {i}"})

        # Get first page
        r = client.get("/action-items/?page=1&page_size=10")
        assert r.status_code == 200
        json = r.json()
        assert json["ok"] is True
        data = json["data"]
        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["page"] == 1

        # Get second page
        r = client.get("/action-items/?page=2&page_size=10")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data["items"]) == 5

    def test_pagination_boundary_page_size_one(self, client):
        """Test with minimum page size."""
        client.post("/action-items/", json={"description": "Item 1"})
        client.post("/action-items/", json={"description": "Item 2"})

        r = client.get("/action-items/?page=1&page_size=1")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data["items"]) == 1

    def test_pagination_invalid_page(self, client):
        """Test with invalid page number."""
        r = client.get("/action-items/?page=0&page_size=10")
        assert r.status_code == 422


class TestActionItemsCRUD:
    def test_create_and_complete_action_item(self, client):
        payload = {"description": "Ship it"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201, r.text
        item = r.json()["data"]
        assert item["completed"] is False

        r = client.put(f"/action-items/{item['id']}/complete")
        assert r.status_code == 200
        done = r.json()["data"]
        assert done["completed"] is True

    def test_create_item_validation(self, client):
        r = client.post("/action-items/", json={"description": ""})
        assert r.status_code == 422

    def test_create_item_missing_field(self, client):
        """Test missing required description field."""
        r = client.post("/action-items/", json={})
        assert r.status_code == 422

    def test_complete_item_not_found(self, client):
        r = client.put("/action-items/99999/complete")
        assert r.status_code == 404
        assert r.json()["error"]["code"] == "NOT_FOUND"

    def test_complete_item_twice(self, client):
        """Test completing an already completed item."""
        r = client.post("/action-items/", json={"description": "Test"})
        item_id = r.json()["data"]["id"]

        # Complete once
        r = client.put(f"/action-items/{item_id}/complete")
        assert r.status_code == 200
        assert r.json()["data"]["completed"] is True

        # Complete again (should still work)
        r = client.put(f"/action-items/{item_id}/complete")
        assert r.status_code == 200
        assert r.json()["data"]["completed"] is True


class TestActionItemsFilter:
    def test_filter_by_completed(self, client):
        # Create items
        client.post("/action-items/", json={"description": "Open item"})
        r2 = client.post("/action-items/", json={"description": "Done item"})
        client.put(f"/action-items/{r2.json()['data']['id']}/complete")

        # Filter for open items
        r = client.get("/action-items/?completed=false")
        assert r.status_code == 200
        data = r.json()["data"]
        assert all(not item["completed"] for item in data["items"])

        # Filter for completed items
        r = client.get("/action-items/?completed=true")
        assert r.status_code == 200
        data = r.json()["data"]
        assert all(item["completed"] for item in data["items"])

    def test_filter_all_items(self, client):
        client.post("/action-items/", json={"description": "Item 1"})
        client.post("/action-items/", json={"description": "Item 2"})

        r = client.get("/action-items/")
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["total"] >= 2

    def test_filter_with_pagination(self, client):
        """Test combined filter and pagination."""
        # Create 5 open and 5 completed items
        for i in range(5):
            r = client.post("/action-items/", json={"description": f"Open {i}"})
        for i in range(5):
            r = client.post("/action-items/", json={"description": f"Done {i}"})
            client.put(f"/action-items/{r.json()['data']['id']}/complete")

        # Filter for completed with pagination
        r = client.get("/action-items/?completed=true&page=1&page_size=3")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data["items"]) == 3
        assert data["total"] == 5
        assert all(item["completed"] for item in data["items"])


class TestActionItemsBulkComplete:
    def test_bulk_complete(self, client):
        # Create items
        ids = []
        for i in range(3):
            r = client.post("/action-items/", json={"description": f"Bulk {i}"})
            ids.append(r.json()["data"]["id"])

        # Bulk complete
        r = client.post("/action-items/bulk-complete", json={"ids": ids})
        assert r.status_code == 200
        items = r.json()["data"]
        assert len(items) == 3
        assert all(item["completed"] for item in items)

    def test_bulk_complete_empty_list(self, client):
        r = client.post("/action-items/bulk-complete", json={"ids": []})
        assert r.status_code == 422

    def test_bulk_complete_not_found(self, client):
        r = client.post("/action-items/bulk-complete", json={"ids": [99999]})
        assert r.status_code == 404
        assert r.json()["error"]["code"] == "NOT_FOUND"

    def test_bulk_complete_single_item(self, client):
        """Test bulk complete with single item."""
        r = client.post("/action-items/", json={"description": "Single"})
        item_id = r.json()["data"]["id"]

        r = client.post("/action-items/bulk-complete", json={"ids": [item_id]})
        assert r.status_code == 200
        assert len(r.json()["data"]) == 1
        assert r.json()["data"][0]["completed"] is True

    def test_bulk_complete_mixed_valid_invalid(self, client):
        """Test bulk complete with some valid and some invalid IDs."""
        r = client.post("/action-items/", json={"description": "Valid"})
        valid_id = r.json()["data"]["id"]

        # Should fail on first invalid ID
        r = client.post("/action-items/bulk-complete", json={"ids": [valid_id, 99998, 99999]})
        assert r.status_code == 404

    def test_bulk_complete_already_completed(self, client):
        """Test bulk completing already completed items."""
        r = client.post("/action-items/", json={"description": "Already done"})
        item_id = r.json()["data"]["id"]
        client.put(f"/action-items/{item_id}/complete")

        # Should still work
        r = client.post("/action-items/bulk-complete", json={"ids": [item_id]})
        assert r.status_code == 200
        assert r.json()["data"][0]["completed"] is True
