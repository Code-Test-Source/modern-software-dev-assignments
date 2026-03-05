import re


def extract_action_items(text: str) -> list[str]:
    """Extract action items from text.

    Matches:
    - Lines ending with "!"
    - Lines starting with "TODO:" (case-insensitive)
    - Markdown task syntax "- [ ] task text"
    """
    items = []
    for line in text.splitlines():
        stripped = line.strip()

        # Markdown task syntax: - [ ] task text
        task_match = re.match(r"^-\s*\[\s*\]\s*(.+)$", stripped)
        if task_match:
            items.append(task_match.group(1).strip())
            continue

        # Remove leading "- " if present
        clean = stripped.lstrip("- ").strip()

        # Lines ending with "!" or starting with "TODO:"
        if clean and (clean.endswith("!") or clean.lower().startswith("todo:")):
            items.append(clean)

    return items


def extract_hashtags(text: str) -> list[str]:
    """Extract hashtags from text.

    Matches: #hashtag (alphanumeric and underscores)
    Returns: list of hashtags without the # prefix
    """
    pattern = r"#([a-zA-Z0-9_]+)"
    matches = re.findall(pattern, text)
    return list(set(matches))  # Return unique hashtags


def extract_all(text: str) -> dict:
    """Extract all structured content from text.

    Returns:
        dict with 'hashtags' and 'action_items' keys
    """
    return {
        "hashtags": extract_hashtags(text),
        "action_items": extract_action_items(text),
    }
