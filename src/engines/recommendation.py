"""
Graph-Based Recommendation Engine
Uses Personalized PageRank algorithm on user-item interaction network
"""

from collections import defaultdict
from typing import Dict, List, Tuple, Set


class RecommendationGraph:
    """
    Weighted Directed Graph for User-Item recommendations.
    
    Graph Structure:
        - Nodes: Users and Products
        - Edges: user -> product (weight = interaction strength)
    
    Algorithm: Personalized PageRank
        - Time Complexity: O(iterations * edges)
        - Space Complexity: O(nodes)
    """
    
    def __init__(self, damping_factor: float = 0.85, iterations: int = 20):
        """
        Initialize recommendation graph.
        
        Args:
            damping_factor: Probability of following an edge (0-1)
            iterations: Number of PageRank iterations
        """
        self.graph = defaultdict(lambda: defaultdict(float))  # adjacency list
        self.users: Set[int] = set()
        self.products: Set[int] = set()
        self.damping_factor = damping_factor
        self.iterations = iterations

    def add_interaction(
        self,
        user_id: int,
        product_id: int,
        weight: float = 1.0
    ) -> None:
        """
        Add user-product interaction edge.
        Time Complexity: O(1)
        
        Args:
            user_id: User identifier
            product_id: Product identifier
            weight: Interaction strength (higher = stronger)
        """
        self.graph[user_id][product_id] += weight
        self.users.add(user_id)
        self.products.add(product_id)

    def get_neighbors(self, user_id: int) -> Dict[int, float]:
        """
        Get all products a user has interacted with.
        Time Complexity: O(1)
        
        Args:
            user_id: User to query
            
        Returns:
            Dictionary mapping product_id to interaction weight
        """
        return dict(self.graph[user_id])

    def get_user_product_count(self) -> Tuple[int, int]:
        """
        Get counts of users and products in graph.
        
        Returns:
            Tuple of (user_count, product_count)
        """
        return len(self.users), len(self.products)

    def personalized_pagerank(
        self,
        user_id: int,
        top_k: int = 5
    ) -> List[Tuple[int, float]]:
        """
        Personalized PageRank algorithm.
        Time Complexity: O(iterations * edges)
        
        Args:
            user_id: User to generate recommendations for
            top_k: Number of recommendations to return
            
        Returns:
            List of tuples (product_id, relevance_score)
        """
        if user_id not in self.users:
            return []

        # Initialize ranks uniformly
        ranks = defaultdict(float)
        for product in self.products:
            ranks[product] = 1.0 / len(self.products) if self.products else 0

        # Create personalization vector (bias towards user's interactions)
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
                # Personalization component (teleportation)
                new_ranks[product] = (
                    (1 - self.damping_factor) * personalization[product]
                )

                # Damping component (contributions from other users)
                for user in self.users:
                    user_edges = self.graph[user]
                    if user_edges and product in user_edges:
                        # Contribution from this user
                        contribution = ranks[product] / len(user_edges)
                        new_ranks[product] += (
                            self.damping_factor * contribution
                        )

            ranks = new_ranks

        # Return top-k products (exclude already interacted)
        recommendations = [
            (p, ranks[p])
            for p in self.products
            if p not in user_interactions or user_interactions[p] < 1.0
        ]
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:top_k]

    def get_similar_users(
        self,
        user_id: int,
        top_k: int = 5
    ) -> List[Tuple[int, float]]:
        """
        Find similar users based on product interaction overlap.
        Uses Jaccard similarity.
        Time Complexity: O(users * products)
        
        Args:
            user_id: User to find similar users for
            top_k: Number of similar users to return
            
        Returns:
            List of tuples (similar_user_id, similarity_score)
        """
        if user_id not in self.users:
            return []

        user_products = set(self.graph[user_id].keys())
        similarities = []

        for other_user in self.users:
            if other_user == user_id:
                continue

            other_products = set(self.graph[other_user].keys())
            
            # Jaccard similarity
            intersection = len(user_products & other_products)
            union = len(user_products | other_products)
            
            if union > 0:
                similarity = intersection / union
                similarities.append((other_user, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def get_graph_stats(self) -> Dict:
        """
        Get graph statistics.
        
        Returns:
            Dictionary with graph metrics
        """
        total_edges = sum(
            len(products) for products in self.graph.values()
        )
        
        return {
            "total_users": len(self.users),
            "total_products": len(self.products),
            "total_edges": total_edges,
            "avg_interactions_per_user": (
                total_edges / len(self.users) if self.users else 0
            ),
            "density": (
                total_edges / (len(self.users) * len(self.products))
                if self.users and self.products else 0
            )
        }

    def __repr__(self) -> str:
        return (f"RecommendationGraph(users={len(self.users)}, "
                f"products={len(self.products)}, "
                f"edges={sum(len(p) for p in self.graph.values())})")
