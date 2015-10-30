from engine.exceptions import ParserError, LogicError, StateError, Messages
import LogicHandler

import re


class Parser(object):
    """ Takes user input. Processes it into list of things user wants to do.
        Gets response from LogicHandler. Gives response back to user.
    """

    def __init__(self, player, castle):
        """ ALL INFO ABOUT DATA STORED IN StateManager
            JUST LINK THIS WITH A StateManager OBJECT
        """
        self.castle = castle
        self.player = player

    def _is_number(self, word):
        try:
            int(word)
        except ValueError:
            return False
        else:
            return True

    def process(self, user_input):
        """Takes user_input, processes it into an attempted command."""
        words = user_input.split()
        words = [re.sub('\W+\'', '', word) for word in words]
        words = [word if ((word in self.castle.canonicals) or self._is_number(word)) else self.castle.noncanonicals.get(word, None) for word in words]
        words = [word for word in words if word is not None]

        if not words:
            raise ParserError(Messages.GOBBLEDEGOOK)

        return words

    def execute(self, user_input):
        """Gives processed user input to LogicHandler, gets response."""
        try:
            legit_input = self.process(user_input)
            if legit_input[0] not in self.castle.commands.keys():
                raise ParserError(Messages.UNKNOWN_VERB.format(legit_input[0]))
            response = LogicHandler.handle_command(self.castle, self.player, legit_input)
        except (ParserError, StateError, LogicError) as e:
            response = e.message
        finally:
            return response
