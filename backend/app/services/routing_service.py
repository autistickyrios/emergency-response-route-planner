from typing import Dict, List, Optional, Tuple

from backend.app.algorithms.astar import astar
from backend.app.algorithms.bfs import bfs
from backend.app.algorithms.dijkstra import dijkstra
from backend.app.algorithms.dfs import dfs
from backend.app.algorithms.graph import Graph
from backend.app.models.route import AlgorithmName


def calculate_route(
    graph: Graph,
    source: str,
    destination: str,
    algorithm: AlgorithmName,
) -> Optional[List[str]]:

    algorithms = {
        "bfs": bfs,
        "dfs": dfs,
        "dijkstra": dijkstra,
        "astar": astar,
    }

    selected_algorithm = algorithms[algorithm]

    return selected_algorithm(
        graph,
        source,
        destination,
    )


def calculate_route_metrics(
    graph: Graph,
    path: List[str],
) -> Tuple[float, float]:

    total_distance = 0.0
    total_time = 0.0

    for current, next_node in zip(path, path[1:]):

        edge = next(
            (
                edge
                for edge in graph.get_neighbors(current)
                if edge.destination == next_node
            ),
            None,
        )

        if edge is None:
            raise ValueError(
                f"Edge not found between {current} and {next_node}"
            )

        total_distance += edge.distance
        total_time += edge.cost

    return total_distance, total_time