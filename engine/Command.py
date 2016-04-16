from engine.exceptions import StateError, LogicError, Messages


class Command(object):
    """ Holds logic for, well, commands.
    """
    ##############################################################
    # Example ChangefulCommand and associated methods
    ##############################################################

    # go = ChangefulCommand(syntax=[is_a_direction], rules=[path_exists], state_changes=move_player, response=look)

    # def is_a_direction(world, word):
    #     return word in world.directions
    #
    # def path_exists(world, player, direction):
    #     if not <condition>:
    #         raise LogicError(Messages.NO_PATH)

    # def move_player(world, player, direction):
    #     change player location

    # def look(world, player):
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

    def __call__(self, world, player, *args):
        """ Called by LogicHandler. Does three things:
            * makes sure command syntax is correct
            * checks if command can be run
            * returns the correct response
        """
        if args and not self.syntax:
            raise LogicError(Messages.TOO_MANY_ARGS)
        if self.syntax:
            self.check_syntax(world, *args)
        if self.rules:
            self.check_rules(world, player, *args)
        return self.calculate_response(world, player)

    def check_syntax(self, world, *args):
        """ Makes sure that the command has been called
            with the correct number of arguments
            and that the arguments are the right type.
        """
        if len(args) < len(self.syntax):
            raise LogicError(Messages.TOO_FEW_ARGS.format(self.name))
        elif len(args) > len(self.syntax):
            raise LogicError(Messages.TOO_MANY_ARGS)

        for arg, expected in zip(args, self.syntax):
            expected(world, arg)

    def check_rules(self, world, player, *args):
        """ Calls the functions that check whether the command
            can be executed.

            If one of the checks doesn't pass, the check will raise.
        """
        for check in self.rules:
            check(world, player, *args)

    def calculate_response(self, world, player):
        """ Calls the function that formulates and formats
            the response to be sent back.
        """
        return self.response(world, player)


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

    def __call__(self, world, player, *args):
        """ Same as above, except that it changes game state
            if checks pass.
        """
        if self.syntax:
            self.check_syntax(world, *args)
        if self.rules:
            self.check_rules(world, player, *args)
        self.change_state(world, player, *args)
        return self.calculate_response(world, player)

    def change_state(self, world, player, *args):
        """ Manages changes in world state.
            Wraps the state-changing methods in a transaction
            and will roll state back if something goes wrong.
        """
        # world.start_transaction()
        try:
            for state_change in self.state_changes:
                state_change(world, player, *args)
        except StateError:
            # world.rollback()
            raise LogicError(Messages.BAD_STATE_CHANGE)
        # finally:
            # world.commit()
