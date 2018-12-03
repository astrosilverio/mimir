from braga import System, Aspect

from mimir.core import components


class ContextSystem(System):

    def __init__(self, world):
        super(ContextSystem, self).__init__(world=world, aspect=Aspect(all_of=set([components.Contexts])))

    def find_contexts_for_entity(self, entity):
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
