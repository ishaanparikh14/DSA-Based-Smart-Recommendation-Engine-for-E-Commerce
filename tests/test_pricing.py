"""
Unit Tests for Dynamic Pricing Engine
Tests pricing rules and range queries (simulating Red-Black Tree)
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engines.pricing import DynamicPricingEngine
from src.models.pricing import PricingRule


class TestPricingRule(unittest.TestCase):
    """Test PricingRule model"""

    def test_rule_creation(self):
        """Test creating a pricing rule"""
        rule = PricingRule(0, 10, 1.15, priority=1, rule_name="Low Stock")
        
        self.assertEqual(rule.min_inv, 0)
        self.assertEqual(rule.max_inv, 10)
        self.assertEqual(rule.multiplier, 1.15)
        self.assertEqual(rule.priority, 1)
        self.assertEqual(rule.rule_name, "Low Stock")

    def test_rule_applies(self):
        """Test rule applicability check"""
        rule = PricingRule(10, 50, 1.0)
        
        self.assertFalse(rule.applies(5))   # Below range
        self.assertTrue(rule.applies(10))   # Lower bound
        self.assertTrue(rule.applies(30))   # Within range
        self.assertTrue(rule.applies(50))   # Upper bound
        self.assertFalse(rule.applies(55))  # Above range

    def test_get_discount_percent(self):
        """Test discount percentage calculation"""
        rule1 = PricingRule(0, 10, 1.15)  # 15% markup
        self.assertEqual(rule1.get_discount_percent(), 15.0)
        
        rule2 = PricingRule(50, 100, 0.90)  # 10% discount
        self.assertEqual(rule2.get_discount_percent(), -10.0)


class TestDynamicPricingEngine(unittest.TestCase):
    """Test Dynamic Pricing Engine"""

    def setUp(self):
        """Setup pricing engine before each test"""
        self.engine = DynamicPricingEngine()

    def test_engine_initialization(self):
        """Test engine is properly initialized"""
        self.assertEqual(len(self.engine.pricing_rules), 0)
        self.assertEqual(len(self.engine.base_prices), 0)
        self.assertEqual(len(self.engine.current_inventory), 0)

    def test_add_pricing_rule(self):
        """Test adding pricing rules"""
        self.engine.add_pricing_rule(0, 10, 1.15, priority=1)
        self.engine.add_pricing_rule(11, 50, 1.0, priority=2)
        
        self.assertEqual(len(self.engine.pricing_rules), 2)

    def test_rules_sorted_by_priority(self):
        """Test rules are sorted by priority (descending)"""
        self.engine.add_pricing_rule(0, 10, 1.15, priority=1)
        self.engine.add_pricing_rule(11, 50, 1.0, priority=3)
        self.engine.add_pricing_rule(51, 100, 0.90, priority=2)
        
        priorities = [rule.priority for rule in self.engine.pricing_rules]
        self.assertEqual(priorities, [3, 2, 1])  # Descending order

    def test_set_base_price(self):
        """Test setting base prices"""
        self.engine.set_base_price(101, 1000.0)
        self.engine.set_base_price(102, 500.0)
        
        self.assertEqual(self.engine.base_prices[101], 1000.0)
        self.assertEqual(self.engine.base_prices[102], 500.0)

    def test_set_invalid_price(self):
        """Test setting negative price raises error"""
        with self.assertRaises(ValueError):
            self.engine.set_base_price(101, -100.0)

    def test_update_inventory(self):
        """Test updating inventory"""
        self.engine.update_inventory(101, 45)
        self.engine.update_inventory(102, 5)
        
        self.assertEqual(self.engine.current_inventory[101], 45)
        self.assertEqual(self.engine.current_inventory[102], 5)

    def test_set_user_segment(self):
        """Test setting user segments"""
        self.engine.set_user_segment(1, "premium")
        self.engine.set_user_segment(2, "normal")
        
        self.assertEqual(self.engine.user_segments[1], "premium")
        self.assertEqual(self.engine.user_segments[2], "normal")

    def test_invalid_user_segment(self):
        """Test invalid segment raises error"""
        with self.assertRaises(ValueError):
            self.engine.set_user_segment(1, "invalid_segment")

    def test_calculate_price_base_only(self):
        """Test price calculation with no rules"""
        self.engine.set_base_price(101, 1000.0)
        self.engine.update_inventory(101, 50)
        
        price = self.engine.calculate_price(101, 1)
        self.assertEqual(price, 1000.0)

    def test_calculate_price_with_inventory_rule(self):
        """Test price calculation with inventory-based rule"""
        self.engine.set_base_price(101, 1000.0)
        self.engine.update_inventory(101, 5)  # Low stock
        self.engine.add_pricing_rule(0, 10, 1.15, priority=1)  # +15%
        
        price = self.engine.calculate_price(101, 1)
        self.assertEqual(price, 1150.0)  # 1000 * 1.15

    def test_calculate_price_with_user_segment(self):
        """Test price calculation with user segment discount"""
        self.engine.set_base_price(101, 1000.0)
        self.engine.update_inventory(101, 50)
        self.engine.set_user_segment(1, "premium")  # 5% discount
        
        price = self.engine.calculate_price(101, 1)
        self.assertEqual(price, 950.0)  # 1000 * 0.95

    def test_calculate_price_combined(self):
        """Test price with both inventory rule and segment"""
        self.engine.set_base_price(101, 1000.0)
        self.engine.update_inventory(101, 60)  # High stock
        self.engine.add_pricing_rule(51, 100, 0.90, priority=1)  # -10%
        self.engine.set_user_segment(1, "premium")  # -5%
        
        price = self.engine.calculate_price(101, 1)
        self.assertEqual(price, 855.0)  # 1000 * 0.90 * 0.95

    def test_get_applicable_rule(self):
        """Test finding applicable rule for inventory"""
        self.engine.add_pricing_rule(0, 10, 1.15, priority=1)
        self.engine.add_pricing_rule(11, 50, 1.0, priority=2)
        self.engine.add_pricing_rule(51, 100, 0.90, priority=3)
        
        rule1 = self.engine.get_applicable_rule(5)
        self.assertEqual(rule1.multiplier, 1.15)
        
        rule2 = self.engine.get_applicable_rule(25)
        self.assertEqual(rule2.multiplier, 1.0)
        
        rule3 = self.engine.get_applicable_rule(75)
        self.assertEqual(rule3.multiplier, 0.90)

    def test_get_price_breakdown(self):
        """Test detailed price breakdown"""
        self.engine.set_base_price(101, 1000.0)
        self.engine.update_inventory(101, 5)
        self.engine.add_pricing_rule(0, 10, 1.15, priority=1, rule_name="Low Stock")
        self.engine.set_user_segment(1, "premium")
        
        breakdown = self.engine.get_price_breakdown(101, 1)
        
        self.assertEqual(breakdown['base_price'], 1000.0)
        self.assertEqual(breakdown['inventory'], 5)
        self.assertEqual(breakdown['inventory_multiplier'], 1.15)
        self.assertEqual(breakdown['inventory_rule'], "Low Stock")
        self.assertEqual(breakdown['user_segment'], "premium")
        self.assertEqual(breakdown['segment_multiplier'], 0.95)
        self.assertAlmostEqual(breakdown['final_price'], 1092.5)


class TestPricingEdgeCases(unittest.TestCase):
    """Test edge cases"""

    def test_product_not_found(self):
        """Test calculating price for non-existent product"""
        engine = DynamicPricingEngine()
        price = engine.calculate_price(999, 1)
        self.assertEqual(price, 0.0)

    def test_no_applicable_rule(self):
        """Test when no rule applies"""
        engine = DynamicPricingEngine()
        engine.set_base_price(101, 1000.0)
        engine.update_inventory(101, 150)  # Above all rules
        engine.add_pricing_rule(0, 10, 1.15)
        engine.add_pricing_rule(11, 50, 1.0)
        
        price = engine.calculate_price(101, 1)
        self.assertEqual(price, 1000.0)  # Base price only

    def test_zero_inventory(self):
        """Test with zero inventory"""
        engine = DynamicPricingEngine()
        engine.set_base_price(101, 1000.0)
        engine.update_inventory(101, 0)
        engine.add_pricing_rule(0, 10, 1.20)
        
        price = engine.calculate_price(101, 1)
        self.assertEqual(price, 1200.0)  # Rule applies


def run_pricing_tests():
    """Run all pricing tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPricingRule))
    suite.addTests(loader.loadTestsFromTestCase(TestDynamicPricingEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestPricingEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    run_pricing_tests()
