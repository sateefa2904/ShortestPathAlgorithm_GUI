from __future__ import annotations

from math import inf
from typing import List



def format_distance(value: float) -> str:
    return "INF" if value == inf else f"{value:.2f}"



def format_path(path: List[int]) -> str:
    if not path:
        return "No path exists."
    return " -> ".join(str(node) for node in path)