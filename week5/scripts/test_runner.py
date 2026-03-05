#!/usr/bin/env python3
"""
Test Runner with Coverage and Flaky Test Detection

This script runs pytest with coverage and automatically retries failing tests
to detect flaky tests.

Usage:
    python scripts/test_runner.py [--threshold N] [--max-retries N] [test_path]

Examples:
    python scripts/test_runner.py
    python scripts/test_runner.py --threshold 80
    python scripts/test_runner.py backend/tests/test_notes.py
"""

import argparse
import re
import subprocess
import sys


def run_pytest(
    test_path: str = "backend/tests", coverage: bool = True, threshold: int = 80
) -> tuple[bool, str, list[str]]:
    """Run pytest with coverage and return results."""
    cmd = ["pytest", test_path, "-v"]

    if coverage:
        cmd.extend(
            [
                "--cov=backend/app",
                "--cov-report=term-missing",
                "--cov-report=html:data/coverage",
                f"--cov-fail-under={threshold}",
            ]
        )

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr

    # Parse failed tests from output
    failed_tests = []
    if result.returncode != 0:
        # Look for FAILED test names
        failed_pattern = r"FAILED (.*?)::(.*?)(?:\s|-)"
        failed_tests = re.findall(failed_pattern, output)
        failed_tests = [f"{path}::{name}" for path, name in failed_tests]

    return result.returncode == 0, output, failed_tests


def retry_test(test_name: str, max_retries: int = 2) -> tuple[bool, str]:
    """Retry a single test multiple times to check if it's flaky."""
    for attempt in range(1, max_retries + 1):
        print(f"  Retry attempt {attempt}/{max_retries} for {test_name}...")
        result = subprocess.run(["pytest", test_name, "-v"], capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
    return False, result.stdout


def main():
    parser = argparse.ArgumentParser(description="Test runner with coverage and flaky detection")
    parser.add_argument(
        "test_path", nargs="default", default="backend/tests", help="Test path to run"
    )
    parser.add_argument("--threshold", type=int, default=80, help="Minimum coverage threshold")
    parser.add_argument("--max-retries", type=int, default=2, help="Max retries for flaky tests")
    parser.add_argument("--no-coverage", action="store_true", help="Skip coverage reporting")
    args = parser.parse_args()

    print("=" * 50)
    print("TEST RUN WITH COVERAGE")
    print("=" * 50)
    print(f"Test path: {args.test_path}")
    print(f"Coverage threshold: {args.threshold}%")
    print(f"Max retries: {args.max_retries}")
    print()

    # Step 1: Run tests with coverage
    success, output, failed_tests = run_pytest(
        args.test_path, coverage=not args.no_coverage, threshold=args.threshold
    )
    print(output)

    flaky_tests = []
    genuine_failures = []

    # Step 2: Retry failed tests
    if failed_tests:
        print("\n" + "=" * 50)
        print("CHECKING FOR FLAKY TESTS")
        print("=" * 50)

        for test in failed_tests:
            print(f"\nRetrying: {test}")
            passed, _ = retry_test(test, args.max_retries)
            if passed:
                flaky_tests.append(test)
                print("  -> FLAKY (passed on retry)")
            else:
                genuine_failures.append(test)
                print("  -> GENUINE FAILURE")

    # Step 3: Print summary
    print("\n" + "=" * 50)
    print("TEST RUN SUMMARY")
    print("=" * 50)

    if success:
        print("Status: SUCCESS")
    elif flaky_tests and not genuine_failures:
        print("Status: SUCCESS (with flaky tests)")
    else:
        print("Status: FAILURE")

    if flaky_tests:
        print(f"\nFlaky tests detected ({len(flaky_tests)}):")
        for t in flaky_tests:
            print(f"  - {t}")

    if genuine_failures:
        print(f"\nGenuine failures ({len(genuine_failures)}):")
        for t in genuine_failures:
            print(f"  - {t}")

    print("=" * 50)

    return 0 if success or (flaky_tests and not genuine_failures) else 1


if __name__ == "__main__":
    sys.exit(main())
