"""
Shopping Cart Implementation using Doubly Linked List
Provides O(1) insertion and deletion operations
"""

import time
from typing import List, Tuple, Optional


class CartNode:
    """Node in the shopping cart (doubly linked list)"""
    
    def __init__(self, product_id: int, quantity: int, price: float):
        """
        Initialize a cart node.
        
        Args:
            product_id: Unique identifier for the product
            quantity: Number of units
            price: Price per unit
        """
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.prev: Optional['CartNode'] = None
        self.next: Optional['CartNode'] = None
        self.timestamp = time.time()

    def get_subtotal(self) -> float:
        """Calculate subtotal for this item"""
        return self.quantity * self.price

    def __repr__(self) -> str:
        return f"CartNode(product_id={self.product_id}, quantity={self.quantity}, price={self.price})"


class ShoppingCart:
    """
    Shopping Cart using Doubly Linked List
    Time Complexity: O(1) for insertions/deletions with hash map lookup
    Space Complexity: O(n) where n is number of items
    """
    
    def __init__(self, user_id: int):
        """
        Initialize shopping cart for a user.
        
        Args:
            user_id: Unique identifier for the user
        """
        self.user_id = user_id
        self.head: Optional[CartNode] = None
        self.tail: Optional[CartNode] = None
        self.size = 0
        self.product_map = {}  # O(1) lookup: product_id -> node

    def add_item(self, product_id: int, quantity: int, price: float) -> None:
        """
        Add item to cart - O(1) operation.
        
        Args:
            product_id: Product to add
            quantity: Number of units
            price: Price per unit
        """
        if product_id in self.product_map:
            # Update existing item
            node = self.product_map[product_id]
            node.quantity += quantity
            node.timestamp = time.time()
            return

        # Create new node
        new_node = CartNode(product_id, quantity, price)

        if not self.head:
            # First item in cart
            self.head = self.tail = new_node
        else:
            # Append to end
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.product_map[product_id] = new_node
        self.size += 1

    def remove_item(self, product_id: int) -> bool:
        """
        Remove item from cart - O(1) operation.
        
        Args:
            product_id: Product to remove
            
        Returns:
            True if item was removed, False if not found
        """
        if product_id not in self.product_map:
            return False

        node = self.product_map[product_id]

        # Update links
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        del self.product_map[product_id]
        self.size -= 1
        return True

    def update_quantity(self, product_id: int, quantity: int) -> bool:
        """
        Update quantity of an item in cart.
        
        Args:
            product_id: Product to update
            quantity: New quantity (if 0 or negative, item is removed)
            
        Returns:
            True if updated, False if not found
        """
        if product_id not in self.product_map:
            return False

        if quantity <= 0:
            return self.remove_item(product_id)

        node = self.product_map[product_id]
        node.quantity = quantity
        node.timestamp = time.time()
        return True

    def get_item(self, product_id: int) -> Optional[CartNode]:
        """
        Get specific item from cart - O(1).
        
        Args:
            product_id: Product to retrieve
            
        Returns:
            CartNode if found, None otherwise
        """
        return self.product_map.get(product_id)

    def get_total(self) -> float:
        """
        Calculate cart total.
        Time Complexity: O(n)
        
        Returns:
            Total price of all items
        """
        total = 0.0
        current = self.head
        while current:
            total += current.get_subtotal()
            current = current.next
        return total

    def get_items(self) -> List[Tuple[int, int, float]]:
        """
        Get all cart items as list.
        Time Complexity: O(n)
        
        Returns:
            List of tuples (product_id, quantity, price)
        """
        items = []
        current = self.head
        while current:
            items.append((current.product_id, current.quantity, current.price))
            current = current.next
        return items

    def clear(self) -> None:
        """Clear all items from cart"""
        self.head = None
        self.tail = None
        self.product_map.clear()
        self.size = 0

    def is_empty(self) -> bool:
        """Check if cart is empty"""
        return self.size == 0

    def __len__(self) -> int:
        """Return number of items in cart"""
        return self.size

    def __repr__(self) -> str:
        return f"ShoppingCart(user_id={self.user_id}, items={self.size}, total={self.get_total():.2f})"
