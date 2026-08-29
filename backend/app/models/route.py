from typing import List, Literal

from pydantic import BaseModel, Field


AlgorithmName = Literal["bfs", "dfs", "dijkstra", "astar"]


class RouteRequest(BaseModel):
    source: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    algorithm: AlgorithmName = "astar"


class RouteResponse(BaseModel):
    algorithm: AlgorithmName
    path: List[str]
    total_distance_km: float
    estimated_time_minutes: float
    nodes_explored: int