"""
Top-K Selector using Heap
Efficient selection of top recommendations
"""

from data_structures.heap import MaxHeap, top_k_selection
from typing import List, Tuple, Any


class TopKSelector:
    """
    Heap-based Top-K selection for recommendations.
    
    Time Complexity: O(n log k) where n is candidates, k is top-k
    """
    
    def __init__(self):
        """Initialize Top-K selector"""
        self.heap = MaxHeap()
    
    def select_top_k(
        self,
        items: List[Tuple[Any, float]],
        k: int,
        use_heap: bool = True,
        normalize: bool = True
    ) -> List[Tuple[Any, float]]:
        """
        Select top-k items by score.
        
        Args:
            items: List of (item, score) tuples
            k: Number of top items to select
            use_heap: If True, use heap; else use sorting
            normalize: If True, normalize scores to 0-1 range
            
        Returns:
            List of top-k (item, score) tuples
        """
        if not items:
            return []
        
        # Select top-k
        if use_heap:
            top_items = top_k_selection(items, k, use_max=True)
        else:
            # Fallback to sorting
            sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
            top_items = sorted_items[:k]
        
        # Normalize scores to 0-1 range
        if normalize and top_items:
            scores = [score for _, score in top_items]
            min_score = min(scores)
            max_score = max(scores)
            
            if max_score > min_score:
                # Normalize to 0-1
                normalized = [
                    (item, (score - min_score) / (max_score - min_score))
                    for item, score in top_items
                ]
                return normalized
        
        return top_items
    
    def select_top_k_with_diversity(
        self,
        items: List[Tuple[Any, float]],
        k: int,
        diversity_key: Any = None,
        max_per_group: int = 3
    ) -> List[Tuple[Any, float]]:
        """
        Select top-k items with diversity constraint.
        
        Args:
            items: List of (item, score) tuples
            k: Number of top items to select
            diversity_key: Function to extract diversity key from item
            max_per_group: Maximum items per diversity group
            
        Returns:
            List of top-k (item, score) tuples with diversity
        """
        if not diversity_key:
            return self.select_top_k(items, k)
        
        # Sort by score
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        
        # Select with diversity
        selected = []
        group_counts = {}
        
        for item, score in sorted_items:
            if len(selected) >= k:
                break
            
            group = diversity_key(item)
            count = group_counts.get(group, 0)
            
            if count < max_per_group:
                selected.append((item, score))
                group_counts[group] = count + 1
        
        return selected
    
    def __repr__(self) -> str:
        return f"TopKSelector()"
