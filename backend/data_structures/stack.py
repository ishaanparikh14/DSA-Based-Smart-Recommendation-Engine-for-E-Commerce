"""
Stack Implementation for Recent Product Views
LIFO (Last In First Out) data structure
"""

from typing import Any, Optional, List


class StackNode:
    """Node in stack"""
    
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['StackNode'] = None


class Stack:
    """
    Stack implementation using linked list.
    
    Time Complexity:
        - Push: O(1)
        - Pop: O(1)
        - Peek: O(1)
    
    Space Complexity: O(n) where n is number of items
    
    Use Case: Track recent product views (most recent at top)
    """
    
    def __init__(self, max_size: Optional[int] = None):
        """
        Initialize stack.
        
        Args:
            max_size: Maximum stack size (None for unlimited)
        """
        self.top: Optional[StackNode] = None
        self.size = 0
        self.max_size = max_size
    
    def push(self, data: Any) -> bool:
        """
        Push item onto stack.
        Time Complexity: O(1)
        
        Args:
            data: Item to push
            
        Returns:
            True if pushed, False if stack is full
        """
        if self.max_size and self.size >= self.max_size:
            # Remove oldest item (bottom of stack) if at capacity
            self._remove_bottom()
        
        new_node = StackNode(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        return True
    
    def pop(self) -> Optional[Any]:
        """
        Pop item from stack.
        Time Complexity: O(1)
        
        Returns:
            Top item if exists, None if empty
        """
        if self.is_empty():
            return None
        
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data
    
    def peek(self) -> Optional[Any]:
        """
        View top item without removing.
        Time Complexity: O(1)
        
        Returns:
            Top item if exists, None if empty
        """
        return self.top.data if self.top else None
    
    def _remove_bottom(self) -> None:
        """Remove bottom item from stack (for max_size enforcement)"""
        if not self.top:
            return
        
        if not self.top.next:
            self.top = None
            self.size = 0
            return
        
        current = self.top
        while current.next and current.next.next:
            current = current.next
        
        current.next = None
        self.size -= 1
    
    def is_empty(self) -> bool:
        """Check if stack is empty"""
        return self.top is None
    
    def get_all(self) -> List[Any]:
        """
        Get all items in stack (top to bottom).
        Time Complexity: O(n)
        
        Returns:
            List of items from top to bottom
        """
        items = []
        current = self.top
        while current:
            items.append(current.data)
            current = current.next
        return items
    
    def clear(self) -> None:
        """Clear all items from stack"""
        self.top = None
        self.size = 0
    
    def __len__(self) -> int:
        """Return number of items in stack"""
        return self.size
    
    def __repr__(self) -> str:
        items = self.get_all()
        return f"Stack(size={self.size}, top={items[0] if items else None})"
