"""
Category Filter using Trie
CRITICAL: Ensures recommendations match user's preferred categories
Prevents irrelevant suggestions (e.g., beauty cream for Python course)
"""

from data_structures.trie import Trie
from models import Product, User
from typing import List, Set, Dict


class CategoryFilter:
    """
    Category-based filtering using Trie data structure.
    
    This is the FIRST filter in the recommendation pipeline to ensure relevance.
    """
    
    def __init__(self):
        """Initialize category filter with Trie"""
        self.trie = Trie()
        self.category_products: Dict[str, Set[int]] = {}
    
    def build_from_products(self, products: List[Product]) -> None:
        """
        Build category index from products.
        
        Args:
            products: List of products
        """
        for product in products:
            category = product.category
            
            # Insert category into trie with product ID
            self.trie.insert(category, product.id)
            
            # Track products by category
            if category not in self.category_products:
                self.category_products[category] = set()
            self.category_products[category].add(product.id)
    
    def get_products_in_category(self, category: str) -> Set[int]:
        """
        Get all products in a specific category.
        
        Args:
            category: Category name
            
        Returns:
            Set of product IDs in category
        """
        return self.trie.get_products_in_category(category)
    
    def get_products_in_user_categories(self, user: User) -> Set[int]:
        """
        Get all products in user's preferred categories.
        
        Args:
            user: User object
            
        Returns:
            Set of product IDs in user's preferred categories
        """
        if not user.preferred_categories:
            # If user has no preferences, return all products
            all_products = set()
            for products in self.category_products.values():
                all_products.update(products)
            return all_products
        
        # Get products from user's preferred categories
        return self.trie.get_products_in_categories(list(user.preferred_categories))
    
    def filter_by_user_categories(
        self,
        product_ids: List[int],
        user: User,
        allow_exploration: bool = True,
        exploration_ratio: float = 0.2
    ) -> List[int]:
        """
        Filter product list to match user's preferred categories.
        
        Args:
            product_ids: List of candidate product IDs
            user: User object
            allow_exploration: If True, allow some products from other categories
            exploration_ratio: Ratio of non-preferred category products to include
            
        Returns:
            Filtered list of product IDs
        """
        if not user.preferred_categories:
            return product_ids
        
        # Get products in user's preferred categories
        preferred_products = self.get_products_in_user_categories(user)
        
        # Separate into preferred and non-preferred
        in_category = []
        out_of_category = []
        
        for product_id in product_ids:
            if product_id in preferred_products:
                in_category.append(product_id)
            else:
                out_of_category.append(product_id)
        
        # If exploration is allowed, include some non-preferred products
        if allow_exploration and out_of_category:
            num_exploration = int(len(in_category) * exploration_ratio)
            exploration_products = out_of_category[:num_exploration]
            return in_category + exploration_products
        
        return in_category
    
    def get_category_match_score(self, product_id: int, user: User, product_map: Dict[int, Product]) -> float:
        """
        Calculate how well a product matches user's category preferences.
        
        Args:
            product_id: Product to score
            user: User object
            product_map: Mapping of product ID to Product object
            
        Returns:
            Match score (1.0 = perfect match, 0.0 = no match)
        """
        product = product_map.get(product_id)
        if not product:
            return 0.0
        
        if not user.preferred_categories:
            return 0.5  # Neutral score if no preferences
        
        # Check if product's category is in user's preferences
        if product.category in user.preferred_categories:
            # Higher score if category appears more in user's history
            category_frequency = sum(
                1 for pid in user.purchase_history
                if product_map.get(pid) and product_map[pid].category == product.category
            )
            # Normalize by total purchase history
            if user.purchase_history:
                return 0.5 + (0.5 * category_frequency / len(user.purchase_history))
            return 1.0
        
        return 0.0  # Product not in preferred categories
    
    def get_all_categories(self) -> List[str]:
        """Get all categories in the system"""
        return self.trie.get_all_categories()
    
    def search_categories(self, prefix: str) -> List[str]:
        """
        Search for categories by prefix.
        
        Args:
            prefix: Category prefix to search
            
        Returns:
            List of matching categories
        """
        return self.trie.starts_with(prefix)
    
    def get_stats(self) -> Dict:
        """Get category filter statistics"""
        return {
            'total_categories': len(self.category_products),
            'total_products': sum(len(products) for products in self.category_products.values()),
            'categories': list(self.category_products.keys())
        }
    
    def __repr__(self) -> str:
        return f"CategoryFilter(categories={len(self.category_products)})"
