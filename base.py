from Command import Command, ChangefulCommand
from hogwartsexceptions import RowlingError, Messages


class BaseStatefulThing(object):
    def __init__(self, description=None, inventory=None):
        self.description = description
        self.inventory = inventory

    def __str__(self):
        return self.description

    def __contains__(self, thing):
        return thing in self.inventory

class Player(object):
    def __init__(self, id, username, description=None, inventory=None):
        super(Player, self).__init__(description, inventory)
        self.username = username
        self.id = id

class Room(object):
    def __init__(self, description=None, inventory=None, paths=None):
        super(Room, self).__init__(description, inventory)
        self.paths = paths

class Thing(object):
    def __init__(self, description=None, inventory=None):
        super(Thing, self).__init__(description, inventory)


def is_a_direction(castle, word):
    if word not in castle.directions and word not in castle.passwords:
        raise RowlingError(Messages.DIRECTION_ERROR)


def path_exists(castle, player, direction):
    if direction in castle.passwords and direction not in player.location.paths:
        raise RowlingError(Messages.NOTHING_HAPPENS)
    if direction not in player.location.paths:
        raise RowlingError(Messages.PATH_ERROR)


def move_player(castle, player, direction):
    new_location = player.location.paths[direction]
    player.location = new_location


def _look(castle, player):
    return str(player.location)


look = Command(name='look', response=self._look)
go = ChangefulCommand(name='go',
    syntax=[is_a_direction],
    rules=[path_exists],
    state_changes=[move_player],
    response=_look)