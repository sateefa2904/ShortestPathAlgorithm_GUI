from __future__ import annotations
from typing import Dict, List, Tuple

class MinHeap:
    """
    Binary min-heap for Dijkstra's algorithm.
    Stores (priority, vertex) tuples and supports decrease_key.
    """

    def __init__(self) -> None:
        self.heap: List[Tuple[float, int]] = []
        self.position: Dict[int, int] = {}

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def insert(self, priority: float, vertex: int) -> None:
        if vertex in self.position:
            self.decrease_key(vertex, priority)
            return

        self.heap.append((priority, vertex))
        index = len(self.heap) - 1
        self.position[vertex] = index
        self._bubble_up(index)

    def extract_min(self) -> Tuple[float, int]:
        if self.is_empty():
            raise IndexError("extract_min from empty heap")

        min_item = self.heap[0]
        last_item = self.heap.pop()
        del self.position[min_item[1]]

        if self.heap:
            self.heap[0] = last_item
            self.position[last_item[1]] = 0
            self._bubble_down(0)

        return min_item

    def decrease_key(self, vertex: int, new_priority: float) -> None:
        if vertex not in self.position:
            self.insert(new_priority, vertex)
            return

        index = self.position[vertex]
        current_priority, _ = self.heap[index]

        if new_priority >= current_priority:
            return

        self.heap[index] = (new_priority, vertex)
        self._bubble_up(index)

    def _bubble_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index][0] < self.heap[parent][0]:
                self._swap(index, parent)
                index = parent
            else:
                break

    def _bubble_down(self, index: int) -> None:
        size = len(self.heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest != index:
                self._swap(index, smallest)
                index = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i][1]] = i
        self.position[self.heap[j][1]] = j