"""
Main E-Commerce Engine
Integrates all components into a unified system
"""

from typing import Dict, List, Tuple, Optional
from ..models.cart import ShoppingCart
from ..models.session import UserSession
from .recommendation import RecommendationGraph
from .pricing import DynamicPricingEngine
from .deal_selector import DealSelector
from ..utils.knapsack import bundle_optimization


class ECommerceEngine:
    """
    Unified E-Commerce Personalization Engine.
    
    Integrates:
        - Graph-based recommendations (Personalized PageRank)
        - Dynamic pricing (Inventory + Segment-based)
        - Session management (Stack/Queue)
        - Shopping cart (Doubly Linked List)
        - Deal selection (Min-Heap)
        - Bundle optimization (0/1 Knapsack)
    """
    
    def __init__(
        self,
        damping_factor: float = 0.85,
        pagerank_iterations: int = 20,
        top_deals_count: int = 5
    ):
        """
        Initialize e-commerce engine.
        
        Args:
            damping_factor: PageRank damping factor (0-1)
            pagerank_iterations: Number of PageRank iterations
            top_deals_count: Number of top deals to track
        """
        self.users: Dict[int, UserSession] = {}
        self.carts: Dict[int, ShoppingCart] = {}
        self.recommendation_graph = RecommendationGraph(
            damping_factor=damping_factor,
            iterations=pagerank_iterations
        )
        self.pricing_engine = DynamicPricingEngine()
        self.deal_selector = DealSelector(k=top_deals_count)

    # ========================================================================
    # User Management
    # ========================================================================

    def create_user(
        self,
        user_id: int,
        segment: str = "normal"
    ) -> Dict:
        """
        Create/register a user.
        
        Args:
            user_id: Unique user identifier
            segment: User segment (premium/normal/budget/vip)
            
        Returns:
            User creation status
        """
        if user_id in self.users:
            return {
                "status": "exists",
                "message": "User already exists",
                "user_id": user_id
            }

        self.users[user_id] = UserSession(user_id, segment)
        self.carts[user_id] = ShoppingCart(user_id)
        self.pricing_engine.set_user_segment(user_id, segment)

        return {
            "status": "created",
            "message": "User created successfully",
            "user_id": user_id,
            "segment": segment
        }

    def get_user(self, user_id: int) -> Optional[UserSession]:
        """Get user session object."""
        return self.users.get(user_id)

    # ========================================================================
    # Tracking & Analytics
    # ========================================================================

    def track_view(self, user_id: int, product_id: int) -> None:
        """
        Track user viewing a product.
        Updates: session history, recommendation graph
        
        Args:
            user_id: User identifier
            product_id: Product being viewed
        """
        if user_id not in self.users:
            self.create_user(user_id)

        self.users[user_id].add_view(product_id)
        # Add edge in recommendation graph (view = weight 1.0)
        self.recommendation_graph.add_interaction(
            user_id, product_id, weight=1.0
        )

    def track_purchase(self, user_id: int, product_id: int) -> None:
        """
        Track user purchasing a product.
        Updates: session history, recommendation graph (higher weight)
        
        Args:
            user_id: User identifier
            product_id: Product being purchased
        """
        if user_id not in self.users:
            self.create_user(user_id)

        self.users[user_id].add_purchase(product_id)
        # Purchases have stronger weight (3.0) in recommendations
        self.recommendation_graph.add_interaction(
            user_id, product_id, weight=3.0
        )

    def track_cart_addition(self, user_id: int, product_id: int) -> None:
        """
        Track user adding product to cart.
        
        Args:
            user_id: User identifier
            product_id: Product being added
        """
        if user_id not in self.users:
            self.create_user(user_id)

        self.users[user_id].add_cart_action(product_id)

    # ========================================================================
    # Shopping Cart Operations
    # ========================================================================

    def add_to_cart(
        self,
        user_id: int,
        product_id: int,
        quantity: int = 1
    ) -> Dict:
        """
        Add product to user's cart.
        
        Args:
            user_id: User identifier
            product_id: Product to add
            quantity: Number of units
            
        Returns:
            Cart operation result
        """
        if user_id not in self.carts:
            self.carts[user_id] = ShoppingCart(user_id)

        price = self.pricing_engine.calculate_price(product_id, user_id)
        
        if price <= 0:
            return {
                "status": "error",
                "message": "Product not found or invalid price"
            }

        self.carts[user_id].add_item(product_id, quantity, price)
        self.track_cart_addition(user_id, product_id)

        return {
            "status": "success",
            "message": "Item added to cart",
            "product_id": product_id,
            "quantity": quantity,
            "price": price
        }

    def remove_from_cart(
        self,
        user_id: int,
        product_id: int
    ) -> Dict:
        """
        Remove product from user's cart.
        
        Args:
            user_id: User identifier
            product_id: Product to remove
            
        Returns:
            Cart operation result
        """
        if user_id not in self.carts:
            return {"status": "error", "message": "Cart not found"}

        success = self.carts[user_id].remove_item(product_id)
        
        return {
            "status": "success" if success else "error",
            "message": (
                "Item removed from cart" if success
                else "Item not found in cart"
            )
        }

    def update_cart_quantity(
        self,
        user_id: int,
        product_id: int,
        quantity: int
    ) -> Dict:
        """
        Update quantity of item in cart.
        
        Args:
            user_id: User identifier
            product_id: Product to update
            quantity: New quantity
            
        Returns:
            Cart operation result
        """
        if user_id not in self.carts:
            return {"status": "error", "message": "Cart not found"}

        success = self.carts[user_id].update_quantity(product_id, quantity)
        
        return {
            "status": "success" if success else "error",
            "message": (
                "Quantity updated" if success
                else "Item not found in cart"
            )
        }

    def get_cart_summary(self, user_id: int) -> Dict:
        """
        Get shopping cart summary.
        
        Args:
            user_id: User identifier
            
        Returns:
            Cart details including items and total
        """
        if user_id not in self.carts:
            return {"items": [], "total": 0, "item_count": 0}

        cart = self.carts[user_id]
        return {
            "user_id": user_id,
            "items": cart.get_items(),
            "total": cart.get_total(),
            "item_count": cart.size,
            "is_empty": cart.is_empty()
        }

    # ========================================================================
    # Recommendations
    # ========================================================================

    def get_recommendations(
        self,
        user_id: int,
        k: int = 5
    ) -> List[Tuple[int, float]]:
        """
        Get personalized product recommendations using PageRank.
        
        Args:
            user_id: User to generate recommendations for
            k: Number of recommendations
            
        Returns:
            List of tuples (product_id, relevance_score)
        """
        return self.recommendation_graph.personalized_pagerank(user_id, k)

    def get_similar_users(
        self,
        user_id: int,
        k: int = 5
    ) -> List[Tuple[int, float]]:
        """
        Find similar users based on interaction patterns.
        
        Args:
            user_id: User identifier
            k: Number of similar users to return
            
        Returns:
            List of tuples (similar_user_id, similarity_score)
        """
        return self.recommendation_graph.get_similar_users(user_id, k)

    # ========================================================================
    # Pricing
    # ========================================================================

    def get_price(self, product_id: int, user_id: int) -> float:
        """
        Get dynamic price for a product.
        
        Args:
            product_id: Product identifier
            user_id: User identifier
            
        Returns:
            Calculated price
        """
        return self.pricing_engine.calculate_price(product_id, user_id)

    def get_price_breakdown(
        self,
        product_id: int,
        user_id: int
    ) -> Dict:
        """
        Get detailed price calculation breakdown.
        
        Args:
            product_id: Product identifier
            user_id: User identifier
            
        Returns:
            Price components and rules applied
        """
        return self.pricing_engine.get_price_breakdown(product_id, user_id)

    # ========================================================================
    # Session & User Info
    # ========================================================================

    def get_user_session_info(self, user_id: int) -> Dict:
        """
        Get comprehensive user session details.
        
        Args:
            user_id: User identifier
            
        Returns:
            Session statistics and history
        """
        if user_id not in self.users:
            return {"error": "User not found"}

        session = self.users[user_id]
        return session.get_summary()

    # ========================================================================
    # Bundle Optimization
    # ========================================================================

    def optimize_bundle(
        self,
        user_id: int,
        max_budget: float
    ) -> Dict:
        """
        Find optimal product bundle within budget using knapsack DP.
        
        Args:
            user_id: User identifier
            max_budget: Maximum budget constraint
            
        Returns:
            Optimal bundle details
        """
        # Get top deals from deal selector
        top_deals = self.deal_selector.get_top_deals()
        products = [
            (prod_id, price)
            for prod_id, _, price, _ in top_deals
        ]

        if not products:
            return {
                "bundle": [],
                "total_value": 0,
                "message": "No deals available"
            }

        bundle_ids = bundle_optimization(products, max_budget)
        total = sum(
            price for pid, price in products if pid in bundle_ids
        )

        return {
            "user_id": user_id,
            "bundle": bundle_ids,
            "total_value": total,
            "budget_used": total,
            "budget_remaining": max_budget - total,
            "item_count": len(bundle_ids)
        }

    # ========================================================================
    # System Statistics
    # ========================================================================

    def get_system_stats(self) -> Dict:
        """
        Get comprehensive system statistics.
        
        Returns:
            Dictionary with all system metrics
        """
        return {
            "total_users": len(self.users),
            "active_users": sum(
                1 for u in self.users.values() if u.is_active()
            ),
            "total_carts": len(self.carts),
            "non_empty_carts": sum(
                1 for c in self.carts.values() if not c.is_empty()
            ),
            "recommendation_graph": (
                self.recommendation_graph.get_graph_stats()
            ),
            "pricing_rules": len(self.pricing_engine.pricing_rules),
            "tracked_products": len(self.pricing_engine.base_prices),
            "top_deals_count": len(self.deal_selector)
        }

    def __repr__(self) -> str:
        return (f"ECommerceEngine(users={len(self.users)}, "
                f"carts={len(self.carts)})")
