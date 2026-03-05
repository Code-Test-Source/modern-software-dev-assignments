"""Tests for enhanced action item extraction functionality."""

from backend.app.services.extract import (
    ActionItemMatch,
    extract_action_items,
    extract_action_items_structured,
)


class TestExtractActionItemsBasic:
    """Tests for basic string-based extraction (backward compatibility)."""

    def test_extract_basic_patterns(self):
        """Test that basic TODO: and ACTION: patterns work."""
        text = """
        TODO: write tests
        ACTION: review PR
        Not actionable
        """.strip()
        items = extract_action_items(text)
        assert "TODO: write tests" in items
        assert "ACTION: review PR" in items
        assert len(items) == 2

    def test_extract_exclamation_sentences(self):
        """Test that lines ending with ! are detected as action items."""
        text = """
        Ship it!
        This is urgent!
        Not actionable.
        """.strip()
        items = extract_action_items(text)
        assert "Ship it!" in items
        assert "This is urgent!" in items
        assert len(items) == 2

    def test_extract_with_bullet_points(self):
        """Test extraction with markdown bullet points."""
        text = """
        - TODO: write tests
        - ACTION: review PR
        - Ship it!
        """.strip()
        items = extract_action_items(text)
        assert "TODO: write tests" in items
        assert "ACTION: review PR" in items
        assert "Ship it!" in items


class TestExtractActionItemsExtendedPatterns:
    """Tests for extended action item patterns."""

    def test_extract_fixme(self):
        """Test FIXME: pattern detection."""
        text = "FIXME: this code is broken"
        items = extract_action_items(text)
        assert "FIXME: this code is broken" in items

    def test_extract_bug(self):
        """Test BUG: pattern detection."""
        text = "BUG: null pointer exception"
        items = extract_action_items(text)
        assert "BUG: null pointer exception" in items

    def test_extract_hack(self):
        """Test HACK: pattern detection."""
        text = "HACK: temporary workaround"
        items = extract_action_items(text)
        assert "HACK: temporary workaround" in items

    def test_extract_note(self):
        """Test NOTE: pattern detection (informational but tracked)."""
        text = "NOTE: remember to update docs"
        items = extract_action_items(text)
        assert "NOTE: remember to update docs" in items

    def test_case_insensitive_patterns(self):
        """Test that patterns are case-insensitive."""
        text = """
        todo: lowercase
        Todo: Mixed case
        TODO: UPPERCASE
        """.strip()
        items = extract_action_items(text)
        assert len(items) == 3


class TestExtractActionItemsStructured:
    """Tests for structured extraction with metadata."""

    def test_returns_action_item_match_objects(self):
        """Test that structured extraction returns ActionItemMatch objects."""
        text = "TODO: write tests"
        items = extract_action_items_structured(text)
        assert len(items) == 1
        assert isinstance(items[0], ActionItemMatch)
        assert items[0].description == "write tests"
        assert items[0].marker == "TODO"

    def test_extracts_priority(self):
        """Test priority extraction from action items."""
        text = "TODO(high): urgent task"
        items = extract_action_items_structured(text)
        assert len(items) == 1
        assert items[0].priority == "high"
        assert items[0].description == "urgent task"

    def test_extracts_priority_medium_and_low(self):
        """Test medium and low priority extraction."""
        text = """
        TODO(medium): normal task
        TODO(low): can wait
        """.strip()
        items = extract_action_items_structured(text)
        assert items[0].priority == "medium"
        assert items[1].priority == "low"

    def test_extracts_assignee(self):
        """Test assignee extraction from @mentions."""
        text = "TODO: @john review this code"
        items = extract_action_items_structured(text)
        assert len(items) == 1
        assert items[0].assignee == "john"
        assert items[0].description == "review this code"

    def test_extracts_assignee_with_multiple_mentions(self):
        """Test that first @mention is captured as assignee."""
        text = "TODO: @alice coordinate with @bob"
        items = extract_action_items_structured(text)
        assert items[0].assignee == "alice"
        assert "@bob" in items[0].description

    def test_extracts_due_date(self):
        """Test due date extraction."""
        text = "TODO: finish report by Friday"
        items = extract_action_items_structured(text)
        assert items[0].due_hint == "Friday"

    def test_extracts_due_date_with_by_keyword(self):
        """Test 'by' keyword due date extraction."""
        text = "ACTION: submit form by 2024-01-15"
        items = extract_action_items_structured(text)
        assert items[0].due_hint == "2024-01-15"

    def test_combined_metadata_extraction(self):
        """Test extraction of multiple metadata fields."""
        text = "TODO(high): @alice finish by tomorrow"
        items = extract_action_items_structured(text)
        assert items[0].marker == "TODO"
        assert items[0].priority == "high"
        assert items[0].assignee == "alice"
        assert items[0].due_hint == "tomorrow"

    def test_original_text_preserved(self):
        """Test that original text is preserved in match."""
        text = "TODO(high): @alice urgent task by Friday"
        items = extract_action_items_structured(text)
        assert items[0].original == "TODO(high): @alice urgent task by Friday"


class TestEdgeCases:
    """Tests for edge cases and robustness."""

    def test_empty_text(self):
        """Test handling of empty text."""
        assert extract_action_items("") == []
        assert extract_action_items_structured("") == []

    def test_no_action_items(self):
        """Test text with no action items."""
        text = "This is just a regular note with no action items."
        assert extract_action_items(text) == []
        assert extract_action_items_structured(text) == []

    def test_multiple_items_same_line(self):
        """Test multiple action items in the same text block."""
        text = """
        TODO: first task
        Some regular text
        FIXME: second task
        """.strip()
        items = extract_action_items(text)
        assert len(items) == 2

    def test_whitespace_handling(self):
        """Test proper handling of various whitespace."""
        text = """
        TODO:   task with extra spaces
        ACTION:\ttask with tab
        """.strip()
        items = extract_action_items_structured(text)
        assert len(items) == 2
        assert "extra spaces" in items[0].description

    def test_marker_with_colon_required(self):
        """Test that markers require colon to be detected."""
        text = "TODO this is not an action item"
        items = extract_action_items(text)
        assert len(items) == 0
