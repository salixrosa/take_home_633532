from Node import Node


class DirectedEdge:
    # This would also probably be a dataclass in Kotlin
    def __init__(self, start: Node, end: Node, weight: int = 0):
        self.start = start
        self.end = end
        self.weight = weight

    def __repr__(self):  # This is just for debugging / usability; it makes the logging more useful
        return f'DirectedEdge(\'{self.start}\', \'{self.end}\', \'{self.weight}\')'