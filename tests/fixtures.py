from __future__ import absolute_import

from braga import Component, Assemblage, World

from core.components import Name
from core.systems import NameSystem
from engine.Command import Command, ChangefulCommand
from engine.exceptions import LogicError


DIRECTION_ERROR = "I don't know how to go that direction."
PATH_ERROR = "You can't go that way."


class Location(Component):

    INITIAL_PROPERTIES = ['location']

    def __init__(self, location=None):
        self.location = location


class Description(Component):

    INITIAL_PROPERTIES = ['description']

    def __init__(self, description=None):
        self.description = description


class Mapping(Component):

    INITIAL_PROPERTIES = ['paths']

    def __init__(self, paths=None):
        self.paths = paths if paths else dict()


class Direction(Component):
    pass


def _is_a_direction(world, entity):
    if not entity.has_component(Direction):
        raise LogicError(DIRECTION_ERROR)


def _path_exists(world, player, direction):
    if direction not in player.location.paths:
        raise LogicError(PATH_ERROR)


def _move_player(world, player, direction):
    new_location = player.location.paths[direction]
    player.location = new_location


def _look(world, player):
    return player.location.description


look = Command(name='look', response=_look)
go = ChangefulCommand(name='go', syntax=[_is_a_direction], rules=[_path_exists], state_changes=[_move_player], response=_look)
commands = {'look': look, 'go': go}

room_factory = Assemblage(components=[Description, Mapping])


def make_toy_world():
    world = World()
    name_system = NameSystem(world)
    player = world.make_entity(Assemblage(components=[Location]))
    for direction_name, direction_shorthand in [
            ('north', 'n'),
            ('south', 's'),
            ('east', 'e'),
            ('west', 'w'),
            ('up', 'u'),
            ('down', 'd')]:
        direction_entity = world.make_entity(
            Assemblage(components=[Direction, Name]),
            name=direction_name)
        name_system.add_name(direction_name, direction_entity)
        name_system.add_name(direction_shorthand, direction_entity)

        if direction_name == 'north':
            north = direction_entity
        if direction_name == 'south':
            south = direction_entity

    room_one = world.make_entity(
        room_factory,
        description="You are in room one.")
    room_two = world.make_entity(
        room_factory,
        description="You are in room two.")
    room_one.paths = {north: room_two}
    room_two.paths = {south: room_one}

    player.location = room_one

    return world, name_system, player, room_one, room_two
