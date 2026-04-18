from __future__ import annotations

from algorithms import (
    NegativeCycleError,
    DijkstraNegativeWeightError,
    bellman_ford,
    bfs_shortest_path,
    dijkstra,
    reconstruct_path,
)
from graph import Graph, WeightedGraph
from utils import format_distance, format_path



def demo_bfs() -> None:
    print("\n=== BFS Demo (Unweighted Graph) ===")
    graph = Graph(6, directed=False)
    edges = [(0, 1), (0, 2), (1, 3), (2, 4), (4, 5), (3, 5)]
    for u, v in edges:
        graph.add_edge(u, v)

    source, target = 0, 5
    distance, parent = bfs_shortest_path(graph, source)
    path = reconstruct_path(parent, source, target)

    print(f"Source: {source}, Target: {target}")
    print(f"Distance: {format_distance(distance[target])}")
    print(f"Path: {format_path(path)}")



def demo_dijkstra() -> None:
    print("\n=== Dijkstra Demo (Weighted Positive Graph) ===")
    graph = WeightedGraph(5, directed=False)
    edges = [
        (0, 1, 4),
        (0, 2, 1),
        (2, 1, 2),
        (1, 3, 1),
        (2, 3, 5),
        (3, 4, 3),
    ]
    for u, v, w in edges:
        graph.add_edge(u, v, w)

    source, target = 0, 4
    distance, parent = dijkstra(graph, source)
    path = reconstruct_path(parent, source, target)

    print(f"Source: {source}, Target: {target}")
    print(f"Distance: {format_distance(distance[target])}")
    print(f"Path: {format_path(path)}")



def demo_bellman_ford() -> None:
    print("\n=== Bellman-Ford Demo (Negative Edge, No Negative Cycle) ===")
    graph = WeightedGraph(5, directed=True)
    edges = [
        (0, 1, 6),
        (0, 2, 7),
        (1, 3, 5),
        (1, 2, 8),
        (1, 4, -4),
        (2, 3, -3),
        (2, 4, 9),
        (3, 1, -2),
        (4, 3, 7),
    ]
    for u, v, w in edges:
        graph.add_edge(u, v, w)

    source, target = 0, 4

    try:
        distance, parent = bellman_ford(graph, source, early_stop=True)
        path = reconstruct_path(parent, source, target)
        print(f"Source: {source}, Target: {target}")
        print(f"Distance: {format_distance(distance[target])}")
        print(f"Path: {format_path(path)}")
    except NegativeCycleError as exc:
        print(str(exc))



def demo_negative_cycle() -> None:
    print("\n=== Bellman-Ford Demo (Negative Cycle Detection) ===")
    graph = WeightedGraph(4, directed=True)
    edges = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 3, -1),
        (3, 1, -1),
    ]
    for u, v, w in edges:
        graph.add_edge(u, v, w)

    try:
        bellman_ford(graph, 0)
        print("No negative cycle detected.")
    except NegativeCycleError as exc:
        print(str(exc))



def main() -> None:
    demo_bfs()
    demo_dijkstra()
    demo_bellman_ford()
    demo_negative_cycle()

    print("\nProject 3 core shortest path algorithms are working.")
    print("Next steps: benchmarking engine + GUI.")


if __name__ == "__main__":
    main()