"""
Unit Tests for Bundle Optimization (Knapsack)
Tests 0/1 Knapsack and Fractional Knapsack algorithms
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.knapsack import (
    bundle_optimization,
    bundle_optimization_with_weights,
    fractional_knapsack
)


class TestBundleOptimization(unittest.TestCase):
    """Test 0/1 Knapsack bundle optimization"""

    def test_basic_knapsack(self):
        """Test basic knapsack optimization"""
        products = [
            (101, 100),
            (102, 200),
            (103, 300),
        ]
        max_budget = 400
        
        bundle = bundle_optimization(products, max_budget)
        
        self.assertIsInstance(bundle, list)
        self.assertGreater(len(bundle), 0)
        
        # Calculate total
        total = sum(price for pid, price in products if pid in bundle)
        self.assertLessEqual(total, max_budget)

    def test_exact_budget_match(self):
        """Test when products exactly match budget"""
        products = [
            (101, 100),
            (102, 150),
            (103, 250),
        ]
        max_budget = 500
        
        bundle = bundle_optimization(products, max_budget)
        total = sum(price for pid, price in products if pid in bundle)
        
        self.assertEqual(total, 500)
        self.assertEqual(len(bundle), 3)

    def test_insufficient_budget(self):
        """Test when budget is too small"""
        products = [
            (101, 500),
            (102, 600),
        ]
        max_budget = 100
        
        bundle = bundle_optimization(products, max_budget)
        self.assertEqual(bundle, [])

    def test_single_product(self):
        """Test with single product"""
        products = [(101, 250)]
        max_budget = 300
        
        bundle = bundle_optimization(products, max_budget)
        self.assertEqual(bundle, [101])

    def test_all_products_fit(self):
        """Test when all products fit in budget"""
        products = [
            (101, 50),
            (102, 75),
            (103, 100),
        ]
        max_budget = 300
        
        bundle = bundle_optimization(products, max_budget)
        self.assertEqual(len(bundle), 3)

    def test_empty_products(self):
        """Test with no products"""
        products = []
        max_budget = 500
        
        bundle = bundle_optimization(products, max_budget)
        self.assertEqual(bundle, [])

    def test_zero_budget(self):
        """Test with zero budget"""
        products = [(101, 100)]
        max_budget = 0
        
        bundle = bundle_optimization(products, max_budget)
        self.assertEqual(bundle, [])


class TestBundleOptimizationWithWeights(unittest.TestCase):
    """Test enhanced knapsack with value and cost"""

    def test_value_cost_knapsack(self):
        """Test knapsack with separate value and cost"""
        products = [
            (101, 150, 100),  # value=150, cost=100
            (102, 250, 200),  # value=250, cost=200
            (103, 300, 250),  # value=300, cost=250
        ]
        max_budget = 400
        
        result = bundle_optimization_with_weights(products, max_budget)
        
        self.assertIn('bundle', result)
        self.assertIn('total_value', result)
        self.assertIn('total_cost', result)
        self.assertIn('budget_remaining', result)
        self.assertIn('efficiency', result)
        
        self.assertLessEqual(result['total_cost'], max_budget)
        self.assertGreaterEqual(result['budget_remaining'], 0)

    def test_efficiency_calculation(self):
        """Test value/cost efficiency"""
        products = [
            (101, 100, 50),  # efficiency = 2.0
            (102, 150, 100), # efficiency = 1.5
        ]
        max_budget = 200
        
        result = bundle_optimization_with_weights(products, max_budget)
        
        # Should select both for maximum value
        self.assertEqual(len(result['bundle']), 2)
        self.assertEqual(result['total_value'], 250)
        self.assertEqual(result['total_cost'], 150)

    def test_empty_products_with_weights(self):
        """Test with no products"""
        products = []
        max_budget = 500
        
        result = bundle_optimization_with_weights(products, max_budget)
        
        self.assertEqual(result['bundle'], [])
        self.assertEqual(result['total_value'], 0)
        self.assertEqual(result['total_cost'], 0)


class TestFractionalKnapsack(unittest.TestCase):
    """Test fractional knapsack (greedy algorithm)"""

    def test_fractional_knapsack_basic(self):
        """Test basic fractional knapsack"""
        products = [
            (101, 120, 100),  # value=120, cost=100, ratio=1.2
            (102, 100, 100),  # value=100, cost=100, ratio=1.0
            (103, 60, 50),    # value=60, cost=50, ratio=1.2
        ]
        max_budget = 200
        
        result = fractional_knapsack(products, max_budget)
        
        self.assertIn('bundle', result)
        self.assertIn('total_value', result)
        self.assertIn('total_cost', result)
        
        self.assertLessEqual(result['total_cost'], max_budget)

    def test_fractional_selection(self):
        """Test that fractions are used when needed"""
        products = [
            (101, 100, 100),  # ratio=1.0
            (102, 150, 150),  # ratio=1.0
        ]
        max_budget = 200
        
        result = fractional_knapsack(products, max_budget)
        
        # Should take all of 101 and part of 102
        bundle = result['bundle']
        
        # Check that fractions are recorded
        for prod_id, fraction in bundle:
            self.assertGreater(fraction, 0)
            self.assertLessEqual(fraction, 1.0)

    def test_all_items_full(self):
        """Test when all items fit completely"""
        products = [
            (101, 50, 50),
            (102, 75, 75),
        ]
        max_budget = 200
        
        result = fractional_knapsack(products, max_budget)
        bundle = result['bundle']
        
        # Both items should be taken fully
        for prod_id, fraction in bundle:
            self.assertEqual(fraction, 1.0)

    def test_zero_cost_items(self):
        """Test handling of zero-cost items"""
        products = [
            (101, 100, 0),  # Free item
            (102, 50, 50),
        ]
        max_budget = 100
        
        result = fractional_knapsack(products, max_budget)
        
        # Should handle gracefully (skip zero-cost items)
        self.assertIsInstance(result['bundle'], list)


class TestKnapsackEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def test_negative_budget(self):
        """Test with negative budget"""
        products = [(101, 100)]
        max_budget = -100
        
        bundle = bundle_optimization(products, max_budget)
        self.assertEqual(bundle, [])

    def test_large_numbers(self):
        """Test with large product prices"""
        products = [
            (101, 10000),
            (102, 15000),
            (103, 20000),
        ]
        max_budget = 30000
        
        bundle = bundle_optimization(products, max_budget)
        self.assertIsInstance(bundle, list)

    def test_many_products(self):
        """Test with many products"""
        products = [(i, 100) for i in range(100, 150)]
        max_budget = 1000
        
        bundle = bundle_optimization(products, max_budget)
        
        # Should select 10 products
        self.assertEqual(len(bundle), 10)


def run_knapsack_tests():
    """Run all knapsack tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestBundleOptimization))
    suite.addTests(loader.loadTestsFromTestCase(TestBundleOptimizationWithWeights))
    suite.addTests(loader.loadTestsFromTestCase(TestFractionalKnapsack))
    suite.addTests(loader.loadTestsFromTestCase(TestKnapsackEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    run_knapsack_tests()
