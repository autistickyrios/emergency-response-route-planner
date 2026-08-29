import heapq
from typing import Dict, List, Optional, Tuple

from .graph import Graph


def dijkstra(
    graph: Graph,
    start: str,
    goal: str,
) -> Optional[List[str]]:
    """
    Dijkstra's shortest-path algorithm.

    Finds the path with the minimum total travel cost.
    Edge costs account for traffic and blocked roads.
    """

    if start not in graph.nodes:
        raise ValueError(f"Unknown start node: {start}")

    if goal not in graph.nodes:
        raise ValueError(f"Unknown goal node: {goal}")

    # distance[node] = cheapest known cost from start to node
    distances: Dict[str, float] = {
        node_id: float("inf")
        for node_id in graph.nodes
    }

    # parent[node] = previous node on the best known path
    parent: Dict[str, Optional[str]] = {
        node_id: None
        for node_id in graph.nodes
    }

    distances[start] = 0.0

    # (cost, node)
    priority_queue: List[Tuple[float, str]] = [(0.0, start)]

    while priority_queue:
        current_cost, current = heapq.heappop(priority_queue)

        # Ignore outdated queue entries.
        if current_cost > distances[current]:
            continue

        if current == goal:
            break

        for edge in graph.get_neighbors(current):
            if edge.blocked:
                continue

            neighbor = edge.destination
            new_cost = current_cost + edge.cost

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                parent[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (new_cost, neighbor),
                )

    if distances[goal] == float("inf"):
        return None

    return _reconstruct_path(parent, goal)


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