"""
User Session Management
Tracks user behavior using Stack (browsing history) & Queue (recent actions)
"""

import time
from collections import defaultdict, deque
from typing import List, Tuple, Dict


class UserSession:
    """
    Track user behavior using Stack (browsing history) & Queue (recent actions).
    
    Data Structures:
        - Stack: Browsing history (LIFO - most recent on top)
        - Queue: Recent actions (FIFO with max size)
        - Hash Maps: View counts and purchase history
    """
    
    def __init__(self, user_id: int, user_segment: str = "normal"):
        """
        Initialize user session.
        
        Args:
            user_id: Unique identifier for the user
            user_segment: User category (premium/normal/budget) for pricing
        """
        self.user_id = user_id
        self.user_segment = user_segment
        self.browsing_history: List[int] = []  # Stack: most recent on top
        self.recent_actions = deque(maxlen=10)  # Queue: last 10 actions
        self.view_count = defaultdict(int)  # Product view frequency
        self.purchase_history = defaultdict(int)  # Product purchase count
        self.cart_additions = defaultdict(int)  # Cart addition count
        self.session_start = time.time()
        self.last_activity = time.time()

    def add_view(self, product_id: int) -> None:
        """
        User views a product - push to stack, enqueue action.
        Time Complexity: O(1)
        
        Args:
            product_id: Product being viewed
        """
        self.browsing_history.append(product_id)
        self.view_count[product_id] += 1
        self.recent_actions.append(("view", product_id, time.time()))
        self.last_activity = time.time()

    def add_purchase(self, product_id: int) -> None:
        """
        User purchases a product.
        Time Complexity: O(1)
        
        Args:
            product_id: Product being purchased
        """
        self.purchase_history[product_id] += 1
        self.recent_actions.append(("purchase", product_id, time.time()))
        self.last_activity = time.time()

    def add_cart_action(self, product_id: int) -> None:
        """
        User adds product to cart.
        Time Complexity: O(1)
        
        Args:
            product_id: Product being added to cart
        """
        self.cart_additions[product_id] += 1
        self.recent_actions.append(("add_to_cart", product_id, time.time()))
        self.last_activity = time.time()

    def get_recent_browsing(self, k: int = 5) -> List[int]:
        """
        Get last k viewed products from stack.
        Time Complexity: O(k)
        
        Args:
            k: Number of recent items to retrieve
            
        Returns:
            List of up to k most recent product IDs
        """
        return self.browsing_history[-k:] if self.browsing_history else []

    def get_recent_actions(self) -> List[Tuple[str, int, float]]:
        """
        Get recent action queue.
        
        Returns:
            List of tuples (action_type, product_id, timestamp)
        """
        return list(self.recent_actions)

    def get_most_viewed_products(self, k: int = 5) -> List[Tuple[int, int]]:
        """
        Get top k most viewed products.
        Time Complexity: O(n log k) where n is unique products viewed
        
        Args:
            k: Number of top products to return
            
        Returns:
            List of tuples (product_id, view_count)
        """
        sorted_views = sorted(
            self.view_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_views[:k]

    def get_session_duration(self) -> float:
        """
        Calculate session duration in seconds.
        
        Returns:
            Duration since session start
        """
        return time.time() - self.session_start

    def get_idle_time(self) -> float:
        """
        Calculate idle time since last activity.
        
        Returns:
            Seconds since last activity
        """
        return time.time() - self.last_activity

    def is_active(self, timeout: float = 1800) -> bool:
        """
        Check if session is still active.
        
        Args:
            timeout: Idle timeout in seconds (default 30 minutes)
            
        Returns:
            True if session is active, False if timed out
        """
        return self.get_idle_time() < timeout

    def get_summary(self) -> Dict:
        """
        Get comprehensive session summary.
        
        Returns:
            Dictionary with session statistics
        """
        return {
            "user_id": self.user_id,
            "segment": self.user_segment,
            "session_duration": self.get_session_duration(),
            "idle_time": self.get_idle_time(),
            "total_views": sum(self.view_count.values()),
            "unique_views": len(self.view_count),
            "total_purchases": sum(self.purchase_history.values()),
            "unique_purchases": len(self.purchase_history),
            "cart_additions": sum(self.cart_additions.values()),
            "is_active": self.is_active()
        }

    def __repr__(self) -> str:
        return (f"UserSession(user_id={self.user_id}, segment={self.user_segment}, "
                f"views={sum(self.view_count.values())}, "
                f"purchases={sum(self.purchase_history.values())})")
