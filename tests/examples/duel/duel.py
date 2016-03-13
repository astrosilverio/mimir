from __future__ import absolute_import

from braga import World
from braga.examples import duel

from engine.Parser import Parser
from tests.examples.duel.commands import commands


def setUp():
    # Make World
    duel_world = World()
    duel_world.add_system(duel.ContainerSystem)
    duel_world.add_system(duel.EquipmentSystem)

    # Make room
    duel_room = duel_world.make_entity(
        duel.room_factory,
        description="You are in a large, dusty room, standing at one end of a long wooden table. Someone has placed a sign on an easel that says 'Duelling club'. There is a door in the southwest corner."
    )

    # Make duellers
    player = duel_world.make_entity(
        duel.player_factory,
        description="You stare trepidously down the table at Justin Finch-Fletchley.",
        name="You")

    justin = duel_world.make_entity(
        duel.player_factory,
        description="Justin Finch-Fletchley stares at you bullishly from the other end of the table.",
        name="Justin Finch-Fletchley")

    # Make wands
    player_wand = duel_world.make_entity(
        duel.wand_factory,
        description="Surprisingly swishy.",
        name="your wand",
        owner=player)

    justin_wand = duel_world.make_entity(
        duel.wand_factory,
        description="Heavy but brittle.",
        name="justin's wand",
        owner=justin)

    castle = setup_castle(
        players={'me': player, 'justin': justin},
        commands=commands,
        canonicals=set(['look', 'inventory', 'expelliarmus', 'set', 'check', 'justin', 'wand', 'state', 'equip', "justin's", 'give']),
        noncanonicals={'use': 'equip', 'my': 'your'})

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
