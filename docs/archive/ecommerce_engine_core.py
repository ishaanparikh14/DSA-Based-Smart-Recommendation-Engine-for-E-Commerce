"""
DSA-Driven E-Commerce Personalization Engine
Core Logic Implementation
Project: Personalised E-Commerce Platform (CS-B2 DSA Lab)

Components:
1. Graph-based Recommendation Engine (User-Item Interaction)
2. Dynamic Pricing Module (Heaps + Red-Black Trees)
3. User Session Management (Stack/Queue/Linked Lists)
4. Bundle Optimization (0/1 Knapsack DP)
5. Personalized PageRank Algorithm
"""

from collections import defaultdict, deque
from heapq import heappush, heappop, heapreplace
from typing import Dict, List, Tuple, Set
import time


# ============================================================================
# 1. DOUBLY LINKED LIST - For Shopping Cart
# ============================================================================

class CartNode:
    """Node in the shopping cart (doubly linked list)"""
    def __init__(self, product_id: int, quantity: int, price: float):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.prev = None
        self.next = None
        self.timestamp = time.time()


class ShoppingCart:
    """Shopping Cart using Doubly Linked List - O(1) insertions/deletions"""
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.head = None
        self.tail = None
        self.size = 0
        self.product_map = {}  # O(1) lookup: product_id -> node

    def add_item(self, product_id: int, quantity: int, price: float):
        """Add item to cart - O(1)"""
        if product_id in self.product_map:
            node = self.product_map[product_id]
            node.quantity += quantity
            return

        new_node = CartNode(product_id, quantity, price)

        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.product_map[product_id] = new_node
        self.size += 1

    def remove_item(self, product_id: int) -> bool:
        """Remove item from cart - O(1)"""
        if product_id not in self.product_map:
            return False

        node = self.product_map[product_id]

        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        del self.product_map[product_id]
        self.size -= 1
        return True

    def get_total(self) -> float:
        """Calculate cart total"""
        total = 0
        current = self.head
        while current:
            total += current.quantity * current.price
            current = current.next
        return total

    def get_items(self) -> List[Tuple[int, int, float]]:
        """Get all cart items"""
        items = []
        current = self.head
        while current:
            items.append((current.product_id, current.quantity, current.price))
            current = current.next
        return items


# ============================================================================
# 2. USER SESSION MANAGEMENT - Stack/Queue for behavior tracking
# ============================================================================

class UserSession:
    """Track user behavior using Stack (browsing history) & Queue (recent actions)"""
    def __init__(self, user_id: int, user_segment: str = "normal"):
        self.user_id = user_id
        self.user_segment = user_segment  # For dynamic pricing segmentation
        self.browsing_history = []  # Stack: most recent on top
        self.recent_actions = deque(maxlen=10)  # Queue: last 10 actions
        self.view_count = defaultdict(int)  # Product view frequency
        self.purchase_history = defaultdict(int)  # Product purchase count
        self.last_activity = time.time()

    def add_view(self, product_id: int):
        """User views a product - push to stack, enqueue action"""
        self.browsing_history.append(product_id)
        self.view_count[product_id] += 1
        self.recent_actions.append(("view", product_id, time.time()))
        self.last_activity = time.time()

    def add_purchase(self, product_id: int):
        """User purchases a product"""
        self.purchase_history[product_id] += 1
        self.recent_actions.append(("purchase", product_id, time.time()))
        self.last_activity = time.time()

    def get_recent_browsing(self, k: int = 5) -> List[int]:
        """Get last k viewed products from stack - O(k)"""
        return self.browsing_history[-k:] if self.browsing_history else []

    def get_recent_actions(self) -> List[Tuple]:
        """Get recent action queue"""
        return list(self.recent_actions)


# ============================================================================
# 3. RED-BLACK TREE SIMULATION - Dynamic Pricing Rules with Range Queries
# ============================================================================

class PricingRule:
    """A pricing rule with inventory range and price multiplier"""
    def __init__(self, min_inv: int, max_inv: int, multiplier: float, priority: int):
        self.min_inv = min_inv
        self.max_inv = max_inv
        self.multiplier = multiplier
        self.priority = priority
        self.created_at = time.time()

    def applies(self, inventory: int) -> bool:
        return self.min_inv <= inventory <= self.max_inv


