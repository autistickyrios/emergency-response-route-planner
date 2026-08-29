from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Edge:
    destination: str
    distance: float
    travel_time: float
    traffic_multiplier: float = 1.0
    blocked: bool = False

    @property
    def cost(self) -> float:
        """Current travel cost in minutes."""
        if self.blocked:
            return float("inf")

        return self.travel_time * self.traffic_multiplier


@dataclass
class Node:
    id: str
    name: str
    latitude: float
    longitude: float


@dataclass
class Graph:
    nodes: Dict[str, Node] = field(default_factory=dict)
    adjacency: Dict[str, List[Edge]] = field(default_factory=dict)

    def add_node(
        self,
        node_id: str,
        name: str,
        latitude: float,
        longitude: float,
    ) -> None:
        self.nodes[node_id] = Node(
            id=node_id,
            name=name,
            latitude=latitude,
            longitude=longitude,
        )

        self.adjacency.setdefault(node_id, [])

    def add_edge(
        self,
        source: str,
        destination: str,
        distance: float,
        travel_time: float,
        traffic_multiplier: float = 1.0,
        blocked: bool = False,
        bidirectional: bool = True,
    ) -> None:
        if source not in self.nodes:
            raise ValueError(f"Unknown source node: {source}")

        if destination not in self.nodes:
            raise ValueError(f"Unknown destination node: {destination}")

        edge = Edge(
            destination=destination,
            distance=distance,
            travel_time=travel_time,
            traffic_multiplier=traffic_multiplier,
            blocked=blocked,
        )

        self.adjacency[source].append(edge)

        if bidirectional:
            reverse_edge = Edge(
                destination=source,
                distance=distance,
                travel_time=travel_time,
                traffic_multiplier=traffic_multiplier,
                blocked=blocked,
            )

            self.adjacency[destination].append(reverse_edge)

    def get_neighbors(self, node_id: str) -> List[Edge]:
        return self.adjacency.get(node_id, [])

    def get_node(self, node_id: str) -> Node:
        if node_id not in self.nodes:
            raise ValueError(f"Unknown node: {node_id}")

        return self.nodes[node_id]