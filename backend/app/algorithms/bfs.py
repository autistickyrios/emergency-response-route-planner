from collections import deque
from typing import Dict, List, Optional

from .graph import Graph


def bfs(graph: Graph, start: str, goal: str) -> Optional[List[str]]:
    """
    Breadth-First Search.

    Finds a path with the minimum number of edges.
    Road weights are intentionally ignored.
    """

    if start not in graph.nodes:
        raise ValueError(f"Unknown start node: {start}")

    if goal not in graph.nodes:
        raise ValueError(f"Unknown goal node: {goal}")

    queue = deque([start])
    visited = {start}
    parent: Dict[str, Optional[str]] = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            return _reconstruct_path(parent, goal)

        for edge in graph.get_neighbors(current):
            if edge.blocked:
                continue

            neighbor = edge.destination

            if neighbor in visited:
                continue

            visited.add(neighbor)
            parent[neighbor] = current
            queue.append(neighbor)

    return None


def _reconstruct_path(
    parent: Dict[str, Optional[str]],
    goal: str,
) -> List[str]:
    path = []
    current: Optional[str] = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path