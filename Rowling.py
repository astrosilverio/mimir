import logging

from hogwartsexceptions import MaraudersMapError, RowlingError, Messages

logger = logging.getLogger('Rowling')


""" Recieves from Legilimens what the user wants to do, who user is, which castle they're in.
    Decides if user can do what they want.
    Makes MaraudersMap change state if necessary.
    Gives Legilimens a response.
    should not contain instancemethods
"""

# SHOULD MAYBE MOVE THIS TO JSON AND THEN IT'S ALL IN THE CASTLE
# Below is sample commands and errors dicts

# MAYBE IT'S TIME FOR COMMANDS TO BE OBJECTS

#   commands = {'go': {'syntax': ['direction'], 'rules': ['path_exists', 'player_can_move'], 'state_changes': 'move_player'},
#               'look': {'syntax': {'primary': [], 'alias-to': ['examine','noun']}, 'rules': ['can_look_in_room']}}
#   errors = {'path_exists': "You can't go that way.", 'player_can_move': "You can't move right now.",
#               'can_look_in_room': "You can't see a thing."}


def handle_command(self, castle, player, command):
    """ Takes processed command from Legilimens.
        Performs checks.
        If command can be performed, executes it.
        Otherwise, set response to appropriate error.
        Passes response to Legilimens.
    """
    verb = command[0]
    args = command[1:]
    command = castle.commands.get(verb, None)
    if not command:
        # if handle_command is called by Legilimens, we'll never see this
        logger.error("handle_command called from outside Legilimens.execute by player %s in game %s", player.id, castle.name)
        raise RowlingError(Messages.UNKNOWN_VERB)

    castle.transaction()
    try:
        self.handle_auto_movements(castle)
        result = command.execute(*args)
    except MaraudersMapError:
        castle.rollback()
        raise RowlingError(Messages.BAD_STATE_CHANGE)
    castle.commit()

    return result if result else None


def handle_auto_movements(self, castle):
    """ Runs automated logic after every turn.
        Use to, e.g., release the basilisk at turn #100.
    """
    pass
