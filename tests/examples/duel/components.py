from braga import Component, Assemblage

from engine.exceptions import LogicError
from tests.fixtures import Description, Container, Location, Mapping


# Components
class Equippable(Component):

    def __init__(self, bearer=None, equip_name=None):
        self.bearer = bearer
        self.equip_name = equip_name


class ObjectLoyalty(Component):

    def __init__(self, owner=None):
        self.owner = owner


class EquipmentBearing(Component):

    def __init__(self, bearer=None):
        self.bearer = bearer
        self.equipment = set()

    def equip(self, thing):
        if not thing.has_component(Equippable):
            raise LogicError

        setattr(self, thing.equip_name, thing)
        thing.bearer = self.bearer
        self.equipment.add(thing)

    def unequip(self, thing):
        delattr(self, thing.equip_name)
        self.equipment.remove(thing)
        thing.bearer = None


class ExpelliarmusSkill(Component):

    def __init__(self, skill=None):
        self.expelliarmus_skill = skill if skill else 0


class Name(Component):

    def __init__(self, name=None):
        self.name = name


# Make room factory
room_factory = Assemblage()
room_factory.add_component(Name)
room_factory.add_component(Description)
room_factory.add_component(Container)
room_factory.add_component(Mapping)


def make_room(name=None, description=None, paths=None):
    room = room_factory.make()
    room.name = name
    room.description = description
    return room


# Make player factory
player_factory = Assemblage()
player_factory.add_component(Description)
player_factory.add_component(Container)
player_factory.add_component(Location)
player_factory.add_component(ExpelliarmusSkill)
player_factory.add_component(Name)
player_factory.add_component(EquipmentBearing)


def make_player(
        name=None,
        description=None,
        location=None):
    player = player_factory.make()
    player.name = name
    player.description = description
    player_equipment = player.get_component(EquipmentBearing)
    player_equipment.bearer = player
    if location:
        player.location = location
        location.pick_up(player)
    return player


# Make wand factory
wand_factory = Assemblage()
wand_factory.add_component(Description)
wand_factory.add_component(Name)
wand_factory.add_component(Equippable)
wand_factory.add_component(ObjectLoyalty)


def make_wand(description=None, name=None, player=None):
    wand = wand_factory.make()
    wand.description = description
    wand.name = name
    wand.equip_name = 'wand'
    wand.owner = player
    return wand
