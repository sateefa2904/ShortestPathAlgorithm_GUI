from __future__ import annotations

import csv
import os
import time
from dataclasses import dataclass
from typing import List

from algorithms import NegativeCycleError, bellman_ford, bfs_shortest_path, dijkstra
from graph import Graph, WeightedGraph


@dataclass
class BenchmarkResult:
    algorithm: str
    graph_type: str
    num_vertices: int
    num_edges: int
    edge_probability: float
    average_runtime_ms: float
    successful_trials: int
    notes: str = ""


class BenchmarkRunner:
    """
    Runs controlled timing experiments for BFS, Dijkstra, and Bellman-Ford.
    """

    def __init__(self, trials_per_size: int = 5) -> None:
        if trials_per_size <= 0:
            raise ValueError("trials_per_size must be positive.")
        self.trials_per_size = trials_per_size

    def benchmark_bfs(
        self,
        sizes: List[int],
        edge_probability: float,
        directed: bool = False,
        ensure_connected: bool = True,
    ) -> List[BenchmarkResult]:
        results: List[BenchmarkResult] = []

        for size in sizes:
            runtimes: List[float] = []
            edge_count = 0

            for _ in range(self.trials_per_size):
                graph = Graph.random_graph(
                    num_vertices=size,
                    edge_probability=edge_probability,
                    directed=directed,
                    ensure_connected=ensure_connected,
                )
                edge_count = graph.edge_count()
                source = 0

                start = time.perf_counter()
                bfs_shortest_path(graph, source)
                end = time.perf_counter()

                runtimes.append((end - start) * 1000)

            average_runtime = sum(runtimes) / len(runtimes)

            results.append(
                BenchmarkResult(
                    algorithm="BFS",
                    graph_type="Unweighted",
                    num_vertices=size,
                    num_edges=edge_count,
                    edge_probability=edge_probability,
                    average_runtime_ms=average_runtime,
                    successful_trials=len(runtimes),
                )
            )

        return results

    def benchmark_dijkstra(
        self,
        sizes: List[int],
        edge_probability: float,
        directed: bool = False,
        ensure_connected: bool = True,
        min_weight: int = 1,
        max_weight: int = 20,
    ) -> List[BenchmarkResult]:
        results: List[BenchmarkResult] = []

        for size in sizes:
            runtimes: List[float] = []
            edge_count = 0

            for _ in range(self.trials_per_size):
                graph = WeightedGraph.random_graph(
                    num_vertices=size,
                    edge_probability=edge_probability,
                    min_weight=min_weight,
                    max_weight=max_weight,
                    directed=directed,
                    allow_negative_edges=False,
                    ensure_connected=ensure_connected,
                )
                edge_count = graph.edge_count()
                source = 0

                start = time.perf_counter()
                dijkstra(graph, source)
                end = time.perf_counter()

                runtimes.append((end - start) * 1000)

            average_runtime = sum(runtimes) / len(runtimes)

            results.append(
                BenchmarkResult(
                    algorithm="Dijkstra",
                    graph_type="Weighted (Nonnegative)",
                    num_vertices=size,
                    num_edges=edge_count,
                    edge_probability=edge_probability,
                    average_runtime_ms=average_runtime,
                    successful_trials=len(runtimes),
                )
            )

        return results

    def benchmark_bellman_ford(
        self,
        sizes: List[int],
        edge_probability: float,
        directed: bool = True,
        ensure_connected: bool = True,
        min_weight: int = 1,
        max_weight: int = 20,
        allow_negative_edges: bool = False,
        negative_edge_probability: float = 0.1,
        early_stop: bool = True,
    ) -> List[BenchmarkResult]:
        results: List[BenchmarkResult] = []

        for size in sizes:
            runtimes: List[float] = []
            edge_count = 0
            skipped_trials = 0

            for _ in range(self.trials_per_size):
                graph = WeightedGraph.random_graph(
                    num_vertices=size,
                    edge_probability=edge_probability,
                    min_weight=min_weight,
                    max_weight=max_weight,
                    directed=directed,
                    allow_negative_edges=allow_negative_edges,
                    negative_edge_probability=negative_edge_probability,
                    ensure_connected=ensure_connected,
                )
                edge_count = graph.edge_count()
                source = 0

                try:
                    start = time.perf_counter()
                    bellman_ford(graph, source, early_stop=early_stop)
                    end = time.perf_counter()

                    runtimes.append((end - start) * 1000)

                except NegativeCycleError:
                    skipped_trials += 1

            average_runtime = sum(runtimes) / len(runtimes) if runtimes else 0.0

            notes = ""
            if skipped_trials > 0:
                notes = f"{skipped_trials} trial(s) skipped due to negative cycle detection."

            graph_type = (
                "Weighted (Negative Edges Allowed)"
                if allow_negative_edges
                else "Weighted (General)"
            )

            results.append(
                BenchmarkResult(
                    algorithm="Bellman-Ford",
                    graph_type=graph_type,
                    num_vertices=size,
                    num_edges=edge_count,
                    edge_probability=edge_probability,
                    average_runtime_ms=average_runtime,
                    successful_trials=len(runtimes),
                    notes=notes,
                )
            )

        return results

    def save_results_to_csv(self, results: List[BenchmarkResult], output_path: str) -> None:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    "algorithm",
                    "graph_type",
                    "num_vertices",
                    "num_edges",
                    "edge_probability",
                    "average_runtime_ms",
                    "successful_trials",
                    "notes",
                ]
            )

            for result in results:
                writer.writerow(
                    [
                        result.algorithm,
                        result.graph_type,
                        result.num_vertices,
                        result.num_edges,
                        result.edge_probability,
                        f"{result.average_runtime_ms:.6f}",
                        result.successful_trials,
                        result.notes,
                    ]
                )


def run_default_benchmarks() -> List[BenchmarkResult]:
    runner = BenchmarkRunner(trials_per_size=5)
    sizes = [50, 100, 250, 500, 1000]
    edge_probability = 0.1

    results: List[BenchmarkResult] = []

    results.extend(
        runner.benchmark_bfs(
            sizes=sizes,
            edge_probability=edge_probability,
            directed=False,
            ensure_connected=True,
        )
    )

    results.extend(
        runner.benchmark_dijkstra(
            sizes=sizes,
            edge_probability=edge_probability,
            directed=False,
            ensure_connected=True,
            min_weight=1,
            max_weight=20,
        )
    )

    results.extend(
        runner.benchmark_bellman_ford(
            sizes=sizes,
            edge_probability=edge_probability,
            directed=True,
            ensure_connected=True,
            min_weight=1,
            max_weight=20,
            allow_negative_edges=False,
            early_stop=True,
        )
    )

    return results


def print_results(results: List[BenchmarkResult]) -> None:
    print("\n=== Benchmark Results ===")
    for result in results:
        print(
            f"{result.algorithm:14} | "
            f"{result.graph_type:28} | "
            f"V={result.num_vertices:4} | "
            f"E={result.num_edges:6} | "
            f"Avg={result.average_runtime_ms:10.4f} ms | "
            f"Trials={result.successful_trials}"
        )
        if result.notes:
            print(f"  Notes: {result.notes}")


def main() -> None:
    results = run_default_benchmarks()

    runner = BenchmarkRunner()
    output_path = "../data/benchmark_results.csv"
    runner.save_results_to_csv(results, output_path)

    print_results(results)
    print(f"\nBenchmarking complete. Results saved to {output_path}")


if __name__ == "__main__":
    main()