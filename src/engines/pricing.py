"""
Dynamic Pricing Engine
Uses sorted pricing rules (simulating Red-Black Tree) for range queries
"""

from typing import Dict, List, Optional
from ..models.pricing import PricingRule


class DynamicPricingEngine:
    """
    Dynamic Pricing Engine using sorted list for range queries.
    Simulates Red-Black Tree operations for efficient range-based pricing.
    
    Features:
        - Inventory-based pricing rules
        - User segment-based pricing
        - Base price management
    
    Time Complexity:
        - Add rule: O(n) worst case (insertion in sorted list)
        - Calculate price: O(k) where k is number of rules
    """
    
    def __init__(self):
        """Initialize pricing engine."""
        self.pricing_rules: List[PricingRule] = []  # Sorted by priority
        self.base_prices: Dict[int, float] = {}  # product_id -> base_price
        self.current_inventory: Dict[int, int] = {}  # product_id -> count
        self.user_segments: Dict[int, str] = {}  # user_id -> segment
        
        # Predefined segment multipliers
        self.segment_multipliers = {
            "premium": 0.95,   # 5% discount
            "normal": 1.0,     # No change
            "budget": 1.05,    # 5% markup
            "vip": 0.90        # 10% discount
        }

    def add_pricing_rule(
        self,
        min_inv: int,
        max_inv: int,
        multiplier: float,
        priority: int = 0,
        rule_name: str = ""
    ) -> None:
        """
        Add dynamic pricing rule.
        Time Complexity: O(n) for insertion in sorted position
        
        Args:
            min_inv: Minimum inventory for rule
            max_inv: Maximum inventory for rule
            multiplier: Price multiplier
            priority: Rule priority (higher applied first)
            rule_name: Optional descriptive name
        """
        rule = PricingRule(min_inv, max_inv, multiplier, priority, rule_name)
        self.pricing_rules.append(rule)
        # Sort by priority (descending)
        self.pricing_rules.sort(key=lambda x: x.priority, reverse=True)

    def set_base_price(self, product_id: int, price: float) -> None:
        """
        Set base price for a product.
        Time Complexity: O(1)
        
        Args:
            product_id: Product identifier
            price: Base price
        """
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.base_prices[product_id] = price

    def update_inventory(self, product_id: int, quantity: int) -> None:
        """
        Update product inventory level.
        Time Complexity: O(1)
        
        Args:
            product_id: Product identifier
            quantity: Current inventory count
        """
        if quantity < 0:
            raise ValueError("Inventory cannot be negative")
        self.current_inventory[product_id] = quantity

    def set_user_segment(self, user_id: int, segment: str) -> None:
        """
        Set user segment for personalized pricing.
        Time Complexity: O(1)
        
        Args:
            user_id: User identifier
            segment: Segment type (premium/normal/budget/vip)
        """
        valid_segments = self.segment_multipliers.keys()
        if segment not in valid_segments:
            raise ValueError(
                f"Invalid segment. Must be one of: {valid_segments}"
            )
        self.user_segments[user_id] = segment

    def get_applicable_rule(self, inventory: int) -> Optional[PricingRule]:
        """
        Find the first applicable pricing rule.
        Time Complexity: O(k) where k is number of rules
        
        Args:
            inventory: Current inventory level
            
        Returns:
            First matching PricingRule or None
        """
        for rule in self.pricing_rules:
            if rule.applies(inventory):
                return rule
        return None

    def calculate_price(
        self,
        product_id: int,
        user_id: int
    ) -> float:
        """
        Calculate dynamic price for a product.
        Considers: base price, inventory levels, user segment
        Time Complexity: O(k) where k is number of pricing rules
        
        Args:
            product_id: Product to price
            user_id: User requesting price
            
        Returns:
            Final calculated price
        """
        if product_id not in self.base_prices:
            return 0.0

        base_price = self.base_prices[product_id]
        inventory = self.current_inventory.get(product_id, 0)

        # Apply inventory-based multiplier (range query on rules)
        multiplier = 1.0
        applicable_rule = self.get_applicable_rule(inventory)
        if applicable_rule:
            multiplier = applicable_rule.multiplier

        # Apply user segment discount
        user_segment = self.user_segments.get(user_id, "normal")
        segment_multiplier = self.segment_multipliers.get(user_segment, 1.0)

        return base_price * multiplier * segment_multiplier

    def get_price_breakdown(
        self,
        product_id: int,
        user_id: int
    ) -> Dict:
        """
        Get detailed price calculation breakdown.
        
        Args:
            product_id: Product to price
            user_id: User requesting price
            
        Returns:
            Dictionary with price components
        """
        if product_id not in self.base_prices:
            return {"error": "Product not found"}

        base_price = self.base_prices[product_id]
        inventory = self.current_inventory.get(product_id, 0)
        user_segment = self.user_segments.get(user_id, "normal")
        
        applicable_rule = self.get_applicable_rule(inventory)
        inventory_multiplier = (
            applicable_rule.multiplier if applicable_rule else 1.0
        )
        segment_multiplier = self.segment_multipliers.get(user_segment, 1.0)
        
        final_price = self.calculate_price(product_id, user_id)

        return {
            "product_id": product_id,
            "base_price": base_price,
            "inventory": inventory,
            "inventory_multiplier": inventory_multiplier,
            "inventory_rule": (
                applicable_rule.rule_name if applicable_rule else "None"
            ),
            "user_segment": user_segment,
            "segment_multiplier": segment_multiplier,
            "final_price": final_price,
            "total_discount_percent": (
                ((final_price - base_price) / base_price * 100)
                if base_price > 0 else 0
            )
        }

    def get_all_rules(self) -> List[Dict]:
        """
        Get all pricing rules.
        
        Returns:
            List of rule dictionaries
        """
        return [rule.to_dict() for rule in self.pricing_rules]

    def __repr__(self) -> str:
        return (f"DynamicPricingEngine(products={len(self.base_prices)}, "
                f"rules={len(self.pricing_rules)})")
