"""
Co-Occurrence Graph Builder
Analyzes transaction data to build product co-purchase relationships
"""

from data_structures.graph import Graph
from models import Transaction, Product
from typing import List, Dict, Tuple


class CoOccurrenceGraph:
    """
    Builds co-occurrence graph from transaction data.
    
    Use Case: Market basket analysis - which products are bought together
    """
    
    def __init__(self):
        """Initialize co-occurrence graph"""
        self.graph = Graph(directed=False)  # Undirected graph
        self.product_frequency: Dict[int, int] = {}  # How often each product is purchased
    
    def build_from_transactions(self, transactions: List[Transaction]) -> None:
        """
        Build co-occurrence graph from transactions.
        
        Args:
            transactions: List of transactions
        """
        for transaction in transactions:
            product_ids = transaction.product_ids
            
            # Update individual product frequency
            for product_id in product_ids:
                self.product_frequency[product_id] = self.product_frequency.get(product_id, 0) + 1
                self.graph.add_vertex(product_id)
            
            # Add edges between all pairs in transaction
            for i in range(len(product_ids)):
                for j in range(i + 1, len(product_ids)):
                    # Add edge with weight = 1 (increment if already exists)
                    self.graph.add_edge(product_ids[i], product_ids[j], weight=1.0)
    
    def get_frequently_bought_together(self, product_id: int, k: int = 5) -> List[Tuple[int, float]]:
        """
        Get products frequently bought with given product.
        
        Args:
            product_id: Product to find co-purchases for
            k: Number of recommendations to return
            
        Returns:
            List of tuples (product_id, co_occurrence_score)
        """
        return self.graph.get_top_neighbors(product_id, k)
    
    def get_co_occurrence_score(self, product_a: int, product_b: int) -> float:
        """
        Get co-occurrence score between two products.
        
        Args:
            product_a: First product
            product_b: Second product
            
        Returns:
            Co-occurrence score (edge weight)
        """
        return self.graph.get_edge_weight(product_a, product_b)
    
    def get_stats(self) -> Dict:
        """Get graph statistics"""
        stats = self.graph.get_stats()
        stats['total_transactions'] = sum(self.product_frequency.values())
        stats['unique_products'] = len(self.product_frequency)
        return stats
    
    def __repr__(self) -> str:
        return f"CoOccurrenceGraph({self.graph})"
