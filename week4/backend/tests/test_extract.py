from backend.app.services.extract import extract_action_items, extract_tags


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "Ship it!" in items


def test_extract_tags():
    text = "This is a #note with #tags and #important items #work"
    tags = extract_tags(text)
    assert "note" in tags
    assert "tags" in tags
    assert "important" in tags
    assert "work" in tags


def test_extract_tags_unique():
    text = "#work #WORK #Work #personal #work"
    tags = extract_tags(text)
    assert tags == ["work", "personal"]


def test_extract_tags_empty():
    tags = extract_tags("No tags here!")
    assert tags == []


def test_extract_tags_with_punctuation():
    text = "Check #email, #work! and #home."
    tags = extract_tags(text)
    assert "email" in tags
    assert "work" in tags
    assert "home" in tags
