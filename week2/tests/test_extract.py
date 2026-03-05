import json

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_bullet_list(monkeypatch):
    # Mock Ollama chat() to keep test deterministic and offline.
    def fake_chat(*args, **kwargs):
        return {
            "message": {
                "content": json.dumps({"items": ["Set up database", "Implement extract endpoint"]})
            }
        }

    monkeypatch.setattr("week2.app.services.extract.chat", fake_chat)

    text = "- [ ] Set up database\n- [ ] Implement extract endpoint"
    items = extract_action_items_llm(text)
    assert items == ["Set up database", "Implement extract endpoint"]


def test_extract_action_items_llm_keyword_lines(monkeypatch):
    # Ensure duplicate LLM items are normalized away.
    def fake_chat(*args, **kwargs):
        return {
            "message": {
                "content": json.dumps(
                    {"items": ["Write tests", "Refactor db layer", "Write tests"]}
                )
            }
        }

    monkeypatch.setattr("week2.app.services.extract.chat", fake_chat)

    text = "TODO: Write tests\nAction: Refactor db layer"
    items = extract_action_items_llm(text)
    assert items == ["Write tests", "Refactor db layer"]


def test_extract_action_items_llm_empty_input(monkeypatch):
    # Empty input should short-circuit before chat() is called.
    called = False

    def fake_chat(*args, **kwargs):
        nonlocal called
        called = True
        return {"message": {"content": '{"items": []}'}}

    monkeypatch.setattr("week2.app.services.extract.chat", fake_chat)

    items = extract_action_items_llm("   ")
    assert items == []
    assert called is False
