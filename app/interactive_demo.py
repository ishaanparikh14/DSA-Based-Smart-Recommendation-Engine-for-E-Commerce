"""
Interactive Shopping Demo with Recommendation Engine
A user-friendly demonstration of the DSA E-Commerce Engine
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engines.ecommerce_engine import ECommerceEngine


# Product catalog with realistic items
PRODUCT_CATALOG = {
    101: {"name": "Wireless Headphones", "price": 2999, "category": "Electronics", "inventory": 45},
    102: {"name": "Smart Watch", "price": 4999, "category": "Electronics", "inventory": 8},
    103: {"name": "Laptop Backpack", "price": 1499, "category": "Accessories", "inventory": 100},
    104: {"name": "USB-C Cable", "price": 299, "category": "Accessories", "inventory": 25},
    105: {"name": "Portable Charger", "price": 1999, "category": "Electronics", "inventory": 60},
    106: {"name": "Phone Case", "price": 499, "category": "Accessories", "inventory": 12},
    107: {"name": "Bluetooth Speaker", "price": 3499, "category": "Electronics", "inventory": 70},
    108: {"name": "Screen Protector", "price": 199, "category": "Accessories", "inventory": 15},
    109: {"name": "Wireless Mouse", "price": 899, "category": "Electronics", "inventory": 55},
    110: {"name": "Keyboard", "price": 1799, "category": "Electronics", "inventory": 40},
}


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_divider():
    """Print a divider line"""
    print("-" * 70)


def setup_engine():
    """Initialize the e-commerce engine with products and spoofed data"""
    print("\n🔧 Initializing E-Commerce Engine...")
    engine = ECommerceEngine(damping_factor=0.85, pagerank_iterations=15)
    
    # Setup products with pricing
    for prod_id, details in PRODUCT_CATALOG.items():
        engine.pricing_engine.set_base_price(prod_id, details["price"])
        engine.pricing_engine.update_inventory(prod_id, details["inventory"])
    
    # Add dynamic pricing rules
    engine.pricing_engine.add_pricing_rule(0, 10, 1.15, priority=1, rule_name="Low Stock Premium")
    engine.pricing_engine.add_pricing_rule(11, 50, 1.0, priority=2, rule_name="Normal Stock")
    engine.pricing_engine.add_pricing_rule(51, 100, 0.92, priority=3, rule_name="High Stock Discount")
    
    print("✓ Products loaded")
    print("✓ Dynamic pricing configured")
    
    # Spoof user behavior data (simulate other users' interactions)
    print("\n📊 Loading customer behavior data...")
    
    # Create dummy users with interaction patterns
    dummy_users = [
        (201, "normal", [(101, 2), (105, 1), (107, 1)]),  # Electronics fan
        (202, "premium", [(102, 1), (101, 1), (109, 1)]),  # Tech enthusiast
        (203, "normal", [(103, 1), (104, 2), (106, 1)]),  # Accessories buyer
        (204, "budget", [(104, 1), (108, 1), (106, 1)]),  # Budget shopper
        (205, "normal", [(107, 1), (105, 1), (110, 1)]),  # Electronics buyer
    ]
    
    for user_id, segment, interactions in dummy_users:
        engine.create_user(user_id, segment)
        for prod_id, weight in interactions:
            # Simulate views
            engine.track_view(user_id, prod_id)
            # Some purchases (higher weight)
            if weight > 1:
                engine.track_purchase(user_id, prod_id)
    
    print(f"✓ Loaded data from {len(dummy_users)} customers")
    print("✓ Recommendation graph initialized")
    
    return engine


def display_product_catalog():
    """Display available products"""
    print_header("📦 AVAILABLE PRODUCTS")
    print(f"\n{'ID':<6} {'Product Name':<25} {'Price':<12} {'Stock':<10} {'Category':<15}")
    print_divider()
    
    for prod_id, details in sorted(PRODUCT_CATALOG.items()):
        stock_status = "🟢 In Stock" if details["inventory"] > 20 else "🟡 Low Stock" if details["inventory"] > 10 else "🔴 Limited"
        print(f"{prod_id:<6} {details['name']:<25} Rs. {details['price']:<8} {stock_status:<10} {details['category']:<15}")


def show_cart(engine, user_id):
    """Display current cart contents"""
    cart = engine.get_cart_summary(user_id)
    
    print_header("🛒 YOUR SHOPPING CART")
    
    if cart['is_empty']:
        print("\n  Your cart is empty. Add some products!")
        return
    
    print(f"\n{'Product':<30} {'Qty':<8} {'Price':<12} {'Subtotal':<12}")
    print_divider()
    
    for prod_id, qty, price in cart['items']:
        product_name = PRODUCT_CATALOG[prod_id]['name']
        subtotal = qty * price
        print(f"{product_name:<30} {qty:<8} Rs. {price:<9.2f} Rs. {subtotal:<9.2f}")
    
    print_divider()
    print(f"{'TOTAL':<30} {cart['item_count']} items{'':<5} {'':12} Rs. {cart['total']:<9.2f}")
    print()


def add_to_cart_interactive(engine, user_id):
    """Interactive product addition to cart"""
    while True:
        print("\n🛍️  Add Products to Cart")
        print("   Enter product ID (or 'done' to finish, 'show' to see cart)")
        
        choice = input("\n   Your choice: ").strip().lower()
        
        if choice == 'done':
            break
        elif choice == 'show':
            show_cart(engine, user_id)
            continue
        
        try:
            prod_id = int(choice)
            
            if prod_id not in PRODUCT_CATALOG:
                print("   ❌ Invalid product ID!")
                continue
            
            # Show product details
            product = PRODUCT_CATALOG[prod_id]
            price = engine.get_price(prod_id, user_id)
            
            print(f"\n   Selected: {product['name']}")
            print(f"   Price: Rs. {price:.2f}")
            
            qty = input("   Quantity (default 1): ").strip()
            qty = int(qty) if qty else 1
            
            # Add to cart
            engine.track_view(user_id, prod_id)
            result = engine.add_to_cart(user_id, prod_id, qty)
            
            if result['status'] == 'success':
                print(f"   ✓ Added {qty}x {product['name']} to cart!")
            else:
                print(f"   ❌ {result['message']}")
                
        except ValueError:
            print("   ❌ Please enter a valid product ID or 'done'")


def explain_recommendation_process(engine, user_id):
    """Explain how recommendations work with the user's data"""
    print_header("🧠 HOW RECOMMENDATIONS WORK")
    
    print("\n📚 Step 1: ANALYZING YOUR BEHAVIOR")
    print("   We track what you viewed and added to cart...")
    
    session = engine.get_user_session_info(user_id)
    
    if session['total_views'] > 0:
        print(f"\n   ✓ You viewed {session['total_views']} products")
        print(f"   ✓ You added {session['cart_additions']} items to cart")
        
        recent = session.get('recent_browsing', [])
        if recent:
            viewed_names = [PRODUCT_CATALOG[pid]['name'] for pid in recent[:3]]
            print(f"   ✓ Recent interest: {', '.join(viewed_names)}")
    
    time.sleep(1)
    
    print("\n📊 Step 2: BUILDING INTERACTION GRAPH")
    print("   We create connections between you and products...")
    
    graph_stats = engine.recommendation_graph.get_graph_stats()
    print(f"\n   ✓ Total users in network: {graph_stats['total_users']}")
    print(f"   ✓ Total products tracked: {graph_stats['total_products']}")
    print(f"   ✓ Total interactions: {graph_stats['total_edges']}")
    
    time.sleep(1)
    
    print("\n🔗 Step 3: FINDING SIMILAR CUSTOMERS")
    print("   We find other customers with similar tastes...")
    
    similar_users = engine.get_similar_users(user_id, k=2)
    if similar_users:
        for other_user_id, similarity in similar_users[:2]:
            print(f"   ✓ Found customer #{other_user_id} with {similarity*100:.1f}% similarity")
    else:
        print("   • Building your profile... (more data needed)")
    
    time.sleep(1)
    
    print("\n⚡ Step 4: PAGERANK ALGORITHM")
    print("   We use Google's PageRank algorithm to rank products...")
    print("   • Products you viewed get initial score")
    print("   • Products viewed by similar users get bonus scores")
    print("   • Scores propagate through the network over 15 iterations")
    
    time.sleep(1)
    
    print("\n✨ Step 5: GENERATING RECOMMENDATIONS")
    print("   Calculating personalized recommendations for you...")


