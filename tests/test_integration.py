"""
Integration Tests for Complete E-Commerce Engine
Tests end-to-end workflows and component interactions
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engines.ecommerce_engine import ECommerceEngine


class TestECommerceEngineIntegration(unittest.TestCase):
    """Test complete e-commerce engine integration"""

    def setUp(self):
        """Setup engine before each test"""
        self.engine = ECommerceEngine(
            damping_factor=0.85,
            pagerank_iterations=20,
            top_deals_count=5
        )
        
        # Setup sample products
        self.setup_products()

    def setup_products(self):
        """Setup sample products with pricing"""
        products = [
            (101, 1000, 45),
            (102, 500, 5),
            (103, 2000, 100),
            (104, 800, 25),
            (105, 1500, 60),
        ]
        
        for prod_id, price, inventory in products:
            self.engine.pricing_engine.set_base_price(prod_id, price)
            self.engine.pricing_engine.update_inventory(prod_id, inventory)
        
        # Add pricing rules
        self.engine.pricing_engine.add_pricing_rule(0, 10, 1.15, priority=1)
        self.engine.pricing_engine.add_pricing_rule(11, 50, 1.0, priority=2)
        self.engine.pricing_engine.add_pricing_rule(51, 100, 0.90, priority=3)
        
        # Add deals
        self.engine.deal_selector.add_deal(101, 1000, 10)
        self.engine.deal_selector.add_deal(102, 500, 15)
        self.engine.deal_selector.add_deal(103, 2000, 20)

    def test_create_user(self):
        """Test user creation"""
        result = self.engine.create_user(1, "premium")
        
        self.assertEqual(result['status'], 'created')
        self.assertIn(1, self.engine.users)
        self.assertIn(1, self.engine.carts)

    def test_create_duplicate_user(self):
        """Test creating same user twice"""
        self.engine.create_user(1, "normal")
        result = self.engine.create_user(1, "premium")
        
        self.assertEqual(result['status'], 'exists')

    def test_complete_shopping_workflow(self):
        """Test complete user shopping workflow"""
        # Create user
        self.engine.create_user(1, "premium")
        
        # Browse products
        self.engine.track_view(1, 101)
        self.engine.track_view(1, 102)
        self.engine.track_view(1, 103)
        
        # Check session
        session = self.engine.get_user_session_info(1)
        self.assertEqual(session['total_views'], 3)
        
        # Add to cart
        self.engine.add_to_cart(1, 101, 2)
        self.engine.add_to_cart(1, 102, 1)
        
        # Check cart
        cart = self.engine.get_cart_summary(1)
        self.assertEqual(cart['item_count'], 2)
        self.assertGreater(cart['total'], 0)
        
        # Make purchase
        self.engine.track_purchase(1, 101)
        
        # Verify purchase tracked
        session = self.engine.get_user_session_info(1)
        self.assertEqual(session['total_purchases'], 1)

    def test_recommendation_workflow(self):
        """Test recommendation generation workflow"""
        # Create users and simulate interactions
        self.engine.create_user(1, "normal")
        self.engine.create_user(2, "normal")
        
        # User 1 interactions
        self.engine.track_view(1, 101)
        self.engine.track_view(1, 102)
        self.engine.track_purchase(1, 101)
        
        # User 2 interactions
        self.engine.track_view(2, 101)
        self.engine.track_view(2, 103)
        
        # Get recommendations
        recs = self.engine.get_recommendations(1, k=3)
        
        self.assertIsInstance(recs, list)
        self.assertGreater(len(recs), 0)
        
        # Each recommendation has product_id and score
        for prod_id, score in recs:
            self.assertIsInstance(prod_id, int)
            self.assertIsInstance(score, float)

    def test_dynamic_pricing_workflow(self):
        """Test dynamic pricing based on inventory and segment"""
        self.engine.create_user(1, "premium")
        self.engine.create_user(2, "budget")
        
        # Same product, different users
        price1 = self.engine.get_price(101, 1)  # Premium user
        price2 = self.engine.get_price(101, 2)  # Budget user
        
        # Premium should get better price
        self.assertLess(price1, price2)
        
        # Low stock product should be more expensive
        price_low_stock = self.engine.get_price(102, 1)  # Inventory = 5
        price_high_stock = self.engine.get_price(103, 1)  # Inventory = 100
        
        # Low stock should cost more
        self.assertGreater(price_low_stock, 500)  # Base price with premium

    def test_cart_operations_workflow(self):
        """Test complete cart operations"""
        self.engine.create_user(1, "normal")
        
        # Add items
        self.engine.add_to_cart(1, 101, 2)
        self.engine.add_to_cart(1, 102, 1)
        self.engine.add_to_cart(1, 103, 3)
        
        cart = self.engine.get_cart_summary(1)
        self.assertEqual(cart['item_count'], 3)
        
        # Update quantity
        self.engine.update_cart_quantity(1, 101, 5)
        
        cart = self.engine.get_cart_summary(1)
        items = cart['items']
        prod_101 = [item for item in items if item[0] == 101][0]
        self.assertEqual(prod_101[1], 5)  # Quantity updated
        
        # Remove item
        self.engine.remove_from_cart(1, 102)
        
        cart = self.engine.get_cart_summary(1)
        self.assertEqual(cart['item_count'], 2)

    def test_bundle_optimization_workflow(self):
        """Test bundle optimization with real engine state"""
        self.engine.create_user(1, "normal")
        
        # Optimize bundle
        bundle = self.engine.optimize_bundle(1, max_budget=2000)
        
        self.assertIn('bundle', bundle)
        self.assertIn('total_value', bundle)
        self.assertLessEqual(bundle['budget_used'], 2000)
        self.assertGreaterEqual(bundle['budget_remaining'], 0)

    def test_similar_users_workflow(self):
        """Test finding similar users"""
        # Create users with overlapping interests
        self.engine.create_user(1, "normal")
        self.engine.create_user(2, "normal")
        self.engine.create_user(3, "normal")
        
        # User 1 and 2 view similar products
        self.engine.track_view(1, 101)
        self.engine.track_view(1, 102)
        
        self.engine.track_view(2, 101)
        self.engine.track_view(2, 102)
        
        # User 3 views different products
        self.engine.track_view(3, 104)
        self.engine.track_view(3, 105)
        
        # Find similar users to User 1
        similar = self.engine.get_similar_users(1, k=2)
        
        self.assertIsInstance(similar, list)
        if len(similar) > 0:
            # User 2 should be most similar
            most_similar_id, similarity = similar[0]
            self.assertEqual(most_similar_id, 2)

    def test_system_stats(self):
        """Test getting comprehensive system statistics"""
        # Create some activity
        self.engine.create_user(1, "premium")
        self.engine.create_user(2, "normal")
        
        self.engine.track_view(1, 101)
        self.engine.add_to_cart(1, 101, 1)
        
        stats = self.engine.get_system_stats()
        
        self.assertEqual(stats['total_users'], 2)
        self.assertGreater(stats['active_users'], 0)
        self.assertEqual(stats['non_empty_carts'], 1)
        self.assertGreater(stats['tracked_products'], 0)
        self.assertGreater(stats['pricing_rules'], 0)

    def test_price_breakdown_integration(self):
        """Test detailed price breakdown"""
        self.engine.create_user(1, "vip")
        
        breakdown = self.engine.get_price_breakdown(102, 1)
        
        self.assertIn('base_price', breakdown)
        self.assertIn('inventory', breakdown)
        self.assertIn('inventory_rule', breakdown)
        self.assertIn('user_segment', breakdown)
        self.assertIn('final_price', breakdown)
        
        # VIP should get discount
        self.assertLess(breakdown['final_price'], breakdown['base_price'])


class TestEngineEdgeCases(unittest.TestCase):
    """Test edge cases in engine"""

    def test_operations_without_user(self):
        """Test operations create user automatically"""
        engine = ECommerceEngine()
        
        # Track view should create user
        engine.track_view(1, 101)
        self.assertIn(1, engine.users)
        
        # Track purchase should create user
        engine.track_purchase(2, 102)
        self.assertIn(2, engine.users)

    def test_empty_engine(self):
        """Test operations on empty engine"""
        engine = ECommerceEngine()
        
        recs = engine.get_recommendations(999)
        self.assertEqual(recs, [])
        
        price = engine.get_price(999, 1)
        self.assertEqual(price, 0.0)

    def test_multiple_users_parallel_carts(self):
        """Test multiple users with separate carts"""
        engine = ECommerceEngine()
        
        # Setup products
        engine.pricing_engine.set_base_price(101, 1000)
        engine.pricing_engine.update_inventory(101, 50)
        
        # Create users and add to cart
        for user_id in range(1, 4):
            engine.create_user(user_id, "normal")
            engine.add_to_cart(user_id, 101, user_id)
        
        # Each user should have different cart
        cart1 = engine.get_cart_summary(1)
        cart2 = engine.get_cart_summary(2)
        cart3 = engine.get_cart_summary(3)
        
        # Different quantities
        items1 = cart1['items']
        items2 = cart2['items']
        items3 = cart3['items']
        
        self.assertEqual(items1[0][1], 1)  # User 1: 1 item
        self.assertEqual(items2[0][1], 2)  # User 2: 2 items
        self.assertEqual(items3[0][1], 3)  # User 3: 3 items


def run_integration_tests():
    """Run all integration tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestECommerceEngineIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEngineEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    run_integration_tests()
