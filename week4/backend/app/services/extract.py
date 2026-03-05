import re


def extract_action_items(text: str) -> list[str]:
    """Extract action items from text.

    Action items are lines that:
    - End with an exclamation mark (!)
    - Start with 'TODO:' (case-insensitive)
    """
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    return [line for line in lines if line.endswith("!") or line.lower().startswith("todo:")]


def extract_tags(text: str) -> list[str]:
    """Extract hashtags from text.

    Tags are words prefixed with # (e.g., #work, #important)
    Returns unique tags in order of first appearance.
    """
    pattern = r"#(\w+)"
    matches = re.findall(pattern, text)
    # Return unique tags preserving order
    seen = set()
    unique_tags = []
    for tag in matches:
        if tag.lower() not in seen:
            seen.add(tag.lower())
            unique_tags.append(tag.lower())
    return unique_tags
