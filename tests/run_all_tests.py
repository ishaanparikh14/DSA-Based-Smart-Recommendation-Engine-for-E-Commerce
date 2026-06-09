"""
Test Runner - Run all test suites
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.test_cart import run_cart_tests
from tests.test_session import run_session_tests
from tests.test_pricing import run_pricing_tests
from tests.test_recommendation import run_recommendation_tests
from tests.test_knapsack import run_knapsack_tests
from tests.test_integration import run_integration_tests


def run_all_tests():
    """Run all test suites and report results"""
    print("\n" + "=" * 70)
    print("DSA E-COMMERCE ENGINE - COMPREHENSIVE TEST SUITE")
    print("=" * 70 + "\n")
    
    test_suites = [
        ("Shopping Cart (Doubly Linked List)", run_cart_tests),
        ("User Session (Stack/Queue)", run_session_tests),
        ("Dynamic Pricing Engine", run_pricing_tests),
        ("Recommendation Graph (PageRank)", run_recommendation_tests),
        ("Bundle Optimization (Knapsack)", run_knapsack_tests),
        ("Integration Tests", run_integration_tests),
    ]
    
    results = []
    
    for name, test_func in test_suites:
        print("\n" + "=" * 70)
        print(f"RUNNING: {name}")
        print("=" * 70)
        
        result = test_func()
        results.append((name, result))
        
        if result.wasSuccessful():
            print(f"\n✓ {name}: ALL TESTS PASSED")
        else:
            print(f"\n✗ {name}: SOME TESTS FAILED")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for name, result in results:
        tests_run = result.testsRun
        failures = len(result.failures)
        errors = len(result.errors)
        
        total_tests += tests_run
        total_failures += failures
        total_errors += errors
        
        status = "✓ PASS" if result.wasSuccessful() else "✗ FAIL"
        print(f"{status} | {name}: {tests_run} tests, {failures} failures, {errors} errors")
    
    print("\n" + "-" * 70)
    print(f"TOTAL: {total_tests} tests, {total_failures} failures, {total_errors} errors")
    
    if total_failures == 0 and total_errors == 0:
        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉")
    else:
        print(f"\n⚠️  {total_failures + total_errors} TEST(S) FAILED")
    
    print("=" * 70 + "\n")
    
    return total_failures == 0 and total_errors == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
