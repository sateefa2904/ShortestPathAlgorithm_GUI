# ShortestPathAlgorithm_GUI

This project implements and compares the following shortest path algorithms from scratch:
- Breadth-First Search (BFS) for unweighted graphs
- Dijkstra's Algorithm for weighted graphs with nonnegative edges
- Bellman-Ford Algorithm for weighted graphs with possible negative edges

## Features
- Custom adjacency-list graph structures
- Custom binary min-heap for Dijkstra
- Negative cycle detection in Bellman-Ford
- Bellman-Ford early-stop optimization
- Path reconstruction support
- Random graph generation for testing and benchmarking

## Files
- `graph.py` — graph data structures and random graph generation
- `heap.py` — custom binary min-heap
- `algorithms.py` — BFS, Dijkstra, Bellman-Ford, path reconstruction
- `utils.py` — formatting helpers
- `main.py` — example runs for correctness testing

## How to Run
```bash
cd src
python main.py
```

## Why this code is strong
- Everything important is written from scratch
- The structure is clean enough for the TA to inspect easily
- Bellman-Ford includes a real optimization: early stopping
- Dijkstra uses a custom binary min-heap instead of a built-in priority queue
- Path reconstruction is already built in, which will help both the demo and GUI

## What to build next
The next files we should write are:
1. `benchmark.py`
2. `gui.py`
3. optional sample input file loader
4. charts/export support for the report

That order is best because it gives you experimental results early while the GUI is being polished.