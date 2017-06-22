from hogwarts.engine.exceptions import ParserError, LogicError, StateError, Messages

import re


class Parser(object):
    """ Takes user input. Processes it into list of things user wants to do.
        Gets response from LogicHandler. Gives response back to user.
    """

    def __init__(self, world, name_system, player, commands=None):
        self.world = world
        self.player = player
        self.commands = commands if commands else dict()
        self.name_system = name_system

    def _is_number(self, word):
        try:
            int(word)
        except ValueError:
            return False
        else:
            return True

    def get_entity(self, word):
        if self._is_number(word):
            return word
        entity = self.name_system.get_token_from_name(word)
        if not entity:
            raise ParserError("Cannot find entity with that name")
        return entity

    def normalize(self, user_input):
        """Takes user_input, processes it into a series of strings that represent in-game concepts."""
        words = user_input.split()
        words = [re.sub('[\W+\\+[!\'+]]', '', word) for word in words]
        words.reverse()
        tokens = []

        while len(words) >= 1:
            word = words.pop()
            if word in self.name_system.tokens or self._is_number(word) or word in self.commands.keys():
                tokens.append(word)
            elif not words:
                break
            elif ' '.join([word, words[-1]]) in self.name_system.tokens:
                tokens.append(' '.join([word, words[-1]]))

        if not tokens:
            raise ParserError(Messages.GOBBLEDEGOOK)

        if tokens[0] not in self.commands.keys():
            raise ParserError(Messages.UNKNOWN_VERB.format(tokens[0]))

        return tokens

    def tokenize(self, normalized_input):
        """Takes a list of strings and associates them with in-game entities."""
        tokenized_input = [self.commands.get(normalized_input[0])]
        tokenized_input.extend([self.get_entity(word) for word in normalized_input[1:]])

        return tokenized_input

    def execute(self, user_input):
        """Gives processed user input to command, gets response."""
        try:
            processed_input = self.tokenize(self.normalize(user_input))
            response = processed_input[0](self.world, self.player, *processed_input[1:])
        except (ParserError, StateError, LogicError) as e:
            response = e.message
        finally:
            return response
