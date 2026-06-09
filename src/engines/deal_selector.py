"""
Deal Selector using Min-Heap
Selects top-k best deals efficiently using priority queue
"""

from heapq import heappush, heapreplace
from typing import List, Tuple, Dict


class DealSelector:
    """
    Select top-k best deals using Min-Heap.
    
    Data Structure: Min-Heap
    Time Complexity:
        - Add deal: O(log k)
        - Get top deals: O(k log k)
    Space Complexity: O(k)
    """
    
    def __init__(self, k: int = 5):
        """
        Initialize deal selector.
        
        Args:
            k: Number of top deals to maintain
        """
        if k <= 0:
            raise ValueError("k must be positive")
        
        self.k = k
        self.heap: List[Tuple[float, int, float, float]] = []
        # Heap elements: (discount_amount, product_id, final_price, discount_percent)

    def add_deal(
        self,
        product_id: int,
        original_price: float,
        discount_percent: float
    ) -> bool:
        """
        Add deal to selector.
        Time Complexity: O(log k)
        
        Args:
            product_id: Product identifier
            original_price: Original price before discount
            discount_percent: Discount percentage (0-100)
            
        Returns:
            True if deal was added/updated in top-k
        """
        if original_price < 0 or discount_percent < 0 or discount_percent > 100:
            raise ValueError("Invalid price or discount values")

        final_price = original_price * (1 - discount_percent / 100)
        discount_amount = original_price * discount_percent / 100

        # Min-heap: keep k largest discounts
        if len(self.heap) < self.k:
            heappush(
                self.heap,
                (discount_amount, product_id, final_price, discount_percent)
            )
            return True
        elif discount_amount > self.heap[0][0]:
            heapreplace(
                self.heap,
                (discount_amount, product_id, final_price, discount_percent)
            )
            return True
        
        return False

    def get_top_deals(self) -> List[Tuple[int, float, float, float]]:
        """
        Get top-k deals sorted by discount amount.
        Time Complexity: O(k log k)
        
        Returns:
            List of tuples (product_id, discount_amount, final_price, discount_percent)
        """
        # Sort in descending order by discount amount
        sorted_deals = sorted(self.heap, reverse=True)
        return [
            (prod_id, discount, price, disc_pct)
            for discount, prod_id, price, disc_pct in sorted_deals
        ]

    def get_top_deals_detailed(self) -> List[Dict]:
        """
        Get top-k deals with detailed information.
        
        Returns:
            List of dictionaries with deal details
        """
        deals = []
        for prod_id, discount, price, disc_pct in self.get_top_deals():
            deals.append({
                "product_id": prod_id,
                "discount_amount": discount,
                "final_price": price,
                "discount_percent": disc_pct,
                "original_price": price / (1 - disc_pct / 100) if disc_pct < 100 else 0
            })
        return deals

    def clear(self) -> None:
        """Clear all deals from selector."""
        self.heap.clear()

    def get_deal_count(self) -> int:
        """Get current number of deals in selector."""
        return len(self.heap)

    def is_full(self) -> bool:
        """Check if selector has k deals."""
        return len(self.heap) >= self.k

    def get_min_deal(self) -> Tuple[int, float, float, float]:
        """
        Get the deal with minimum discount (worst in top-k).
        Time Complexity: O(1)
        
        Returns:
            Tuple (product_id, discount_amount, final_price, discount_percent)
            or None if empty
        """
        if not self.heap:
            return None
        
        discount, prod_id, price, disc_pct = self.heap[0]
        return (prod_id, discount, price, disc_pct)

    def __len__(self) -> int:
        """Return number of deals currently stored."""
        return len(self.heap)

    def __repr__(self) -> str:
        return f"DealSelector(k={self.k}, current_deals={len(self.heap)})"
