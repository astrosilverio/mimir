from hogwartsexceptions import ParserError, LogicError, MaraudersMapError, Messages
import LogicHandler

import re


class Parser(object):
    """ Takes user input. Processes it into list of things user wants to do.
        Gets response from LogicHandler. Gives response back to user.
    """

    def __init__(self, username, castle):
        """ ALL INFO ABOUT DATA STORED IN MARAUDERSMAP
            JUST LINK THIS WITH A MARAUDERSMAP OBJECT
        """
        self.castle = castle
        self.player = self.castle.add_player(username)

    def process(self, user_input):
        """ Takes user_input, processes it into an attempted command.
        """
        words = user_input.split()
        words = [re.sub('\W+', '', word) for word in words]
        words = [word if (word in self.castle.canonicals) else self.castle.noncanonicals.get(word, None) for word in words]
        words = [word for word in words if word is not None]

        if not words:
            raise ParserError(Messages.GOBBLEDEGOOK)

        return words

    def execute(self, user_input):
        """ Gives processed user input to LogicHandler, gets response.
        """
        try:
            legit_input = self.process(user_input)
            if legit_input[0] not in self.castle.commands.keys():
                raise ParserError(Messages.UNKNOWN_VERB.format(legit_input[0]))
            response = LogicHandler.handle_command(self.castle, self.player, legit_input)
        except (ParserError, MaraudersMapError, LogicError) as e:
            response = e.message
        finally:
            return response
