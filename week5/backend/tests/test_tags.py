class TestTagsCRUD:
    def test_create_tag(self, client):
        r = client.post("/tags/", json={"name": "python"})
        assert r.status_code == 201
        data = r.json()["data"]
        assert data["name"] == "python"

    def test_create_tag_validation(self, client):
        # Empty name
        r = client.post("/tags/", json={"name": ""})
        assert r.status_code == 422

        # Invalid characters
        r = client.post("/tags/", json={"name": "tag with spaces"})
        assert r.status_code == 422

    def test_create_duplicate_tag(self, client):
        client.post("/tags/", json={"name": "duplicate"})
        r = client.post("/tags/", json={"name": "duplicate"})
        assert r.status_code == 400
        assert "already exists" in r.json()["error"]["message"].lower()

    def test_list_tags(self, client):
        client.post("/tags/", json={"name": "tag1"})
        client.post("/tags/", json={"name": "tag2"})

        r = client.get("/tags/")
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["total"] >= 2

    def test_get_tag(self, client):
        r = client.post("/tags/", json={"name": "gettest"})
        tag_id = r.json()["data"]["id"]

        r = client.get(f"/tags/{tag_id}")
        assert r.status_code == 200
        assert r.json()["data"]["name"] == "gettest"

    def test_get_tag_not_found(self, client):
        r = client.get("/tags/99999")
        assert r.status_code == 404

    def test_delete_tag(self, client):
        r = client.post("/tags/", json={"name": "deletetest"})
        tag_id = r.json()["data"]["id"]

        r = client.delete(f"/tags/{tag_id}")
        assert r.status_code == 200
        assert r.json()["data"]["deleted"] is True

        r = client.get(f"/tags/{tag_id}")
        assert r.status_code == 404

    def test_delete_tag_not_found(self, client):
        r = client.delete("/tags/99999")
        assert r.status_code == 404


class TestNoteTagAssociation:
    def test_attach_tags_to_note(self, client):
        # Create note and tags
        r = client.post("/notes/", json={"title": "Test", "content": "Content"})
        note_id = r.json()["data"]["id"]

        r1 = client.post("/tags/", json={"name": "tag1"})
        r2 = client.post("/tags/", json={"name": "tag2"})
        tag1_id = r1.json()["data"]["id"]
        tag2_id = r2.json()["data"]["id"]

        # Attach tags
        r = client.post(f"/notes/{note_id}/tags", json={"tag_ids": [tag1_id, tag2_id]})
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data["attached"]) == 2

        # Verify tags on note
        r = client.get(f"/notes/{note_id}")
        assert r.status_code == 200
        tags = r.json()["data"]["tags"]
        tag_names = {t["name"] for t in tags}
        assert tag_names == {"tag1", "tag2"}

    def test_attach_tag_not_found(self, client):
        r = client.post("/notes/", json={"title": "Test", "content": "Content"})
        note_id = r.json()["data"]["id"]

        r = client.post(f"/notes/{note_id}/tags", json={"tag_ids": [99999]})
        assert r.status_code == 404

    def test_detach_tag_from_note(self, client):
        # Create note with tag
        r = client.post("/notes/", json={"title": "Test", "content": "Content"})
        note_id = r.json()["data"]["id"]

        r = client.post("/tags/", json={"name": "removeme"})
        tag_id = r.json()["data"]["id"]

        client.post(f"/notes/{note_id}/tags", json={"tag_ids": [tag_id]})

        # Detach tag
        r = client.delete(f"/notes/{note_id}/tags/{tag_id}")
        assert r.status_code == 200

        # Verify tag removed
        r = client.get(f"/notes/{note_id}")
        tags = r.json()["data"]["tags"]
        assert len(tags) == 0

    def test_filter_notes_by_tag(self, client):
        # Create notes with different tags
        r1 = client.post("/notes/", json={"title": "Python Note", "content": "Content"})
        r2 = client.post("/notes/", json={"title": "Java Note", "content": "Content"})
        note1_id = r1.json()["data"]["id"]
        note2_id = r2.json()["data"]["id"]

        r = client.post("/tags/", json={"name": "python"})
        python_tag_id = r.json()["data"]["id"]
        client.post(f"/notes/{note1_id}/tags", json={"tag_ids": [python_tag_id]})

        r = client.post("/tags/", json={"name": "java"})
        java_tag_id = r.json()["data"]["id"]
        client.post(f"/notes/{note2_id}/tags", json={"tag_ids": [java_tag_id]})

        # Filter by python tag
        r = client.get("/notes/?tag=python")
        assert r.status_code == 200
        items = r.json()["data"]["items"]
        for item in items:
            tag_names = {t["name"] for t in item["tags"]}
            assert "python" in tag_names

    def test_filter_search_by_tag(self, client):
        # Create notes with tags
        r = client.post("/notes/", json={"title": "SearchTest", "content": "Content"})
        note_id = r.json()["data"]["id"]

        r = client.post("/tags/", json={"name": "searchable"})
        tag_id = r.json()["data"]["id"]
        client.post(f"/notes/{note_id}/tags", json={"tag_ids": [tag_id]})

        # Search with tag filter
        r = client.get("/notes/search/?tag=searchable")
        assert r.status_code == 200
        assert r.json()["data"]["total"] >= 1

    def test_filter_by_nonexistent_tag(self, client):
        r = client.get("/notes/?tag=nonexistent")
        assert r.status_code == 200
        assert r.json()["data"]["total"] == 0


class TestExtractWithTags:
    def test_extract_creates_tags(self, client):
        r = client.post("/notes/", json={"title": "Test", "content": "This has #tag1 and #tag2"})
        note_id = r.json()["data"]["id"]

        r = client.post(f"/notes/{note_id}/extract?apply=true")
        assert r.status_code == 200
        data = r.json()["data"]
        assert "tag1" in data["hashtags"]
        assert "tag2" in data["hashtags"]
        assert len(data["created_tags"]) == 2

        # Verify tags were attached to note
        r = client.get(f"/notes/{note_id}")
        tag_names = {t["name"] for t in r.json()["data"]["tags"]}
        assert tag_names == {"tag1", "tag2"}

    def test_extract_uses_existing_tags(self, client):
        # Create tag first
        client.post("/tags/", json={"name": "existing"})

        r = client.post("/notes/", json={"title": "Test", "content": "Use #existing tag"})
        note_id = r.json()["data"]["id"]

        r = client.post(f"/notes/{note_id}/extract?apply=true")
        assert r.status_code == 200
        data = r.json()["data"]
        assert len(data["created_tags"]) == 0  # No new tags created

        # Verify tag attached
        r = client.get(f"/notes/{note_id}")
        tag_names = {t["name"] for t in r.json()["data"]["tags"]}
        assert "existing" in tag_names