def show_recommendations(engine, user_id):
    """Generate and display recommendations"""
    print_header("💡 PERSONALIZED RECOMMENDATIONS FOR YOU")
    
    recommendations = engine.get_recommendations(user_id, k=5)
    
    if not recommendations:
        print("\n   We need more data about your preferences.")
        print("   Try viewing or adding more products!")
        return
    
    print("\n   Based on your browsing and similar customers, we recommend:\n")
    print(f"   {'Rank':<6} {'Product Name':<30} {'Score':<12} {'Price':<12}")
    print("   " + "-" * 68)
    
    for idx, (prod_id, score) in enumerate(recommendations, 1):
        if prod_id in PRODUCT_CATALOG:
            product = PRODUCT_CATALOG[prod_id]
            price = engine.get_price(prod_id, user_id)
            
            # Visual score bar
            bar_length = int(score * 50)
            bar = "█" * bar_length
            
            print(f"   {idx:<6} {product['name']:<30} {score:<12.4f} Rs. {price:<9.2f}")
            print(f"         {bar}")


def explain_pricing(engine, user_id, prod_id):
    """Explain dynamic pricing for a product"""
    print_header("💰 DYNAMIC PRICING EXPLANATION")
    
    product = PRODUCT_CATALOG[prod_id]
    breakdown = engine.get_price_breakdown(prod_id, user_id)
    
    print(f"\n   Product: {product['name']}")
    print(f"\n   📊 Pricing Breakdown:")
    print(f"      Base Price:        Rs. {breakdown['base_price']:.2f}")
    print(f"      Current Stock:     {breakdown['inventory']} units")
    print(f"      Stock Rule:        {breakdown['inventory_rule']}")
    print(f"      Stock Multiplier:  {breakdown['inventory_multiplier']:.2f}x")
    print(f"      Your Segment:      {breakdown['user_segment'].upper()}")
    print(f"      Segment Discount:  {breakdown['segment_multiplier']:.2f}x")
    print(f"\n   💵 FINAL PRICE:      Rs. {breakdown['final_price']:.2f}")
    
    if breakdown['total_discount_percent'] < 0:
        print(f"   🎉 You save {abs(breakdown['total_discount_percent']):.1f}%!")
    elif breakdown['total_discount_percent'] > 0:
        print(f"   ⚠️  {breakdown['total_discount_percent']:.1f}% premium (low stock)")


