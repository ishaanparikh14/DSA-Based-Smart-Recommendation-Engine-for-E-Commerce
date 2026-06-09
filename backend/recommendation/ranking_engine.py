"""
Ranking Engine using BST
Multi-criteria filtering and ranking for recommendations
"""

from data_structures.bst import BST
from models import Product, User
from typing import List, Tuple, Dict, Optional


class RankingEngine:
    """
    BST-based ranking engine for multi-criteria product filtering.
    
    Criteria: Price range, inventory availability, popularity
    """
    
    def __init__(self):
        """Initialize ranking engine"""
        self.price_bst = BST()
        self.inventory_bst = BST()
        self.popularity_bst = BST()
        self.product_map: Dict[int, Product] = {}
    
    def build_from_products(self, products: List[Product]) -> None:
        """
        Build BSTs from products.
        
        Args:
            products: List of products
        """
        for product in products:
            self.product_map[product.id] = product
            
            # Insert into price BST
            self.price_bst.insert(product.id, product.price)
            
            # Insert into inventory BST
            self.inventory_bst.insert(product.id, product.inventory)
            
            # Insert into popularity BST (based on purchases + views)
            popularity_score = product.purchases * 2 + product.views
            self.popularity_bst.insert(product.id, popularity_score)
    
    def filter_by_price_range(
        self,
        product_ids: List[int],
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[int]:
        """
        Filter products by price range.
        
        Args:
            product_ids: Candidate product IDs
            min_price: Minimum price (None for no limit)
            max_price: Maximum price (None for no limit)
            
        Returns:
            Filtered product IDs
        """
        if min_price is None and max_price is None:
            return product_ids
        
        # Get products in price range from BST
        min_p = min_price if min_price is not None else 0.0
        max_p = max_price if max_price is not None else float('inf')
        
        products_in_range = set(self.price_bst.range_query(min_p, max_p))
        
        # Filter candidate products
        return [pid for pid in product_ids if pid in products_in_range]
    
    def filter_by_inventory(
        self,
        product_ids: List[int],
        min_inventory: int = 1
    ) -> List[int]:
        """
        Filter products by inventory availability.
        
        Args:
            product_ids: Candidate product IDs
            min_inventory: Minimum inventory required
            
        Returns:
            Filtered product IDs (only in-stock items)
        """
        products_in_stock = set(self.inventory_bst.range_query(min_inventory, float('inf')))
        return [pid for pid in product_ids if pid in products_in_stock]
    
    def rank_by_popularity(
        self,
        product_ids: List[int],
        reverse: bool = True
    ) -> List[Tuple[int, float]]:
        """
        Rank products by popularity score.
        
        Args:
            product_ids: Product IDs to rank
            reverse: If True, rank highest first
            
        Returns:
            List of tuples (product_id, popularity_score)
        """
        ranked = []
        for product_id in product_ids:
            product = self.product_map.get(product_id)
            if product:
                popularity = product.purchases * 2 + product.views
                ranked.append((product_id, popularity))
        
        ranked.sort(key=lambda x: x[1], reverse=reverse)
        return ranked
    
    def calculate_composite_score(
        self,
        product_id: int,
        user: User,
        base_score: float = 0.0,
        weights: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Calculate composite ranking score for a product.
        
        Args:
            product_id: Product to score
            user: User object
            base_score: Base recommendation score
            weights: Weight dictionary for different factors
            
        Returns:
            Composite score
        """
        if weights is None:
            weights = {
                'base': 0.4,
                'popularity': 0.3,
                'inventory': 0.2,
                'price': 0.1
            }
        
        product = self.product_map.get(product_id)
        if not product:
            return 0.0
        
        # Base score (from collaborative filtering, etc.)
        score = base_score * weights.get('base', 0.4)
        
        # Popularity score (normalized)
        popularity = product.purchases * 2 + product.views
        max_popularity = 100  # Assume max for normalization
        popularity_normalized = min(popularity / max_popularity, 1.0)
        score += popularity_normalized * weights.get('popularity', 0.3)
        
        # Inventory score (higher inventory = higher score)
        inventory_normalized = min(product.inventory / 100, 1.0)
        score += inventory_normalized * weights.get('inventory', 0.2)
        
        # Price score (lower price = higher score for budget-conscious)
        # Invert price (cheaper is better)
        max_price = 2000  # Assume max price for normalization
        price_normalized = 1.0 - min(product.price / max_price, 1.0)
        score += price_normalized * weights.get('price', 0.1)
        
        return score
    
    def rank_products(
        self,
        product_scores: List[Tuple[int, float]],
        user: User,
        apply_filters: bool = True
    ) -> List[Tuple[int, float]]:
        """
        Rank products with composite scoring.
        
        Args:
            product_scores: List of (product_id, base_score) tuples
            user: User object
            apply_filters: If True, filter out-of-stock items
            
        Returns:
            Ranked list of (product_id, composite_score) tuples
        """
        ranked = []
        
        for product_id, base_score in product_scores:
            # Filter out-of-stock if requested
            if apply_filters:
                product = self.product_map.get(product_id)
                if not product or product.inventory < 1:
                    continue
            
            # Calculate composite score
            composite_score = self.calculate_composite_score(product_id, user, base_score)
            ranked.append((product_id, composite_score))
        
        # Sort by composite score
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked
    
    def get_stats(self) -> Dict:
        """Get ranking engine statistics"""
        return {
            'total_products': len(self.product_map),
            'price_range': (
                self.price_bst.find_min(),
                self.price_bst.find_max()
            ),
            'inventory_range': (
                self.inventory_bst.find_min(),
                self.inventory_bst.find_max()
            )
        }
    
    def __repr__(self) -> str:
        return f"RankingEngine(products={len(self.product_map)})"
