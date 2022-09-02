import csv

from DirectedEdge import DirectedEdge
from Graph import Graph
from Node import Node
from shortest_path import shortest_paths


def get_sample_graph():
    sample_route_data = []

    with open('sample_route_data.csv') as sample_route_file:
        reader = csv.DictReader(sample_route_file)
        for row in reader:
            sample_route_data.append(DirectedEdge(Node(row["node_1"]), Node(row["node_2"]), int(row["weight"])))

    return Graph(sample_route_data)


def test_cases_using_sample_data():
    test_cases_on_sample_routes = [
        # start, finish, expected path, expected distance, message
        ["A", "A", [], 0, f'Empty path and zero distance if start and finish are the same'],
        ["A", "C", [[Node("A"), Node("C")]], 10, f''],
        ["C", "A", [[Node("C"), Node("A")]], 8, 'Paired with previous test, handles directionality'],
        ["D", "A", [], float("inf"), f'Empty path and infinite distance if route is not possible'],
        ["Z", "A", [], float("inf"), f'Empty path and infinite distance if start node is not in graph at all'],
        ["A", "Z", [], float("inf"), f'Empty path and infinite distance if finish node is not in graph at all'],
    ]

    sample_graph = get_sample_graph()
    for test_case in test_cases_on_sample_routes:
        calculated_path, calculated_distance = shortest_paths(sample_graph, Node(test_case[0]),
                                                              Node(test_case[1]))
        status = "PASS" if calculated_path == test_case[2] and calculated_distance == test_case[3] else "FAIL"
        print(f'Testing with sample data and path... {test_case[0]} to {test_case[1]} {test_case[4]}: {status}')
        if status == "FAIL":
            print("\t", calculated_path, calculated_distance)


def test_duplicate_edges():  # known to be failing
    node_a = Node("A")
    node_b = Node("B")
    shorter_edge = DirectedEdge(node_a, node_b, 5)
    middle_edge = DirectedEdge(node_a, node_b, 10)
    longer_edge = DirectedEdge(node_a, node_b, 15)
    minimal_edge = DirectedEdge(node_a, node_b, 0)
    bad_graph = Graph([longer_edge, shorter_edge, middle_edge, longer_edge, minimal_edge])
    calculated_path, calculated_distance = shortest_paths(bad_graph, node_a, node_b)
    status = "PASS" if calculated_path == [[node_a, node_b]] and calculated_distance == 5 else "FAIL"
    print(f'Testing with 3 duplicate edges... ensuring shortest distance is used: {status}')
    if status == "FAIL":
        print("\t", calculated_path, calculated_distance)


def test_cyclic_routes():
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D")
    edge_1 = DirectedEdge(node_a, node_b, 1)
    edge_2 = DirectedEdge(node_b, node_c, 2)
    edge_3 = DirectedEdge(node_c, node_b, 3)
    edge_4 = DirectedEdge(node_c, node_d, 4)
    cyclic_simple_graph = Graph([edge_1, edge_2, edge_3, edge_4])
    calculated_path, calculated_distance = shortest_paths(cyclic_simple_graph, node_a, node_d)
    status = "PASS" if calculated_path == [[node_a, node_b, node_c, node_d]] and calculated_distance == 7 else "FAIL"
    print(f'Testing smaller graph with cycles to ensure no looping... {status}')
    if status == "FAIL":
        print("\t", calculated_path, calculated_distance)


def test_nonsensical_edge():
    node_a = Node("A")
    node_b = Node("B")
    bad_edge = DirectedEdge(node_a, node_a, 1)
    edge = DirectedEdge(node_a, node_b, 1)
    simple_graph_with_nonsensical_edge = Graph([bad_edge, edge])
    calculated_path, calculated_distance = shortest_paths(simple_graph_with_nonsensical_edge, node_a, node_b)
    status = "PASS" if calculated_path == [[node_a, node_b]] and calculated_distance == 1 else "FAIL"
    print(f'Testing smaller graph with bad edge... {status}')
    if status == "FAIL":
        print("\t", calculated_path, calculated_distance)


