import logging

from hogwartsexceptions import LogicError, Messages

logger = logging.getLogger('LogicHandler')

################################################################################################
#    Recieves from Parser what the user wants to do, who user is, which castle they're in.
#    Decides if user can do what they want.
#    Makes MaraudersMap change state if necessary.
#    Gives Parser a response.
################################################################################################


def handle_command(self, castle, player, command):
    """ Takes processed command from Parser.
        Performs checks.
        If command can be performed, executes it.
        Otherwise, set response to appropriate error.
        Passes response to Parser.
    """
    verb = command[0]
    args = command[1:]
    command = castle.commands.get(verb, None)
    if not command:
        # if handle_command is called by Parser, we'll never see this
        logger.error("handle_command called from outside Parser.execute by player %s in game %s", player.id, castle.name)
        raise LogicError(Messages.UNKNOWN_VERB)

    self.handle_auto_movements(castle)
    result = command.execute(castle, player, *args)

    return result if result else None


def handle_auto_movements(self, castle):
    """ Runs automated logic after every turn.
        Use to, e.g., release the basilisk at turn #100.
    """
    pass
