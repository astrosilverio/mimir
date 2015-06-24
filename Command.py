from hogwartsexceptions import StateError, LogicError, Messages


class Command(object):
    """ Holds logic for, well, commands.
    """
    ##############################################################
    # Example ChangefulCommand and associated methods
    ##############################################################

    # go = ChangefulCommand(syntax=[is_a_direction], rules=[path_exists], state_changes=move_player, response=look)

    # def is_a_direction(castle, word):
    #     return word in castle.directions
    #
    # def path_exists(castle, player, direction):
    #     if not <condition>:
    #         raise LogicError(Messages.NO_PATH)

    # def move_player(castle, player, direction):
    #     change player location

    # def look(castle, player):
    #     return player.location.description

    def __init__(self, name=None, syntax=None, rules=None, response=None):
        """ Expected params:
            * name -- the input string that will trigger this command
            * syntax -- (optional) list containing validators for args;
                        should be same length as expected number of args
            * rules -- (optional) list containing methods that will check if command can be executed
            * response -- (optional) method that composes response to player
        """
        self.name = name
        self.syntax = syntax
        self.rules = rules
        self.response = response

    def execute(self, castle, player, *args):
        """ Called by LogicHandler. Does three things:
            * makes sure command syntax is correct
            * checks if command can be run
            * returns the correct response
        """
        if args and not self.syntax:
            raise LogicError(Messages.TOO_MANY_ARGS)
        if self.syntax:
            self.check_syntax(castle, *args)
        if self.rules:
            self.check_rules(castle, player, *args)
        return self.calculate_response(castle, player)

    def check_syntax(self, castle, *args):
        """ Makes sure that the command has been called
            with the correct number of arguments
            and that the arguments are the right type.
        """
        if len(args) < len(self.syntax):
            raise LogicError(Messages.TOO_FEW_ARGS.format(self.name))
        elif len(args) > len(self.syntax):
            raise LogicError(Messages.TOO_MANY_ARGS)

        for arg, expected in zip(args, self.syntax):
            expected(castle, arg)

    def check_rules(self, castle, player, *args):
        """ Calls the functions that check whether the command
            can be executed.

            If one of the checks doesn't pass, the check will raise.
        """
        for check in self.rules:
            check(castle, player, *args)

    def calculate_response(self, castle, player):
        """ Calls the function that formulates and formats
            the response to be sent back.
        """
        return self.response(castle, player)


class ChangefulCommand(Command):
    def __init__(self, name=None, syntax=None, rules=None, state_changes=None, response=None):
        """ Expected params:
            * name -- the input string that will trigger this command
            * syntax -- (optional) list containing validators for args;
                        should be same length as expected number of args
            * rules -- (optional) list containing methods that will check if command can be executed
            * state_changes -- (optional) list containing methods that change game state
            * response -- (optional) method that composes response to player
        """
        super(ChangefulCommand, self).__init__(name, syntax, rules, response)
        self.state_changes = state_changes

    def execute(self, castle, player, *args):
        """ Same as above, except that it changes game state
            if checks pass.
        """
        if self.syntax:
            self.check_syntax(castle, *args)
        if self.rules:
            self.check_rules(castle, player, *args)
        self.change_state(castle, player, *args)
        return self.calculate_response(castle, player)

    def change_state(self, castle, player, *args):
        """ Manages changes in castle state.
            Wraps the state-changing methods in a transaction
            and will roll state back if something goes wrong.
        """
        castle.start_transaction()
        try:
            for state_change in self.state_changes:
                state_change(castle, player, *args)
        except StateError:
            castle.rollback()
            raise LogicError(Messages.BAD_STATE_CHANGE)
        finally:
            castle.commit()
