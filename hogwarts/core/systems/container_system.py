from braga import System

from hogwarts.core.components import Container, Moveable
from hogwarts.core.systems.decorators import entry_point

container_system = System()


@entry_point
@container_system
def move(thing, new_container, auto_update=False):
    """Moves a Moveable into a Container."""
    if not thing.has_component(Moveable):
        raise ValueError("You cannot move this item")
    if not new_container.has_component(Container):
        raise ValueError("Invalid destination")
    old_container = thing.location
    thing.location = new_container
    new_container.inventory.add(thing)
    if old_container:
        old_container.inventory.remove(thing)