class DynamicPricingEngine:
    """
    Dynamic Pricing using sorted list (simulating RBT for range queries)
    Rules: If inventory in [min, max], apply price multiplier
    """
    def __init__(self):
        self.pricing_rules = []  # Sorted by min_inv
        self.base_prices = {}  # product_id -> base_price
        self.current_inventory = {}  # product_id -> current_count
        self.user_segments = {}  # user_id -> segment (premium/normal/budget)

    def add_pricing_rule(self, min_inv: int, max_inv: int, multiplier: float, priority: int = 0):
        """Add dynamic pricing rule - O(log n) insertion in sorted list"""
        rule = PricingRule(min_inv, max_inv, multiplier, priority)
        self.pricing_rules.append(rule)
        self.pricing_rules.sort(key=lambda x: x.priority, reverse=True)

    def set_base_price(self, product_id: int, price: float):
        """Set base price for a product"""
        self.base_prices[product_id] = price

    def update_inventory(self, product_id: int, quantity: int):
        """Update product inventory"""
        self.current_inventory[product_id] = quantity

    def calculate_price(self, product_id: int, user_id: int) -> float:
        """
        Calculate dynamic price for a product
        Considers: base price, inventory levels, user segment
        """
        if product_id not in self.base_prices:
            return 0

        base_price = self.base_prices[product_id]
        inventory = self.current_inventory.get(product_id, 0)

        # Apply inventory-based multiplier - Range query on pricing rules
        multiplier = 1.0
        for rule in self.pricing_rules:
            if rule.applies(inventory):
                multiplier = rule.multiplier
                break

        # Apply user segment discount - O(1)
        user_segment = self.user_segments.get(user_id, "normal")
        segment_discount = {
            "premium": 0.95,
            "normal": 1.0,
            "budget": 1.05
        }.get(user_segment, 1.0)

        return base_price * multiplier * segment_discount


# ============================================================================
# 4. GRAPH-BASED RECOMMENDATION ENGINE - User-Item Interaction Network
# ============================================================================

