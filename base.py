from Command import Command, ChangefulCommand
from hogwartsexceptions import RowlingError, Messages


class Player(object):
    def __init__(self, username, description=None, inventory=None, location=None):
        self.username = username
        self.description = description
        self.inventory = inventory if inventory else []
        self.location = location

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.description

    def __contains__(self, thing):
        return thing in self.inventory


class Room(object):
    def __init__(self, name, description=None, inventory=None, paths=None):
        self.name = name
        self.description = description
        self.inventory = inventory if inventory else []
        self.paths = paths if paths else {}

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.description

    def __contains__(self, thing):
        return thing in self.inventory


class Thing(object):
    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.description


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


def location_description(castle, player):
    return str(player.location)


look = Command(name='look', response=location_description)
go = ChangefulCommand(
    name='go',
    syntax=[is_a_direction],
    rules=[path_exists],
    state_changes=[move_player],
    response=location_description)
