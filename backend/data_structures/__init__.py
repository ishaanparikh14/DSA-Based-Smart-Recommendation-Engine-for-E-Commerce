"""
Data Structures Package
8 core DSA implementations for e-commerce recommendation engine
"""

from .hash_map import HashMap
from .stack import Stack
from .queue import Queue
from .linked_list import DoublyLinkedList, LinkedListNode
from .trie import Trie
from .bst import BST
from .heap import MinHeap, MaxHeap, top_k_selection
from .graph import Graph

__all__ = [
    'HashMap',
    'Stack',
    'Queue',
    'DoublyLinkedList',
    'LinkedListNode',
    'Trie',
    'BST',
    'MinHeap',
    'MaxHeap',
    'top_k_selection',
    'Graph'
]