def test_zero_cost_edge():
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    free_edge = DirectedEdge(node_a, node_b, 0)
    normal_edge = DirectedEdge(node_b, node_c, 1)
    simple_graph_with_free_edge = Graph([free_edge, normal_edge])
    calculated_path, calculated_distance = shortest_paths(simple_graph_with_free_edge, node_a, node_c)
    status = "PASS" if calculated_path == [[node_a, node_b, node_c]] and calculated_distance == 1 else "FAIL"
    print(f'Testing graph with zero-cost edge in path... {status}')
    if status == "FAIL":
        print("\t", calculated_path, calculated_distance)


def test_negative_cost_edge_in_path():
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    free_edge = DirectedEdge(node_a, node_b, -1)
    normal_edge = DirectedEdge(node_b, node_c, 1)
    simple_graph_with_free_edge = Graph([free_edge, normal_edge])
    calculated_path, calculated_distance = shortest_paths(simple_graph_with_free_edge, node_a, node_c)
    status = "PASS" if calculated_path == [[node_a, node_b, node_c]] and calculated_distance == 0 else "FAIL"
    print(f'Testing graph with negative edge in path... {status}')
    if status == "FAIL":
        print("\t", calculated_path, calculated_distance)


def test_negative_cost_edge_as_loop():
    # We don't run this because it will loop infinitely.
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    normal_edge_1 = DirectedEdge(node_a, node_b, 1)
    normal_edge_2 = DirectedEdge(node_b, node_c, 1)
    loop_edge = DirectedEdge(node_a, node_a, -1)
    simple_graph_with_free_edge = Graph([normal_edge_1, normal_edge_2,loop_edge])
    calculated_path, calculated_distance = shortest_paths(simple_graph_with_free_edge, node_a, node_c)
    status = "PASS" if calculated_path == [[node_a, node_b, node_c]] and calculated_distance == 2 else "FAIL"
    print(f'Testing graph with negative edge as loop... {status}')
    if status == "FAIL":
        print("\t", calculated_path, calculated_distance)


def test_paths_of_equal_distance_both_returned():
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D")
    edge_a_b = DirectedEdge(node_a, node_b, 1)
    edge_a_c = DirectedEdge(node_a, node_c, 2)
    edge_b_d = DirectedEdge(node_b, node_d, 2)
    edge_c_d = DirectedEdge(node_c, node_d, 1)
    graph = Graph([edge_a_b, edge_a_c, edge_b_d, edge_c_d])
    expected_path_1 = [node_a, node_b, node_d]
    expected_path_2 = [node_a, node_c, node_d]
    calculated_paths, calculated_distance = shortest_paths(graph, node_a, node_d)
    status = "PASS" if len(calculated_paths) == 2 and expected_path_1 in calculated_paths and expected_path_2 in calculated_paths and calculated_distance == 3 else "FAIL"
    print(f'Testing graph with two paths of equal distance... {status}')
    if status == "FAIL":
        print("\t", calculated_paths, calculated_distance)


def test_paths_of_equal_distance_different_node_counts_both_returned():
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    edge_a_b = DirectedEdge(node_a, node_b, 1)
    edge_b_c = DirectedEdge(node_b, node_c, 2)
    edge_a_c = DirectedEdge(node_a, node_c, 3)
    graph = Graph([edge_a_b, edge_b_c, edge_a_c])
    calculated_path, calculated_distance = shortest_paths(graph, node_a, node_c)
    status = "PASS" if calculated_path == [[node_a, node_b, node_c], [node_a, node_c]] and calculated_distance == 3 else "FAIL"
    print(f'Testing graph with two paths of equal distance but different numbers of nodes... {status}')
    if status == "FAIL":
        print("\t", calculated_path, calculated_distance)


test_nonsensical_edge()
test_cyclic_routes()
test_duplicate_edges()
test_cases_using_sample_data()
test_zero_cost_edge()
test_negative_cost_edge_in_path()
# test_negative_cost_edge_as_loop() # We don't run this because it will loop infinitely.
test_paths_of_equal_distance_both_returned()
test_paths_of_equal_distance_different_node_counts_both_returned()

