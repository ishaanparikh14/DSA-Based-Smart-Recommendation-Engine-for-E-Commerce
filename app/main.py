"""
Main Application Entry Point
Demonstrates usage of the E-Commerce Engine
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engines.ecommerce_engine import ECommerceEngine
from config.settings import (
    RECOMMENDATION_CONFIG,
    PRICING_CONFIG,
    DEAL_CONFIG
)


def setup_engine() -> ECommerceEngine:
    """Initialize and configure the e-commerce engine."""
    engine = ECommerceEngine(
        damping_factor=RECOMMENDATION_CONFIG["damping_factor"],
        pagerank_iterations=RECOMMENDATION_CONFIG["pagerank_iterations"],
        top_deals_count=DEAL_CONFIG["top_deals_count"]
    )

    # Setup default pricing rules
    for rule in PRICING_CONFIG["default_pricing_rules"]:
        engine.pricing_engine.add_pricing_rule(
            min_inv=rule["min_inv"],
            max_inv=rule["max_inv"],
            multiplier=rule["multiplier"],
            priority=rule["priority"],
            rule_name=rule["name"]
        )

    return engine


def setup_sample_products(engine: ECommerceEngine):
    """Setup sample products with pricing and inventory."""
    products = [
        (101, 1000, 45),   # Product ID, Base Price, Inventory
        (102, 500, 5),
        (103, 2000, 100),
        (104, 800, 25),
        (105, 1500, 60),
        (106, 300, 8),
        (107, 1200, 70),
        (108, 900, 15),
    ]

    for prod_id, price, inventory in products:
        engine.pricing_engine.set_base_price(prod_id, price)
        engine.pricing_engine.update_inventory(prod_id, inventory)

    # Add some deals
    deals = [
        (101, 1000, 10),   # Product ID, Original Price, Discount %
        (102, 500, 15),
        (103, 2000, 20),
        (104, 800, 12),
        (105, 1500, 8),
    ]

    for prod_id, price, discount in deals:
        engine.deal_selector.add_deal(prod_id, price, discount)


def simulate_user_behavior(engine: ECommerceEngine):
    """Simulate user interactions."""
    # Create users
    print("=" * 60)
    print("CREATING USERS")
    print("=" * 60)
    
    users = [
        (1, "premium"),
        (2, "normal"),
        (3, "budget"),
        (4, "vip")
    ]
    
    for user_id, segment in users:
        result = engine.create_user(user_id, segment)
        print(f"User {user_id} ({segment}): {result['status']}")

    # Simulate browsing
    print("\n" + "=" * 60)
    print("SIMULATING USER INTERACTIONS")
    print("=" * 60)
    
    # User 1 interactions
    engine.track_view(1, 101)
    engine.track_view(1, 102)
    engine.track_view(1, 103)
    engine.track_view(1, 101)  # Views same product again
    engine.track_purchase(1, 101)
    print("✓ User 1: Viewed products 101, 102, 103 and purchased 101")

    # User 2 interactions
    engine.track_view(2, 101)
    engine.track_view(2, 104)
    engine.track_view(2, 105)
    engine.track_purchase(2, 104)
    print("✓ User 2: Viewed products 101, 104, 105 and purchased 104")

    # User 3 interactions
    engine.track_view(3, 102)
    engine.track_view(3, 103)
    engine.track_view(3, 106)
    print("✓ User 3: Viewed products 102, 103, 106")

    # User 4 interactions
    engine.track_view(4, 105)
    engine.track_view(4, 107)
    engine.track_purchase(4, 105)
    print("✓ User 4: Viewed products 105, 107 and purchased 105")


def demonstrate_features(engine: ECommerceEngine):
    """Demonstrate key features of the engine."""
    
    # Recommendations
    print("\n" + "=" * 60)
    print("PERSONALIZED RECOMMENDATIONS")
    print("=" * 60)
    
    for user_id in [1, 2]:
        recs = engine.get_recommendations(user_id, k=3)
        print(f"\nUser {user_id} Recommendations:")
        for prod_id, score in recs:
            print(f"  Product {prod_id}: Relevance Score = {score:.4f}")

    # Dynamic Pricing
    print("\n" + "=" * 60)
    print("DYNAMIC PRICING")
    print("=" * 60)
    
    test_prices = [
        (101, 1),  # Premium user
        (101, 2),  # Normal user
        (102, 3),  # Budget user, low stock product
    ]
    
    for prod_id, user_id in test_prices:
        breakdown = engine.get_price_breakdown(prod_id, user_id)
        user = engine.get_user(user_id)
        print(f"\nProduct {prod_id} - User {user_id} ({user.user_segment}):")
        print(f"  Base Price: Rs. {breakdown['base_price']:.2f}")
        print(f"  Inventory: {breakdown['inventory']} units")
        print(f"  Rule Applied: {breakdown['inventory_rule']}")
        print(f"  Final Price: Rs. {breakdown['final_price']:.2f}")
        print(f"  Discount: {breakdown['total_discount_percent']:.2f}%")

    # Shopping Cart
    print("\n" + "=" * 60)
    print("SHOPPING CART OPERATIONS")
    print("=" * 60)
    
    # User 1 adds items to cart
    engine.add_to_cart(1, 101, 1)
    engine.add_to_cart(1, 102, 2)
    engine.add_to_cart(1, 104, 1)
    
    cart_summary = engine.get_cart_summary(1)
    print(f"\nUser 1 Cart:")
    print(f"  Items: {cart_summary['item_count']}")
    print(f"  Total: Rs. {cart_summary['total']:.2f}")
    print(f"  Items Details:")
    for prod_id, qty, price in cart_summary['items']:
        print(f"    Product {prod_id}: {qty} x Rs. {price:.2f} = Rs. {qty * price:.2f}")

    # Bundle Optimization
    print("\n" + "=" * 60)
    print("BUNDLE OPTIMIZATION (0/1 Knapsack)")
    print("=" * 60)
    
    bundle = engine.optimize_bundle(1, max_budget=2000)
    print(f"\nOptimal Bundle for User 1 (Budget: Rs. 2000):")
    print(f"  Products in Bundle: {bundle['bundle']}")
    print(f"  Total Value: Rs. {bundle['total_value']:.2f}")
    print(f"  Budget Used: Rs. {bundle['budget_used']:.2f}")
    print(f"  Remaining: Rs. {bundle['budget_remaining']:.2f}")

    # User Session Info
    print("\n" + "=" * 60)
    print("USER SESSION ANALYTICS")
    print("=" * 60)
    
    session = engine.get_user_session_info(1)
    print(f"\nUser 1 Session Summary:")
    print(f"  Segment: {session['segment']}")
    print(f"  Total Views: {session['total_views']}")
    print(f"  Unique Products Viewed: {session['unique_views']}")
    print(f"  Total Purchases: {session['total_purchases']}")
    print(f"  Session Duration: {session['session_duration']:.2f} seconds")
    print(f"  Is Active: {session['is_active']}")

    # System Statistics
    print("\n" + "=" * 60)
    print("SYSTEM STATISTICS")
    print("=" * 60)
    
    stats = engine.get_system_stats()
    print(f"\nSystem Overview:")
    print(f"  Total Users: {stats['total_users']}")
    print(f"  Active Users: {stats['active_users']}")
    print(f"  Non-Empty Carts: {stats['non_empty_carts']}")
    print(f"  Tracked Products: {stats['tracked_products']}")
    print(f"  Pricing Rules: {stats['pricing_rules']}")
    
    graph_stats = stats['recommendation_graph']
    print(f"\nRecommendation Graph:")
    print(f"  Total Edges: {graph_stats['total_edges']}")
    print(f"  Avg Interactions/User: {graph_stats['avg_interactions_per_user']:.2f}")
    print(f"  Graph Density: {graph_stats['density']:.4f}")


def main():
    """Main application entry point."""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  DSA-DRIVEN E-COMMERCE PERSONALIZATION ENGINE".center(58) + "║")
    print("║" + "  Production-Grade Implementation".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")

    # Initialize engine
    engine = setup_engine()
    print("✓ Engine initialized")

    # Setup products
    setup_sample_products(engine)
    print("✓ Sample products configured")

    # Simulate behavior
    simulate_user_behavior(engine)

    # Demonstrate features
    demonstrate_features(engine)

    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
