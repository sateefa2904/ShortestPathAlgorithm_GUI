from __future__ import annotations
import random
from typing import List, Tuple, Optional

class Graph:
    """
    Unweighted graph using an adjancency list.
    Supports directed or undirected graphs.
    """

    def __init__(self, num_vertices: int, directed: bool = False) -> None:
        if num_vertices <= 0:
            raise ValueError("Number of vertices must be positive.")
        
        self.num_vertices = num_vertices
        self.directed = directed
        self.adj_list: List[List[int]] = [[] for i in range(num_vertices)]

    def add_edge(self, u: int, v: int) -> None:
        self._validate_vertex(u)
        self._validate_vertex(v)

        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
        if not self.directed and u not in self.adj_list[v]:
            self.adj_list[v].append(u)
    def neighbors(self, u: int) -> List[int]:
        self._validate_vertex(u)
        return self.adj_list[u]
    def edge_count(self) -> int:
        total = sum(len(neighbors) for neighbors in self.adj_list)
        return total if self.directed else total//2
    def _validate_vertex(self, vertex: int) -> None:
        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Vertex {vertex} is out of range.")
        
    @staticmethod
    def random_graph(
        num_vertices: int,
        edge_probability: float,
        directed: bool = False,
        ensure_connected: bool = False,
    ) -> "Graph":
        if not (0 <= edge_probability <= 1):
            raise ValueError("edge_probability must be between 0 and 1.")

        graph = Graph(num_vertices, directed=directed)

        if ensure_connected and num_vertices > 1:
            for i in range(num_vertices - 1):
                graph.add_edge(i, i + 1)

        for u in range(num_vertices):
            start_v = 0 if directed else u + 1
            for v in range(start_v, num_vertices):
                if u == v:
                    continue
                if random.random() < edge_probability:
                    graph.add_edge(u, v)

        return graph

class WeightedGraph:
    """
    Weighted graph using adjacency list.
    Each adjacency list entry is a tuple (neighbor, weight).
    """
    def __init__(self, num_vertices: int, directed: bool = False) -> None:
        if num_vertices <= 0:
            raise ValueError("Number of vertices must be positive.")

        self.num_vertices = num_vertices
        self.directed = directed
        self.adj_list: List[List[Tuple[int, float]]] = [[] for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int, weight: float) -> None:
        self._validate_vertex(u)
        self._validate_vertex(v)

        if u == v:
            return

        if not self._edge_exists(u, v):
            self.adj_list[u].append((v, weight))

        if not self.directed and not self._edge_exists(v, u):
            self.adj_list[v].append((u, weight))

    def neighbors(self, u: int) -> List[Tuple[int, float]]:
        self._validate_vertex(u)
        return self.adj_list[u]

    def edges(self) -> List[Tuple[int, int, float]]:
        result: List[Tuple[int, int, float]] = []
        for u in range(self.num_vertices):
            for v, w in self.adj_list[u]:
                if self.directed or u < v:
                    result.append((u, v, w))
        return result

    def edge_count(self) -> int:
        return len(self.edges())

    def has_negative_weight(self) -> bool:
        for u in range(self.num_vertices):
            for _, w in self.adj_list[u]:
                if w < 0:
                    return True
        return False

    def _edge_exists(self, u: int, v: int) -> bool:
        return any(neighbor == v for neighbor, _ in self.adj_list[u])

    def _validate_vertex(self, vertex: int) -> None:
        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Vertex {vertex} is out of range.")

    @staticmethod
    def random_graph(
        num_vertices: int,
        edge_probability: float,
        min_weight: int = 1,
        max_weight: int = 20,
        directed: bool = False,
        allow_negative_edges: bool = False,
        negative_edge_probability: float = 0.1,
        ensure_connected: bool = False,
    ) -> "WeightedGraph":
        if not (0 <= edge_probability <= 1):
            raise ValueError("edge_probability must be between 0 and 1.")
        if min_weight > max_weight:
            raise ValueError("min_weight cannot be greater than max_weight.")

        graph = WeightedGraph(num_vertices, directed=directed)

        def random_weight() -> int:
            weight = random.randint(min_weight, max_weight)
            if allow_negative_edges and random.random() < negative_edge_probability:
                weight *= -1
            return weight

        if ensure_connected and num_vertices > 1:
            for i in range(num_vertices - 1):
                graph.add_edge(i, i + 1, random_weight())

        for u in range(num_vertices):
            start_v = 0 if directed else u + 1
            for v in range(start_v, num_vertices):
                if u == v:
                    continue
                if random.random() < edge_probability:
                    graph.add_edge(u, v, random_weight())

        return graph