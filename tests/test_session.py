"""
Unit Tests for User Session Management
Tests Stack (browsing history) and Queue (recent actions)
"""

import unittest
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.session import UserSession


class TestUserSession(unittest.TestCase):
    """Test UserSession functionality"""

    def setUp(self):
        """Setup session before each test"""
        self.session = UserSession(user_id=1, user_segment="normal")

    def test_session_initialization(self):
        """Test session is properly initialized"""
        self.assertEqual(self.session.user_id, 1)
        self.assertEqual(self.session.user_segment, "normal")
        self.assertEqual(len(self.session.browsing_history), 0)
        self.assertEqual(len(self.session.recent_actions), 0)

    def test_add_view(self):
        """Test adding product views"""
        self.session.add_view(101)
        self.session.add_view(102)
        
        self.assertEqual(len(self.session.browsing_history), 2)
        self.assertEqual(self.session.view_count[101], 1)
        self.assertEqual(self.session.view_count[102], 1)

    def test_add_multiple_views_same_product(self):
        """Test viewing same product multiple times"""
        self.session.add_view(101)
        self.session.add_view(101)
        self.session.add_view(101)
        
        self.assertEqual(self.session.view_count[101], 3)
        self.assertEqual(len(self.session.browsing_history), 3)

    def test_add_purchase(self):
        """Test adding purchases"""
        self.session.add_purchase(101)
        self.session.add_purchase(102)
        
        self.assertEqual(self.session.purchase_history[101], 1)
        self.assertEqual(self.session.purchase_history[102], 1)

    def test_add_cart_action(self):
        """Test tracking cart additions"""
        self.session.add_cart_action(101)
        self.session.add_cart_action(102)
        
        self.assertEqual(self.session.cart_additions[101], 1)
        self.assertEqual(self.session.cart_additions[102], 1)

    def test_get_recent_browsing(self):
        """Test getting recent browsing history (Stack - LIFO)"""
        products = [101, 102, 103, 104, 105]
        for pid in products:
            self.session.add_view(pid)
        
        recent = self.session.get_recent_browsing(3)
        self.assertEqual(recent, [103, 104, 105])  # Last 3

    def test_recent_actions_queue(self):
        """Test recent actions queue (FIFO with max size)"""
        # Add 12 actions (queue max is 10)
        for i in range(12):
            self.session.add_view(100 + i)
        
        actions = self.session.get_recent_actions()
        self.assertEqual(len(actions), 10)  # Only last 10
        
        # First action should be for product 102 (100 and 101 dropped)
        self.assertEqual(actions[0][1], 102)

    def test_get_most_viewed_products(self):
        """Test getting most viewed products"""
        self.session.add_view(101)
        self.session.add_view(101)
        self.session.add_view(101)
        self.session.add_view(102)
        self.session.add_view(102)
        self.session.add_view(103)
        
        most_viewed = self.session.get_most_viewed_products(2)
        self.assertEqual(len(most_viewed), 2)
        self.assertEqual(most_viewed[0], (101, 3))  # 101 viewed 3 times
        self.assertEqual(most_viewed[1], (102, 2))  # 102 viewed 2 times

    def test_session_duration(self):
        """Test session duration calculation"""
        time.sleep(0.1)  # Wait a bit
        duration = self.session.get_session_duration()
        self.assertGreater(duration, 0)
        self.assertLess(duration, 1)  # Should be less than 1 second

    def test_idle_time(self):
        """Test idle time calculation"""
        self.session.add_view(101)
        time.sleep(0.1)
        idle = self.session.get_idle_time()
        self.assertGreater(idle, 0)

    def test_is_active(self):
        """Test session activity check"""
        self.assertTrue(self.session.is_active(timeout=1800))
        
        # Simulate old activity
        self.session.last_activity = time.time() - 2000
        self.assertFalse(self.session.is_active(timeout=1800))

    def test_get_summary(self):
        """Test getting comprehensive session summary"""
        self.session.add_view(101)
        self.session.add_view(102)
        self.session.add_purchase(101)
        self.session.add_cart_action(103)
        
        summary = self.session.get_summary()
        
        self.assertEqual(summary['user_id'], 1)
        self.assertEqual(summary['segment'], 'normal')
        self.assertEqual(summary['total_views'], 2)
        self.assertEqual(summary['unique_views'], 2)
        self.assertEqual(summary['total_purchases'], 1)
        self.assertTrue(summary['is_active'])


class TestSessionEdgeCases(unittest.TestCase):
    """Test edge cases"""

    def test_empty_session(self):
        """Test operations on new session"""
        session = UserSession(1)
        
        self.assertEqual(session.get_recent_browsing(), [])
        self.assertEqual(session.get_recent_actions(), [])
        self.assertEqual(session.get_most_viewed_products(), [])

    def test_different_segments(self):
        """Test creating sessions with different segments"""
        segments = ["premium", "normal", "budget", "vip"]
        
        for segment in segments:
            session = UserSession(1, segment)
            self.assertEqual(session.user_segment, segment)


def run_session_tests():
    """Run all session tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestUserSession))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    run_session_tests()
