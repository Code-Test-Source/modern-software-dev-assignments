"""Comprehensive tests for Action Items endpoints including pagination and sorting."""
import time


class TestActionItemsPagination:
    """Tests for action item pagination functionality."""

    def test_pagination_skip_and_limit(self, client):
        """Test basic skip and limit pagination."""
        # Create 5 action items
        for i in range(5):
            client.post("/action-items/", json={"description": f"Task {i}"})
            time.sleep(0.01)

        # Get first 2 items (skip=0, limit=2)
        response = client.get("/action-items/?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Get next 2 items (skip=2, limit=2)
        response = client.get("/action-items/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Get last item (skip=4, limit=2)
        response = client.get("/action-items/?skip=4&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_pagination_skip_beyond_available(self, client):
        """Test pagination when skip exceeds total items."""
        client.post("/action-items/", json={"description": "Single task"})

        response = client.get("/action-items/?skip=100&limit=10")
        assert response.status_code == 200
        assert response.json() == []

    def test_pagination_default_limit(self, client):
        """Test that default limit is applied."""
        # Create more than default limit items
        for i in range(60):
            client.post("/action-items/", json={"description": f"Task {i}"})

        response = client.get("/action-items/")
        assert response.status_code == 200
        data = response.json()
        # Default limit is 50
        assert len(data) == 50

    def test_pagination_limit_max_enforced(self, client):
        """Test that limit cannot exceed 200 (FastAPI validation)."""
        for i in range(250):
            client.post("/action-items/", json={"description": f"Task {i}"})

        # FastAPI validates limit <= 200, returns 422 for larger values
        response = client.get("/action-items/?limit=300")
        assert response.status_code == 422  # Validation error

        # Verify limit=200 works
        response = client.get("/action-items/?limit=200")
        assert response.status_code == 200
        assert len(response.json()) == 200


class TestActionItemsSorting:
    """Tests for action item sorting functionality."""

    def test_sort_by_created_at_descending(self, client):
        """Test sorting by created_at descending (default)."""
        client.post("/action-items/", json={"description": "First task"})
        time.sleep(0.01)
        client.post("/action-items/", json={"description": "Second task"})
        time.sleep(0.01)
        client.post("/action-items/", json={"description": "Third task"})

        response = client.get("/action-items/?sort=-created_at")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        # Most recent first
        assert data[0]["description"] == "Third task"
        assert data[1]["description"] == "Second task"
        assert data[2]["description"] == "First task"

    def test_sort_by_created_at_ascending(self, client):
        """Test sorting by created_at ascending."""
        client.post("/action-items/", json={"description": "First task"})
        time.sleep(0.01)
        client.post("/action-items/", json={"description": "Second task"})
        time.sleep(0.01)
        client.post("/action-items/", json={"description": "Third task"})

        response = client.get("/action-items/?sort=created_at")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        # Oldest first
        assert data[0]["description"] == "First task"
        assert data[1]["description"] == "Second task"
        assert data[2]["description"] == "Third task"

    def test_sort_by_description(self, client):
        """Test sorting by description field."""
        client.post("/action-items/", json={"description": "Zebra task"})
        client.post("/action-items/", json={"description": "Apple task"})
        client.post("/action-items/", json={"description": "Mango task"})

        response = client.get("/action-items/?sort=description")
        assert response.status_code == 200
        data = response.json()
        descriptions = [item["description"] for item in data]
        assert descriptions == sorted(descriptions)

    def test_sort_by_description_descending(self, client):
        """Test sorting by description descending."""
        client.post("/action-items/", json={"description": "Zebra task"})
        client.post("/action-items/", json={"description": "Apple task"})
        client.post("/action-items/", json={"description": "Mango task"})

        response = client.get("/action-items/?sort=-description")
        assert response.status_code == 200
        data = response.json()
        descriptions = [item["description"] for item in data]
        assert descriptions == sorted(descriptions, reverse=True)

    def test_sort_invalid_field_defaults_to_created_at(self, client):
        """Test that invalid sort field falls back to created_at desc."""
        client.post("/action-items/", json={"description": "Task"})

        response = client.get("/action-items/?sort=invalid_field")
        assert response.status_code == 200
        # Should not error
        assert len(response.json()) >= 1


class TestActionItemsFiltering:
    """Tests for action item filtering by completed status."""

    def test_filter_completed_true(self, client):
        """Test filtering for completed items only."""
        # Create and complete an item
        r = client.post("/action-items/", json={"description": "Completed task"})
        item_id = r.json()["id"]
        client.put(f"/action-items/{item_id}/complete")

        # Create an incomplete item
        client.post("/action-items/", json={"description": "Incomplete task"})

        response = client.get("/action-items/?completed=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        for item in data:
            assert item["completed"] is True

    def test_filter_completed_false(self, client):
        """Test filtering for incomplete items only."""
        # Create and complete an item
        r = client.post("/action-items/", json={"description": "Completed task"})
        item_id = r.json()["id"]
        client.put(f"/action-items/{item_id}/complete")

        # Create an incomplete item
        client.post("/action-items/", json={"description": "Incomplete task"})

        response = client.get("/action-items/?completed=false")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        for item in data:
            assert item["completed"] is False

    def test_filter_combined_with_pagination(self, client):
        """Test filtering combined with pagination."""
        # Create 5 completed items
        for i in range(5):
            r = client.post("/action-items/", json={"description": f"Completed {i}"})
            client.put(f"/action-items/{r.json()['id']}/complete")

        # Create 5 incomplete items
        for i in range(5):
            client.post("/action-items/", json={"description": f"Incomplete {i}"})

        # Get first 3 completed items
        response = client.get("/action-items/?completed=true&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        for item in data:
            assert item["completed"] is True


class TestActionItemsCRUD:
    """Tests for basic CRUD operations."""

    def test_create_action_item(self, client):
        """Test creating an action item."""
        response = client.post("/action-items/", json={"description": "Test task"})
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "Test task"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data

    def test_complete_action_item(self, client):
        """Test completing an action item."""
        create_response = client.post("/action-items/", json={"description": "To complete"})
        item_id = create_response.json()["id"]

        response = client.put(f"/action-items/{item_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

    def test_update_action_item(self, client):
        """Test updating an action item."""
        create_response = client.post("/action-items/", json={"description": "Original"})
        item_id = create_response.json()["id"]

        response = client.patch(f"/action-items/{item_id}", json={"description": "Updated", "completed": True})
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Updated"
        assert data["completed"] is True

    def test_partial_update_action_item(self, client):
        """Test partial update of an action item."""
        create_response = client.post("/action-items/", json={"description": "Original"})
        item_id = create_response.json()["id"]

        response = client.patch(f"/action-items/{item_id}", json={"completed": True})
        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Original"  # Unchanged
        assert data["completed"] is True

    def test_get_nonexistent_item(self, client):
        """Test getting an item that doesn't exist."""
        response = client.patch("/action-items/99999", json={"description": "Test"})
        assert response.status_code == 404
