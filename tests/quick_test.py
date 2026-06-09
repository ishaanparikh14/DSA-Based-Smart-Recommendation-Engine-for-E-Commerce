"""
Quick test runner for specific components
Useful for testing during development
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_cart_only():
    """Run only cart tests"""
    from tests.test_cart import run_cart_tests
    print("Running Cart Tests...")
    return run_cart_tests()


def test_session_only():
    """Run only session tests"""
    from tests.test_session import run_session_tests
    print("Running Session Tests...")
    return run_session_tests()


def test_pricing_only():
    """Run only pricing tests"""
    from tests.test_pricing import run_pricing_tests
    print("Running Pricing Tests...")
    return run_pricing_tests()


def test_recommendation_only():
    """Run only recommendation tests"""
    from tests.test_recommendation import run_recommendation_tests
    print("Running Recommendation Tests...")
    return run_recommendation_tests()


def test_knapsack_only():
    """Run only knapsack tests"""
    from tests.test_knapsack import run_knapsack_tests
    print("Running Knapsack Tests...")
    return run_knapsack_tests()


def test_integration_only():
    """Run only integration tests"""
    from tests.test_integration import run_integration_tests
    print("Running Integration Tests...")
    return run_integration_tests()


if __name__ == "__main__":
    print("\nQuick Test Runner")
    print("=" * 50)
    print("1. Cart Tests")
    print("2. Session Tests")
    print("3. Pricing Tests")
    print("4. Recommendation Tests")
    print("5. Knapsack Tests")
    print("6. Integration Tests")
    print("7. All Tests")
    print("=" * 50)
    
    choice = input("\nSelect test suite (1-7): ").strip()
    
    tests = {
        '1': test_cart_only,
        '2': test_session_only,
        '3': test_pricing_only,
        '4': test_recommendation_only,
        '5': test_knapsack_only,
        '6': test_integration_only,
        '7': lambda: __import__('tests.run_all_tests', fromlist=['run_all_tests']).run_all_tests()
    }
    
    if choice in tests:
        tests[choice]()
    else:
        print("Invalid choice!")
