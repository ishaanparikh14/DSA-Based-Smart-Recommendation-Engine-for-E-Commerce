"""
Pricing Rule Model
Represents a dynamic pricing rule based on inventory levels
"""

import time
from typing import Dict


class PricingRule:
    """
    A pricing rule with inventory range and price multiplier.
    Used in Dynamic Pricing Engine for range-based queries.
    """
    
    def __init__(
        self,
        min_inv: int,
        max_inv: int,
        multiplier: float,
        priority: int = 0,
        rule_name: str = ""
    ):
        """
        Initialize a pricing rule.
        
        Args:
            min_inv: Minimum inventory level for rule to apply
            max_inv: Maximum inventory level for rule to apply
            multiplier: Price multiplier (e.g., 1.15 = +15%, 0.90 = -10%)
            priority: Rule priority (higher = applied first)
            rule_name: Optional descriptive name
        """
        self.min_inv = min_inv
        self.max_inv = max_inv
        self.multiplier = multiplier
        self.priority = priority
        self.rule_name = rule_name or f"Rule_{min_inv}_{max_inv}"
        self.created_at = time.time()

    def applies(self, inventory: int) -> bool:
        """
        Check if rule applies to given inventory level.
        Time Complexity: O(1)
        
        Args:
            inventory: Current inventory level
            
        Returns:
            True if inventory is within rule's range
        """
        return self.min_inv <= inventory <= self.max_inv

    def get_discount_percent(self) -> float:
        """
        Calculate discount/markup percentage.
        
        Returns:
            Percentage change (positive for markup, negative for discount)
        """
        return (self.multiplier - 1.0) * 100

    def to_dict(self) -> Dict:
        """
        Convert rule to dictionary representation.
        
        Returns:
            Dictionary with rule details
        """
        return {
            "rule_name": self.rule_name,
            "inventory_range": [self.min_inv, self.max_inv],
            "multiplier": self.multiplier,
            "discount_percent": self.get_discount_percent(),
            "priority": self.priority,
            "created_at": self.created_at
        }

    def __repr__(self) -> str:
        return (f"PricingRule(name='{self.rule_name}', "
                f"range=[{self.min_inv}, {self.max_inv}], "
                f"multiplier={self.multiplier}, priority={self.priority})")

    def __lt__(self, other: 'PricingRule') -> bool:
        """Support sorting by priority (higher priority first)"""
        return self.priority > other.priority
