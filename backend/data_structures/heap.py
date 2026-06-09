"""
Min-Heap Implementation for Top-K Selection
Efficient priority queue for selecting best recommendations
"""

from typing import Any, List, Tuple, Optional, Callable
import heapq


class HeapItem:
    """Item in the heap with score and data"""
    
    def __init__(self, score: float, data: Any):
        """
        Initialize heap item.
        
        Args:
            score: Priority score (lower = higher priority for min-heap)
            data: Associated data
        """
        self.score = score
        self.data = data
    
    def __lt__(self, other: 'HeapItem') -> bool:
        """Comparison for heap ordering"""
        return self.score < other.score
    
    def __repr__(self) -> str:
        return f"HeapItem(score={self.score}, data={self.data})"


class MinHeap:
    """
    Min-Heap for Top-K selection.
    
    Time Complexity:
        - Insert: O(log n)
        - Extract min: O(log n)
        - Peek min: O(1)
        - Build heap: O(n)
    
    Space Complexity: O(n)
    
    Use Case: Select Top-K recommendations efficiently
    """
    
    def __init__(self):
        """Initialize empty min-heap"""
        self.heap: List[HeapItem] = []
    
    def push(self, score: float, data: Any) -> None:
        """
        Insert item into heap.
        Time Complexity: O(log n)
        
        Args:
            score: Priority score
            data: Associated data
        """
        item = HeapItem(score, data)
        heapq.heappush(self.heap, item)
    
    def pop(self) -> Optional[Tuple[float, Any]]:
        """
        Remove and return minimum item.
        Time Complexity: O(log n)
        
        Returns:
            Tuple of (score, data) or None if empty
        """
        if not self.heap:
            return None
        
        item = heapq.heappop(self.heap)
        return (item.score, item.data)
    
    def peek(self) -> Optional[Tuple[float, Any]]:
        """
        View minimum item without removing.
        Time Complexity: O(1)
        
        Returns:
            Tuple of (score, data) or None if empty
        """
        if not self.heap:
            return None
        
        item = self.heap[0]
        return (item.score, item.data)
    
    def is_empty(self) -> bool:
        """Check if heap is empty"""
        return len(self.heap) == 0
    
    def size(self) -> int:
        """Return number of items in heap"""
        return len(self.heap)
    
    def clear(self) -> None:
        """Clear all items from heap"""
        self.heap = []
    
    def __len__(self) -> int:
        """Return number of items in heap"""
        return len(self.heap)
    
    def __repr__(self) -> str:
        return f"MinHeap(size={len(self.heap)})"


class MaxHeap:
    """
    Max-Heap for Top-K selection (highest scores first).
    
    Implemented using min-heap with negated scores.
    """
    
    def __init__(self):
        """Initialize empty max-heap"""
        self.heap: List[HeapItem] = []
    
    def push(self, score: float, data: Any) -> None:
        """
        Insert item into heap.
        Time Complexity: O(log n)
        
        Args:
            score: Priority score
            data: Associated data
        """
        # Negate score for max-heap behavior
        item = HeapItem(-score, data)
        heapq.heappush(self.heap, item)
    
    def pop(self) -> Optional[Tuple[float, Any]]:
        """
        Remove and return maximum item.
        Time Complexity: O(log n)
        
        Returns:
            Tuple of (score, data) or None if empty
        """
        if not self.heap:
            return None
        
        item = heapq.heappop(self.heap)
        return (-item.score, item.data)  # Negate back
    
    def peek(self) -> Optional[Tuple[float, Any]]:
        """
        View maximum item without removing.
        Time Complexity: O(1)
        
        Returns:
            Tuple of (score, data) or None if empty
        """
        if not self.heap:
            return None
        
        item = self.heap[0]
        return (-item.score, item.data)  # Negate back
    
    def is_empty(self) -> bool:
        """Check if heap is empty"""
        return len(self.heap) == 0
    
    def size(self) -> int:
        """Return number of items in heap"""
        return len(self.heap)
    
    def clear(self) -> None:
        """Clear all items from heap"""
        self.heap = []
    
    def __len__(self) -> int:
        """Return number of items in heap"""
        return len(self.heap)
    
    def __repr__(self) -> str:
        return f"MaxHeap(size={len(self.heap)})"


def top_k_selection(items: List[Tuple[float, Any]], k: int, use_max: bool = True) -> List[Tuple[float, Any]]:
    """
    Select top-K items efficiently using heap.
    Time Complexity: O(n log k)
    
    Args:
        items: List of (score, data) tuples
        k: Number of top items to select
        use_max: If True, select k highest scores; if False, select k lowest
        
    Returns:
        List of top-k (score, data) tuples
    """
    if use_max:
        heap = MaxHeap()
    else:
        heap = MinHeap()
    
    for score, data in items:
        heap.push(score, data)
    
    # Extract top-k
    results = []
    for _ in range(min(k, len(heap))):
        item = heap.pop()
        if item:
            results.append(item)
    
    return results
