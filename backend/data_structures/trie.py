"""
Trie (Prefix Tree) Implementation for Category Hierarchies
Enables fast category matching and filtering
"""

from typing import Dict, List, Optional, Set


class TrieNode:
    """Node in the Trie"""
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.is_end_of_word = False
        self.product_ids: Set[int] = set()  # Products in this category
        self.category_name: Optional[str] = None


class Trie:
    """
    Trie (Prefix Tree) for category hierarchies.
    
    Time Complexity:
        - Insert: O(m) where m is length of category name
        - Search: O(m)
        - Prefix search: O(m + k) where k is number of results
    
    Space Complexity: O(n * m) where n is number of categories
    
    Use Case: Fast category matching for recommendation filtering
    """
    
    def __init__(self):
        """Initialize empty trie"""
        self.root = TrieNode()
        self.all_categories: Set[str] = set()
    
    def insert(self, category: str, product_id: Optional[int] = None) -> None:
        """
        Insert category into trie.
        Time Complexity: O(m) where m is length of category
        
        Args:
            category: Category name to insert
            product_id: Optional product ID to associate with this category
        """
        # Normalize category (lowercase, strip whitespace)
        category = category.lower().strip()
        self.all_categories.add(category)
        
        node = self.root
        for char in category:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.category_name = category
        
        if product_id is not None:
            node.product_ids.add(product_id)
    
    def search(self, category: str) -> bool:
        """
        Check if exact category exists.
        Time Complexity: O(m)
        
        Args:
            category: Category to search for
            
        Returns:
            True if category exists, False otherwise
        """
        category = category.lower().strip()
        node = self._find_node(category)
        return node is not None and node.is_end_of_word

    def search_trace(self, prefix: str) -> List[str]:
        """
        Trace the search path for a prefix.
        
        Args:
            prefix: Prefix to trace
            
        Returns:
            List of nodes visited (represented by char/category part)
        """
        trace = []
        node = self.root
        prefix = prefix.lower().strip()
        
        for char in prefix:
            if char in node.children:
                trace.append(char)
                node = node.children[char]
            else:
                break
                
        return trace
    
    def starts_with(self, prefix: str) -> List[str]:
        """
        Find all categories with given prefix.
        Time Complexity: O(m + k) where k is number of results
        
        Args:
            prefix: Prefix to search for
            
        Returns:
            List of categories starting with prefix
        """
        prefix = prefix.lower().strip()
        node = self._find_node(prefix)
        
        if not node:
            return []
        
        # Collect all categories from this node
        results = []
        self._collect_categories(node, prefix, results)
        return results
    
    def get_products_in_category(self, category: str) -> Set[int]:
        """
        Get all product IDs in a category.
        Time Complexity: O(m)
        
        Args:
            category: Category to query
            
        Returns:
            Set of product IDs in this category
        """
        category = category.lower().strip()
        node = self._find_node(category)
        
        if node and node.is_end_of_word:
            return node.product_ids.copy()
        return set()
    
    def get_products_in_categories(self, categories: List[str]) -> Set[int]:
        """
        Get all product IDs across multiple categories.
        
        Args:
            categories: List of categories to query
            
        Returns:
            Set of product IDs in any of the categories
        """
        all_products = set()
        for category in categories:
            all_products.update(self.get_products_in_category(category))
        return all_products
    
    def _find_node(self, word: str) -> Optional[TrieNode]:
        """Helper: Find node for given word"""
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def _collect_categories(self, node: TrieNode, prefix: str, results: List[str]) -> None:
        """Helper: Recursively collect all categories from node"""
        if node.is_end_of_word:
            results.append(node.category_name)
        
        for char, child_node in node.children.items():
            self._collect_categories(child_node, prefix + char, results)
    
    def get_all_categories(self) -> List[str]:
        """Get all categories in trie"""
        return sorted(list(self.all_categories))
    
    def __repr__(self) -> str:
        return f"Trie(categories={len(self.all_categories)})"
