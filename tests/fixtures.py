from mock import Mock, MagicMock

from braga.models import Entity, Component

from engine.Command import Command, ChangefulCommand
from engine.exceptions import LogicError
from engine.StateManager import StateManager


class TestPlayer(object):
    def __init__(self, id=1, username='zork', location=None):
        self.id = id
        self.username = username
        self.location = location


class TestRoom(object):
    def __init__(self, name):
        self.name = name


class TestCommand(object):
    def __init__(self):
        self.rules = []


class Description(Component):

    def __init__(self, description=None):
        self.description = description


class Mapping(Component):

    def __init__(self, paths=None):
        self.paths = paths if paths else dict()


class Container(Component):

    def __init__(self, inventory=None):
        self._inventory = set()
        if inventory:
            self._inventory |= inventory

    @property
    def inventory(self):
        return self._inventory

    def pick_up(self, thing):
        self._inventory.add(thing)

    def put_down(self, thing):
        self._inventory.remove(thing)

    def print_inventory(self):
        return '\n'.join([thing.name for thing in self.inventory])


class Location(Component):

    def __init__(self, location=None):
        self.location = location


class CommandTestBase(object):

    def create_stuff(self):
        self.room_one = Entity()
        self.room_two = Entity()

        room_one_description = Description("You are in room one.")
        room_one_mapping = Mapping({'n': self.room_two})
        self.room_one.components.add(room_one_description)
        self.room_one.components.add(room_one_mapping)

        room_two_description = Description("You are in room two.")
        room_two_mapping = Mapping({'s': self.room_one})
        self.room_two.components.add(room_two_description)
        self.room_two.components.add(room_two_mapping)

        self.castle = StateManager('commandtest', 'initstate')
        self.castle.directions = set(['n', 's', 'e', 'w'])

        self.player = Entity()
        player_location = Location(self.room_one)
        self.player.components.add(player_location)

        self.look = Command(name='look', response=self._look)
        self.go = ChangefulCommand(name='go', syntax=[self._is_a_direction], rules=[self._path_exists], state_changes=[self._move_player], response=self._look)

        self.castle.commands = {'look': self.look, 'go': self.go}
        self.castle.canonicals = set(['look', 'go', 'n', 'e', 'w', 's'])
        self.castle.noncanonicals = {'north': 'n', 'east': 'e', 'west': 'w', 'south': 's'}

        self.direction_error = "I don't know how to go that direction."
        self.path_error = "You can't go that way."

    def _is_a_direction(self, castle, word):
        if word not in castle.directions:
            raise LogicError(self.direction_error)

    def _path_exists(self, castle, player, direction):
        if direction not in player.location.paths:
            raise LogicError(self.path_error)

    def _move_player(self, castle, player, direction):
        new_location = player.location.paths[direction]
        player.location = new_location

    def _look(self, castle, player):
        return player.location.description
