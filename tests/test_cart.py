"""
Unit Tests for Shopping Cart (Doubly Linked List)
Tests O(1) operations: add, remove, update
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.cart import CartNode, ShoppingCart


class TestCartNode(unittest.TestCase):
    """Test CartNode functionality"""

    def test_node_creation(self):
        """Test creating a cart node"""
        node = CartNode(101, 2, 500.0)
        self.assertEqual(node.product_id, 101)
        self.assertEqual(node.quantity, 2)
        self.assertEqual(node.price, 500.0)
        self.assertIsNone(node.prev)
        self.assertIsNone(node.next)

    def test_node_subtotal(self):
        """Test subtotal calculation"""
        node = CartNode(101, 3, 250.0)
        self.assertEqual(node.get_subtotal(), 750.0)


class TestShoppingCart(unittest.TestCase):
    """Test ShoppingCart operations"""

    def setUp(self):
        """Setup cart before each test"""
        self.cart = ShoppingCart(user_id=1)

    def test_cart_initialization(self):
        """Test cart is properly initialized"""
        self.assertEqual(self.cart.user_id, 1)
        self.assertEqual(self.cart.size, 0)
        self.assertTrue(self.cart.is_empty())
        self.assertIsNone(self.cart.head)
        self.assertIsNone(self.cart.tail)

    def test_add_single_item(self):
        """Test adding a single item - O(1)"""
        self.cart.add_item(101, 2, 500.0)
        self.assertEqual(self.cart.size, 1)
        self.assertFalse(self.cart.is_empty())
        self.assertEqual(self.cart.get_total(), 1000.0)

    def test_add_multiple_items(self):
        """Test adding multiple items"""
        self.cart.add_item(101, 1, 500.0)
        self.cart.add_item(102, 2, 300.0)
        self.cart.add_item(103, 1, 700.0)
        
        self.assertEqual(self.cart.size, 3)
        self.assertEqual(self.cart.get_total(), 1800.0)

    def test_add_duplicate_item(self):
        """Test adding same item twice (should update quantity)"""
        self.cart.add_item(101, 2, 500.0)
        self.cart.add_item(101, 3, 500.0)
        
        self.assertEqual(self.cart.size, 1)  # Still 1 unique item
        node = self.cart.get_item(101)
        self.assertEqual(node.quantity, 5)  # 2 + 3

    def test_remove_item(self):
        """Test removing item - O(1)"""
        self.cart.add_item(101, 2, 500.0)
        self.cart.add_item(102, 1, 300.0)
        
        success = self.cart.remove_item(101)
        self.assertTrue(success)
        self.assertEqual(self.cart.size, 1)
        self.assertEqual(self.cart.get_total(), 300.0)

    def test_remove_nonexistent_item(self):
        """Test removing item that doesn't exist"""
        success = self.cart.remove_item(999)
        self.assertFalse(success)

    def test_update_quantity(self):
        """Test updating item quantity"""
        self.cart.add_item(101, 2, 500.0)
        success = self.cart.update_quantity(101, 5)
        
        self.assertTrue(success)
        node = self.cart.get_item(101)
        self.assertEqual(node.quantity, 5)
        self.assertEqual(self.cart.get_total(), 2500.0)

    def test_update_quantity_to_zero(self):
        """Test updating quantity to 0 removes item"""
        self.cart.add_item(101, 2, 500.0)
        success = self.cart.update_quantity(101, 0)
        
        self.assertTrue(success)
        self.assertEqual(self.cart.size, 0)

    def test_get_items(self):
        """Test getting all items as list"""
        self.cart.add_item(101, 2, 500.0)
        self.cart.add_item(102, 1, 300.0)
        
        items = self.cart.get_items()
        self.assertEqual(len(items), 2)
        self.assertIn((101, 2, 500.0), items)
        self.assertIn((102, 1, 300.0), items)

    def test_clear_cart(self):
        """Test clearing all items"""
        self.cart.add_item(101, 2, 500.0)
        self.cart.add_item(102, 1, 300.0)
        self.cart.clear()
        
        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.size, 0)
        self.assertEqual(self.cart.get_total(), 0)

    def test_linked_list_integrity(self):
        """Test doubly linked list maintains proper links"""
        self.cart.add_item(101, 1, 500.0)
        self.cart.add_item(102, 1, 300.0)
        self.cart.add_item(103, 1, 700.0)
        
        # Check head
        self.assertEqual(self.cart.head.product_id, 101)
        self.assertIsNone(self.cart.head.prev)
        
        # Check tail
        self.assertEqual(self.cart.tail.product_id, 103)
        self.assertIsNone(self.cart.tail.next)
        
        # Check middle node
        middle = self.cart.head.next
        self.assertEqual(middle.product_id, 102)
        self.assertEqual(middle.prev.product_id, 101)
        self.assertEqual(middle.next.product_id, 103)


class TestCartEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def test_empty_cart_operations(self):
        """Test operations on empty cart"""
        cart = ShoppingCart(1)
        self.assertEqual(cart.get_total(), 0)
        self.assertEqual(cart.get_items(), [])
        self.assertFalse(cart.remove_item(101))

    def test_single_item_removal(self):
        """Test removing only item makes cart empty"""
        cart = ShoppingCart(1)
        cart.add_item(101, 1, 500.0)
        cart.remove_item(101)
        
        self.assertTrue(cart.is_empty())
        self.assertIsNone(cart.head)
        self.assertIsNone(cart.tail)


def run_cart_tests():
    """Run all cart tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCartNode))
    suite.addTests(loader.loadTestsFromTestCase(TestShoppingCart))
    suite.addTests(loader.loadTestsFromTestCase(TestCartEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    run_cart_tests()
