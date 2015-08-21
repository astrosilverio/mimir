from ecs import Component


class Alive(Component):

    def __init__(self, alive=True):
        self._alive = alive

    @property
    def alive(self):
        return self._alive

    def die(self):
        self._alive = False

    def resurrect(self):
        self._alive = True


class Portable(Component):

    def __init__(self, location=None):
        self.location = location

    @property
    def is_portable(self):
        return True


class Container(Component):

    def __init__(self, inventory=None, size=None):
        self._inventory = inventory if inventory else set()
        self.size = size if size else None

    @property
    def inventory(self):
        return self._inventory

    @property
    def is_not_full(self):
        return not self.size or len(self._inventory) < self.size

    def add(self, *args):
        to_add = set(args)
        self._inventory |= to_add

    def remove(self, *args):
        to_remove = set(args)
        self._inventory -= to_remove
