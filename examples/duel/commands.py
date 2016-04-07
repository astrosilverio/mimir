import random

from braga import Aspect
from braga.examples import duel

from engine.Command import Command, ChangefulCommand
from engine.exceptions import LogicError

player_aspect = Aspect.make_from(duel.player_factory)


# Command Responses
def _look(world, player):
    return player.location.description


def _inventory(world, player):
    return '/n'.join([thing.name for thing in player.inventory])


def _red_sparks(world, player):
    return "A stream of red sparks shoots out the end of your wand!\n\nJustin's wand spins out of his hand and flies to you.\nYour casting skill for the expelliarmus spell has increased."


def _get_skill(world, player):
    return "\n".join([str(player.skill), "Your chance of success is {}/20.".format(_get_expelliarmus_skill(player))])


def _describe_wand(world, player):
    return "You are using {}".format(player.wand.name.lower())


def _summarize_game(world, player):
    summary = "You are carrying:\n{inventory} \
        \n\nYour expelliarmus skill is: {skill}".format(
        inventory='\t'+'\n\t'.join(_inventory(world, player).split('\n')),
        skill=str(player.skill))
    if hasattr(player, 'wand'):
        summary = summary + "\n\nYou are using {wand}.".format(wand=player.wand.name.lower())
    other_players = world.entities_with_aspect(player_aspect) - set([player])
    for other_player in other_players:
        if hasattr(other_player, 'wand'):
            summary = summary + "\n\n{name} is using {wand}.".format(name=other_player.name, wand=other_player.wand.name)
    return summary


# Syntax
def _is_a_player(world, entity):
    if entity not in player_aspect:
        raise LogicError("You can only perform that action on other people!")


def _is_expelliarmus(world, word):
    if word != 'expelliarmus':
        raise LogicError("You can only set your skill for expelliarmus.")


def _is_valid_number(world, word):
    try:
        int(word)
    except TypeError, ValueError:
        raise LogicError("You must use an integer skill level.")


# Rules
def _is_in_same_room(world, player, other_player):
    if player.location != other_player.location:
        raise LogicError("You're too far away to do that!")


def _has_a_wand(world, player, other_player):
    try:
        other_player.wand
    except AttributeError:
        raise LogicError("Nothing happens. Your opponent is not carrying their wand!")


def _get_expelliarmus_skill(player):
    player_skill = 0
    if hasattr(player, 'wand'):
        player_skill += 1
        if player.wand.owner == player:
            player_skill += 4

    if hasattr(player, 'wand') and hasattr(player, 'skill'):
        player_skill += player.skill
    return player_skill


def _player_can_successfully_cast_expelliarmus(world, player, other_player):
    player_skill = _get_expelliarmus_skill(player)
    if player_skill < random.randint(1, 20):
        raise LogicError("Nothing happens.")


def _legal_skill_level(world, player, skill):
    skill = int(skill)
    if not 0 < skill <= 15:
        raise LogicError("Skill levels range from 0 to 15.")


def _is_in_inventory(world, player, thing):
    if thing not in player.inventory:
        raise LogicError("You are not carrying that.")


def _is_equippable(world, entity):
    if not entity.has_component(duel.Equipment):
        raise LogicError("You cannot equip that.")


# State Changes
def _confiscate_wand(world, player, other_player):
    other_player_wand = other_player.wand
    world.systems[duel.EquipmentSystem].unequip(other_player, other_player_wand)
    world.systems[duel.ContainerSystem].move(other_player_wand, player)


def _increase_expelliarmus_skill(world, player, other_player):
    if player.skill < 15:
        player.skill += 1


def _set_expelliarmus_skill(world, player, skill):
    level = int(skill)
    player.skill = level


def _equip_object(world, player, thing):
    try:
        existing_equipped_object = player.__getattribute__(thing.equipment_type)
    except AttributeError:
        pass
    else:
        world.systems[duel.EquipmentSystem].unequip(player, existing_equipped_object)
    world.systems[duel.EquipmentSystem].equip(player, thing)


def _equip_someone_else(world, player, equippable, other_player):
    if equippable.bearer == player:
        world.systems[duel.EquipmentSystem].unequip(player, equippable)
    world.systems[duel.ContainerSystem].move(equippable, other_player)
    _equip_object(world, other_player, equippable)


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
    syntax=[_is_equippable],
    rules=[_is_in_inventory],
    state_changes=[_equip_object],
    response=_describe_wand)

give_away_wand = ChangefulCommand(
    name='give',
    syntax=[_is_equippable, _is_a_player],
    state_changes=[_equip_someone_else],
    response=_summarize_game)

get_game_state = Command(
    name='state',
    response=_summarize_game)

set_expelliarmus_skill = ChangefulCommand(
    name='set',
    syntax=[_is_valid_number],
    rules=[_legal_skill_level],
    state_changes=[_set_expelliarmus_skill],
    response=_get_skill)

get_expelliarmus_skill = Command(
    name='check',
    response=_get_skill)


commands = {
    'look': look,
    'inventory': inventory,
    'expelliarmus': expelliarmus,
    'set': set_expelliarmus_skill,
    'check': get_expelliarmus_skill,
    'state': get_game_state,
    'equip': equip,
    'use': equip,
    'give': give_away_wand
}
