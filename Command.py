class Command(object):
    """ Holds logic for, well, commands.
        For example, examine = Command(syntax=[thing], rules=[player_can_see], response=print_detail)
    """

    ##############################################################
    # Example ChangefulCommand and associated methods
    ##############################################################

    # go = ChangefulCommand(syntax=[direction], rules=path_exists, state_changes=move_player)

    # def path_exists(castle, player):
    #     if something:
    #         return True
    #     else:
    #         raise RowlingError(Messages.NO_PATH)

    # def move_player(castle, player, direction):
    #     pass

    # def look(castle, player):
    #     pass

    def __init__(self, syntax=None, rules=None, response=None):
        self.syntax = syntax
        self.rules = rules
        self.response = response

    def execute(self, castle, player, *args):
        """ Called by Rowling. Does three things:
            * makes sure command syntax is correct
            * checks if command can be run
            * returns the correct response
        """
        self.check_syntax(*args)
        self.check_rules(castle, player)
        return self.calculate_response(castle, player)

    def check_syntax(self, *args):
        """ Makes sure that the command has been called
            with the correct number of arguments
            and that the arguments are the right type.
        """
        pass

    def check_rules(self, castle, player):
        """ Calls the functions that check whether the command
            can be executed.

            If one of the checks doesn't pass, the check will raise.
        """
        for check in self.rules:
            check(castle, player)

    def calculate_response(self, castle, player):
        """ Calls the function that formulates and formats
            the response to be sent back.
        """
        return self.response(castle, player)


class ChangefulCommand(Command):
    def __init__(self, syntax=None, rules=None, state_changes=None, response=None):
        super(ChangefulCommand, self).__init__(syntax, rules, response)
        self.state_changes = state_changes

    def execute(self, castle, player, *args):
        """ Same as above, except that it changes game state
            if checks pass.
        """
        self.check_syntax(*args)
        self.check_rules(castle, player)
        self.change_state(castle, player, *args)
        return player.location.description

    def change_state(self, castle, player, *args):
        """ Calls the functions that change castle state.
        """
        for state_change in self.state_changes:
            state_change(castle, player, *args)
