from backend.app.services.extract import extract_action_items, extract_all, extract_hashtags


class TestExtractActionItems:
    def test_extract_action_items_basic(self):
        text = """
        This is a note
        - TODO: write tests
        - Ship it!
        Not actionable
        """.strip()
        items = extract_action_items(text)
        assert "TODO: write tests" in items
        assert "Ship it!" in items

    def test_extract_markdown_tasks(self):
        """Test extraction of markdown task syntax - [ ] task."""
        text = """
        My tasks:
        - [ ] Buy groceries
        - [x] Already done
        - [ ] Call mom
        """
        items = extract_action_items(text)
        assert "Buy groceries" in items
        assert "Call mom" in items
        assert "Already done" not in items  # Completed tasks should not be extracted

    def test_extract_todo_case_insensitive(self):
        """Test TODO extraction is case insensitive."""
        text = "todo: lowercase\nTODO: uppercase"
        items = extract_action_items(text)
        assert len(items) == 2
        assert "todo: lowercase" in items
        assert "TODO: uppercase" in items

    def test_extract_exclamation(self):
        """Test lines ending with !."""
        text = "Do this now!"
        items = extract_action_items(text)
        assert "Do this now!" in items


class TestExtractHashtags:
    def test_extract_hashtags_basic(self):
        text = "This is a #test note with #multiple #hashtags"
        tags = extract_hashtags(text)
        assert set(tags) == {"test", "multiple", "hashtags"}

    def test_extract_hashtags_unique(self):
        """Test that duplicate hashtags are deduplicated."""
        text = "#work #work #work"
        tags = extract_hashtags(text)
        assert tags == ["work"]

    def test_extract_hashtags_with_underscores(self):
        """Test hashtags with underscores."""
        text = "Check out #my_project and #feature_request"
        tags = extract_hashtags(text)
        assert set(tags) == {"my_project", "feature_request"}

    def test_extract_hashtags_with_numbers(self):
        """Test hashtags with numbers."""
        text = "#project1 #task2 #v2_0"
        tags = extract_hashtags(text)
        assert set(tags) == {"project1", "task2", "v2_0"}

    def test_extract_no_hashtags(self):
        """Test text with no hashtags."""
        text = "This is just plain text"
        tags = extract_hashtags(text)
        assert tags == []


class TestExtractAll:
    def test_extract_all_combined(self):
        text = """
        Project notes #work
        - [ ] Send report
        TODO: Review PR
        """
        result = extract_all(text)
        assert "work" in result["hashtags"]
        assert "Send report" in result["action_items"]
        assert "TODO: Review PR" in result["action_items"]


class TestExtractEndpoint:
    def test_extract_endpoint_basic(self, client):
        """Test basic extraction endpoint."""
        r = client.post(
            "/notes/",
            json={"title": "Test", "content": "This is #important\n- [ ] do task"},
        )
        note_id = r.json()["data"]["id"]

        r = client.post(f"/notes/{note_id}/extract")
        assert r.status_code == 200
        data = r.json()["data"]
        assert "important" in data["hashtags"]
        assert "do task" in data["action_items"]
        assert data["created_action_items"] == 0

    def test_extract_endpoint_with_apply(self, client):
        """Test extraction with apply=true creates action items."""
        r = client.post(
            "/notes/",
            json={"title": "Test", "content": "- [ ] Task 1\n- [ ] Task 2"},
        )
        note_id = r.json()["data"]["id"]

        r = client.post(f"/notes/{note_id}/extract?apply=true")
        assert r.status_code == 200
        data = r.json()["data"]
        assert data["created_action_items"] == 2

        # Verify action items were created
        r = client.get("/action-items/")
        items = r.json()["data"]["items"]
        task_descriptions = [item["description"] for item in items]
        assert "Task 1" in task_descriptions
        assert "Task 2" in task_descriptions

    def test_extract_endpoint_not_found(self, client):
        """Test extraction on non-existent note."""
        r = client.post("/notes/99999/extract")
        assert r.status_code == 404
        assert r.json()["error"]["code"] == "NOT_FOUND"
