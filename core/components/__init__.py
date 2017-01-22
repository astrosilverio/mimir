from braga import Component


class Name(Component):
    """A short name for the Entity. Need not be unique."""

    INITIAL_PROPERTIES = ['name']

    def __init__(self, name=None):
        self.name = name
        self.names = [name]


class Container(Component):
    """Ability to have an inventory. For rooms and players."""

    INITIAL_PROPERTIES = ['inventory']

    def __init__(self, inventory=None):
        self._inventory = set()
        if inventory:
            for item in inventory:
                self._inventory.add(item)

    @property
    def inventory(self):
        return self._inventory


class Moveable(Component):
    """Ability to be moved, stores Entity's location. For players and wands."""

    INITIAL_PROPERTIES = ['location']

    def __init__(self, location=None):
        self.location = location
