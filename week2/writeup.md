# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Tomson** \
SUNet ID: **N/A (not provided)** \
Citations: **https://ollama.com/blog/structured-outputs, https://ollama.com/library**

This assignment took me about **3** hours to do.


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt:
```
Analyze week2/app/services/extract.py and add a new function extract_action_items_llm() that uses Ollama chat with structured JSON output ({"items": [string]}). Keep the existing heuristic extractor unchanged, handle empty input safely, and deduplicate/normalize items before returning.
```

Generated Code Snippets:
```
week2/app/services/extract.py (lines ~19-37, ~88-128):
- Added DEFAULT_OLLAMA_MODEL.
- Added _normalize_items(raw_items).
- Added extract_action_items_llm(text, model=DEFAULT_OLLAMA_MODEL) using Ollama structured output schema.
```

### Exercise 2: Add Unit Tests
Prompt:
```
Write unit tests for extract_action_items_llm() in week2/tests/test_extract.py. Cover at least: bullet-list notes, keyword-prefixed notes, and empty input. Mock Ollama chat() so tests run offline and deterministically.
```

Generated Code Snippets:
```
week2/tests/test_extract.py (lines ~21-70):
- Added test_extract_action_items_llm_bullet_list
- Added test_extract_action_items_llm_keyword_lines
- Added test_extract_action_items_llm_empty_input
- All tests mock week2.app.services.extract.chat via monkeypatch
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt:
```
Refactor the week2 backend for clearer API contracts and lifecycle. Introduce typed request/response schemas with Pydantic, clean up routers to use those models, move DB initialization to FastAPI lifespan startup, and improve endpoint error handling for LLM failures.
```

Generated/Modified Code Snippets:
```
week2/app/schemas.py (lines ~1-35):
- Added NoteCreate, NoteResponse, ActionItemResponse, ActionItemDoneUpdate,
  ExtractActionItemsRequest, ExtractActionItemsResponse

week2/app/routers/action_items.py (lines ~8-13, ~20-38, ~41-68, ~71-90):
- Switched to typed request/response models
- Added 502 error handling wrapper around extract_action_items_llm
- Kept existing extract/list/done behavior with clearer contracts

week2/app/routers/notes.py (lines ~6, ~12-37):
- Switched to typed request/response models
- Refactored create/get endpoints to return NoteResponse

week2/app/main.py (lines ~14-21):
- Added FastAPI lifespan startup hook
- Moved init_db() into app startup lifecycle
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt:
```
Integrate the LLM extractor into a new backend endpoint and wire the frontend with an "Extract LLM" button. Also expose a notes listing endpoint and add a "List Notes" button in the frontend that fetches and renders all notes.
```

Generated Code Snippets:
```
week2/app/routers/action_items.py (lines ~41-68):
- Added POST /action-items/extract-llm endpoint

week2/app/routers/notes.py (lines ~22-29):
- Added GET /notes endpoint

week2/frontend/index.html (lines ~24-33, ~62-113):
- Added Extract LLM button and List Notes button
- Added shared extractWithEndpoint() helper
- Added frontend calls to /action-items/extract-llm and /notes
- Added notes rendering block
```


### Exercise 5: Generate a README from the Codebase
Prompt:
```
Skipped per instruction from collaborator: "no need to find readme.md".
```

Generated Code Snippets:
```
No files modified for Exercise 5.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields.
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope.
