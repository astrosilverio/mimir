from engine.exceptions import ParserError, LogicError, StateError, Messages
from tests.fixtures import NameSystem

import re


class Parser(object):
    """ Takes user input. Processes it into list of things user wants to do.
        Gets response from LogicHandler. Gives response back to user.
    """

    def __init__(self, world, player, commands=None, canonicals=None, noncanonicals=None):
        self.world = world
        self.player = player
        self.commands = commands if commands else dict()
        self.canonicals = canonicals if canonicals else set()
        self.noncanonicals = noncanonicals if noncanonicals else dict()

        self.name_system = self.world.systems.get(NameSystem)
        if not self.name_system:
            raise ValueError("world needs a name system")

    def _is_number(self, word):
        try:
            int(word)
        except ValueError:
            return False
        else:
            return True

    def get_entity(self, word):
        entity = self.name_system.get_entity_from_name(word)
        if not entity:
            raise ParserError("Cannot find entity with that name")

    def process(self, user_input):
        """Takes user_input, processes it into an attempted command."""
        words = user_input.split()
        words = [re.sub('\W+\'', '', word) for word in words]
        words = [word if ((word in self.canonicals) or self._is_number(word)) else self.noncanonicals.get(word, None) for word in words]
        words = [word for word in words if word is not None]

        if not words:
            raise ParserError(Messages.GOBBLEDEGOOK)

        if words[0] not in self.commands.keys():
            raise ParserError(Messages.UNKNOWN_VERB.format(words[0]))

        processed_input = [self.commands.get(words[0])]
        processed_input.extend([self.get_entity(word) for word in words[1:]])

        return processed_input

    def execute(self, user_input):
        """Gives processed user input to command, gets response."""
        try:
            processed_input = self.process(user_input)
            response = processed_input[0].execute(processed_input[1:])
        except (ParserError, StateError, LogicError) as e:
            response = e.message
        finally:
            return response
