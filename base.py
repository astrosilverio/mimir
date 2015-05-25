from collections import defaultdict
import random

from Command import Command, ChangefulCommand
from hogwartsexceptions import RowlingError, Messages


class Player(object):
    def __init__(self, username, inventory=None, location=None):
        self.username = username
        self.inventory = inventory if inventory else set()
        self.location = location

    def __repr__(self):
        return self.username.title()

    def __str__(self):
        return self.resting_description

    def __contains__(self, thing):
        return thing in self.inventory

    @property
    def resting_description(self):
        return "{} is here.".format(repr(self))


class Room(object):
    def __init__(self, name, description=None, inventory=None, paths=None):
        self.name = name
        self.description = description
        self.inventory = inventory if inventory else set()
        self.paths = paths if paths else {}

    def __repr__(self):
        return self.name.title()

    def __str__(self):
        base_description = self.description
        contents_descriptions = "\n".join([i.resting_description for i in self.inventory])
        return "\n\n".join([base_description, contents_descriptions])

    def __contains__(self, thing):
        return thing in self.inventory


class Thing(object):

    ARTICLES = defaultdict(lambda: 'a')
    ARTICLES['vowel'] = 'an'
    ARTICLES['plural'] = 'some'
    ARTICLES['proper'] = 'the'

    VERB_ENDINGS = defaultdict(lambda: 's')
    VERB_ENDINGS['plural'] = ''

    RESTING_DESCRIPTORS = [
        "{article} {noun} lie{verb_ending} on the ground here.",
    ]

    def __init__(self, name, description=None, word_type=None):
        self.name = name
        self.description = description
        self.word_type = word_type

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.description

    @property
    def resting_description(self):
        descriptor = random.choice(self.RESTING_DESCRIPTORS)
        return descriptor.format(
            article=self.ARTICLES[self.word_type].title(),
            noun=repr(self),
            verb_ending=self.VERB_ENDINGS[self.word_type])


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
