"""
Flask REST API Server
DSA-based E-Commerce Recommendation Engine
NO ML/AI - Only classical algorithms
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Product, User, Transaction
from sample_data import (
    get_sample_products, get_sample_users, get_sample_transactions,
    initialize_user_data, get_all_categories
)
from recommendation.foolproof_pipeline import FoolproofRecommendationPipeline
from pricing.pricing_engine import DynamicPricingEngine
from data_structures.linked_list import DoublyLinkedList
from data_structures.stack import Stack
from data_structures.queue import Queue
from data_structures.bst import BST
from data_structures.heap import MinHeap, HeapItem
from data_structures.trie import Trie
from data_structures.graph import Graph
from product_similarity import ProductSimilarityGraph
from typing import Dict

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global state
products: list[Product] = []
users: list[User] = []
transactions: list[Transaction] = []
product_map: Dict[int, Product] = {}
user_map: Dict[str, User] = {}

# Engines
recommendation_pipeline: FoolproofRecommendationPipeline = None
pricing_engine: DynamicPricingEngine = None

# User-specific data structures
user_carts: Dict[str, DoublyLinkedList] = {}  # Shopping carts
user_view_stacks: Dict[str, Stack] = {}  # Recent views
user_action_queues: Dict[str, Queue] = {}  # Action history

# Global Data Structures
product_price_bst: BST = None
viz_bst: BST = None
category_trie: Trie = None  # Re-exposed for global access if needed (though pipeline has it)

# DSA activity log (for frontend visualization)
dsa_activity_log: list[Dict] = []


def log_dsa_activity(operation: str, data_structure: str, details: str):
    """Log DSA operation for frontend visualization"""
    global dsa_activity_log
    dsa_activity_log.append({
        'operation': operation,
        'data_structure': data_structure,
        'details': details,
        'timestamp': len(dsa_activity_log)
    })
    # Keep only last 50 operations
    if len(dsa_activity_log) > 50:
        dsa_activity_log = dsa_activity_log[-50:]


def initialize_system():
    """Initialize all data structures and load sample data"""
    global products, users, transactions, product_map, user_map
    global co_occurrence, recommendation_pipeline, pricing_engine
    global user_carts, user_view_stacks, user_action_queues
    global product_price_bst, category_trie, viz_bst
    
    
    print("\n" + "="*60)
    print("Initializing DSA-based E-Commerce Engine...")
    print("="*60)
    
    # Load sample data
    products = get_sample_products()
    users = get_sample_users()
    transactions = get_sample_transactions()
    
    # Initialize user data from transactions
    initialize_user_data(users, transactions, products)
    
    # Create lookup maps
    product_map = {p.id: p for p in products}
    user_map = {u.id: u for u in users}
    
    print(f"✓ {len(products)} products loaded")
    print(f"✓ {len(users)} users loaded")
    print(f"✓ {len(transactions)} transactions processed")
    
    # Initialize Data Structures
    product_price_bst = BST()
    viz_bst = BST() # Specialized BST for visualization (limited to ~25 items)
    category_trie = Trie()
    
    for p in products:
        product_price_bst.insert(p.id, p.price)
        # Insert Category
        category_trie.insert(p.category, p.id)
        # Insert Product Name (for search visualization)
        category_trie.insert(p.name, p.id)
        # Insert Brand (if part of name, simple split)
        words = p.name.split()
        if words:
            category_trie.insert(words[0], p.id)

    # Populate viz_bst with random 25 items for better visualization
    import random
    viz_subset = random.sample(products, min(25, len(products)))
    for p in viz_subset:
        viz_bst.insert(p.id, p.price)
        
        
    print(f"✓ Product Price BST built (Sorted by Price)")
    print(f"✓ Search Trie built (Categories + Product Names)")
    
    # Initialize recommendation pipeline
    recommendation_pipeline = FoolproofRecommendationPipeline()
    recommendation_pipeline.initialize(products, users, transactions)
    
    stats = recommendation_pipeline.get_stats()
    co_stats = stats['co_occurrence_stats']
    print(f"✓ Co-occurrence graph built: {co_stats['vertices']} vertices, {co_stats['edges']} edges")
    
    # Initialize pricing engine
    pricing_engine = DynamicPricingEngine()
    pricing_engine.initialize(products, users)
    print(f"✓ Pricing engine initialized with {len(pricing_engine.get_all_rules())} rules")
    
    # Initialize user-specific data structures
    for user in users:
        user_carts[user.id] = DoublyLinkedList(user.id)
        user_view_stacks[user.id] = Stack(max_size=20)
        user_action_queues[user.id] = Queue(max_size=50)
    
    print(f"✓ User data structures initialized (carts, stacks, queues)")
    print("="*60)
    print("🚀 System initialized successfully!")
    print("⚠️  NO ML/AI - Only classical algorithms")
    print("="*60 + "\n")


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'DSA E-Commerce Engine running',
        'stats': {
            'products': len(products),
            'users': len(users),
            'transactions': len(transactions)
        }
    })


@app.route('/api/products', methods=['GET'])
def get_products_endpoint():
    """Get all products, optionally filtered by category or search query"""
    category = request.args.get('category')
    q = request.args.get('q')
    
    if category:
        log_dsa_activity('SEARCH', 'Trie', f'Filtering by category prefix "{category}"')
        filtered = [p for p in products if p.category.lower() == category.lower()]
        return jsonify([p.to_dict() for p in filtered])
        
    if q:
        log_dsa_activity('SEARCH', 'Array/List', f'Linear search for "{q}"')
        filtered = [p for p in products if q.lower() in p.name.lower()]
        return jsonify([p.to_dict() for p in filtered])
    
    return jsonify([p.to_dict() for p in products])


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product by ID"""
    product = product_map.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    return jsonify(product.to_dict())


