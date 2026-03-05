"""Action item extraction service with pattern recognition and metadata analysis."""

import re
from dataclasses import dataclass


@dataclass
class ActionItemMatch:
    """Represents a detected action item with extracted metadata."""

    description: str
    marker: str
    original: str
    priority: str | None = None
    assignee: str | None = None
    due_hint: str | None = None


# Pattern markers for action items (case-insensitive matching)
MARKER_PATTERN = r"^(TODO|ACTION|FIXME|BUG|HACK|NOTE)\b"
# Priority pattern: marker(priority) or marker[priority]
PRIORITY_PATTERN = r"\((high|medium|low)\)|\[(high|medium|low)\]"
# Assignee pattern: @username
ASSIGNEE_PATTERN = r"@(\w+)"
# Due date pattern: "by <text>" at end of line
DUE_PATTERN = r"\bby\s+(\S+(?:\s+\S+)?)"


def extract_action_items(text: str) -> list[str]:
    """Extract action items from text as simple strings.

    Detects lines with action markers (TODO:, ACTION:, FIXME:, BUG:, HACK:, NOTE:)
    and sentences ending with exclamation marks.

    Args:
        text: Input text to scan for action items.

    Returns:
        List of action item strings.
    """
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[str] = []
    markers = ("todo:", "action:", "fixme:", "bug:", "hack:", "note:")

    for line in lines:
        normalized = line.lower()
        # Check for marker patterns (require colon)
        if any(normalized.startswith(m) for m in markers):
            results.append(line)
        elif line.endswith("!"):
            results.append(line)
    return results


def extract_action_items_structured(text: str) -> list[ActionItemMatch]:
    """Extract action items with structured metadata.

    Parses action items and extracts:
    - Marker type (TODO, ACTION, FIXME, BUG, HACK, NOTE)
    - Priority (high, medium, low) from parentheses or brackets
    - Assignee from @mentions
    - Due date hints from "by <date>" patterns

    Args:
        text: Input text to scan for action items.

    Returns:
        List of ActionItemMatch objects with extracted metadata.
    """
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[ActionItemMatch] = []

    for line in lines:
        # Check if line starts with a marker followed by colon
        marker_match = re.match(MARKER_PATTERN, line, re.IGNORECASE)
        if not marker_match:
            continue

        marker = marker_match.group(1).upper()
        remaining = line[marker_match.end() :].strip()

        # Remove leading colon if present
        if remaining.startswith(":"):
            remaining = remaining[1:].strip()

        original = line
        priority = None
        assignee = None
        due_hint = None

        # Extract priority from parentheses or brackets
        priority_match = re.match(PRIORITY_PATTERN, remaining, re.IGNORECASE)
        if priority_match:
            priority = priority_match.group(1) or priority_match.group(2)
            priority = priority.lower()
            remaining = remaining[priority_match.end() :].strip()
            # Remove trailing colon after priority
            if remaining.startswith(":"):
                remaining = remaining[1:].strip()

        # Extract assignee from @mentions
        assignee_match = re.search(ASSIGNEE_PATTERN, remaining)
        if assignee_match:
            assignee = assignee_match.group(1)
            # Keep the @mention in description for now (will be cleaned later)

        # Extract due date hint
        due_match = re.search(DUE_PATTERN, remaining, re.IGNORECASE)
        if due_match:
            due_hint = due_match.group(1)

        # Clean description: remove @assignee prefix if it's at the start
        description = remaining
        if assignee:
            # Remove the assignee prefix if at start
            description = re.sub(rf"^@{assignee}\s*", "", description)

        results.append(
            ActionItemMatch(
                description=description,
                marker=marker,
                original=original,
                priority=priority,
                assignee=assignee,
                due_hint=due_hint,
            )
        )

    return results
