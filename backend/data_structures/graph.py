"""
Graph Implementation for Co-occurrence Analysis
Weighted graph for product relationships and collaborative filtering
"""

from collections import defaultdict
from typing import Dict, List, Tuple, Set, Optional


class Graph:
    """
    Weighted Undirected Graph for product co-occurrence.
    
    Time Complexity:
        - Add edge: O(1)
        - Get neighbors: O(1)
        - BFS/DFS: O(V + E)
    
    Space Complexity: O(V + E) where V = vertices, E = edges
    
    Use Case: Co-purchase analysis, product relationships
    """
    
    def __init__(self, directed: bool = False):
        """
        Initialize graph.
        
        Args:
            directed: If True, create directed graph; else undirected
        """
        self.graph: Dict[int, Dict[int, float]] = defaultdict(lambda: defaultdict(float))
        self.directed = directed
        self.vertices: Set[int] = set()
        self.edge_count = 0
    
    def add_vertex(self, vertex: int) -> None:
        """
        Add vertex to graph.
        Time Complexity: O(1)
        
        Args:
            vertex: Vertex (product ID) to add
        """
        self.vertices.add(vertex)
        if vertex not in self.graph:
            self.graph[vertex] = defaultdict(float)
    
    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """
        Add weighted edge between vertices.
        Time Complexity: O(1)
        
        Args:
            u: First vertex (product ID)
            v: Second vertex (product ID)
            weight: Edge weight (co-occurrence frequency)
        """
        self.vertices.add(u)
        self.vertices.add(v)
        
        # Add edge u -> v
        self.graph[u][v] += weight
        
        # If undirected, add edge v -> u
        if not self.directed:
            self.graph[v][u] += weight
        
        self.edge_count += 1
    
    def get_neighbors(self, vertex: int) -> Dict[int, float]:
        """
        Get all neighbors of a vertex with edge weights.
        Time Complexity: O(1)
        
        Args:
            vertex: Vertex to query
            
        Returns:
            Dictionary mapping neighbor -> edge weight
        """
        return dict(self.graph[vertex])
    
    def get_edge_weight(self, u: int, v: int) -> float:
        """
        Get weight of edge between two vertices.
        
        Args:
            u: First vertex
            v: Second vertex
            
        Returns:
            Edge weight, or 0 if edge doesn't exist
        """
        return self.graph[u].get(v, 0.0)
    
    def has_edge(self, u: int, v: int) -> bool:
        """Check if edge exists between vertices"""
        return v in self.graph[u]
    
    def get_degree(self, vertex: int) -> int:
        """Get degree (number of neighbors) of vertex"""
        return len(self.graph[vertex])
    
    def get_all_edges(self) -> List[Tuple[int, int, float]]:
        """
        Get all edges in graph.
        
        Returns:
            List of tuples (u, v, weight)
        """
        edges = []
        seen = set()
        
        for u in self.graph:
            for v, weight in self.graph[u].items():
                if self.directed or (u, v) not in seen:
                    edges.append((u, v, weight))
                    if not self.directed:
                        seen.add((u, v))
                        seen.add((v, u))
        
        return edges
    
    def bfs(self, start: int, max_depth: Optional[int] = None) -> List[int]:
        """
        Breadth-First Search from start vertex.
        Time Complexity: O(V + E)
        
        Args:
            start: Starting vertex
            max_depth: Maximum depth to traverse (None for unlimited)
            
        Returns:
            List of vertices in BFS order
        """
        if start not in self.vertices:
            return []
        
        visited = set()
        queue = [(start, 0)]  # (vertex, depth)
        result = []
        
        while queue:
            vertex, depth = queue.pop(0)
            
            if vertex in visited:
                continue
            
            if max_depth is not None and depth > max_depth:
                continue
            
            visited.add(vertex)
            result.append(vertex)
            
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        
        return result
    
    def get_top_neighbors(self, vertex: int, k: int = 5) -> List[Tuple[int, float]]:
        """
        Get top-k neighbors by edge weight.
        
        Args:
            vertex: Vertex to query
            k: Number of top neighbors to return
            
        Returns:
            List of tuples (neighbor, weight) sorted by weight descending
        """
        neighbors = self.get_neighbors(vertex)
        sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[1], reverse=True)
        return sorted_neighbors[:k]
    
    def jaccard_similarity(self, u: int, v: int) -> float:
        """
        Calculate Jaccard similarity between two vertices.
        Similarity = |neighbors(u) ∩ neighbors(v)| / |neighbors(u) ∪ neighbors(v)|
        
        Args:
            u: First vertex
            v: Second vertex
            
        Returns:
            Jaccard similarity score (0-1)
        """
        neighbors_u = set(self.graph[u].keys())
        neighbors_v = set(self.graph[v].keys())
        
        if not neighbors_u and not neighbors_v:
            return 0.0
        
        intersection = len(neighbors_u & neighbors_v)
        union = len(neighbors_u | neighbors_v)
        
        return intersection / union if union > 0 else 0.0
    
    def get_stats(self) -> Dict:
        """
        Get graph statistics.
        
        Returns:
            Dictionary with graph metrics
        """
        total_edges = len(self.get_all_edges())
        avg_degree = sum(self.get_degree(v) for v in self.vertices) / len(self.vertices) if self.vertices else 0
        
        return {
            'vertices': len(self.vertices),
            'edges': total_edges,
            'avg_degree': avg_degree,
            'directed': self.directed
        }
    
    def clear(self) -> None:
        """Clear all vertices and edges"""
        self.graph.clear()
        self.vertices.clear()
        self.edge_count = 0
    
    def __len__(self) -> int:
        """Return number of vertices"""
        return len(self.vertices)
    
    def __repr__(self) -> str:
        return f"Graph(vertices={len(self.vertices)}, edges={len(self.get_all_edges())}, directed={self.directed})"
