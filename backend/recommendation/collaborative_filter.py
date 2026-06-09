"""
Collaborative Filtering using Jaccard Similarity
Finds similar users based on purchase overlap (NO matrix factorization)
"""

from data_structures.graph import Graph
from models import User
from typing import List, Tuple, Set, Dict


class CollaborativeFilter:
    """
    User-user collaborative filtering using Jaccard similarity.
    
    100% set-based operations - NO machine learning
    """
    
    def __init__(self):
        """Initialize collaborative filter"""
        self.user_graph = Graph(directed=False)
        self.user_purchases: Dict[str, Set[int]] = {}
    
    def add_user(self, user: User) -> None:
        """
        Add user to collaborative filter.
        
        Args:
            user: User object
        """
        self.user_purchases[user.id] = set(user.purchase_history)
        self.user_graph.add_vertex(user.id)
    
    def build_similarity_graph(self, users: List[User], threshold: float = 0.1) -> None:
        """
        Build user similarity graph using Jaccard similarity.
        
        Args:
            users: List of users
            threshold: Minimum similarity to create edge
        """
        # Add all users
        for user in users:
            self.add_user(user)
        
        # Calculate pairwise similarities
        user_ids = list(self.user_purchases.keys())
        for i in range(len(user_ids)):
            for j in range(i + 1, len(user_ids)):
                user_a = user_ids[i]
                user_b = user_ids[j]
                
                similarity = self._jaccard_similarity(
                    self.user_purchases[user_a],
                    self.user_purchases[user_b]
                )
                
                if similarity >= threshold:
                    self.user_graph.add_edge(user_a, user_b, weight=similarity)
    
    def _jaccard_similarity(self, set_a: Set[int], set_b: Set[int]) -> float:
        """
        Calculate Jaccard similarity between two sets.
        
        Jaccard = |A ∩ B| / |A ∪ B|
        
        Args:
            set_a: First set
            set_b: Second set
            
        Returns:
            Similarity score (0-1)
        """
        if not set_a and not set_b:
            return 0.0
        
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        
        return intersection / union if union > 0 else 0.0
    
    def get_similar_users(self, user_id: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Get most similar users.
        
        Args:
            user_id: User to find similar users for
            k: Number of similar users to return
            
        Returns:
            List of tuples (similar_user_id, similarity_score)
        """
        return self.user_graph.get_top_neighbors(user_id, k)
    
    def get_collaborative_recommendations(
        self,
        user_id: str,
        k: int = 10,
        num_similar_users: int = 5
    ) -> List[Tuple[int, float]]:
        """
        Get recommendations based on similar users' purchases.
        
        Args:
            user_id: User to recommend for
            k: Number of recommendations
            num_similar_users: Number of similar users to consider
            
        Returns:
            List of tuples (product_id, score)
        """
        # Get similar users
        similar_users = self.get_similar_users(user_id, num_similar_users)
        
        if not similar_users:
            return []
        
        # Get user's current purchases
        user_purchases = self.user_purchases.get(user_id, set())
        
        # Aggregate recommendations from similar users
        product_scores: Dict[int, float] = {}
        
        for similar_user_id, similarity in similar_users:
            similar_purchases = self.user_purchases.get(similar_user_id, set())
            
            # Recommend products the similar user bought but current user hasn't
            for product_id in similar_purchases:
                if product_id not in user_purchases:
                    # Weight by similarity score
                    product_scores[product_id] = product_scores.get(product_id, 0) + similarity
        
        # Sort by score and return top-k
        sorted_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_products[:k]
    
    def get_stats(self) -> Dict:
        """Get collaborative filter statistics"""
        return self.user_graph.get_stats()
    
    def __repr__(self) -> str:
        return f"CollaborativeFilter(users={len(self.user_purchases)})"
