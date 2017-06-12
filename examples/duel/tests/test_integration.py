from mock import patch
import unittest

from braga.examples import duel

from engine.exceptions import StateError, LogicError, ParserError
from examples.duel.duel import setUp as duel_setup
from examples.duel.commands import player_aspect


class TestInitialState(unittest.TestCase):

    def setUp(self):
        self.parser = duel_setup()
        self.world = self.parser.world
        self.player = self.parser.player

    def test_parser_attributes(self):
        self.assertIsNotNone(self.world)
        players = self.world.entities_with_aspect(player_aspect)
        self.assertEqual(len(players), 2)

        self.assertIsNotNone(self.player)
        self.assertEqual(self.player.name, "you")

    def test_parsing_attributes(self):
        self.assertItemsEqual(
            self.parser.commands.keys(),
            ['look', 'inventory', 'expelliarmus', 'set', 'check', 'state', 'equip', 'trade', 'use'])

    def test_player_attributes(self):
        self.assertEqual(
            self.player.description,
            "You stare trepidously down the table at Justin Finch-Fletchley.")
        self.assertEqual(self.player.location.name, "Duel Room")
        self.assertEqual(len(self.player.inventory), 1)
        self.assertEqual(self.player.inventory.pop().name, "your wand")
        self.assertEqual(self.player.name, "you")
        self.assertIsNotNone(self.player.wand)

    def test_justin_attributes(self):
        justin = self.parser.get_entity("justin")
        self.assertEqual(
            justin.description,
            "Justin Finch-Fletchley stares at you bullishly from the other end of the table.")
        self.assertEqual(justin.location.name, "Duel Room")
        self.assertEqual(len(justin.inventory), 1)
        self.assertEqual(justin.inventory.pop().name, "justin's wand")
        self.assertEqual(justin.name, "justin finch-fletchley")
        self.assertIsNotNone(justin.wand)


class TestBasicCommands(unittest.TestCase):

    def setUp(self):
        self.parser = duel_setup()

    def test_initial_inventory(self):
        try:
            response = self.parser.execute('inventory')
        except (StateError, LogicError, ParserError):
            self.fail("`inventory` should not raise an error")

        self.assertEqual(response, "your wand")

    def test_look(self):
        try:
            response = self.parser.execute('look')
        except (StateError, LogicError, ParserError):
            self.fail("`look` should not raise an error")

        self.assertEqual(response, self.parser.player.location.description)


class TestExpelliarmus(unittest.TestCase):

    def setUp(self):
        self.parser = duel_setup()

    def test_good_syntax(self):
        try:
            self.parser.execute('expelliarmus justin')
        except LogicError:
            self.fail("correct syntax of expelliarmus should not raise an error")

    def test_bad_syntax(self):
        response = self.parser.execute('expelliarmus his wand')
        self.assertEqual(response, "You can only perform that action on other people!")

    @patch('examples.duel.commands._get_expelliarmus_skill', return_value=20)
    def test_successful_expelliarmus(self, _):
        response = self.parser.execute('expelliarmus justin')
        # this is a bit gross
        self.assertEqual(
            response,
            "A stream of red sparks shoots out the end of your wand!\
\n\nJustin's wand spins out of his hand and flies to you.\
\nYour casting skill for the expelliarmus spell has increased.")


class TestExpelliarmusHelperCommands(unittest.TestCase):

    def setUp(self):
        self.parser = duel_setup()

    def test_set(self):
        try:
            response = self.parser.execute('set skill 10')
        except (StateError, LogicError, ParserError):
            self.fail("correct usage of `set` should not raise an error")

        self.assertEqual(response, '10\nYour chance of success is 15/20.')
        self.assertEqual(self.parser.player.skill, 10)

    def test_set_non_integer_skill(self):
        try:
            response = self.parser.execute('set skill my wand')
        except (StateError, LogicError, ParserError):
            self.fail("incorrect usage of `set` should not raise an error")

        self.assertEqual(response, "You must use an integer skill level.")
        self.assertEqual(self.parser.player.skill, 0)

    def test_set_out_of_range_skill(self):
        response = self.parser.execute('set skill 100000')

        self.assertEqual(response, "Skill levels range from 0 to 15.")
        self.assertEqual(self.parser.player.skill, 0)

    def test_get(self):
        try:
            response = self.parser.execute('check skill')
        except (StateError, LogicError, ParserError):
            self.fail("correct usage of `get` should not raise an error")

        self.assertEqual(response, "0\nYour chance of success is 5/20.")


class TestEquip(unittest.TestCase):

    def setUp(self):
        self.parser = duel_setup()
        self.parser.world.systems[duel.EquipmentSystem].unequip(
            self.parser.get_entity("justin"),
            self.parser.get_entity("justin's wand")
        )

    def test_can_equip_wand_in_inventory(self):
        self.parser.world.systems[duel.ContainerSystem].move(
            self.parser.get_entity("justin's wand"),
            self.parser.get_entity("you"))
        self.parser.world.refresh()
        try:
            response = self.parser.execute("equip justin's wand")
        except LogicError:
            self.fail("correct syntax for `equip` should not raise an error")

        self.assertEqual(response, "You are using justin's wand")

    def test_cannot_equip_wand_not_in_inventory(self):
        response = self.parser.execute("equip justin's wand")
        self.assertEqual(response, "You are not carrying that.")


class TestTrade(unittest.TestCase):

    def setUp(self):
        self.parser = duel_setup()

    def test_full_parser_integration(self):
        try:
            response = self.parser.execute('trade wands with justin')
        except Exception:
            self.fail("That is correct syntax")

        expected_response = "You are carrying:\n\tjustin's wand \
        \n\nYour expelliarmus skill is: {skill}\
\n\nYou are using justin's wand\
\n\njustin finch-fletchley is using your wand".format(skill=self.parser.player.skill)

        self.assertEqual(response, expected_response)
