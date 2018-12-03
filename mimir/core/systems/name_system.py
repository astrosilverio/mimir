from collections import defaultdict

from braga import Aspect, System

from mimir.core.components import Name


class NameSystem(System):
    """Associates strings with Entities."""
    def __init__(self, world):
        super(NameSystem, self).__init__(world=world, aspect=Aspect(all_of=set([Name])))
        self.names = defaultdict(list)
        self.update()

    @property
    def tokens(self):
        return self.names.keys()

    def get_token_from_name(self, name, entity=None):
        from mimir.core.systems import ContextSystem
        context_system = self.world.systems.get(ContextSystem)

        self_context = None
        location_context = None
        contained_contexts = None

        if entity:
            self_context, location_context, contained_contexts = context_system.find_contexts_for_entity(entity)

        if self_context and self_context.get(name):
            return self_context.get(name)

        possible_tokens = []
        if location_context and location_context.get(name):
            possible_tokens.append(location_context.get(name))
        if contained_contexts:
            contained_tokens = [context.get(name) for context in contained_contexts if context.get(name)]
            possible_tokens.extend(contained_tokens)
        if self.names.get(name):
            possible_tokens.extend(self.names.get(name))

        if len(possible_tokens) > 1:
            raise ValueError("For now I can't handle confusion")

        if not possible_tokens:
            raise ValueError("I don't know what you're talking about")

        return possible_tokens[0]

    def add_name(self, name, entity):
        if entity in self.names[name]:
            raise ValueError('Duplicate entity names')
        self.names[name].append(entity)
        # entity.names.append(name)

    def update(self):
        for entity in self.entities:
            for name in entity.names:
                self.names[name].append(entity)
