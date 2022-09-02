from typing import Dict, List

from Graph import Graph
from Node import Node


def shortest_paths(graph: Graph, start: Node, finish: Node):
    if start == finish:
        return [], 0

    paths: List[List[Node]] = []
    nodes_w_unexplored_neighbors = graph.nodes
    distances: Dict[Node, float] = {node: float("inf") for node in nodes_w_unexplored_neighbors}
    linked_nodes: Dict[Node, List[Node]] = {node: [] for node in nodes_w_unexplored_neighbors}

    if start not in graph.nodes or finish not in graph.nodes:
        return paths, float("inf")

    distances[start] = 0  # a key element of the algorithm, ensures we calculate distances fanning out from the initial node
    while len(nodes_w_unexplored_neighbors) != 0:
        node_to_calculate_from = _find_next_node(nodes_w_unexplored_neighbors, distances)
        nodes_w_unexplored_neighbors.remove(node_to_calculate_from)
        if node_to_calculate_from == finish:
            continue  # if we're looking at the final node in the path, we don't need to look out to its neighbors
        for neighboring_edge in graph.get_routes_from(node_to_calculate_from):
            calculated_distance = distances[node_to_calculate_from] + neighboring_edge.weight
            neighbor_node = neighboring_edge.end
            if calculated_distance == distances[neighbor_node]:
                linked_nodes[neighbor_node].append(node_to_calculate_from)
            elif calculated_distance < distances[neighbor_node]:
                distances[neighbor_node] = calculated_distance
                linked_nodes[neighbor_node] = [node_to_calculate_from]

    if distances[finish] == float("inf"):
        return paths, distances[finish]

    paths = _break_out_paths(linked_nodes, finish)
    return paths, distances[finish]


def _find_next_node(valid_nodes: List[Node], nodes_with_distances: Dict[Node, float]):
    max_distance_node = None
    for node in valid_nodes:
        if max_distance_node is None or nodes_with_distances[node] < nodes_with_distances[max_distance_node]:
            max_distance_node = node
    return max_distance_node


def _break_out_paths(dictionary_of_connected_nodes: Dict[Node, List[Node]], end_of_path: Node) -> List[List[Node]]:
    incomplete_paths: List[List[Node]] = [[end_of_path]]
    complete_paths: List[List[Node]] = []
    while len(incomplete_paths) != 0:
        incomplete_path = incomplete_paths.pop()
        last_node_in_complete_path = incomplete_path[-1]
        next_nodes = dictionary_of_connected_nodes[last_node_in_complete_path]
        if len(next_nodes) == 0:
            complete_paths.append(incomplete_path)
            continue
        for next_node in next_nodes:
            incomplete_paths.append(incomplete_path + [next_node])

    for path in complete_paths:
        path.reverse()

    return complete_paths