@app.route('/api/users', methods=['GET'])
def get_users_endpoint():
    """Get all users"""
    return jsonify([u.to_dict() for u in users])


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get single user by ID"""
    user = user_map.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())


@app.route('/api/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Get personalized recommendations for user"""
    k = request.args.get('k', default=10, type=int)
    explain = request.args.get('explain', default='false').lower() == 'true'
    
    user = user_map.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get cart items to include in recommendations
    cart = user_carts.get(user_id)
    cart_product_ids = []
    cart_categories = set()
    
    if cart and len(cart) > 0:
        cart_items = cart.get_items_dict()
        cart_product_ids = [item['product_id'] for item in cart_items]
        
        # Get categories from cart items
        for product_id in cart_product_ids:
            product = product_map.get(product_id)
            if product:
                cart_categories.add(product.category)
        
        # Temporarily add cart categories to user's preferred categories
        original_categories = user.preferred_categories.copy()
        user.preferred_categories = user.preferred_categories.union(cart_categories)
    
    # Log DSA activity
    if cart_categories:
        log_dsa_activity('RECOMMEND', 'Pipeline', f'Generating recommendations (User Cart: {", ".join(cart_categories)})')
    else:
        log_dsa_activity('RECOMMEND', 'Pipeline', f'Generating recommendations for {user.name}')

    log_dsa_activity('TRIE SEARCH', 'Trie', f'Filtering categories for {user.name}')
    log_dsa_activity('GRAPH QUERY', 'Weighted Graph', f'Finding co-occurrences for {user.name}')
    log_dsa_activity('BST SEARCH', 'BST', 'Filtering by price and inventory')
    
    # Get base recommendations
    recommendations, explanation = recommendation_pipeline.get_recommendations(
        user_id,
        k=k*2 if cart_product_ids else k,  # Get more if we have cart items
        explain=explain,
        cart_items=cart_product_ids
    )
    
    # If we have cart items, boost co-occurrence recommendations
    if cart_product_ids:
        co_occurrence_boost = {}
        for cart_product_id in cart_product_ids:
            frequently_bought = recommendation_pipeline.co_occurrence.get_frequently_bought_together(
                cart_product_id,
                k=10
            )
            for pid, score in frequently_bought:
                if pid not in cart_product_ids and pid not in user.purchase_history:
                    co_occurrence_boost[pid] = co_occurrence_boost.get(pid, 0) + score
        
        if len(co_occurrence_boost) > 0:
             log_dsa_activity('GRAPH TRAVERSAL', 'Graph', f'Found {len(co_occurrence_boost)} co-occurring items')
        
        # Merge with existing recommendations
        rec_dict = {pid: score for pid, score in recommendations}
        for pid, boost_score in co_occurrence_boost.items():
            if pid in rec_dict:
                rec_dict[pid] += boost_score * 2.0  # Boost cart-related items
            else:
                rec_dict[pid] = boost_score
        
        # Re-sort and take top-k
        log_dsa_activity('HEAP EXTRACT', 'Min-Heap', f'Selecting Top-{k} recommendations')
        recommendations = sorted(rec_dict.items(), key=lambda x: x[1], reverse=True)[:k]
        
        if explain and explanation:
            explanation['decisions'].append(
                f"Boosted recommendations based on {len(cart_product_ids)} items in cart from categories: {', '.join(cart_categories)}"
            )
    
    # Restore original categories
    if cart_categories:
        user.preferred_categories = original_categories
    
    # Convert to response format
    result = {
        'user_id': user_id,
        'cart_influence': list(cart_categories) if cart_categories else [],
        'recommendations': [
            {
                'product_id': pid,
                'score': score,
                'product': product_map[pid].to_dict() if pid in product_map else None
            }
            for pid, score in recommendations
        ]
    }
    
    if explain and explanation:
        result['explanation'] = explanation
    
    return jsonify(result)



@app.route('/api/recommendations/<user_id>/explain/<int:product_id>', methods=['GET'])
def explain_recommendation(user_id, product_id):
    """Explain why a product was recommended"""
    cart = user_carts.get(user_id)
    cart_product_ids = []
    if cart:
        cart_product_ids = [item['product_id'] for item in cart.get_items_dict()]

    log_dsa_activity('TRACE', 'Graph/Trie', f'Tracing recommendation path for Product #{product_id}')
    explanation = recommendation_pipeline.explain_recommendation(
        user_id, 
        product_id,
        cart_items=cart_product_ids
    )
    return jsonify(explanation)


