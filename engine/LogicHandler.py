import logging

from engine.exceptions import LogicError, Messages

logger = logging.getLogger('LogicHandler')

################################################################################################
#    Recieves from Parser what the user wants to do, who user is, which castle they're in.
#    Decides if user can do what they want.
#    Makes StateManager change state if necessary.
#    Gives Parser a response.
################################################################################################


def handle_command(castle, player, command):
    """ Takes processed command from Parser.
        Performs checks.
        If command can be performed, executes it.
        Otherwise, set response to appropriate error.
        Passes response to Parser.
    """
    verb = command[0]
    args = command[1:]
    command = castle.commands.get(verb, None)

    handle_auto_movements(castle)
    result = command.execute(castle, player, *args)

    return result if result else None


def handle_auto_movements(castle):
    """ Runs automated logic after every turn.
        Use to, e.g., release the basilisk at turn #100.
    """
    pass
