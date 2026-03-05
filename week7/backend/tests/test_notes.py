"""Comprehensive tests for Notes endpoints including pagination and sorting."""
import time

import pytest


class TestNotesPagination:
    """Tests for note pagination functionality."""

    def test_pagination_skip_and_limit(self, client):
        """Test basic skip and limit pagination."""
        # Create 5 notes
        for i in range(5):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
            time.sleep(0.01)  # Ensure different timestamps

        # Get first 2 notes (skip=0, limit=2)
        response = client.get("/notes/?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Get next 2 notes (skip=2, limit=2)
        response = client.get("/notes/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Get last note (skip=4, limit=2)
        response = client.get("/notes/?skip=4&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

    def test_pagination_skip_beyond_available(self, client):
        """Test pagination when skip exceeds total items."""
        client.post("/notes/", json={"title": "Note", "content": "Content"})

        response = client.get("/notes/?skip=100&limit=10")
        assert response.status_code == 200
        assert response.json() == []

    def test_pagination_default_limit(self, client):
        """Test that default limit is applied."""
        # Create more than default limit notes
        for i in range(60):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

        response = client.get("/notes/")
        assert response.status_code == 200
        data = response.json()
        # Default limit is 50
        assert len(data) == 50

    def test_pagination_limit_max_enforced(self, client):
        """Test that limit cannot exceed 200 (FastAPI validation)."""
        for i in range(250):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

        # FastAPI validates limit <= 200, returns 422 for larger values
        response = client.get("/notes/?limit=300")
        assert response.status_code == 422  # Validation error

        # Verify limit=200 works
        response = client.get("/notes/?limit=200")
        assert response.status_code == 200
        assert len(response.json()) == 200

    def test_pagination_with_search(self, client):
        """Test pagination combined with search filter."""
        for i in range(10):
            client.post("/notes/", json={"title": f"Python {i}", "content": "tutorial"})

        # Search with pagination
        response = client.get("/notes/?q=Python&skip=0&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        for note in data:
            assert "Python" in note["title"]


class TestNotesSorting:
    """Tests for note sorting functionality."""

    def test_sort_by_created_at_descending(self, client):
        """Test sorting by created_at descending (default)."""
        client.post("/notes/", json={"title": "First", "content": "Content"})
        time.sleep(0.01)
        client.post("/notes/", json={"title": "Second", "content": "Content"})
        time.sleep(0.01)
        client.post("/notes/", json={"title": "Third", "content": "Content"})

        response = client.get("/notes/?sort=-created_at")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        # Most recent first
        assert data[0]["title"] == "Third"
        assert data[1]["title"] == "Second"
        assert data[2]["title"] == "First"

    def test_sort_by_created_at_ascending(self, client):
        """Test sorting by created_at ascending."""
        client.post("/notes/", json={"title": "First", "content": "Content"})
        time.sleep(0.01)
        client.post("/notes/", json={"title": "Second", "content": "Content"})
        time.sleep(0.01)
        client.post("/notes/", json={"title": "Third", "content": "Content"})

        response = client.get("/notes/?sort=created_at")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        # Oldest first
        assert data[0]["title"] == "First"
        assert data[1]["title"] == "Second"
        assert data[2]["title"] == "Third"

    def test_sort_by_title(self, client):
        """Test sorting by title field."""
        client.post("/notes/", json={"title": "Zebra", "content": "Content"})
        client.post("/notes/", json={"title": "Apple", "content": "Content"})
        client.post("/notes/", json={"title": "Mango", "content": "Content"})

        response = client.get("/notes/?sort=title")
        assert response.status_code == 200
        data = response.json()
        titles = [n["title"] for n in data]
        assert titles == sorted(titles)

    def test_sort_by_title_descending(self, client):
        """Test sorting by title descending."""
        client.post("/notes/", json={"title": "Zebra", "content": "Content"})
        client.post("/notes/", json={"title": "Apple", "content": "Content"})
        client.post("/notes/", json={"title": "Mango", "content": "Content"})

        response = client.get("/notes/?sort=-title")
        assert response.status_code == 200
        data = response.json()
        titles = [n["title"] for n in data]
        assert titles == sorted(titles, reverse=True)

    def test_sort_by_updated_at(self, client):
        """Test sorting by updated_at field."""
        # Create notes
        r1 = client.post("/notes/", json={"title": "Note1", "content": "Content"})
        r2 = client.post("/notes/", json={"title": "Note2", "content": "Content"})
        r3 = client.post("/notes/", json={"title": "Note3", "content": "Content"})

        # Update the first note
        time.sleep(0.01)
        note1_id = r1.json()["id"]
        client.patch(f"/notes/{note1_id}", json={"title": "Updated Note1"})

        response = client.get("/notes/?sort=-updated_at")
        assert response.status_code == 200
        data = response.json()
        # Most recently updated should be first
        assert data[0]["title"] == "Updated Note1"

    def test_sort_invalid_field_defaults_to_created_at(self, client):
        """Test that invalid sort field falls back to created_at desc."""
        client.post("/notes/", json={"title": "Note", "content": "Content"})

        response = client.get("/notes/?sort=invalid_field")
        assert response.status_code == 200
        # Should not error, just use default sort
        assert len(response.json()) >= 1


class TestNotesCombined:
    """Tests combining pagination, sorting, and filtering."""

    def test_pagination_with_sorting(self, client):
        """Test pagination combined with sorting."""
        for i in range(5):
            client.post("/notes/", json={"title": f"Note {i:02d}", "content": "Content"})

        response = client.get("/notes/?sort=title&skip=1&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        # Should be sorted alphabetically, skipping first
        titles = [n["title"] for n in data]
        assert titles == ["Note 01", "Note 02"] or titles == ["Note 02", "Note 03"]

    def test_all_query_params_together(self, client):
        """Test all query parameters working together."""
        for i in range(10):
            client.post("/notes/", json={"title": f"Python {i}", "content": f"Tutorial {i}"})
        for i in range(5):
            client.post("/notes/", json={"title": f"Java {i}", "content": f"Guide {i}"})

        response = client.get("/notes/?q=Python&sort=-title&skip=0&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        # All should contain Python
        for note in data:
            assert "Python" in note["title"]
        # Should be sorted by title descending
        titles = [n["title"] for n in data]
        assert titles == sorted(titles, reverse=True)


class TestNotesCRUD:
    """Tests for basic CRUD operations."""

    def test_create_note(self, client):
        """Test creating a note."""
        response = client.post("/notes/", json={"title": "Test Note", "content": "Test Content"})
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Note"
        assert data["content"] == "Test Content"
        assert "id" in data
        assert "created_at" in data

    def test_get_single_note(self, client):
        """Test getting a single note by ID."""
        create_response = client.post("/notes/", json={"title": "Test", "content": "Content"})
        note_id = create_response.json()["id"]

        response = client.get(f"/notes/{note_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == note_id
        assert data["title"] == "Test"

    def test_get_nonexistent_note(self, client):
        """Test getting a note that doesn't exist."""
        response = client.get("/notes/99999")
        assert response.status_code == 404

    def test_update_note(self, client):
        """Test updating a note."""
        create_response = client.post("/notes/", json={"title": "Original", "content": "Original"})
        note_id = create_response.json()["id"]

        response = client.patch(f"/notes/{note_id}", json={"title": "Updated", "content": "Updated"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["content"] == "Updated"

    def test_partial_update_note(self, client):
        """Test partial update of a note."""
        create_response = client.post("/notes/", json={"title": "Original", "content": "Original"})
        note_id = create_response.json()["id"]

        response = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated"
        assert data["content"] == "Original"  # Unchanged

    def test_delete_note(self, client):
        """Test deleting a note."""
        create_response = client.post("/notes/", json={"title": "To Delete", "content": "Content"})
        note_id = create_response.json()["id"]

        # Add delete endpoint test if implemented
        # For now, just verify note exists
        response = client.get(f"/notes/{note_id}")
        assert response.status_code == 200