class RecommendationGraph:
    """
    Weighted Directed Graph for User-Item recommendations
    Edges: user -> product (weight = interaction strength)
    Uses Personalized PageRank for relevance scoring
    """
    def __init__(self, damping_factor: float = 0.85, iterations: int = 20):
        self.graph = defaultdict(lambda: defaultdict(float))  # adjacency list
        self.users = set()
        self.products = set()
        self.damping_factor = damping_factor
        self.iterations = iterations

    def add_interaction(self, user_id: int, product_id: int, weight: float = 1.0):
        """Add user-product interaction edge - O(1)"""
        self.graph[user_id][product_id] += weight
        self.users.add(user_id)
        self.products.add(product_id)

    def get_neighbors(self, user_id: int) -> Dict[int, float]:
        """Get all products a user has interacted with"""
        return dict(self.graph[user_id])

    def personalized_pagerank(self, user_id: int, top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Personalized PageRank - O(iterations * edges)
        Returns top-k recommended products for user
        """
        if user_id not in self.users:
            return []

        # Initialize ranks
        ranks = defaultdict(float)
        for product in self.products:
            ranks[product] = 1.0 / len(self.products) if self.products else 0

        # Personalization vector (bias towards user's existing interactions)
        personalization = defaultdict(float)
        user_interactions = self.graph[user_id]
        total_interaction = sum(user_interactions.values())

        if total_interaction > 0:
            for product, weight in user_interactions.items():
                personalization[product] = weight / total_interaction

        # PageRank iterations
        for _ in range(self.iterations):
            new_ranks = defaultdict(float)

            for product in self.products:
                # Personalization component
                new_ranks[product] = (1 - self.damping_factor) * personalization[product]

                # Damping component (contributions from users who viewed this product)
                for user in self.users:
                    user_edges = self.graph[user]
                    if user_edges and product in user_edges:
                        contribution = ranks[user] / len(user_edges)
                        new_ranks[product] += self.damping_factor * contribution

            ranks = new_ranks

        # Return top-k products
        recommendations = sorted([(p, ranks[p]) for p in self.products], 
                                key=lambda x: x[1], reverse=True)
        return recommendations[:top_k]


# ============================================================================
# 5. PRIORITY QUEUE (MIN-HEAP) - Top-K Deal Selection
# ============================================================================

class DealSelector:
    """Select top-k best deals using Min-Heap"""
    def __init__(self, k: int = 5):
        self.k = k
        self.heap = []  # Min-heap of tuples (discount, product_id, final_price)

    def add_deal(self, product_id: int, original_price: float, discount_percent: float):
        """Add deal to heap - O(log k)"""
        final_price = original_price * (1 - discount_percent / 100)
        discount_amount = original_price * discount_percent / 100

        if len(self.heap) < self.k:
            heappush(self.heap, (discount_amount, product_id, final_price))
        elif discount_amount > self.heap[0][0]:
            heapreplace(self.heap, (discount_amount, product_id, final_price))

    def get_top_deals(self) -> List[Tuple[int, float, float]]:
        """Get top-k deals - O(k log k)"""
        return sorted(self.heap, reverse=True)


# ============================================================================
# 6. BUNDLE OPTIMIZATION - 0/1 Knapsack Dynamic Programming
# ============================================================================

def bundle_optimization(products: List[Tuple[int, float]], 
                       max_budget: float) -> List[int]:
    """
    0/1 Knapsack DP: Select products to maximize discount within budget
    Returns list of product_ids in optimal bundle

    Time: O(n * budget), Space: O(n * budget)
    """
    n = len(products)
    # DP table: dp[i][w] = max discount using first i products with budget w
    dp = [[0] * (int(max_budget) + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        prod_id, price = products[i - 1]
        for w in range(int(max_budget) + 1):
            # Don't include
            dp[i][w] = dp[i - 1][w]

            # Include if budget allows
            if price <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][int(w - price)] + price)

    # Backtrack to find which products were selected
    bundle = []
    w = int(max_budget)
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            bundle.append(products[i - 1][0])
            w -= int(products[i - 1][1])

    return bundle


# ============================================================================
# 7. MAIN E-COMMERCE ENGINE - Integration
# ============================================================================

class ECommerceEngine:
    """
    Unified E-Commerce Personalization Engine
    Integrates: Graph recommendations, dynamic pricing, session management
    """
    def __init__(self):
        self.users = {}  # user_id -> UserSession
        self.carts = {}  # user_id -> ShoppingCart
        self.recommendation_graph = RecommendationGraph()
        self.pricing_engine = DynamicPricingEngine()
        self.deal_selector = DealSelector(k=5)

    def create_user(self, user_id: int, segment: str = "normal"):
        """Create/register a user"""
        self.users[user_id] = UserSession(user_id, segment)
        self.carts[user_id] = ShoppingCart(user_id)
        self.pricing_engine.user_segments[user_id] = segment

    def track_view(self, user_id: int, product_id: int):
        """Track user viewing a product"""
        if user_id not in self.users:
            self.create_user(user_id)

        self.users[user_id].add_view(product_id)
        # Add edge in recommendation graph (implicit interaction)
        self.recommendation_graph.add_interaction(user_id, product_id, weight=1.0)

    def track_purchase(self, user_id: int, product_id: int):
        """Track user purchasing a product"""
        if user_id not in self.users:
            self.create_user(user_id)

        self.users[user_id].add_purchase(product_id)
        # Stronger weight for purchases in recommendation graph
        self.recommendation_graph.add_interaction(user_id, product_id, weight=3.0)

    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1):
        """Add product to user's cart"""
        price = self.pricing_engine.calculate_price(product_id, user_id)
        if user_id not in self.carts:
            self.carts[user_id] = ShoppingCart(user_id)
        self.carts[user_id].add_item(product_id, quantity, price)

    def get_recommendations(self, user_id: int, k: int = 5) -> List[Tuple[int, float]]:
        """
        Get personalized product recommendations using PageRank
        Returns: [(product_id, relevance_score), ...]
        """
        return self.recommendation_graph.personalized_pagerank(user_id, k)

    def get_price(self, product_id: int, user_id: int) -> float:
        """Get dynamic price for a product"""
        return self.pricing_engine.calculate_price(product_id, user_id)

    def get_cart_summary(self, user_id: int) -> Dict:
        """Get shopping cart summary"""
        if user_id not in self.carts:
            return {"items": [], "total": 0, "count": 0}

        cart = self.carts[user_id]
        return {
            "user_id": user_id,
            "items": cart.get_items(),
            "total": cart.get_total(),
            "item_count": cart.size
        }

    def get_user_session_info(self, user_id: int) -> Dict:
        """Get user session details"""
        if user_id not in self.users:
            return {}

        session = self.users[user_id]
        return {
            "user_id": user_id,
            "segment": session.user_segment,
            "recent_browsing": session.get_recent_browsing(5),
            "recent_actions": session.get_recent_actions(),
            "view_counts": dict(session.view_count),
            "purchase_counts": dict(session.purchase_history)
        }

    def optimize_bundle(self, user_id: int, max_budget: float) -> Dict:
        """Find optimal product bundle within budget using knapsack DP"""
        # Get top deals from deal selector
        top_deals = self.deal_selector.get_top_deals()
        products = [(prod_id, price) for _, prod_id, price in top_deals]

        if not products:
            return {"bundle": [], "total_value": 0}

        bundle_ids = bundle_optimization(products, max_budget)
        total = sum(price for pid, price in products if pid in bundle_ids)

        return {
            "user_id": user_id,
            "bundle": bundle_ids,
            "total_value": total,
            "budget_used": total,
            "budget_remaining": max_budget - total
        }


# ============================================================================
# EXAMPLE USAGE & TESTING
# ============================================================================

if __name__ == "__main__":
    # Initialize engine
    engine = ECommerceEngine()

    # Setup pricing
    engine.pricing_engine.set_base_price(101, 1000)
    engine.pricing_engine.set_base_price(102, 500)
    engine.pricing_engine.set_base_price(103, 2000)
    engine.pricing_engine.set_base_price(104, 800)
    engine.pricing_engine.set_base_price(105, 1500)

    # Update inventory
    engine.pricing_engine.update_inventory(101, 45)  # Mid-range inventory
    engine.pricing_engine.update_inventory(102, 5)   # Low inventory
    engine.pricing_engine.update_inventory(103, 100) # High inventory
    engine.pricing_engine.update_inventory(104, 25)
    engine.pricing_engine.update_inventory(105, 60)

    # Add pricing rules (inventory-based dynamic pricing)
    engine.pricing_engine.add_pricing_rule(0, 10, 1.15, priority=1)      # Low stock: +15%
    engine.pricing_engine.add_pricing_rule(11, 50, 1.0, priority=2)      # Normal stock: +0%
    engine.pricing_engine.add_pricing_rule(51, 100, 0.90, priority=3)    # High stock: -10%

    # Create users
    engine.create_user(1, "premium")
    engine.create_user(2, "normal")
    engine.create_user(3, "budget")

    # Simulate user interactions
    print("=== USER INTERACTIONS ===")
    engine.track_view(1, 101)
    engine.track_view(1, 102)
    engine.track_view(1, 103)
    engine.track_purchase(1, 101)

    engine.track_view(2, 101)
    engine.track_view(2, 104)
    engine.track_view(2, 105)
    engine.track_purchase(2, 102)

    # Get recommendations
    print("\n=== PERSONALIZED RECOMMENDATIONS ===")
    recs_user1 = engine.get_recommendations(1, k=3)
    print(f"User 1 Recommendations: {recs_user1}")

    recs_user2 = engine.get_recommendations(2, k=3)
    print(f"User 2 Recommendations: {recs_user2}")

    # Dynamic pricing
    print("\n=== DYNAMIC PRICING ===")
    price_p101_u1 = engine.get_price(101, 1)  # Premium user
    price_p101_u2 = engine.get_price(101, 2)  # Normal user
    price_p102_u3 = engine.get_price(102, 3)  # Budget user (low stock)

    print(f"Product 101 - User 1 (premium): Rs. {price_p101_u1:.2f}")
    print(f"Product 101 - User 2 (normal): Rs. {price_p101_u2:.2f}")
    print(f"Product 102 - User 3 (budget, low stock): Rs. {price_p102_u3:.2f}")

    # Shopping cart
    print("\n=== SHOPPING CART ===")
    engine.add_to_cart(1, 101, 1)
    engine.add_to_cart(1, 102, 2)
    engine.add_to_cart(1, 104, 1)

    cart_summary = engine.get_cart_summary(1)
    print(f"User 1 Cart: {cart_summary['item_count']} items, Total: Rs. {cart_summary['total']:.2f}")
    print(f"Items: {cart_summary['items']}")

    # Bundle optimization
    print("\n=== BUNDLE OPTIMIZATION (Knapsack) ===")
    # Add some deals
    engine.deal_selector.add_deal(101, 1000, 10)  # 10% off
    engine.deal_selector.add_deal(102, 500, 15)   # 15% off
    engine.deal_selector.add_deal(103, 2000, 20)  # 20% off
    engine.deal_selector.add_deal(104, 800, 12)
    engine.deal_selector.add_deal(105, 1500, 8)

    bundle = engine.optimize_bundle(1, max_budget=2000)
    print(f"Optimal Bundle (Budget: Rs. 2000): {bundle}")

    # User session info
    print("\n=== USER SESSION INFO ===")
    session = engine.get_user_session_info(1)
    print(f"User 1 Session: {session}")
