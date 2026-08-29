from typing import Dict, List, Optional

from .graph import Graph


def dfs(graph: Graph, start: str, goal: str) -> Optional[List[str]]:
    """
    Depth-First Search.

    Finds a path by exploring deeply before backtracking.
    It does NOT guarantee the shortest or fastest path.
    """

    if start not in graph.nodes:
        raise ValueError(f"Unknown start node: {start}")

    if goal not in graph.nodes:
        raise ValueError(f"Unknown goal node: {goal}")

    stack = [start]
    visited = {start}
    parent: Dict[str, Optional[str]] = {start: None}

    while stack:
        current = stack.pop()

        if current == goal:
            return _reconstruct_path(parent, goal)

        # Reverse so the first neighbor is processed first.
        neighbors = graph.get_neighbors(current)

        for edge in reversed(neighbors):
            if edge.blocked:
                continue

            neighbor = edge.destination

            if neighbor in visited:
                continue

            visited.add(neighbor)
            parent[neighbor] = current
            stack.append(neighbor)

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