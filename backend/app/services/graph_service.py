from backend.app.algorithms.graph import Graph


def create_city_graph() -> Graph:
    graph = Graph()

    # Emergency station
    graph.add_node(
        "station_01",
        "Central Emergency Station",
        19.0760,
        72.8777,
    )

    # Road junctions
    graph.add_node(
        "junction_01",
        "North Junction",
        19.0790,
        72.8800,
    )

    graph.add_node(
        "junction_02",
        "East Junction",
        19.0740,
        72.8820,
    )

    graph.add_node(
        "junction_03",
        "South Junction",
        19.0710,
        72.8780,
    )

    graph.add_node(
        "junction_04",
        "West Junction",
        19.0730,
        72.8730,
    )

    graph.add_node(
        "junction_05",
        "Central Junction",
        19.0760,
        72.8800,
    )


    # Hospitals
    graph.add_node(
    "hospital_01",
    "City Emergency Hospital",
    19.0800,
    72.8840,
        )

    graph.add_node(
    "hospital_02",
    "East General Hospital",
    19.0735,
    72.8860,
    )

    graph.add_node(
    "hospital_03",
    "West Trauma Center",
    19.0705,
    72.8700,
    )

    graph.add_node(
    "hospital_04",
    "South Medical Center",
    19.0685,
    72.8780,
    )

    # Roads
    graph.add_edge(
        "station_01",
        "junction_01",
        distance=0.5,
        travel_time=2.0,
    )

    graph.add_edge(
        "station_01",
        "junction_02",
        distance=0.7,
        travel_time=3.0,
    )

    graph.add_edge(
        "station_01",
        "junction_04",
        distance=0.6,
        travel_time=2.5,
    )

    graph.add_edge(
        "junction_01",
        "junction_05",
        distance=0.4,
        travel_time=1.5,
    )

    graph.add_edge(
        "junction_02",
        "junction_05",
        distance=0.5,
        travel_time=2.0,
    )

    graph.add_edge(
        "junction_04",
        "junction_03",
        distance=0.5,
        travel_time=2.0,
    )

    graph.add_edge(
        "junction_03",
        "junction_05",
        distance=0.6,
        travel_time=2.0,
    )

    graph.add_edge(
        "junction_05",
        "hospital_01",
        distance=0.6,
        travel_time=2.0,
    )

    graph.add_edge(
        "junction_01",
        "hospital_01",
        distance=0.8,
        travel_time=4.0,
    )

    graph.add_edge(
    "junction_02",
    "hospital_02",
    distance=0.7,
    travel_time=3.0,
    )

    graph.add_edge(
    "junction_04",
    "hospital_03",
    distance=0.6,
    travel_time=2.5,
    )

    graph.add_edge(
    "junction_03",
    "hospital_04",
    distance=0.5,
    travel_time=2.0,
    )

    return graph


CITY_GRAPH = create_city_graph()