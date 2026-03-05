"""Tests for Tag model and related endpoints."""


class TestTagEndpoints:
    """Tests for tag CRUD endpoints."""

    def test_create_tag(self, client):
        """Test creating a new tag."""
        response = client.post("/tags/", json={"name": "python", "color": "#3776AB"})
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "python"
        assert data["color"] == "#3776AB"
        assert "id" in data

    def test_create_tag_without_color(self, client):
        """Test creating a tag without a color."""
        response = client.post("/tags/", json={"name": "javascript"})
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "javascript"
        assert data["color"] is None

    def test_create_duplicate_tag_fails(self, client):
        """Test that creating a tag with duplicate name fails."""
        client.post("/tags/", json={"name": "python"})
        response = client.post("/tags/", json={"name": "python"})
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_list_tags(self, client):
        """Test listing all tags."""
        client.post("/tags/", json={"name": "python"})
        client.post("/tags/", json={"name": "javascript"})

        response = client.get("/tags/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        names = [tag["name"] for tag in data]
        assert "python" in names
        assert "javascript" in names

    def test_get_tag(self, client):
        """Test getting a single tag by ID."""
        create_response = client.post("/tags/", json={"name": "python", "color": "#3776AB"})
        tag_id = create_response.json()["id"]

        response = client.get(f"/tags/{tag_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "python"
        assert data["color"] == "#3776AB"

    def test_get_nonexistent_tag(self, client):
        """Test getting a tag that doesn't exist."""
        response = client.get("/tags/999")
        assert response.status_code == 404

    def test_update_tag(self, client):
        """Test updating a tag."""
        create_response = client.post("/tags/", json={"name": "python"})
        tag_id = create_response.json()["id"]

        response = client.patch(f"/tags/{tag_id}", json={"name": "python3", "color": "#306998"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "python3"
        assert data["color"] == "#306998"

    def test_update_tag_name_conflict(self, client):
        """Test that updating tag name to existing name fails."""
        client.post("/tags/", json={"name": "python"})
        create_response = client.post("/tags/", json={"name": "javascript"})
        tag_id = create_response.json()["id"]

        response = client.patch(f"/tags/{tag_id}", json={"name": "python"})
        assert response.status_code == 400

    def test_delete_tag(self, client):
        """Test deleting a tag."""
        create_response = client.post("/tags/", json={"name": "python"})
        tag_id = create_response.json()["id"]

        response = client.delete(f"/tags/{tag_id}")
        assert response.status_code == 204

        # Verify tag is deleted
        get_response = client.get(f"/tags/{tag_id}")
        assert get_response.status_code == 404


class TestNoteTagRelationship:
    """Tests for Note-Tag many-to-many relationship."""

    def test_create_note_with_tags(self, client):
        """Test creating a note with tags."""
        # Create tags first
        tag1_response = client.post("/tags/", json={"name": "python"})
        tag2_response = client.post("/tags/", json={"name": "tutorial"})
        tag1_id = tag1_response.json()["id"]
        tag2_id = tag2_response.json()["id"]

        # Create note with tags
        response = client.post(
            "/notes/",
            json={"title": "Python Guide", "content": "Learn Python", "tag_ids": [tag1_id, tag2_id]},
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data["tags"]) == 2
        tag_names = [t["name"] for t in data["tags"]]
        assert "python" in tag_names
        assert "tutorial" in tag_names

    def test_create_note_with_nonexistent_tag(self, client):
        """Test that creating a note with nonexistent tag fails."""
        response = client.post(
            "/notes/", json={"title": "Test", "content": "Content", "tag_ids": [999]}
        )
        assert response.status_code == 404

    def test_update_note_tags(self, client):
        """Test updating tags on a note."""
        # Create note without tags
        note_response = client.post("/notes/", json={"title": "Test", "content": "Content"})
        note_id = note_response.json()["id"]

        # Create tags
        tag_response = client.post("/tags/", json={"name": "python"})
        tag_id = tag_response.json()["id"]

        # Update note with tags
        response = client.patch(f"/notes/{note_id}", json={"tag_ids": [tag_id]})
        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) == 1
        assert data["tags"][0]["name"] == "python"

    def test_clear_note_tags(self, client):
        """Test clearing all tags from a note."""
        # Create tag and note with tag
        tag_response = client.post("/tags/", json={"name": "python"})
        tag_id = tag_response.json()["id"]
        note_response = client.post(
            "/notes/", json={"title": "Test", "content": "Content", "tag_ids": [tag_id]}
        )
        note_id = note_response.json()["id"]

        # Clear tags
        response = client.patch(f"/notes/{note_id}", json={"tag_ids": []})
        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) == 0

    def test_filter_notes_by_tag(self, client):
        """Test filtering notes by tag name."""
        # Create tags
        tag1_response = client.post("/tags/", json={"name": "python"})
        tag2_response = client.post("/tags/", json={"name": "javascript"})
        tag1_id = tag1_response.json()["id"]
        tag2_id = tag2_response.json()["id"]

        # Create notes with different tags
        client.post(
            "/notes/",
            json={"title": "Python Guide", "content": "Learn Python", "tag_ids": [tag1_id]},
        )
        client.post(
            "/notes/",
            json={"title": "JS Guide", "content": "Learn JavaScript", "tag_ids": [tag2_id]},
        )

        # Filter by tag
        response = client.get("/notes/?tag=python")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Python Guide"

    def test_delete_tag_removes_from_notes(self, client):
        """Test that deleting a tag removes it from all notes."""
        # Create tag and note with tag
        tag_response = client.post("/tags/", json={"name": "python"})
        tag_id = tag_response.json()["id"]
        note_response = client.post(
            "/notes/", json={"title": "Test", "content": "Content", "tag_ids": [tag_id]}
        )
        note_id = note_response.json()["id"]

        # Delete tag
        client.delete(f"/tags/{tag_id}")

        # Verify note still exists but has no tags
        response = client.get(f"/notes/{note_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["tags"]) == 0


class TestTagValidation:
    """Tests for tag input validation."""

    def test_invalid_color_format(self, client):
        """Test that invalid color format is rejected."""
        response = client.post("/tags/", json={"name": "test", "color": "red"})
        assert response.status_code == 422

    def test_empty_tag_name(self, client):
        """Test that empty tag name is rejected."""
        response = client.post("/tags/", json={"name": ""})
        assert response.status_code == 422

    def test_tag_name_too_long(self, client):
        """Test that tag name over 50 chars is rejected."""
        response = client.post("/tags/", json={"name": "a" * 51})
        assert response.status_code == 422
