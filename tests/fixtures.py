from mock import Mock, MagicMock

from base import Player
from Command import Command, ChangefulCommand

from hogwartsexceptions import RowlingError


class Fixtures(object):

    def create_stuff(self):
        room_one = MagicMock()
        room_one.__str__ = Mock(return_value="You are in room one.")
        room_two = MagicMock()
        room_two.__str__ = Mock(return_value="You are in room two.")
        room_one.paths = {'n': room_two}
        room_two.paths = {'s': room_one}

        self.castle = MagicMock()
        self.castle.directions = set(['n', 's', 'e', 'w'])

        self.player = Player('hermione', location=room_one)

        self.look = Command(name='look', response=self._look)
        self.go = ChangefulCommand(name='go', syntax=[self._is_a_direction], rules=[self._path_exists], state_changes=[self._move_player], response=self._look)

        self.castle.commands = {'look': self.look, 'go': self.go}

        self.direction_error = "I don't know how to go that direction."
        self.path_error = "You can't go that way."

    def _is_a_direction(self, castle, word):
        if word not in castle.directions:
            raise RowlingError(self.direction_error)

    def _path_exists(self, castle, player, direction):
        if direction not in player.location.paths:
            raise RowlingError(self.path_error)

    def _move_player(self, castle, player, direction):
        new_location = player.location.paths[direction]
        player.location = new_location

    def _look(self, castle, player):
        return str(player.location)
