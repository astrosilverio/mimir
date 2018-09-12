from braga import System

from hogwarts.core import components

context_system = System()


@context_system
def find_contexts_for_entity(entity):
    self_context = None
    location_context = None
    contained_contexts = []
    if entity.has_component(components.Context):
        self_context = entity.context
    if entity.has_component(components.Moveable):
        location_context = entity.location.context
    if entity.has_component(components.Container):
        for item in entity.inventory:
            if item.has_component(components.Context):
                contained_contexts.append(item.context)

    return self_context, location_context, contained_contexts
