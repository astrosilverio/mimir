from braga import Component


class Name(Component):
    """A short name for the Entity. Need not be unique."""

    INITIAL_PROPERTIES = ['name']

    def __init__(self, name=None):
        self.name = name
        self.names = [name]


class Description(Component):

    INITIAL_PROPERTIES = ['description']

    def __init__(self, description=None):
        self.description = description


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
    """Ability to be moved, stores Entity's location."""

    INITIAL_PROPERTIES = ['location']

    def __init__(self, location=None):
        self.location = location
        if self.location:
            location.inventory.add(self)


class View(Component):
    """Ability to be the focus of a scene--say, a room or a tabletop.

    Items in `view_contents` are in a list because I presume that there
    may be situations in which a gamemaker would want items in a view
    to be in a particular order."""

    INITIAL_PROPERTIES = ['view_contents']

    def __init__(self, view_contents):
        self._view_contents = list()
        if view_contents:
            for item in view_contents:
                self._view_contents.append(item)

    @property
    def view_contents(self):
        return self._view_contents


class Contexts(Component):
    """Stores references to other entities that provide context
    for the entity this component belongs to, e.g. the Room that a Player is in."""

    INITIAL_PROPERTIES = ['contexts']

    def __init__(self, contexts):
        self._contexts = list()
        if contexts:
            for entity in contexts:
                self._contexts.append(entity)

    @property
    def contexts(self):
        return self._contexts
