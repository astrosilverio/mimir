from braga import Component


class Name(Component):
    """A short name for the Entity. Need not be unique."""

    INITIAL_PROPERTIES = ['name']

    def __init__(self, name=None):
        self.name = name
        self.names = [name]