def main():
    """Main interactive demo"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🛒 INTERACTIVE SHOPPING DEMO WITH AI RECOMMENDATIONS".center(68) + "║")
    print("║" + "  Powered by Data Structures & Algorithms".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Initialize engine
    engine = setup_engine()
    
    # Create user
    print("\n👤 Creating your profile...")
    user_id = 1
    engine.create_user(user_id, "normal")
    print("✓ Welcome! You're logged in as Customer #001")
    
    input("\n   Press Enter to see our products... ")
    
    # Show catalog
    display_product_catalog()
    
    input("\n   Press Enter to start shopping... ")
    
    # Shopping phase
    add_to_cart_interactive(engine, user_id)
    
    # Show final cart
    show_cart(engine, user_id)
    
    input("\n   Press Enter to see how our recommendation engine works... ")
    
    # Explain recommendation process
    explain_recommendation_process(engine, user_id)
    
    input("\n   Press Enter to see your personalized recommendations... ")
    
    # Show recommendations
    show_recommendations(engine, user_id)
    
    # Optional: Explain pricing for a product
    print("\n")
    explain = input("   Want to see how dynamic pricing works? (y/n): ").strip().lower()
    
    if explain == 'y':
        cart = engine.get_cart_summary(user_id)
        if not cart['is_empty']:
            prod_id = cart['items'][0][0]  # First item in cart
            explain_pricing(engine, user_id, prod_id)
    
    # Summary
    print_header("📈 SESSION SUMMARY")
    
    session = engine.get_user_session_info(user_id)
    cart = engine.get_cart_summary(user_id)
    
    print(f"\n   Products Viewed:      {session['total_views']}")
    print(f"   Items in Cart:        {cart['item_count']}")
    print(f"   Cart Total:           Rs. {cart['total']:.2f}")
    print(f"   Recommendations:      Personalized based on behavior")
    print(f"   Session Duration:     {session['session_duration']:.1f} seconds")
    
    print("\n" + "=" * 70)
    print("\n✨ Thank you for trying our AI-powered shopping demo!")
    print("🚀 All powered by custom DSA implementations:")
    print("   • Doubly Linked List (Shopping Cart)")
    print("   • Stack & Queue (User Session)")
    print("   • Graph + PageRank (Recommendations)")
    print("   • Dynamic Pricing (Inventory Rules)")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for shopping! Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please report this issue.\n")
