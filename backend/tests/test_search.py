from backend.app.algorithms.graph import Graph
from backend.app.algorithms.bfs import bfs
from backend.app.algorithms.dfs import dfs


def create_test_graph() -> Graph:
    graph = Graph()

    graph.add_node("A", "Station", 19.0000, 72.0000)
    graph.add_node("B", "Junction B", 19.0010, 72.0010)
    graph.add_node("C", "Junction C", 19.0020, 72.0000)
    graph.add_node("D", "Junction D", 19.0030, 72.0010)
    graph.add_node("E", "Emergency", 19.0040, 72.0000)

    graph.add_edge("A", "B", 1.0, 2.0)
    graph.add_edge("A", "C", 1.0, 2.0)
    graph.add_edge("B", "D", 1.0, 2.0)
    graph.add_edge("C", "D", 1.0, 2.0)
    graph.add_edge("D", "E", 1.0, 2.0)

    return graph


def test_bfs_finds_path():
    graph = create_test_graph()

    path = bfs(graph, "A", "E")

    assert path is not None
    assert path[0] == "A"
    assert path[-1] == "E"
    assert len(path) == 4


def test_dfs_finds_path():
    graph = create_test_graph()

    path = dfs(graph, "A", "E")

    assert path is not None
    assert path[0] == "A"
    assert path[-1] == "E"