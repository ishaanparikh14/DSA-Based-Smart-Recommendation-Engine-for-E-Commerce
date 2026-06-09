"""
Binary Search Tree for Price and Inventory Filtering
Enables efficient range queries and filtering
"""

from typing import Optional, List, Tuple, Callable


class BSTNode:
    """Node in Binary Search Tree"""
    
    def __init__(self, product_id: int, value: float):
        """
        Initialize BST node.
        
        Args:
            product_id: Product identifier
            value: Value to sort by (price or inventory)
        """
        self.product_id = product_id
        self.value = value
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


class BST:
    """
    Binary Search Tree for product filtering.
    
    Time Complexity:
        - Insert: O(log n) average, O(n) worst
        - Search: O(log n) average, O(n) worst
        - Range query: O(log n + k) where k is results
    
    Space Complexity: O(n)
    
    Use Case: Price range filtering, inventory availability checks
    """
    
    def __init__(self):
        """Initialize empty BST"""
        self.root: Optional[BSTNode] = None
        self.size = 0
    
    def insert(self, product_id: int, value: float) -> None:
        """
        Insert product into BST.
        Time Complexity: O(log n) average
        
        Args:
            product_id: Product to insert
            value: Value to sort by (price/inventory)
        """
        if not self.root:
            self.root = BSTNode(product_id, value)
            self.size += 1
        else:
            self._insert_recursive(self.root, product_id, value)
    
    def _insert_recursive(self, node: BSTNode, product_id: int, value: float) -> BSTNode:
        """Helper: Recursive insert"""
        if not node:
            self.size += 1
            return BSTNode(product_id, value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, product_id, value)
        else:
            node.right = self._insert_recursive(node.right, product_id, value)
        
        return node
    
    def search_with_trace(self, value: float) -> Tuple[Optional[int], List[int]]:
        """
        Search for a value and return the trace of visited product IDs.
        
        Args:
            value: Value to search for
            
        Returns:
            Tuple of (found_product_id or None, list_of_visited_product_ids)
        """
        trace = []
        node = self.root
        
        while node:
            trace.append(node.product_id)
            if value == node.value:
                return (node.product_id, trace)
            elif value < node.value:
                node = node.left
            else:
                node = node.right
                
        return (None, trace)

    def get_structure(self) -> Optional[dict]:
        """
        Get the full tree structure for visualization.
        
        Returns:
            Dictionary representing the tree or None
        """
        if not self.root:
            return None
        return self._get_structure_recursive(self.root)

    def _get_structure_recursive(self, node: BSTNode) -> dict:
        """Helper to build tree structure dictionary"""
        return {
            'id': node.product_id,
            'value': node.value,
            'left': self._get_structure_recursive(node.left) if node.left else None,
            'right': self._get_structure_recursive(node.right) if node.right else None
        }

    def range_query(self, min_value: float, max_value: float) -> List[int]:
        """
        Find all products with value in range [min_value, max_value].
        Time Complexity: O(log n + k) where k is number of results
        
        Args:
            min_value: Minimum value (inclusive)
            max_value: Maximum value (inclusive)
            
        Returns:
            List of product IDs in range
        """
        results = []
        self._range_query_recursive(self.root, min_value, max_value, results)
        return results
    
    def _range_query_recursive(self, node: Optional[BSTNode], min_val: float, max_val: float, results: List[int]) -> None:
        """Helper: Recursive range query"""
        if not node:
            return
        
        # If current value is in range, add to results
        if min_val <= node.value <= max_val:
            results.append(node.product_id)
        
        # Recursively search left subtree if needed
        if node.value > min_val:
            self._range_query_recursive(node.left, min_val, max_val, results)
        
        # Recursively search right subtree if needed
        if node.value < max_val:
            self._range_query_recursive(node.right, min_val, max_val, results)
    
    def find_min(self) -> Optional[Tuple[int, float]]:
        """
        Find product with minimum value.
        Time Complexity: O(log n)
        
        Returns:
            Tuple of (product_id, value) or None if empty
        """
        if not self.root:
            return None
        
        node = self.root
        while node.left:
            node = node.left
        
        return (node.product_id, node.value)
    
    def find_max(self) -> Optional[Tuple[int, float]]:
        """
        Find product with maximum value.
        Time Complexity: O(log n)
        
        Returns:
            Tuple of (product_id, value) or None if empty
        """
        if not self.root:
            return None
        
        node = self.root
        while node.right:
            node = node.right
        
        return (node.product_id, node.value)
    
    def get_all_sorted(self) -> List[Tuple[int, float]]:
        """
        Get all products sorted by value (in-order traversal).
        Time Complexity: O(n)
        
        Returns:
            List of tuples (product_id, value) in sorted order
        """
        results = []
        self._inorder_traversal(self.root, results)
        return results
    
    def _inorder_traversal(self, node: Optional[BSTNode], results: List[Tuple[int, float]]) -> None:
        """Helper: In-order traversal"""
        if not node:
            return
        
        self._inorder_traversal(node.left, results)
        results.append((node.product_id, node.value))
        self._inorder_traversal(node.right, results)
    
    def clear(self) -> None:
        """Clear all nodes from BST"""
        self.root = None
        self.size = 0
    
    def __len__(self) -> int:
        """Return number of nodes in BST"""
        return self.size
    
    def __repr__(self) -> str:
        return f"BST(size={self.size})"
