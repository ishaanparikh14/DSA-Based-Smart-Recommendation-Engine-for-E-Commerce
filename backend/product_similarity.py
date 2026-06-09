"""
Product Similarity Graph Generator
Calculates product similarity scores based on user purchase history
and co-purchase patterns for recommendation purposes.
"""

from collections import defaultdict
from typing import Dict, List, Tuple
import math


class ProductSimilarityGraph:
    """Generates a product similarity graph based on purchase history"""
    
    def __init__(self, users_data: list, products_data: list):
        """
        Initialize the similarity graph generator
        
        Args:
            users_data: List of user objects with purchase history
            products_data: List of product objects
        """
        self.users = users_data
        self.products = {p['id']: p for p in products_data}
        self.product_ids = [p['id'] for p in products_data]
        
        # Co-purchase matrix: tracks how often products are bought together
        self.co_purchase_matrix = defaultdict(lambda: defaultdict(int))
        
        # Product purchase counts
        self.product_purchase_count = defaultdict(int)
        
        self._build_co_purchase_matrix()
    
    def _build_co_purchase_matrix(self):
        """Build the co-purchase matrix from user purchase histories"""
        for user in self.users:
            # Get all products this user has purchased
            purchased_products = set()
            
            # Add from purchase history
            if 'purchase_history' in user:
                purchased_products.update(user['purchase_history'])
            
            # Add from cart
            if 'cart' in user:
                purchased_products.update(user['cart'])
            
            # Update co-purchase counts
            purchased_list = list(purchased_products)
            for i, product1 in enumerate(purchased_list):
                self.product_purchase_count[product1] += 1
                for product2 in purchased_list[i+1:]:
                    # Increment both directions for undirected graph
                    self.co_purchase_matrix[product1][product2] += 1
                    self.co_purchase_matrix[product2][product1] += 1
    
    def calculate_jaccard_similarity(self, product1_id: int, product2_id: int) -> float:
        """
        Calculate Jaccard similarity between two products
        
        Jaccard similarity = |A ∩ B| / |A ∪ B|
        where A and B are sets of users who purchased each product
        """
        co_purchases = self.co_purchase_matrix[product1_id][product2_id]
        
        product1_purchases = self.product_purchase_count[product1_id]
        product2_purchases = self.product_purchase_count[product2_id]
        
        if product1_purchases + product2_purchases - co_purchases == 0:
            return 0.0
        
        similarity = co_purchases / (product1_purchases + product2_purchases - co_purchases)
        return round(similarity, 3)
    
    def calculate_cosine_similarity(self, product1_id: int, product2_id: int) -> float:
        """
        Calculate cosine similarity between two products
        
        Cosine similarity = (A · B) / (||A|| * ||B||)
        """
        co_purchases = self.co_purchase_matrix[product1_id][product2_id]
        
        product1_purchases = self.product_purchase_count[product1_id]
        product2_purchases = self.product_purchase_count[product2_id]
        
        if product1_purchases == 0 or product2_purchases == 0:
            return 0.0
        
        similarity = co_purchases / math.sqrt(product1_purchases * product2_purchases)
        return round(similarity, 3)
    
    def get_category_similarity(self, product1_id: int, product2_id: int) -> float:
        """
        Calculate category-based similarity
        Returns 1.0 if same category, 0.5 if same main category, 0.0 otherwise
        """
        if product1_id not in self.products or product2_id not in self.products:
            return 0.0
        
        cat1 = self.products[product1_id].get('category', '')
        cat2 = self.products[product2_id].get('category', '')
        
        if cat1 == cat2:
            return 1.0
        
        # Check if main category matches (e.g., "Electronics" in "Electronics > Laptops")
        main_cat1 = cat1.split('>')[0].strip() if '>' in cat1 else cat1
        main_cat2 = cat2.split('>')[0].strip() if '>' in cat2 else cat2
        
        if main_cat1 == main_cat2:
            return 0.5
        
        return 0.0
    
    def calculate_combined_similarity(self, product1_id: int, product2_id: int) -> float:
        """
        Calculate combined similarity score using multiple factors
        
        Combined score = 0.4 * cosine + 0.3 * jaccard + 0.3 * category
        """
        cosine = self.calculate_cosine_similarity(product1_id, product2_id)
        jaccard = self.calculate_jaccard_similarity(product1_id, product2_id)
        category = self.get_category_similarity(product1_id, product2_id)
        
        combined = 0.4 * cosine + 0.3 * jaccard + 0.3 * category
        return round(combined, 3)
    
    def generate_graph_data(self, min_similarity: float = 0.1, max_edges_per_node: int = 5) -> Dict:
        """
        Generate graph data for visualization
        
        Args:
            min_similarity: Minimum similarity threshold for creating an edge
            max_edges_per_node: Maximum number of edges per node (keeps graph readable)
        
        Returns:
            Dictionary with nodes and edges for graph visualization
        """
        nodes = []
        edges = []
        
        # Create nodes
        for product_id in self.product_ids:
            if product_id in self.products:
                product = self.products[product_id]
                nodes.append({
                    'id': product_id,
                    'name': product.get('name', f'Product {product_id}'),
                    'category': product.get('category', 'Unknown'),
                    'price': product.get('price', 0),
                    'image': product.get('image', ''),
                    'purchaseCount': self.product_purchase_count[product_id]
                })
        
        # Create edges based on similarity
        edge_set = set()  # To avoid duplicate edges
        
        for product1_id in self.product_ids:
            # Calculate similarities with all other products
            similarities = []
            
            for product2_id in self.product_ids:
                if product1_id >= product2_id:  # Avoid duplicates and self-loops
                    continue
                
                similarity = self.calculate_combined_similarity(product1_id, product2_id)
                
                if similarity >= min_similarity:
                    similarities.append((product2_id, similarity))
            
            # Sort by similarity and take top N
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_similarities = similarities[:max_edges_per_node]
            
            # Create edges
            for product2_id, similarity in top_similarities:
                edge_key = (min(product1_id, product2_id), max(product1_id, product2_id))
                
                if edge_key not in edge_set:
                    edge_set.add(edge_key)
                    edges.append({
                        'source': product1_id,
                        'target': product2_id,
                        'weight': similarity,
                        'label': f'{similarity:.2f}'
                    })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'totalProducts': len(nodes),
                'totalConnections': len(edges),
                'avgSimilarity': round(sum(e['weight'] for e in edges) / len(edges), 3) if edges else 0
            }
        }
    
    def get_recommendations_for_product(self, product_id: int, top_n: int = 5) -> List[Tuple[int, float]]:
        """
        Get top N product recommendations for a given product
        
        Returns:
            List of (product_id, similarity_score) tuples
        """
        recommendations = []
        
        for other_id in self.product_ids:
            if other_id == product_id:
                continue
            
            similarity = self.calculate_combined_similarity(product_id, other_id)
            recommendations.append((other_id, similarity))
        
        # Sort by similarity and return top N
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:top_n]
