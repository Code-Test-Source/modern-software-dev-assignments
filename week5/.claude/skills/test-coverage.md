# Test Runner with Coverage and Flaky Test Re-run

A Warp Drive automation for running tests with coverage tracking and automatic flaky test handling.

## Purpose

Run the test suite with comprehensive coverage reporting and automatic detection/handling of flaky tests.

## Usage

```bash
# Run all tests with coverage
/test-coverage

# Run specific test file with coverage
/test-coverage backend/tests/test_notes.py

# Run with coverage threshold (fails if below threshold)
/test-coverage --threshold 80
```

## Workflow Steps

### Step 1: Run Tests with Coverage

Execute pytest with coverage tracking:

```bash
PYTHONPATH=. pytest backend/tests \
  --cov=backend/app \
  --cov-report=term-missing \
  --cov-report=html:data/coverage \
  --cov-fail-under=80 \
  -v
```

### Step 2: Analyze Results

- If all tests pass and coverage >= 80%: SUCCESS
- If tests fail: Identify failing tests
- If coverage < 80%: Report uncovered lines

### Step 3: Handle Flaky Tests

For any failing tests:

1. Re-run the specific failing test up to 2 times:
   ```bash
   PYTHONPATH=. pytest backend/tests/test_file.py::test_name -v
   ```

2. If test passes on retry: Mark as FLAKY, report success
3. If test fails all attempts: Report as GENUINE FAILURE

### Step 4: Generate Report

Output summary including:
- Total tests run
- Pass/fail counts
- Coverage percentage
- List of flaky tests detected
- Uncovered code paths

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--threshold` | 80 | Minimum coverage percentage |
| `--max-retries` | 2 | Max re-runs for flaky tests |
| `--cov-path` | backend/app | Path to measure coverage for |

## Example Output

```
=====================================
TEST RUN SUMMARY
=====================================
Total Tests: 15
Passed: 14
Failed: 0
Flaky: 1 (test_notes.py::test_search_notes)

Coverage: 85.2% (threshold: 80%)
Uncovered lines:
  - backend/app/routers/notes.py:45-50
  - backend/app/services/extract.py:22-30

Status: SUCCESS
=====================================
```

## Integration Notes

This automation can be used:
- Before commits to ensure code quality
- In CI/CD pipelines
- After refactoring to verify no regressions
