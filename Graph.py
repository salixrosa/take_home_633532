from copy import copy
from typing import List

from DirectedEdge import DirectedEdge
from Node import Node


class Graph:
    def __init__(self, list_of_edges: List[DirectedEdge]):
        self.list_of_edges = list_of_edges
        self._nodes = set()
        for edge in list_of_edges:
            self._nodes.add(edge.start)
            self._nodes.add(edge.end)

    """
    Efficiency could be improved by storing the list of applicable edges
    by their start node, so 
    """
    def get_routes_from(self, node: Node):
        edges = []
        for edge in self.list_of_edges:
            if edge.start == node:
                edges.append(edge)
        return edges

    @property
    def nodes(self):
        return copy(self._nodes)  # one of a billion ways to keep this from being accidentally mutated
