"""
Data Models for E-Commerce System
Product, User, and Transaction models
"""

from typing import List, Set, Optional
from dataclasses import dataclass, field
import time


@dataclass
class Product:
    """Product model"""
    id: int
    name: str
    category: str
    price: float
    inventory: int
    description: str = ""
    image_url: str = ""
    views: int = 0
    purchases: int = 0
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'inventory': self.inventory,
            'description': self.description,
            'image_url': self.image_url,
            'views': self.views,
            'purchases': self.purchases
        }


@dataclass
class User:
    """User model"""
    id: str
    name: str
    purchase_history: List[int] = field(default_factory=list)
    viewed_products: List[int] = field(default_factory=list)
    preferred_categories: Set[str] = field(default_factory=set)
    cart_items: List[int] = field(default_factory=list)  # Always starts empty
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'purchase_history': self.purchase_history,
            'viewed_products': self.viewed_products,
            'preferred_categories': list(self.preferred_categories),
            'cart_items': self.cart_items
        }


@dataclass
class Transaction:
    """Transaction model for co-purchase analysis"""
    user_id: str
    product_ids: List[int]
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'user_id': self.user_id,
            'product_ids': self.product_ids,
            'timestamp': self.timestamp
        }
