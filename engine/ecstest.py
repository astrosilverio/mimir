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

    def __init__(self, inventory=None):
        self._inventory = inventory if inventory else set()

    @property
    def inventory(self):
        return self._inventory

    def add(self, *args):
        to_add = set(args)
        self._inventory |= to_add

    def remove(self, *args):
        to_remove = set(args)
        self._inventory -= to_remove


class Entity(object):

    __slots__ = ('guid', 'components')

    def __init__(self, guid):
        self.guid = guid
        self.components = set()

    def __getattr__(self, name):
        for component in self.components:
            try:
                attr = getattr(component, name)
            except AttributeError:
                pass
            else:
                return attr
        raise AttributeError


class EntityManager(object):

    def __init__(self):
        self._entities = {}
        self._components = {}
        self._next_guid = 0

    def create_entity(self):
        entity = Entity(self._next_guid)
        self._next_guid += 1
        self._entities[entity] = set()
        return entity

    def add_component_to_entity(self, entity, component):
        component_type = type(component)
        self._entities[entity].add(component)
        self._components[component_type][entity] = component

    def get_components_for_entity(self, entity):
        return self._entities


cat = Entity(0)
myrtle = Entity(1)

catportable = Portable()
catalive = Alive()
catcontainer = Container()

myrtlealive = Alive(False)

cat.components |= set([catportable, catalive, catcontainer])
myrtle.components.add(myrtlealive)
