from __future__ import annotations

from collections import deque
from math import inf
from typing import Dict, List, Optional, Tuple

from graph import Graph, WeightedGraph
from heap import MinHeap

class NegativeCycleError(Exception):
    """Raised when negative cycle is detected by Bellman Ford algorithm"""

class DijkstraNegativeWeightError(Exception):
    """Raised when Dijkstra is run on a graph with negative weights."""

def reconstruct_path(parent: List[Optional[int]], source: int, target: int) -> List[int]:
    if source == target:
        return [source]
    if target < 0 or target >= len(parent):
        return[]
    
    path: List[int] = []
    current: Optional[int] = target

    while current is not None:
        path.append(current)
        if current == source:
            break
        current = parent[current]

    if not path or path[-1] != source:
        return[]

    path.reverse()
    return path

def bfs_shortest_path(graph: Graph, source: int) -> Tuple[List[float], List[Optional[int]]]:
    if source < 0 or source >= graph.num_vertices:
        raise ValueError("Invalid source vertex.")

    distance = [inf] * graph.num_vertices
    parent: List[Optional[int]] = [None] * graph.num_vertices

    queue = deque([source])
    distance[source] = 0

    while queue:
        u = queue.popleft()
        for v in graph.neighbors(u):
            if distance[v] == inf:
                distance[v] = distance[u] + 1
                parent[v] = u
                queue.append(v)
    return distance, parent

def dijkstra(graph: WeightedGraph, source: int) -> Tuple[List[float], List[Optional[int]]]:
    if source < 0 or source >= graph.num_vertices: # type: ignore
        raise ValueError("Invalid source vertex.")
    if graph.has_negative_weight():
        raise DijkstraNegativeWeightError(
            "Dijkstra's algorithm cannot be used safely with negative edge weights."
        )

    distance = [inf] * graph.num_vertices # pyright: ignore[reportAttributeAccessIssue]
    parent: List[Optional[int]] = [None] * graph.num_vertices # pyright: ignore[reportAttributeAccessIssue]
    visited = [False] * graph.num_vertices # pyright: ignore[reportAttributeAccessIssue]

    distance[source] = 0
    heap = MinHeap()
    heap.insert(0, source)

    while not heap.is_empty():
        current_distance, u = heap.extract_min()

        if visited[u]:
            continue
        visited[u] = True

        for v, weight in graph.neighbors(u):
            if visited[v]:
                continue

            new_distance = current_distance + weight
            if new_distance < distance[v]:
                distance[v] = new_distance
                parent[v] = u
                heap.decrease_key(v, new_distance)

    return distance, parent

def bellman_ford(
    graph: WeightedGraph,
    source: int,
    early_stop: bool = True,
) -> Tuple[List[float], List[Optional[int]]]:
    if source < 0 or source >= graph.num_vertices: # type: ignore
        raise ValueError("Invalid source vertex.")

    distance = [inf] * graph.num_vertices # type: ignore
    parent: List[Optional[int]] = [None] * graph.num_vertices # pyright: ignore[reportAttributeAccessIssue]
    distance[source] = 0

    edges = []
    for u in range(graph.num_vertices): # type: ignore
        for v, w in graph.neighbors(u):
            edges.append((u, v, w))

    for i in range(graph.num_vertices - 1): # pyright: ignore[reportAttributeAccessIssue]
        updated = False
        for u, v, w in edges:
            if distance[u] != inf and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                parent[v] = u
                updated = True

        if early_stop and not updated:
            break

    for u, v, w in edges:
        if distance[u] != inf and distance[u] + w < distance[v]:
            raise NegativeCycleError(
                "Graph contains a negative-weight cycle reachable from the source."
            )

    return distance, parent
