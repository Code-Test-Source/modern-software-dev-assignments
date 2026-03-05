from __future__ import annotations

import json
import os
import re
from typing import Any

from dotenv import load_dotenv
from ollama import chat

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)

# Keep the default model small so local development is lightweight.
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")


def _normalize_items(raw_items: list[Any]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()
    for value in raw_items:
        if not isinstance(value, str):
            continue
        item = value.strip()
        if not item:
            continue
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        normalized.append(item)
    return normalized


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> list[str]:
    lines = text.splitlines()
    extracted: list[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def extract_action_items_llm(text: str, model: str = DEFAULT_OLLAMA_MODEL) -> list[str]:
    clean_text = text.strip()
    if not clean_text:
        return []

    schema = {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {"type": "string"},
            }
        },
        "required": ["items"],
        "additionalProperties": False,
    }

    # Structured output enforces a stable JSON contract from the model.
    response = chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract actionable tasks from user notes. "
                    "Return concise imperative tasks only. "
                    "Respond strictly as JSON matching the provided schema."
                ),
            },
            {
                "role": "user",
                "content": clean_text,
            },
        ],
        format=schema,
    )

    content = response.get("message", {}).get("content", "{}")
    parsed = json.loads(content)
    items = parsed.get("items", []) if isinstance(parsed, dict) else []
    return _normalize_items(items)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
