import random

from engine.Command import Command, ChangefulCommand
from engine.exceptions import LogicError
from .components import EquipmentBearing, Equippable


# Command Responses
def _look(castle, player):
    return player.location.description


def _inventory(castle, player):
    return player.print_inventory()


def _red_sparks(castle, player):
    return "A stream of red sparks shoots out the end of your wand!"


def _get_skill(castle, player):
    return str(player.expelliarmus_skill)


def _describe_wand(castle, player):
    return "You are using {}".format(player.wand.name.lower())


def _summarize_game(castle, player):
    summary = "You are carrying:\n{inventory} \
        \n\nYour expelliarmus skill is: {skill}".format(
        inventory='\t'+'\n\t'.join(player.print_inventory().split('\n')),
        skill=str(player.expelliarmus_skill))
    if hasattr(player, 'wand'):
        summary = summary + "\n\nYou are using {wand}.".format(wand=player.wand.name.lower())
    justin = castle.players['justin']
    if hasattr(justin, 'wand'):
        summary = summary + "\n\nJustin is using {wand}.".format(wand=justin.wand.name.lower())
    return summary


def _describe_someone_else_wand(castle, player):
    return "Justin is using {}".format(castle.players['justin'].wand.name.lower())


# Syntax
def _is_a_player(castle, word):
    if word not in castle.players.keys():
        raise LogicError("You can only perform that action on other people!")


def _is_expelliarmus(castle, word):
    if word != 'expelliarmus':
        raise LogicError("You can only set your skill for expelliarmus.")


def _is_valid_number(castle, word):
    try:
        int(word)
    except ValueError:
        raise LogicError("You must use an integer skill level.")


# Rules
def _is_in_same_room(castle, player, other_player_name):
    other_player = castle.players.get(other_player_name)
    if player.location != other_player.location:
        raise LogicError("You're too far away to do that!")


def _has_a_wand(castle, player, other_player_name):
    other_player = castle.players.get(other_player_name)
    try:
        other_player.wand
    except AttributeError:
        raise LogicError("Nothing happens. Your opponent is not carrying their wand!")


def _player_can_successfully_cast_expelliarmus(castle, player, other_player_name):
    player_skill = 0
    if hasattr(player, 'wand'):
        player_skill += 1
        if player.wand.owner == player:
            player_skill += 4

    if hasattr(player, 'wand') and hasattr(player, 'expelliarmus_skill'):
        player_skill += player.expelliarmus_skill

    if player_skill < random.randint(1, 20):
        raise LogicError("Nothing happens.")


def _legal_skill_level(castle, player, word, skill):
    skill = int(skill)
    if not 0 < skill <= 15:
        raise LogicError("Skill levels range from 0 to 15.")


def _is_in_inventory(castle, player, *args):
    name_of_thing = ' '.join(args)
    thing = player.get_thing(name_of_thing)
    if not thing:
        raise LogicError("You are not carrying that.")


def _is_equippable(castle, player, *args):
    name_of_thing = ' '.join(args)
    thing = player.get_thing(name_of_thing)
    if not thing.has_component(Equippable):
        raise LogicError("You cannot equip that.")


# State Changes
def _confiscate_wand(castle, player, other_player_name):
    other_player = castle.players.get(other_player_name)
    other_player_wand = other_player.wand
    other_player_equipment = other_player.get_component(EquipmentBearing)
    other_player_equipment.unequip(other_player_wand)
    other_player.put_down(other_player_wand)
    player.pick_up(other_player_wand)


def _increase_expelliarmus_skill(castle, player, other_player_name):
    if player.expelliarmus_skill < 15:
        player.expelliarmus_skill += 1


def _set_expelliarmus_skill(castle, player, word, skill):
    level = int(skill)
    player.expelliarmus_skill = level


def _equip_object(castle, player, *args):
    name_of_thing = ' '.join(args)
    thing = player.get_thing(name_of_thing)
    if hasattr(player, thing.equip_name):
        existing_thing = getattr(player, thing.equip_name)
        player.unequip(existing_thing)
    player.equip(thing)


def _equip_someone_else(castle, player, *args):
    args_list = list(args)
    name = [word for word in args_list if word in castle.players.keys()]
    if len(name) != 1:
        raise LogicError("I do not know who you are talking about.")
    args_list.remove(name[0])
    _is_in_inventory(castle, player, *args_list)
    _is_equippable(castle, player, *args_list)
    other_player = castle.players[name[0]]
    name_of_thing = ' '.join(args_list)
    thing = player.get_thing(name_of_thing)
    if thing in player.equipment:
        player.unequip(thing)
    player.put_down(thing)
    other_player.pick_up(thing)
    _equip_object(castle, other_player, *args_list)


# Standard Commands
look = Command(name='look', response=_look)
inventory = Command(name='inventory', response=_inventory)

# Variable-success Commands
expelliarmus = ChangefulCommand(
    name='expelliarmus',
    syntax=[_is_a_player],
    rules=[_is_in_same_room, _has_a_wand, _player_can_successfully_cast_expelliarmus],
    state_changes=[_confiscate_wand, _increase_expelliarmus_skill],
    response=_red_sparks)

# General management Commands
equip = ChangefulCommand(
    name='equip',
    rules=[_is_in_inventory, _is_equippable],
    state_changes=[_equip_object],
    response=_describe_wand)

give_away_wand = ChangefulCommand(
    name='give',
    state_changes=[_equip_someone_else],
    response=_describe_someone_else_wand)

get_game_state = Command(
    name='state',
    response=_summarize_game)

set_expelliarmus_skill = ChangefulCommand(
    name='set',
    syntax=[_is_expelliarmus, _is_valid_number],
    rules=[_legal_skill_level],
    state_changes=[_set_expelliarmus_skill],
    response=_get_skill)

get_expelliarmus_skill = Command(
    name='check',
    syntax=[_is_expelliarmus],
    response=_get_skill)


commands = {
    'look': look,
    'inventory': inventory,
    'expelliarmus': expelliarmus,
    'set': set_expelliarmus_skill,
    'check': get_expelliarmus_skill,
    'state': get_game_state,
    'equip': equip,
    'give': give_away_wand
}
