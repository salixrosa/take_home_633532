class Node:
    """
    Though I'm accustomed to generating the equals and hash methods in Java, Python services
    tend to be less object-oriented, so I rarely see folks implementing equals
    and hash methods. If this were Kotlin, `Node` would be implemented as a dataclass.
    """

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):  # This is just for debugging / usability; it makes the logging more useful
        return f'Node(\'{self.name}\')'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
