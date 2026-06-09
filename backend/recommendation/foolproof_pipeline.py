"""
Foolproof Recommendation Pipeline
Category-first approach ensures relevant recommendations
6-stage pipeline with full explainability
"""

from .co_occurrence_graph import CoOccurrenceGraph
from .collaborative_filter import CollaborativeFilter
from .category_filter import CategoryFilter
from .ranking_engine import RankingEngine
from .top_k_selector import TopKSelector
from models import Product, User, Transaction
from typing import List, Tuple, Dict, Optional


class FoolproofRecommendationPipeline:
    """
    Main recommendation pipeline with category-first approach.
    
    Pipeline Stages:
    1. Co-Occurrence Graph → Market basket analysis
    2. Collaborative Filtering → User-user similarity
    3. Category Filtering → CRITICAL: Match user preferences
    4. Ranking Engine → Multi-criteria scoring
    5. Top-K Selection → Heap-based selection
    6. Explainability → Full decision trace
    
    NO MACHINE LEARNING - 100% classical algorithms
    """
    
    def __init__(self):
        """Initialize recommendation pipeline"""
        self.co_occurrence = CoOccurrenceGraph()
        self.collaborative = CollaborativeFilter()
        self.category_filter = CategoryFilter()
        self.ranking_engine = RankingEngine()
        self.top_k_selector = TopKSelector()
        
        self.products: List[Product] = []
        self.users: List[User] = []
        self.product_map: Dict[int, Product] = {}
        self.user_map: Dict[str, User] = {}
        
        self.initialized = False
    
    def initialize(
        self,
        products: List[Product],
        users: List[User],
        transactions: List[Transaction]
    ) -> None:
        """
        Initialize pipeline with data.
        
        Args:
            products: List of products
            users: List of users
            transactions: List of transactions
        """
        self.products = products
        self.users = users
        self.product_map = {p.id: p for p in products}
        self.user_map = {u.id: u for u in users}
        
        # Build co-occurrence graph
        self.co_occurrence.build_from_transactions(transactions)
        
        # Build collaborative filter
        self.collaborative.build_similarity_graph(users, threshold=0.05)
        
        # Build category filter
        self.category_filter.build_from_products(products)
        
        # Build ranking engine
        self.ranking_engine.build_from_products(products)
        
        self.initialized = True
    
    def get_recommendations(
        self,
        user_id: str,
        k: int = 10,
        explain: bool = False,
        cart_items: List[int] = None
    ) -> Tuple[List[Tuple[int, float]], Optional[Dict]]:
        """
        Get personalized recommendations for user.
        
        Args:
            user_id: User to recommend for
            k: Number of recommendations
            explain: If True, return explanation
            cart_items: List of product IDs in current cart
            
        Returns:
            Tuple of (recommendations, explanation)
            recommendations: List of (product_id, score) tuples
            explanation: Dict with decision trace (if explain=True)
        """
        if not self.initialized:
            raise RuntimeError("Pipeline not initialized. Call initialize() first.")
        
        user = self.user_map.get(user_id)
        if not user:
            return ([], None)
        
        explanation = {
            'user_id': user_id,
            'stages': [],
            'decisions': []
        } if explain else None
        
        # Stage 1: Get collaborative filtering candidates
        collab_candidates = self.collaborative.get_collaborative_recommendations(
            user_id,
            k=k*3,  # Get more candidates for filtering
            num_similar_users=5
        )
        
        if explain:
            explanation['stages'].append({
                'stage': 1,
                'name': 'Collaborative Filtering',
                'candidates': len(collab_candidates),
                'description': 'Found similar users and their purchases'
            })
        
        # Stage 2: Get co-occurrence candidates from user's purchase history
        co_occurrence_candidates = []
        for product_id in user.purchase_history[-5:]:  # Last 5 purchases
            frequently_bought = self.co_occurrence.get_frequently_bought_together(
                product_id,
                k=5
            )
            co_occurrence_candidates.extend(frequently_bought)
        
        if explain:
            explanation['stages'].append({
                'stage': 2,
                'name': 'Co-Occurrence Analysis (History)',
                'candidates': len(co_occurrence_candidates),
                'description': 'Products frequently bought with user\'s purchases'
            })

        # Stage 2.5: Get candidates from Cart Items (Immediate Intent)
        cart_candidates = []
        if cart_items:
            for product_id in cart_items:
                frequently_bought = self.co_occurrence.get_frequently_bought_together(
                    product_id,
                    k=8  # Higher k for cart items
                )
                
                # ALWAYS mix in popular items from the SAME category to ensure diversity
                # This guarantees that even if co-occurrences are weak (noisy), the category is represented
                product = self.product_map.get(product_id)
                if product:
                    cat_products = self.ranking_engine.rank_by_popularity(
                        list(self.category_filter.get_products_in_category(product.category)),
                        reverse=True
                    )[:10]  # Top 10 from category (Increased from 3 to avoid sold-out/purchased suppression)
                    
                    # Add with a guaranteed strong baseline score (e.g., 5.0) 
                    # This competes with strong co-occurrences (typically 1-10 range)
                    for pid, pop_score in cat_products:
                        if pid != product_id:
                            # Use a fixed high score for category relevance instead of raw popularity (which is ~100-200)
                            # This ensures balance between Categories vs Co-occurrences
                            frequently_bought.append((pid, 5.0))

                cart_candidates.extend(frequently_bought)
            
            if explain:
                explanation['stages'].append({
                    'stage': 2.5,
                    'name': 'Cart Context Analysis',
                    'candidates': len(cart_candidates),
                    'description': f'Products related to {len(cart_items)} items in cart'
                })
        
        # Combine candidates with SCALED scores (0-100+ Range)
        all_candidates = {}
        for product_id, score in collab_candidates:
            # Jaccard is 0-1. Scale to 0-50 pts
            all_candidates[product_id] = all_candidates.get(product_id, 0) + score * 50.0
        
        for product_id, score in co_occurrence_candidates:
            # Co-occurrence is edge weight (1-5 typically). Scale to 10-50 pts
            all_candidates[product_id] = all_candidates.get(product_id, 0) + score * 10.0

        for product_id, score in cart_candidates:
            # STRATEGY: "Cart First" - Immediate Intent
            # Base boost of 100 to ensure they top the list (above typical 50-80 range)
            # Plus scaled score
            all_candidates[product_id] = all_candidates.get(product_id, 0) + 100.0 + (score * 10.0)
        
        # Remove already purchased products
        for product_id in user.purchase_history:
            all_candidates.pop(product_id, None)
        
        candidate_list = list(all_candidates.items())
        
        if explain:
            explanation['stages'].append({
                'stage': 3,
                'name': 'Candidate Aggregation',
                'candidates': len(candidate_list),
                'description': 'Combined collaborative and co-occurrence candidates'
            })
        
        # Stage 3: CRITICAL - Category Filtering
        candidate_ids = [pid for pid, _ in candidate_list]
        filtered_ids = self.category_filter.filter_by_user_categories(
            candidate_ids,
            user,
            allow_exploration=True,
            exploration_ratio=0.2
        )
        
        # Rebuild candidate list with filtered IDs
        filtered_candidates = [(pid, all_candidates[pid]) for pid in filtered_ids if pid in all_candidates]
        
        if explain:
            removed = len(candidate_list) - len(filtered_candidates)
            explanation['stages'].append({
                'stage': 4,
                'name': 'Category Filtering (CRITICAL)',
                'candidates': len(filtered_candidates),
                'removed': removed,
                'description': f'Filtered to user\'s preferred categories: {list(user.preferred_categories)}',
                'user_categories': list(user.preferred_categories)
            })
            explanation['decisions'].append(
                f"Category filter removed {removed} irrelevant products"
            )
        
        # Fallback: If no candidates after category filtering, use popular products in user's categories
        if not filtered_candidates and user.preferred_categories:
            category_products = self.category_filter.get_products_in_user_categories(user)
            popular_in_categories = self.ranking_engine.rank_by_popularity(
                list(category_products),
                reverse=True
            )
            # Remove already purchased
            filtered_candidates = [
                (pid, score) for pid, score in popular_in_categories
                if pid not in user.purchase_history
            ][:k*2]
            
            if explain:
                explanation['decisions'].append(
                    f"Fallback: Used popular products in user's categories"
                )
        
        # Stage 4: Ranking with composite scores
        ranked_candidates = self.ranking_engine.rank_products(
            filtered_candidates,
            user,
            apply_filters=True  # Filter out-of-stock
        )
        
        if explain:
            explanation['stages'].append({
                'stage': 5,
                'name': 'Multi-Criteria Ranking',
                'candidates': len(ranked_candidates),
                'description': 'Ranked by popularity, inventory, and price'
            })
        
        # Stage 5: Top-K Selection using Heap
        final_recommendations = self.top_k_selector.select_top_k(
            ranked_candidates,
            k
        )
        
        if explain:
            explanation['stages'].append({
                'stage': 6,
                'name': 'Top-K Selection (Heap)',
                'recommendations': len(final_recommendations),
                'description': f'Selected top {k} using max-heap'
            })
            
            # Add final recommendations to explanation
            explanation['final_recommendations'] = [
                {
                    'product_id': pid,
                    'score': score,
                    'product_name': self.product_map[pid].name if pid in self.product_map else 'Unknown',
                    'category': self.product_map[pid].category if pid in self.product_map else 'Unknown'
                }
                for pid, score in final_recommendations
            ]
        
        return (final_recommendations, explanation)
    
    def explain_recommendation(
        self,
        user_id: str,
        product_id: int,
        cart_items: List[int] = None
    ) -> Dict:
        """
        Explain why a product was recommended to a user.
        
        Args:
            user_id: User ID
            product_id: Product ID to explain
            cart_items: List of product IDs in current cart
            
        Returns:
            Explanation dictionary
        """
        user = self.user_map.get(user_id)
        product = self.product_map.get(product_id)
        
        if not user or not product:
            return {'error': 'User or product not found'}
        
        explanation = {
            'user_id': user_id,
            'product_id': product_id,
            'product_name': product.name,
            'product_category': product.category,
            'reasons': []
        }
        
        # Check Cart Context (Immediate Intent)
        if cart_items:
            # Check co-occurrence with cart items
            for cart_pid in cart_items:
                co_score = self.co_occurrence.get_co_occurrence_score(cart_pid, product_id)
                if co_score > 0:
                    cart_product = self.product_map.get(cart_pid)
                    explanation['reasons'].append({
                        'type': 'cart_related',
                        'score': co_score * 2.0,
                        'description': f"Frequently bought with item in cart: {cart_product.name if cart_product else 'Unknown'}"
                    })
            
            # Check if it was a category fallback from cart
            if not explanation['reasons']:
                # If we have a cart item in the same category but no direct co-occurrence, it's likely a category fallback
                for cart_pid in cart_items:
                    cart_product = self.product_map.get(cart_pid)
                    if cart_product and cart_product.category == product.category:
                        explanation['reasons'].append({
                            'type': 'cart_category_match',
                            'score': 0.8,
                            'description': f"Similar to item in cart: {cart_product.name} ({product.category})"
                        })

        # Check category match
        category_score = self.category_filter.get_category_match_score(
            product_id,
            user,
            self.product_map
        )
        if category_score > 0:
            explanation['reasons'].append({
                'type': 'category_match',
                'score': category_score,
                'description': f"Product is in your preferred category: {product.category}"
            })
        
        # Check co-occurrence
        for purchased_id in user.purchase_history[-5:]:
            co_score = self.co_occurrence.get_co_occurrence_score(purchased_id, product_id)
            if co_score > 0:
                purchased_product = self.product_map.get(purchased_id)
                explanation['reasons'].append({
                    'type': 'frequently_bought_together',
                    'score': co_score,
                    'description': f"Often bought with: {purchased_product.name if purchased_product else 'Unknown'}"
                })
        
        # Check similar users
        similar_users = self.collaborative.get_similar_users(user_id, k=3)
        for similar_user_id, similarity in similar_users:
            similar_user = self.user_map.get(similar_user_id)
            if similar_user and product_id in similar_user.purchase_history:
                explanation['reasons'].append({
                    'type': 'similar_user_purchased',
                    'score': similarity,
                    'description': f"Similar user ({similar_user.name}) purchased this"
                })
        
        # Popularity
        popularity = product.purchases * 2 + product.views
        if popularity > 50:
            explanation['reasons'].append({
                'type': 'popular_product',
                'score': popularity,
                'description': f"Popular product ({product.purchases} purchases, {product.views} views)"
            })
        
        return explanation
    
    def get_stats(self) -> Dict:
        """Get pipeline statistics"""
        return {
            'total_products': len(self.products),
            'total_users': len(self.users),
            'co_occurrence_stats': self.co_occurrence.get_stats(),
            'collaborative_stats': self.collaborative.get_stats(),
            'category_stats': self.category_filter.get_stats(),
            'ranking_stats': self.ranking_engine.get_stats()
        }
    
    def __repr__(self) -> str:
        return f"FoolproofRecommendationPipeline(initialized={self.initialized})"
