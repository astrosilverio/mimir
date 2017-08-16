from braga import System, Aspect

from hogwarts.core.components import Container, Moveable


class ContainerSystem(System):
    """Manages Containers and the Moveables they contain."""
    def __init__(self, world):
        super(ContainerSystem, self).__init__(world=world, aspect=Aspect(all_of=set([Container])))

        for entity in self.world.entities_with_aspect(Aspect(all_of=set([Moveable]))):
            entity.location.inventory.add(entity)

        self.update()

    def update(self):
        """Updates the `inventory` attribute on all Containers in the World"""
        for entity in self.world.entities_with_aspect(Aspect(all_of=set([Moveable]))):
            entity.location.inventory.add(entity)

    def move(self, thing, new_container, auto_update=False):
        """Moves a Moveable into a Container."""
        if not thing.has_component(Moveable):
            raise ValueError("You cannot move this item")
        if not new_container in self.aspect:
            raise ValueError("Invalid destination")
        old_container = thing.location
        thing.location = new_container
        new_container.inventory.add(thing)
        if old_container:
            old_container.inventory.remove(thing)