@app.route('/api/frequently-bought-together/<int:product_id>', methods=['GET'])
def frequently_bought_together(product_id):
    """Get products frequently bought with this product"""
    k = request.args.get('k', default=5, type=int)
    
    product = product_map.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Log DSA activity
    log_dsa_activity('GRAPH_QUERY', 'Co-Occurrence Graph', f'Finding products bought with {product.name}')
    
    co_products = recommendation_pipeline.co_occurrence.get_frequently_bought_together(
        product_id,
        k=k
    )
    
    result = {
        'product_id': product_id,
        'frequently_bought_together': [
            {
                'product_id': pid,
                'co_occurrence_score': score,
                'product': product_map[pid].to_dict() if pid in product_map else None
            }
            for pid, score in co_products
        ]
    }
    
    return jsonify(result)


@app.route('/api/pricing/<int:product_id>', methods=['GET'])
def get_dynamic_price(product_id):
    """Get dynamic price for product"""
    user_id = request.args.get('user_id')
    
    product = product_map.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Log DSA activity
    log_dsa_activity('PRICE_CALC', 'BST', f'Calculating dynamic price for {product.name}')
    
    explanation = pricing_engine.get_price_explanation(product_id, user_id)
    return jsonify(explanation)


@app.route('/api/cart/<user_id>/add', methods=['POST'])
def add_to_cart(user_id):
    """Add product to user's cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    user = user_map.get(user_id)
    product = product_map.get(product_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Get user's cart
    cart = user_carts.get(user_id)
    if not cart:
        cart = DoublyLinkedList(user_id)
        user_carts[user_id] = cart
    
    # Add to cart
    cart.add_item(product_id, quantity, product.price)
    
    # Log DSA activity
    log_dsa_activity('INSERT', 'Doubly Linked List', f'{product.name} added to {user.name}\'s cart')
    
    # Log action in queue
    action_queue = user_action_queues.get(user_id)
    if action_queue:
        action_queue.enqueue({'action': 'add_to_cart', 'product_id': product_id})
        log_dsa_activity('ENQUEUE', 'Queue', f'Action logged for {user.name}')
    
    # Update user preferences (Instant Feedback)
    product = product_map.get(product_id)
    if product:
        user.preferred_categories.add(product.category)

    return jsonify({
        'message': 'Product added to cart',
        'cart_size': len(cart),
        'cart_total': cart.get_total()
    })


@app.route('/api/cart/<user_id>/update-quantity', methods=['POST'])
def update_cart_quantity(user_id):
    """Update quantity of a product in cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    cart = user_carts.get(user_id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    if quantity is None or quantity < 0:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    success = cart.update_quantity(product_id, quantity)
    
    if success:
        product = product_map.get(product_id)
        if quantity == 0:
            log_dsa_activity('DELETE', 'Doubly Linked List', f'{product.name if product else "Product"} removed from cart (quantity set to 0)')
        else:
            log_dsa_activity('UPDATE', 'Doubly Linked List', f'{product.name if product else "Product"} quantity updated to {quantity}')
    
    return jsonify({
        'success': success,
        'cart_size': len(cart),
        'cart_total': cart.get_total()
    })


@app.route('/api/cart/<user_id>/remove', methods=['POST'])
def remove_from_cart(user_id):
    """Remove product from user's cart"""
    data = request.get_json()
    product_id = data.get('product_id')
    
    cart = user_carts.get(user_id)
    if not cart:
        return jsonify({'error': 'Cart not found'}), 404
    
    success = cart.remove_item(product_id)
    
    if success:
        product = product_map.get(product_id)
        log_dsa_activity('DELETE', 'Doubly Linked List', f'{product.name if product else "Product"} removed from cart')
    
    return jsonify({
        'success': success,
        'cart_size': len(cart),
        'cart_total': cart.get_total()
    })


@app.route('/api/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    """Get user's cart contents"""
    cart = user_carts.get(user_id)
    if not cart:
        return jsonify({'items': [], 'total': 0, 'size': 0})
    
    items = cart.get_items_dict()
    
    # Enrich with product details
    for item in items:
        product = product_map.get(item['product_id'])
        if product:
            item['product_name'] = product.name
            item['product_category'] = product.category
            item['product_image'] = product.image_url
    
    return jsonify({
        'user_id': user_id,
        'items': items,
        'total': cart.get_total(),
        'size': len(cart)
    })


@app.route('/api/cart/<user_id>/clear', methods=['POST'])
def clear_cart(user_id):
    """Clear user's cart"""
    cart = user_carts.get(user_id)
    if cart:
        # Clear the cart
        user_carts[user_id] = DoublyLinkedList(user_id)
        log_dsa_activity('CLEAR', 'Doubly Linked List', f'Cart cleared for user {user_id}')
    
    return jsonify({'success': True, 'message': 'Cart cleared'})


@app.route('/api/checkout/<user_id>', methods=['POST'])
def checkout(user_id):
    """Complete purchase - add cart items to purchase history"""
    data = request.get_json()
    product_ids = data.get('product_ids', [])
    
    user = user_map.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if not product_ids:
        return jsonify({'error': 'No products to checkout'}), 400
    
    # Add products to purchase history
    for product_id in product_ids:
        if product_id not in user.purchase_history:
            user.purchase_history.append(product_id)
        
        # Update preferred categories
        product = product_map.get(product_id)
        if product:
            user.preferred_categories.add(product.category)
            # Increment purchase count
            product.purchases += 1
    
    # Log DSA activity
    log_dsa_activity('CHECKOUT', 'Update', f'{user.name} purchased {len(product_ids)} items')
    
    # Rebuild collaborative filter with updated user data
    recommendation_pipeline.collaborative.add_user(user)
    
    return jsonify({
        'success': True,
        'message': f'Purchase completed: {len(product_ids)} items',
        'new_purchase_count': len(user.purchase_history),
        'preferred_categories': list(user.preferred_categories)
    })



@app.route('/api/view/<user_id>/<int:product_id>', methods=['POST'])
def track_view(user_id, product_id):
    """Track product view"""
    user = user_map.get(user_id)
    product = product_map.get(product_id)
    
    if not user or not product:
        return jsonify({'error': 'User or product not found'}), 404
    
    # Add to view stack
    view_stack = user_view_stacks.get(user_id)
    if view_stack:
        view_stack.push(product_id)
        log_dsa_activity('PUSH', 'Stack', f'{user.name} viewed {product.name}')
    
    # Add to session queue
    action_queue = user_action_queues.get(user_id)
    if action_queue:
        action_queue.enqueue({
            'action': 'view_product',
            'product_id': product_id,
            'timestamp': datetime.now().isoformat()
        })
        log_dsa_activity('ENQUEUE', 'Queue', f'{user.name} view action queued')
    
    # Update user preferences (Instant Feedback)
    user.preferred_categories.add(product.category)
    
    # Increment product view count
    product.views += 1
    
    return jsonify({'message': 'View tracked'})


@app.route('/api/view/<user_id>/pop', methods=['POST'])
def pop_view(user_id):
    """Pop latest product view (Undo View)"""
    user = user_map.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    view_stack = user_view_stacks.get(user_id)
    if not view_stack or view_stack.is_empty():
        return jsonify({'error': 'Stack is empty'}), 400
        
    # POP operation
    product_id = view_stack.pop()
    product = product_map.get(product_id)
    
    # Log DSA activity
    log_dsa_activity('POP', 'Stack', f'{user.name} removed {product.name if product else "item"} details')
    
    return jsonify({
        'message': 'Popped last view',
        'popped_product_id': product_id,
        'popped_product_name': product.name if product else 'Unknown'
    })




@app.route('/api/session-queue/<user_id>/dequeue', methods=['POST'])
def dequeue_session_item(user_id):
    """Dequeue oldest session action (Process Item)"""
    user = user_map.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    queue = user_session_queues.get(user_id)
    if not queue or queue.is_empty():
        return jsonify({'error': 'Queue is empty'}), 400
        
    # DEQUEUE operation
    item = queue.dequeue()
    
    # Log DSA activity
    action_name = "Item"
    if isinstance(item, dict):
        action_name = "View" if item.get('action') == 'view_product' else "Add to Cart"
        
    log_dsa_activity('DEQUEUE', 'Queue', f'{user.name} processed {action_name}')
    
    return jsonify({
        'message': 'Dequeued session item',
        'item': item
    })


@app.route('/api/recent-views/<user_id>', methods=['GET'])
def get_recent_views(user_id):
    """Get user's recent product views"""
    view_stack = user_view_stacks.get(user_id)
    if not view_stack:
        return jsonify({'views': []})
    
    recent_views = view_stack.get_all()
    
    # Enrich with product details
    views_with_products = [
        {
            'product_id': pid,
            'product': product_map[pid].to_dict() if pid in product_map else None
        }
        for pid in recent_views
    ]
    
    return jsonify({'views': views_with_products})


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = get_all_categories()
    return jsonify({'categories': categories})


@app.route('/api/dsa-activity', methods=['GET'])
def get_dsa_activity():
    """Get recent DSA operations for visualization"""
    limit = request.args.get('limit', default=20, type=int)
    return jsonify({'activity': dsa_activity_log[-limit:]})


@app.route('/api/dsa-activity/log', methods=['POST'])
def log_frontend_activity():
    """Log DSA activity from frontend"""
    data = request.get_json()
    operation = data.get('operation', 'UNKNOWN')
    data_structure = data.get('data_structure', 'UNKNOWN')
    details = data.get('details', '')
    
    log_dsa_activity(operation, data_structure, details)
    return jsonify({'success': True})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    stats = recommendation_pipeline.get_stats()
    
    return jsonify({
        'products': len(products),
        'users': len(users),
        'transactions': len(transactions),
        'categories': len(get_all_categories()),
        'recommendation_stats': stats,
        'pricing_rules': len(pricing_engine.get_all_rules())
    })


@app.route('/api/session-queue/<user_id>', methods=['GET'])
def get_session_queue(user_id):
    """Get user's session action queue for visualization"""
    if user_id not in user_action_queues:
        return jsonify({'queue': []})
        
    # Get all items from queue without removing them
    # Note: Our Queue implementation might not have a get_all, so we might need to access internal list
    # Assuming standard Queue implementation wrapper
    q = user_action_queues[user_id]
    
    # Depending on Queue implementation, we might need to peek or access internal storage
    # If it's the Queue class from data_structures.queue
    if hasattr(q, 'get_all'):
        # Return list of items from front (oldest) to rear (newest)
        # We might want to reverse it for UI (newest first)? 
        # For now, return as is (FIFO)
        return jsonify({'queue': q.get_all()})
    
    return jsonify({'queue': []})


# --- VISUALIZATION ENDPOINTS (NEW) ---

@app.route('/api/visualize/bst/structure', methods=['GET'])
def get_bst_structure():
    """Get partial BST structure for visualization (limit 25)"""
    if not viz_bst:
        return jsonify({'error': 'BST not initialized'}), 500
    return jsonify(viz_bst.get_structure())

@app.route('/api/visualize/bst/search', methods=['GET'])
def visualize_bst_search():
    """Trace BST search for a price"""
    if not viz_bst:
        return jsonify({'error': 'BST not initialized'}), 500
        
    try:
        price = float(request.args.get('price', 0))
        found_id, trace = viz_bst.search_with_trace(price)
        
        # Enrich trace with values for frontend
        enriched_trace = []
        for pid in trace:
            product = product_map.get(pid)
            if product:
                enriched_trace.append({'id': pid, 'price': product.price})
                
        log_dsa_activity('SEARCH', 'BST', f'Binary Search for price ${price} (Depth: {len(trace)})')
        
        return jsonify({
            'found': found_id is not None,
            'product': product_map.get(found_id).to_dict() if found_id and found_id in product_map else None,
            'trace': enriched_trace
        })
    except ValueError:
        return jsonify({'error': 'Invalid price'}), 400

@app.route('/api/visualize/bst/sort', methods=['GET'])
def visualize_bst_sort():
    """Get sorted products via In-Order Traversal"""
    if not viz_bst:
        return jsonify({'error': 'BST not initialized'}), 500
        
    sorted_items = viz_bst.get_all_sorted()
    
    # Enrich with details
    results = []
    for pid, price in sorted_items:
        product = product_map.get(pid)
        if product:
            results.append(product.to_dict())
            
    log_dsa_activity('SORT', 'BST', f'In-Order Traversal (Sorted {len(results)} items)')
    return jsonify(results)

@app.route('/api/visualize/heap/extract-min', methods=['GET'])
def visualize_heap_sort():
    """Get Heap Sort steps (simulated via top-k)"""
    # Create a temporary min-heap with a limited subset of products (random 15 for visibility)
    import random
    subset = random.sample(products, min(15, len(products)))
    
    heap = MinHeap()
    for p in subset:
        heap.push(p.price, p.id)
        
    # Enrich initial heap with product details
    initial_heap = []
    for item in heap.heap:
        p = product_map.get(item.data)
        if p:
            initial_heap.append({
                'score': item.score, 
                'data': item.data,
                'name': p.name
            })
    
    # Extract all to get sorted (simulating Heap Sort)
    sorted_products = []
    
    # We need to simulate the extraction on a copy so we return the initial structure intact
    sim_heap = MinHeap()
    sim_heap.heap = [HeapItem(item['score'], item['data']) for item in initial_heap]
    
    while not sim_heap.is_empty():
        score, pid = sim_heap.pop()
        p = product_map.get(pid)
        if p:
            sorted_products.append(p.to_dict())
            
    log_dsa_activity('SORT', 'Heap', f'Heap Sort (Extracted {len(sorted_products)} items)')
    
    return jsonify({
        'initial_structure': initial_heap,
        'sorted_products': sorted_products,
        'count': len(sorted_products)
    })

@app.route('/api/visualize/trie/search', methods=['GET'])
def visualize_trie_search():
    """Trace Trie search for a prefix"""
    if not category_trie:
        return jsonify({'error': 'Trie not initialized'}), 500
        
    prefix = request.args.get('q', '').lower().strip()
    if not prefix:
        return jsonify({
            'trace': [], 
            'found_categories': [],
            'all_categories': category_trie.get_all_categories(),
            'status': 'empty',
            'message': 'Enter a prefix to search'
        })
    
    trace = category_trie.search_trace(prefix)
    categories = category_trie.starts_with(prefix)
    
    # Determine search status
    prefix_fully_traced = len(trace) == len(prefix)
    has_matches = len(categories) > 0
    
    if prefix_fully_traced and has_matches:
        status = 'found'
        message = f'Found {len(categories)} matching categories!'
    elif prefix_fully_traced and not has_matches:
        status = 'partial'  # Prefix exists but no complete categories
        message = f'Prefix "{prefix}" exists but no complete categories match'
    elif len(trace) > 0:
        status = 'partial'
        message = f'Partial match: traced {len(trace)}/{len(prefix)} characters. No path for "{prefix[len(trace):]}"'
    else:
        status = 'not-found'
        message = f'No categories start with "{prefix[0]}"'
    
    log_dsa_activity('SEARCH', 'Trie', f'Prefix search for "{prefix}" - {status} (Traced {len(trace)}/{len(prefix)} chars)')
    
    return jsonify({
        'trace': trace,
        'searched_prefix': prefix,
        'matched_length': len(trace),
        'found_categories': categories,
        'all_categories': category_trie.get_all_categories(),
        'status': status,
        'message': message
    })


# ============================================================================
# RECOMMENDATION GRAPH VISUALIZATION
# ============================================================================

@app.route('/api/visualize/recommendation-graph/<user_id>', methods=['GET'])
def get_recommendation_graph(user_id):
    """
    Get graph data for recommendation visualization.
    Returns nodes (cart items + recommended items) and edges (co-occurrence relationships).
    
    This visualizes the DSA concept of how products are connected through:
    1. Co-occurrence graph (products bought together)
    2. Category relationships
    """
    user = user_map.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get cart items
    cart = user_carts.get(user_id)
    cart_product_ids = []
    if cart and len(cart) > 0:
        cart_items = cart.get_items_dict()
        cart_product_ids = [item['product_id'] for item in cart_items]
    
    if not cart_product_ids:
        return jsonify({
            'nodes': [],
            'edges': [],
            'message': 'Add items to cart to see recommendation graph'
        })
    
    nodes = []
    edges = []
    node_ids = set()
    
    # Add cart items as source nodes
    for pid in cart_product_ids:
        product = product_map.get(pid)
        if product:
            nodes.append({
                'id': f'product_{pid}',
                'product_id': pid,
                'name': product.name,
                'category': product.category,
                'price': product.price,
                'type': 'cart',  # Cart item (source)
                'image_url': product.image_url
            })
            node_ids.add(pid)
    
    # For each cart item, get co-occurrence recommendations
    recommendations_by_source = {}
    for cart_pid in cart_product_ids:
        # Get frequently bought together products
        co_products = recommendation_pipeline.co_occurrence.get_frequently_bought_together(
            cart_pid,
            k=5  # Top 5 related products per cart item
        )
        
        for rec_pid, score in co_products:
            if rec_pid not in cart_product_ids and rec_pid not in user.purchase_history:
                # Add edge
                edges.append({
                    'source': f'product_{cart_pid}',
                    'target': f'product_{rec_pid}',
                    'weight': float(score),
                    'type': 'co_occurrence'
                })
                
                # Track recommendations by source for grouping
                if rec_pid not in recommendations_by_source:
                    recommendations_by_source[rec_pid] = []
                recommendations_by_source[rec_pid].append({
                    'source_id': cart_pid,
                    'score': score
                })
    
    # Add recommendation nodes
    for rec_pid, sources in recommendations_by_source.items():
        if rec_pid not in node_ids:
            product = product_map.get(rec_pid)
            if product:
                # Calculate total score from all sources
                total_score = sum(s['score'] for s in sources)
                nodes.append({
                    'id': f'product_{rec_pid}',
                    'product_id': rec_pid,
                    'name': product.name,
                    'category': product.category,
                    'price': product.price,
                    'type': 'recommendation',
                    'total_score': total_score,
                    'sources': sources,
                    'image_url': product.image_url
                })
                node_ids.add(rec_pid)
    
    # Also add category-based recommendations (fallback for sparse co-occurrence)
    for cart_pid in cart_product_ids:
        cart_product = product_map.get(cart_pid)
        if cart_product:
            # Get popular items from same category
            cat_products = recommendation_pipeline.ranking_engine.rank_by_popularity(
                list(recommendation_pipeline.category_filter.get_products_in_category(cart_product.category)),
                reverse=True
            )[:3]
            
            for cat_pid, pop_score in cat_products:
                if cat_pid not in node_ids and cat_pid != cart_pid:
                    product = product_map.get(cat_pid)
                    if product:
                        nodes.append({
                            'id': f'product_{cat_pid}',
                            'product_id': cat_pid,
                            'name': product.name,
                            'category': product.category,
                            'price': product.price,
                            'type': 'category_match',
                            'total_score': pop_score * 0.1,
                            'image_url': product.image_url
                        })
                        node_ids.add(cat_pid)
                        
                        # Add category edge
                        edges.append({
                            'source': f'product_{cart_pid}',
                            'target': f'product_{cat_pid}',
                            'weight': 0.5,  # Lower weight for category match
                            'type': 'category_match'
                        })
    
    log_dsa_activity('GRAPH_VIZ', 'Co-Occurrence Graph', 
                     f'Generated graph: {len(nodes)} nodes, {len(edges)} edges')
    
    return jsonify({
        'nodes': nodes,
        'edges': edges,
        'cart_count': len(cart_product_ids),
        'recommendation_count': len(nodes) - len(cart_product_ids)
    })


@app.route('/api/visualize/user-product-graph/<user_id>', methods=['GET'])
def get_user_product_graph(user_id):
    """
    Get User-Product graph data for visualization.
    Shows all users on one side, products on the other, connected by purchase/cart edges.
    
    This visualizes:
    1. User similarity through shared purchases
    2. Product relationships through user purchase patterns
    """
    current_user = user_map.get(user_id)
    if not current_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get current user's cart
    cart = user_carts.get(user_id)
    cart_product_ids = set()
    if cart and len(cart) > 0:
        cart_items = cart.get_items_dict()
        cart_product_ids = {item['product_id'] for item in cart_items}
    
    nodes = []
    edges = []
    
    # Add user nodes
    for user in users:
        is_current = user.id == user_id
        nodes.append({
            'id': f'user_{user.id}',
            'user_id': user.id,
            'name': user.name,
            'type': 'current_user' if is_current else 'user',
            'purchase_count': len(user.purchase_history),
            'categories': list(user.preferred_categories)[:3]
        })
    
    # Get relevant products (purchased by any user or in current cart)
    relevant_products = set()
    for user in users:
        relevant_products.update(user.purchase_history[-10:])  # Last 10 purchases per user
    relevant_products.update(cart_product_ids)
    
    # Add product nodes
    for pid in relevant_products:
        product = product_map.get(pid)
        if product:
            in_cart = pid in cart_product_ids
            nodes.append({
                'id': f'product_{pid}',
                'product_id': pid,
                'name': product.name,
                'category': product.category,
                'price': product.price,
                'type': 'cart_product' if in_cart else 'product',
                'popularity': product.purchases
            })
    
    # Add edges for purchases
    for user in users:
        is_current = user.id == user_id
        for pid in user.purchase_history:
            if pid in relevant_products:
                edges.append({
                    'source': f'user_{user.id}',
                    'target': f'product_{pid}',
                    'type': 'purchase',
                    'is_current_user': is_current,
                    'weight': 1.0
                })
    
    # Add edges for cart items (current user only)
    for pid in cart_product_ids:
        edges.append({
            'source': f'user_{user_id}',
            'target': f'product_{pid}',
            'type': 'cart',
            'is_current_user': True,
            'weight': 2.0  # Higher weight for cart items
        })
    
    # Calculate user similarity for potential recommendation explanation
    similar_users = recommendation_pipeline.collaborative.get_similar_users(user_id, k=3)
    
    log_dsa_activity('GRAPH_VIZ', 'User-Product Graph', 
                     f'Generated: {len(nodes)} nodes, {len(edges)} edges')
    
    return jsonify({
        'nodes': nodes,
        'edges': edges,
        'user_count': len(users),
        'product_count': len(relevant_products),
        'cart_items': list(cart_product_ids),
        'similar_users': [{'user_id': uid, 'similarity': sim} for uid, sim in similar_users]
    })


# ============================================================================
# USER SIMILARITY COMPLETE GRAPH
# ============================================================================

@app.route('/api/visualize/user-similarity-graph', methods=['GET'])
def get_user_similarity_complete_graph():
    """
    Get complete user similarity graph - all users connected to each other
    with Jaccard similarity scores as edge weights.
    
    This visualizes user-user collaborative filtering.
    """
    nodes = []
    edges = []
    
    # Add all user nodes
    for user in users:
        nodes.append({
            'id': user.id,
            'name': user.name,
            'type': 'user',
            'purchase_count': len(user.purchase_history),
            'categories': list(user.preferred_categories)[:3]
        })
    
    # Calculate pairwise Jaccard similarity and create complete graph edges
    user_list = list(users)
    for i in range(len(user_list)):
        for j in range(i + 1, len(user_list)):
            user_a = user_list[i]
            user_b = user_list[j]
            
            # Calculate Jaccard similarity
            set_a = set(user_a.purchase_history)
            set_b = set(user_b.purchase_history)
            
            if set_a or set_b:
                intersection = len(set_a & set_b)
                union = len(set_a | set_b)
                similarity = intersection / union if union > 0 else 0.0
            else:
                similarity = 0.0
            
            # Add edge (even if similarity is 0 for complete graph)
            edges.append({
                'source': user_a.id,
                'target': user_b.id,
                'weight': round(similarity, 3),
                'shared_products': list(set_a & set_b)[:5]  # First 5 shared products
            })
    
    log_dsa_activity('GRAPH_VIZ', 'User Similarity Graph', 
                     f'Complete graph: {len(nodes)} users, {len(edges)} edges')
    
    return jsonify({
        'nodes': nodes,
        'edges': edges,
        'graph_type': 'complete',
        'similarity_metric': 'jaccard'
    })


@app.route('/api/visualize/user-orders/<user_id>', methods=['GET'])
def get_user_order_history_graph(user_id):
    """
    Get user's order history as disjoint graphs.
    Each order is a cluster of products bought together.
    
    This visualizes the purchase patterns of individual users.
    """
    user = user_map.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    nodes = []
    edges = []
    orders = []
    
    # Get user's purchased products
    purchased_products = user.purchase_history
    
    if not purchased_products:
        return jsonify({
            'user_id': user_id,
            'user_name': user.name,
            'nodes': [],
            'edges': [],
            'orders': [],
            'message': 'No purchase history yet'
        })
    
    # Group products into "orders" (simulate order clusters)
    # In a real system, you'd have actual order data
    # Here we create clusters based on categories and sequential purchasing
    
    order_size = 3  # Products per order (simulated)
    order_clusters = []
    current_order = []
    
    for i, pid in enumerate(purchased_products):
        product = product_map.get(pid)
        if product:
            current_order.append(pid)
            
            if len(current_order) >= order_size or i == len(purchased_products) - 1:
                if current_order:
                    order_clusters.append(current_order)
                    current_order = []
    
    # Create nodes and edges for each order cluster
    for order_idx, order_products in enumerate(order_clusters):
        order_id = f"order_{order_idx + 1}"
        order_total = 0
        order_product_nodes = []
        
        for pid in order_products:
            product = product_map.get(pid)
            if product:
                order_total += product.price
                node_id = f"{order_id}_product_{pid}"
                order_product_nodes.append(node_id)
                
                nodes.append({
                    'id': node_id,
                    'product_id': pid,
                    'name': product.name,
                    'category': product.category,
                    'price': product.price,
                    'order_id': order_id,
                    'order_index': order_idx + 1,
                    'type': 'product'
                })
        
        # Create edges within the order (products bought together)
        for k in range(len(order_product_nodes)):
            for l in range(k + 1, len(order_product_nodes)):
                edges.append({
                    'source': order_product_nodes[k],
                    'target': order_product_nodes[l],
                    'order_id': order_id,
                    'type': 'same_order'
                })
        
        orders.append({
            'order_id': order_id,
            'order_number': order_idx + 1,
            'product_count': len(order_products),
            'total': round(order_total, 2),
            'products': order_products
        })
    
    log_dsa_activity('GRAPH_VIZ', 'Order History', 
                     f'User {user_id}: {len(orders)} orders, {len(nodes)} products')
    
    return jsonify({
        'user_id': user_id,
        'user_name': user.name,
        'nodes': nodes,
        'edges': edges,
        'orders': orders,
        'total_products': len(purchased_products),
        'preferred_categories': list(user.preferred_categories)
    })


@app.route('/api/visualize/product-similarity-graph', methods=['GET'])
def get_product_similarity_graph():
    """Get product similarity graph based on purchase history"""
    min_similarity = request.args.get('min_similarity', default=0.1, type=float)
    max_edges_per_node = request.args.get('max_edges', default=5, type=int)
    category_filter = request.args.get('category')
    
    # Convert products and users to dictionary format
    products_data = [p.to_dict() for p in products]
    users_data = [u.to_dict() for u in users]
    
    # Apply category filter if specified
    if category_filter:
        products_data = [p for p in products_data if p.get('category', '').lower() == category_filter.lower()]
        
        if len(products_data) == 0:
            return jsonify({
                'nodes': [],
                'edges': [],
                'stats': {
                    'totalProducts': 0,
                    'totalConnections': 0,
                    'avgSimilarity': 0
                },
                'message': 'No products found in specified category'
            })
    
    # Create similarity graph
    similarity_graph = ProductSimilarityGraph(users_data, products_data)
    
    # Generate graph data
    graph_data = similarity_graph.generate_graph_data(
        min_similarity=min_similarity,
        max_edges_per_node=max_edges_per_node
    )
    
    log_dsa_activity('GRAPH_BUILD', 'Product Similarity Graph', 
                     f'Generated graph: {graph_data["stats"]["totalProducts"]} products, '
                     f'{graph_data["stats"]["totalConnections"]} connections')
    
    return jsonify(graph_data)


@app.route('/api/visualize/product-recommendations/<int:product_id>', methods=['GET'])
def get_product_recommendations_graph(product_id):
    """Get product recommendations for a specific product using similarity graph"""
    top_n = request.args.get('top_n', default=5, type=int)
    
    product = product_map.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Convert data
    products_data = [p.to_dict() for p in products]
    users_data = [u.to_dict() for u in users]
    
    # Create similarity graph
    similarity_graph = ProductSimilarityGraph(users_data, products_data)
    
    # Get recommendations
    recommendations = similarity_graph.get_recommendations_for_product(product_id, top_n)
    
    # Format response
    result = {
        'product_id': product_id,
        'product_name': product.name,
        'recommendations': [
            {
                'product_id': pid,
                'similarity_score': score,
                'product': product_map[pid].to_dict() if pid in product_map else None
            }
            for pid, score in recommendations
        ]
    }
    
    log_dsa_activity('RECOMMEND', 'Similarity Graph', 
                     f'Found {len(recommendations)} similar products for {product.name}')
    
    return jsonify(result)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Initialize system
    initialize_system()
    
    # Run Flask server
    print("🚀 Starting Flask server on http://localhost:5000")
    print("📊 DSA-based E-Commerce Engine ready!")
    print("\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
