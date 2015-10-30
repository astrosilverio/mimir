from __future__ import absolute_import

from engine.Parser import Parser
from engine.StateManager import StateManager
from tests.examples.duel.commands import commands
from tests.examples.duel.components import make_room, make_player, make_wand


def setup_player(name, description, location, wand_description, wand_name='wand'):
    player = make_player(description=description, location=location, name=name)
    player_wand = make_wand(description=wand_description, name=wand_name)
    player.equip(player_wand)
    player.pick_up(player_wand)
    return player


def setup_castle(players, commands, canonicals, noncanonicals):
    castle = StateManager('duelsim', 'init_state')
    castle.players = players
    castle.commands = commands
    castle.canonicals = canonicals
    castle.noncanonicals = noncanonicals
    return castle


def setUp():
    # Make room
    duel_room = make_room(
        name="Duel Room",
        description="You are in a large, dusty room, standing at one end of a long wooden table. Someone has placed a sign on an easel that says 'Duelling club'. There is a door in the southwest corner."
    )

    # Make duellers
    player = setup_player(
        description="You stare trepidously down the table at Justin Finch-Fletchley.",
        location=duel_room,
        wand_description="Surprisingly swishy.",
        name="You",
        wand_name="Your wand")

    justin = setup_player(
        description="Justin Finch-Fletchley stares at you bullishly from the other end of the table.",
        location=duel_room,
        wand_description="Heavy but brittle.",
        name="Justin Finch-Fletchley",
        wand_name="Justin's wand")

    castle = setup_castle(
        players={'me': player, 'justin': justin},
        commands=commands,
        canonicals=set(['look', 'inventory', 'expelliarmus', 'set', 'check', 'justin', 'wand', 'state']),
        noncanonicals={})

    parser = Parser(player, castle)
    return parser

if __name__ == '__main__':
    parser = setUp()
    while True:
        user_input = raw_input("> ").lower()
        if user_input == 'reset':
            parser = setUp()
        else:
            print parser.execute(user_input)
