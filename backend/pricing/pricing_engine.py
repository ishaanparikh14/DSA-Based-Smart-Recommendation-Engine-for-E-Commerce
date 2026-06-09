"""
Dynamic Pricing Engine
Rule-based pricing (NO ML) using BST for efficient rule matching
"""

from data_structures.bst import BST
from models import Product, User
from typing import Dict, List, Optional, Tuple
import time


class PricingRule:
    """Pricing rule definition"""
    
    def __init__(
        self,
        rule_type: str,
        condition: Dict,
        adjustment: float,
        description: str = ""
    ):
        """
        Initialize pricing rule.
        
        Args:
            rule_type: Type of rule (inventory, demand, cart_abandonment, loyalty)
            condition: Condition dictionary
            adjustment: Price adjustment (multiplier or absolute)
            description: Rule description
        """
        self.rule_type = rule_type
        self.condition = condition
        self.adjustment = adjustment
        self.description = description
    
    def applies(self, context: Dict) -> bool:
        """Check if rule applies to given context"""
        if self.rule_type == "inventory":
            inventory = context.get('inventory', 0)
            return (
                inventory >= self.condition.get('min', 0) and
                inventory <= self.condition.get('max', float('inf'))
            )
        elif self.rule_type == "demand":
            views = context.get('views', 0)
            return views >= self.condition.get('min_views', 0)
        elif self.rule_type == "cart_abandonment":
            time_in_cart = context.get('time_in_cart', 0)
            return time_in_cart >= self.condition.get('min_hours', 0) * 3600
        elif self.rule_type == "loyalty":
            purchase_count = context.get('purchase_count', 0)
            return purchase_count >= self.condition.get('min_purchases', 0)
        return False


class DynamicPricingEngine:
    """
    Rule-based dynamic pricing engine.
    
    NO MACHINE LEARNING - Only deterministic rules
    
    Rules:
    1. Inventory Rule: Low stock → price increase
    2. Demand Rule: High views → price increase
    3. Cart Abandonment: Item in cart > 24h → discount
    4. Loyalty Rule: Frequent buyers → discount
    """
    
    def __init__(self):
        """Initialize pricing engine"""
        self.rules: List[PricingRule] = []
        self.product_map: Dict[int, Product] = {}
        self.user_map: Dict[str, User] = {}
        
        # Initialize default rules
        self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> None:
        """Initialize default pricing rules"""
        # Inventory rules
        self.rules.append(PricingRule(
            "inventory",
            {'min': 0, 'max': 5},
            1.15,  # +15% for very low stock
            "Very low stock premium"
        ))
        
        self.rules.append(PricingRule(
            "inventory",
            {'min': 5, 'max': 10},
            1.10,  # +10% for low stock
            "Low stock premium"
        ))
        
        self.rules.append(PricingRule(
            "inventory",
            {'min': 50, 'max': float('inf')},
            0.95,  # -5% for overstocked
            "Overstock discount"
        ))
        
        # Demand rules
        self.rules.append(PricingRule(
            "demand",
            {'min_views': 100},
            1.05,  # +5% for high demand
            "High demand premium"
        ))
        
        # Cart abandonment rule
        self.rules.append(PricingRule(
            "cart_abandonment",
            {'min_hours': 24},
            0.90,  # -10% if in cart > 24h
            "Cart abandonment discount"
        ))
        
        # Loyalty rule
        self.rules.append(PricingRule(
            "loyalty",
            {'min_purchases': 5},
            0.95,  # -5% for loyal customers
            "Loyalty discount"
        ))
    
    def initialize(self, products: List[Product], users: List[User]) -> None:
        """
        Initialize pricing engine with products and users.
        
        Args:
            products: List of products
            users: List of users
        """
        self.product_map = {p.id: p for p in products}
        self.user_map = {u.id: u for u in users}
    
    def calculate_price(
        self,
        product_id: int,
        user_id: Optional[str] = None,
        cart_timestamp: Optional[float] = None
    ) -> Tuple[float, List[str]]:
        """
        Calculate dynamic price for a product.
        
        Args:
            product_id: Product to price
            user_id: Optional user ID for personalization
            cart_timestamp: Optional timestamp when added to cart
            
        Returns:
            Tuple of (final_price, applied_rules)
        """
        product = self.product_map.get(product_id)
        if not product:
            return (0.0, ["Product not found"])
        
        base_price = product.price
        final_price = base_price
        applied_rules = []
        
        # Build context
        context = {
            'inventory': product.inventory,
            'views': product.views,
            'time_in_cart': 0,
            'purchase_count': 0
        }
        
        # Add cart time if provided
        if cart_timestamp:
            context['time_in_cart'] = time.time() - cart_timestamp
        
        # Add user purchase count if provided
        if user_id:
            user = self.user_map.get(user_id)
            if user:
                context['purchase_count'] = len(user.purchase_history)
        
        # Apply rules
        for rule in self.rules:
            if rule.applies(context):
                final_price *= rule.adjustment
                applied_rules.append(rule.description)
        
        return (round(final_price, 2), applied_rules)
    
    def get_price_explanation(
        self,
        product_id: int,
        user_id: Optional[str] = None
    ) -> Dict:
        """
        Get detailed price explanation.
        
        Args:
            product_id: Product to explain
            user_id: Optional user ID
            
        Returns:
            Price breakdown dictionary
        """
        product = self.product_map.get(product_id)
        if not product:
            return {'error': 'Product not found'}
        
        final_price, applied_rules = self.calculate_price(product_id, user_id)
        
        discount_percent = ((final_price - product.price) / product.price * 100) if product.price > 0 else 0
        
        return {
            'product_id': product_id,
            'product_name': product.name,
            'base_price': product.price,
            'final_price': final_price,
            'discount_percent': round(discount_percent, 2),
            'applied_rules': applied_rules,
            'inventory': product.inventory,
            'views': product.views
        }
    
    def add_custom_rule(self, rule: PricingRule) -> None:
        """Add custom pricing rule"""
        self.rules.append(rule)
    
    def get_all_rules(self) -> List[Dict]:
        """Get all pricing rules"""
        return [
            {
                'type': rule.rule_type,
                'condition': rule.condition,
                'adjustment': rule.adjustment,
                'description': rule.description
            }
            for rule in self.rules
        ]
    
    def __repr__(self) -> str:
        return f"DynamicPricingEngine(products={len(self.product_map)}, rules={len(self.rules)})"
