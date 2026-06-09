"""
Queue Implementation for Session Tracking
FIFO (First In First Out) data structure
"""

from typing import Any, Optional, List


class QueueNode:
    """Node in queue"""
    
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['QueueNode'] = None


class Queue:
    """
    Queue implementation using linked list.
    
    Time Complexity:
        - Enqueue: O(1)
        - Dequeue: O(1)
        - Peek: O(1)
    
    Space Complexity: O(n) where n is number of items
    
    Use Case: Track user actions chronologically (session tracking)
    """
    
    def __init__(self, max_size: Optional[int] = None):
        """
        Initialize queue.
        
        Args:
            max_size: Maximum queue size (None for unlimited)
        """
        self.front: Optional[QueueNode] = None
        self.rear: Optional[QueueNode] = None
        self.size = 0
        self.max_size = max_size
    
    def enqueue(self, data: Any) -> bool:
        """
        Add item to rear of queue.
        Time Complexity: O(1)
        
        Args:
            data: Item to enqueue
            
        Returns:
            True if enqueued, False if queue is full
        """
        if self.max_size and self.size >= self.max_size:
            # Remove oldest item (front) if at capacity
            self.dequeue()
        
        new_node = QueueNode(data)
        
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        
        self.size += 1
        return True
    
    def dequeue(self) -> Optional[Any]:
        """
        Remove item from front of queue.
        Time Complexity: O(1)
        
        Returns:
            Front item if exists, None if empty
        """
        if self.is_empty():
            return None
        
        data = self.front.data
        self.front = self.front.next
        
        if not self.front:
            self.rear = None
        
        self.size -= 1
        return data
    
    def peek(self) -> Optional[Any]:
        """
        View front item without removing.
        Time Complexity: O(1)
        
        Returns:
            Front item if exists, None if empty
        """
        return self.front.data if self.front else None
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return self.front is None
    
    def get_all(self) -> List[Any]:
        """
        Get all items in queue (front to rear).
        Time Complexity: O(n)
        
        Returns:
            List of items from front to rear
        """
        items = []
        current = self.front
        while current:
            items.append(current.data)
            current = current.next
        return items
    
    def clear(self) -> None:
        """Clear all items from queue"""
        self.front = None
        self.rear = None
        self.size = 0
    
    def __len__(self) -> int:
        """Return number of items in queue"""
        return self.size
    
    def __repr__(self) -> str:
        return f"Queue(size={self.size}, front={self.peek()})"
