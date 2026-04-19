from __future__ import annotations


import tkinter as tk
from tkinter import messagebox, ttk
import time
from typing import List

from algorithms import (
    DijkstraNegativeWeightError,
    NegativeCycleError,
    bellman_ford,
    bfs_shortest_path,
    dijkstra,
    reconstruct_path,
)

from benchmark import BenchmarkResult, BenchmarkRunner
from graph import Graph, WeightedGraph
from utils import format_distance, format_path

class GuiBenchmarkRunner(BenchmarkRunner):
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
                    negative_edge_probability=0.0,
                    ensure_connected=ensure_connected,
                )
                edge_count = graph.edge_count()
                source = 0

                start = time.perf_counter()
                dijkstra(graph, source)
                end = time.perf_counter()

                f"Runtime: {runtimes:.4f} ms\n"

                runtimes.append((end - start) * 1000)

            results.append(
                BenchmarkResult(
                    algorithm="Dijkstra",
                    graph_type="Weighted",
                    num_vertices=size,
                    num_edges=edge_count,
                    edge_probability=edge_probability,
                    average_runtime_ms=sum(runtimes) / len(runtimes),
                    successful_trials=self.trials_per_size,
                )
            )

        return results

    def benchmark_bellman_ford(
        self,
        sizes: List[int],
        edge_probability: float,
        directed: bool = False,
        ensure_connected: bool = True,
        min_weight: int = 1,
        max_weight: int = 15,
        allow_negative_edges: bool = False,
        negative_edge_probability: float = 0.15,
        early_stop: bool = True,
    ) -> List[BenchmarkResult]:
        results: List[BenchmarkResult] = []

        for size in sizes:
            runtimes: List[float] = []
            edge_count = 0
            successful_trials = 0
            notes: List[str] = []

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
                    successful_trials += 1
                except NegativeCycleError:
                    notes.append("Negative cycle detected")

            average_runtime_ms = sum(runtimes) / len(runtimes) if runtimes else 0.0
            notes_text = "; ".join(sorted(set(notes)))

            results.append(
                BenchmarkResult(
                    algorithm="Bellman-Ford",
                    graph_type="Weighted",
                    num_vertices=size,
                    num_edges=edge_count,
                    edge_probability=edge_probability,
                    average_runtime_ms=average_runtime_ms,
                    successful_trials=successful_trials,
                    notes=notes_text,
                )
            )

        return results


class ShortestPathApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Project 3 — Shortest Path Algorithm Analyzer")
        self.root.geometry("1120x720")
        self.root.configure(bg="#ffe1eb")

        self.unweighted_graph: Graph | None = None
        self.weighted_graph: WeightedGraph | None = None

        self._configure_styles()
        self._build_layout()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#ffe1eb")
        style.configure("Card.TFrame", background="#ffe1eb")
        style.configure("TLabel", background="#ffe1eb", foreground="#000000", font=("Helvetica", 11))
        style.configure("Title.TLabel", font=("Helvetica", 20, "bold"), foreground="#000000")        
        style.configure("SubTitle.TLabel", font=("Helvetica", 12, "bold"), background="#ffe1eb")
        style.configure("TButton", font=("Helvetica", 11, "bold"), padding=8)
        style.configure("TEntry", padding=5)
        style.configure("TCombobox", padding=4)

    def _build_layout(self) -> None:
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=18, pady=18)

        header = ttk.Label(main_frame, text="Shortest Path Algorithm Analyzer", style="Title.TLabel")
        header.pack(anchor="w", pady=(0, 14))

        content = ttk.Frame(main_frame)
        content.pack(fill="both", expand=True)

        self.left_panel = ttk.Frame(content, style="Card.TFrame")
        self.left_panel.pack(side="left", fill="y", padx=(0, 12), ipadx=12, ipady=12)

        self.right_panel = ttk.Frame(content, style="Card.TFrame")
        self.right_panel.pack(side="right", fill="both", expand=True, ipadx=12, ipady=12)

        self._build_controls()
        self._build_results_area()

    def _build_controls(self) -> None:
        ttk.Label(self.left_panel, text="Controls", style="SubTitle.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12, 10)
        )

        self.algorithm_var = tk.StringVar(value="BFS")
        self.graph_type_var = tk.StringVar(value="Unweighted")
        self.vertices_var = tk.StringVar(value="12")
        self.edge_prob_var = tk.StringVar(value="0.25")
        self.source_var = tk.StringVar(value="0")
        self.target_var = tk.StringVar(value="5")
        self.allow_negative_var = tk.BooleanVar(value=False)

        row = 1
        self._add_label_and_combo("Algorithm", self.algorithm_var, ["BFS", "Dijkstra", "Bellman-Ford"], row)
        row += 1
        self._add_label_and_combo("Graph Type", self.graph_type_var, ["Unweighted", "Weighted"], row)
        row += 1
        self._add_label_and_entry("Vertices", self.vertices_var, row)
        row += 1
        self._add_label_and_entry("Edge Probability", self.edge_prob_var, row)
        row += 1
        self._add_label_and_entry("Source", self.source_var, row)
        row += 1
        self._add_label_and_entry("Target", self.target_var, row)
        row += 1

        negative_check = ttk.Checkbutton(
            self.left_panel,
            text="Allow Negative Weights",
            variable=self.allow_negative_var,
            command=self._sync_graph_type,
        )
        negative_check.grid(row=row, column=0, columnspan=2, sticky="w", padx=12, pady=8)
        row += 1

        ttk.Button(self.left_panel, text="Generate Graph", command=self.generate_graph).grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=12, pady=(10, 6)
        )
        row += 1

        ttk.Button(self.left_panel, text="Run Selected Algorithm", command=self.run_selected_algorithm).grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=12, pady=6
        )
        row += 1

        ttk.Button(self.left_panel, text="Compare Algorithms", command=self.compare_algorithms).grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=12, pady=6
        )
        row += 1

        ttk.Button(self.left_panel, text="Clear Output", command=self.clear_output).grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=12, pady=(6, 12)
        )

    def _build_results_area(self) -> None:
        ttk.Label(self.right_panel, text="Results", style="SubTitle.TLabel").pack(anchor="w", padx=12, pady=(12, 8))

        self.output_text = tk.Text(
            self.right_panel,
            wrap="word",
            bg="#ffe1eb",
            fg="#000000",
            insertbackground="#ffffff",
            font=("Consolas", 11),
            relief="flat",
            padx=12,
            pady=12,
        )
        self.output_text.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    def _add_label_and_entry(self, label_text: str, variable: tk.StringVar, row: int) -> None:
        ttk.Label(self.left_panel, text=label_text).grid(row=row, column=0, sticky="w", padx=12, pady=6)
        entry = ttk.Entry(self.left_panel, textvariable=variable, width=18)
        entry.grid(row=row, column=1, sticky="ew", padx=12, pady=6)

    def _add_label_and_combo(self, label_text: str, variable: tk.StringVar, values: List[str], row: int) -> None:
        ttk.Label(self.left_panel, text=label_text).grid(row=row, column=0, sticky="w", padx=12, pady=6)
        combo = ttk.Combobox(self.left_panel, textvariable=variable, values=values, state="readonly", width=16)
        combo.grid(row=row, column=1, sticky="ew", padx=12, pady=6)

    def _sync_graph_type(self) -> None:
        if self.allow_negative_var.get():
            self.graph_type_var.set("Weighted")

    def generate_graph(self) -> None:
        try:
            num_vertices = int(self.vertices_var.get())
            edge_probability = float(self.edge_prob_var.get())

            if num_vertices <= 1:
                raise ValueError("Vertices must be greater than 1.")
            if not (0 <= edge_probability <= 1):
                raise ValueError("Edge probability must be between 0 and 1.")

            graph_type = self.graph_type_var.get()
            allow_negative = self.allow_negative_var.get()

            if graph_type == "Unweighted":
                self.unweighted_graph = Graph.random_graph(
                    num_vertices=num_vertices,
                    edge_probability=edge_probability,
                    directed=False,
                    ensure_connected=True,
                )
                self.weighted_graph = None
                self._append_output(
                    f"Generated unweighted graph with {num_vertices} vertices and "
                    f"{self.unweighted_graph.edge_count()} edges."
                )
            else:
                self.weighted_graph = WeightedGraph.random_graph(
                    num_vertices=num_vertices,
                    edge_probability=edge_probability,
                    min_weight=1,
                    max_weight=15,
                    directed=False,
                    allow_negative_edges=allow_negative,
                    negative_edge_probability=0.15,
                    ensure_connected=True,
                )
                self.unweighted_graph = None
                self._append_output(
                    f"Generated weighted graph with {num_vertices} vertices and "
                    f"{self.weighted_graph.edge_count()} edges. "
                    f"Negative weights allowed: {allow_negative}."
                )
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))

    def run_selected_algorithm(self) -> None:
        try:
            source = int(self.source_var.get())
            target = int(self.target_var.get())
            algorithm = self.algorithm_var.get()

            if algorithm == "BFS":
                if self.unweighted_graph is None:
                    messagebox.showwarning("Missing Graph", "Please generate an unweighted graph first.")
                    return

                start = time.perf_counter()
                distance, parent = bfs_shortest_path(self.unweighted_graph, source)
                end = time.perf_counter()

                runtime = (end - start) * 1000
                path = reconstruct_path(parent, source, target)
                self._show_algorithm_result("BFS", distance[target], path, runtime)

            elif algorithm == "Dijkstra":
                if self.weighted_graph is None:
                    messagebox.showwarning("Missing Graph", "Please generate a weighted graph first.")
                    return

                start = time.perf_counter()
                distance, parent = dijkstra(self.weighted_graph, source)
                end = time.perf_counter()

                runtime = (end - start) * 1000
                path = reconstruct_path(parent, source, target)
                self._show_algorithm_result("Dijkstra", distance[target], path, runtime)

            elif algorithm == "Bellman-Ford":
                if self.weighted_graph is None:
                    messagebox.showwarning("Missing Graph", "Please generate a weighted graph first.")
                    return

                start = time.perf_counter()
                distance, parent = bellman_ford(self.weighted_graph, source, early_stop=True)
                end = time.perf_counter()

                runtime = (end - start) * 1000
                path = reconstruct_path(parent, source, target)
                self._show_algorithm_result("Bellman-Ford", distance[target], path, runtime)

        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
        except DijkstraNegativeWeightError as exc:
            messagebox.showerror("Dijkstra Error", str(exc))
        except NegativeCycleError as exc:
            messagebox.showerror("Negative Cycle Detected", str(exc))

    def compare_algorithms(self) -> None:
        try:
            num_vertices = int(self.vertices_var.get())
            edge_probability = float(self.edge_prob_var.get())
            allow_negative = self.allow_negative_var.get()

            runner = GuiBenchmarkRunner(trials_per_size=3)
            sizes = [10, 50, 100, 200]
            comparison_lines: List[str] = []

            comparison_lines.append("=== Algorithm Comparison ===")
            comparison_lines.append(
                f"Vertices: {num_vertices} | Edge Probability: {edge_probability} | Negative Weights: {allow_negative}"
            )

            bfs_results = runner.benchmark_bfs(sizes, edge_probability=edge_probability)
            for result in bfs_results:
                comparison_lines.append(
                    f"BFS (n={result.num_vertices}) -> {result.average_runtime_ms:.4f} ms"
                )

            if not allow_negative:
                dijkstra_results = runner.benchmark_dijkstra(sizes, edge_probability=edge_probability)
                for result in dijkstra_results:
                    comparison_lines.append(
                        f"Dijkstra (n={result.num_vertices}) -> {result.average_runtime_ms:.4f} ms"
                    )

            bellman_results = runner.benchmark_bellman_ford(
                sizes,
                edge_probability=edge_probability,
                allow_negative_edges=allow_negative,
                early_stop=True,
            )
            for result in bellman_results:
                extra = f" | {result.notes}" if result.notes else ""
                comparison_lines.append(
                    f"Bellman-Ford (n={result.num_vertices}) -> {result.average_runtime_ms:.4f} ms"
                )

            comparison_lines.append("")
            self._append_output("\n".join(comparison_lines) + "\n" + "-"*50 + "\n")

        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))

    def clear_output(self) -> None:
        self.output_text.delete("1.0", tk.END)

    def _show_algorithm_result(
        self,
        algorithm_name: str,
        distance_value: float,
        path: List[int],
        runtime: float,
        ) -> None:
        self._append_output(
            f"=== {algorithm_name} Result ===\n"
            f"Distance: {format_distance(distance_value)}\n"
            f"Path: {format_path(path)}\n"
            f"Runtime: {runtime:.4f} ms\n"
        )

    def _append_output(self, text: str) -> None:
        self.output_text.insert(tk.END, text + ("" if text.endswith("\n") else "\n"))
        self.output_text.see(tk.END)


def main() -> None:
    root = tk.Tk()
    app = ShortestPathApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()



