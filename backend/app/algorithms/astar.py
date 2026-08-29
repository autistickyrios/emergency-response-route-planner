import heapq
import math
from typing import Dict, List, Optional, Tuple

from .graph import Graph


def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """
    Calculate geographical distance between two coordinates.

    Returns distance in kilometers.
    """

    earth_radius_km = 6371.0

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1_rad)
        * math.cos(lat2_rad)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius_km * c


def heuristic(graph: Graph, current: str, goal: str) -> float:
    """
    Estimate travel cost between current and goal.

    We convert geographical distance into an approximate
    minimum travel time assuming 60 km/h.
    """

    current_node = graph.get_node(current)
    goal_node = graph.get_node(goal)

    distance_km = haversine_distance(
        current_node.latitude,
        current_node.longitude,
        goal_node.latitude,
        goal_node.longitude,
    )

    # 60 km/h = 1 km/minute
    return distance_km


def astar(
    graph: Graph,
    start: str,
    goal: str,
) -> Optional[List[str]]:
    """
    A* search algorithm.

    Uses actual travel cost + geographical heuristic
    to efficiently find a low-cost route.
    """

    if start not in graph.nodes:
        raise ValueError(f"Unknown start node: {start}")

    if goal not in graph.nodes:
        raise ValueError(f"Unknown goal node: {goal}")

    g_score: Dict[str, float] = {
        node_id: float("inf")
        for node_id in graph.nodes
    }

    parent: Dict[str, Optional[str]] = {
        node_id: None
        for node_id in graph.nodes
    }

    g_score[start] = 0.0

    # (f_score, node)
    priority_queue: List[Tuple[float, str]] = [
        (heuristic(graph, start, goal), start)
    ]

    while priority_queue:
        current_f, current = heapq.heappop(priority_queue)

        current_g = g_score[current]

        # Ignore stale queue entries.
        expected_f = current_g + heuristic(
            graph,
            current,
            goal,
        )

        if current_f > expected_f:
            continue

        if current == goal:
            return _reconstruct_path(parent, goal)

        for edge in graph.get_neighbors(current):
            if edge.blocked:
                continue

            neighbor = edge.destination

            tentative_g = current_g + edge.cost

            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current

                f_score = (
                    tentative_g
                    + heuristic(graph, neighbor, goal)
                )

                heapq.heappush(
                    priority_queue,
                    (f_score, neighbor),
                )

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