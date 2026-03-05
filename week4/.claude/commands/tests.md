# Test Runner with Coverage

Run the test suite with coverage analysis and provide actionable feedback.

## Usage
```
/tests [marker_or_path]
```

## Arguments
- `$ARGUMENTS` - Optional: specific test marker (e.g., "notes") or path (e.g., "backend/tests/test_notes.py")

## Steps

1. **Run Tests**: Execute pytest with the following command:
   - If `$ARGUMENTS` is provided: `PYTHONPATH=. pytest -q backend/tests/$ARGUMENTS --maxfail=3 -v --tb=short`
   - If no arguments: `PYTHONPATH=. pytest -q backend/tests --maxfail=3 -v --tb=short`

2. **Analyze Results**:
   - If all tests pass, proceed to coverage
   - If tests fail, summarize each failure with:
     - Test name
     - File and line number
     - Error message
     - Suggested fix

3. **Run Coverage** (only if tests pass):
   ```bash
   PYTHONPATH=. pytest -q backend/tests --cov=backend/app --cov-report=term-missing
   ```

4. **Report**:
   - Total tests run, passed, failed
   - Coverage percentage
   - Files with low coverage (<80%)
   - Specific lines missing coverage

## Output Format

```
## Test Results
- Total: X tests
- Passed: X
- Failed: X (if any)

## Failures (if any)
1. test_name (file.py:line)
   Error: ...
   Suggestion: ...

## Coverage
- Overall: X%
- Files below 80%:
  - path/to/file.py: X% (missing lines: X, Y, Z)

## Next Steps
- [ ] Fix failing tests
- [ ] Add tests for uncovered lines
```

## Safety Notes
- Tests run in isolation with temp databases
- No changes to production database
- Can be run safely at any time
