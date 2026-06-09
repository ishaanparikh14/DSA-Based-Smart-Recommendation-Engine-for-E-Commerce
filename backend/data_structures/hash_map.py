"""
Custom Hash Map Implementation
Provides O(1) average-case lookups for product catalog
Uses chaining for collision resolution
"""

from typing import Any, Optional, List, Tuple


class HashNode:
    """Node in hash map chain"""
    
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.next: Optional['HashNode'] = None


class HashMap:
    """
    Custom Hash Map with chaining collision resolution.
    
    Time Complexity:
        - Insert: O(1) average, O(n) worst case
        - Lookup: O(1) average, O(n) worst case
        - Delete: O(1) average, O(n) worst case
    
    Space Complexity: O(n) where n is number of items
    """
    
    def __init__(self, capacity: int = 100):
        """
        Initialize hash map.
        
        Args:
            capacity: Initial capacity of hash table
        """
        self.capacity = capacity
        self.size = 0
        self.buckets: List[Optional[HashNode]] = [None] * capacity
        self.load_factor_threshold = 0.75
    
    def _hash(self, key: Any) -> int:
        """
        Hash function to map key to bucket index.
        
        Args:
            key: Key to hash
            
        Returns:
            Bucket index
        """
        return hash(key) % self.capacity
    
    def _resize(self) -> None:
        """Resize hash table when load factor exceeds threshold"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.size = 0
        
        # Rehash all existing items
        for bucket in old_buckets:
            current = bucket
            while current:
                self.put(current.key, current.value)
                current = current.next
    
    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update key-value pair.
        Time Complexity: O(1) average
        
        Args:
            key: Key to insert
            value: Value to associate with key
        """
        # Check load factor and resize if needed
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()
        
        index = self._hash(key)
        
        # Check if key already exists
        current = self.buckets[index]
        while current:
            if current.key == key:
                current.value = value  # Update existing
                return
            current = current.next
        
        # Insert new node at beginning of chain
        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Retrieve value by key.
        Time Complexity: O(1) average
        
        Args:
            key: Key to lookup
            
        Returns:
            Value if found, None otherwise
        """
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == key:
                return current.value
            current = current.next
        
        return None
    
    def delete(self, key: Any) -> bool:
        """
        Delete key-value pair.
        Time Complexity: O(1) average
        
        Args:
            key: Key to delete
            
        Returns:
            True if deleted, False if not found
        """
        index = self._hash(key)
        current = self.buckets[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[index] = current.next
                self.size -= 1
                return True
            prev = current
            current = current.next
        
        return False
    
    def contains(self, key: Any) -> bool:
        """Check if key exists in hash map"""
        return self.get(key) is not None
    
    def keys(self) -> List[Any]:
        """Get all keys in hash map"""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append(current.key)
                current = current.next
        return result
    
    def values(self) -> List[Any]:
        """Get all values in hash map"""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append(current.value)
                current = current.next
        return result
    
    def items(self) -> List[Tuple[Any, Any]]:
        """Get all key-value pairs"""
        result = []
        for bucket in self.buckets:
            current = bucket
            while current:
                result.append((current.key, current.value))
                current = current.next
        return result
    
    def clear(self) -> None:
        """Clear all items from hash map"""
        self.buckets = [None] * self.capacity
        self.size = 0
    
    def __len__(self) -> int:
        """Return number of items in hash map"""
        return self.size
    
    def __repr__(self) -> str:
        return f"HashMap(size={self.size}, capacity={self.capacity}, load_factor={self.size/self.capacity:.2f})"
