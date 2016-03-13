from mock import patch
import unittest

from engine.exceptions import StateError, LogicError, ParserError
from tests.examples.duel.duel import setUp as duel_setup


class TestInitialState(unittest.TestCase):

    def setUp(self):
        self.parser = duel_setup()
        self.castle = self.parser.castle
        self.player = self.parser.player

    def test_parser_attributes(self):
        self.assertIsNotNone(self.castle)
        self.assertItemsEqual(self.castle.players.keys(), ['me', 'justin'])

        self.assertIsNotNone(self.player)
        self.assertEqual(self.player.name, "You")

    def test_castle_attributes(self):
        self.assertItemsEqual(self.castle.players.keys(), ['me', 'justin'])
        self.assertItemsEqual(
            self.castle.commands.keys(),
            ['look', 'inventory', 'expelliarmus', 'set', 'check', 'state', 'equip', 'give'])
        self.assertItemsEqual(self.castle.noncanonicals.keys(), ['use', 'my'])

    def test_player_attributes(self):
        self.assertEqual(
            self.player.description,
            "You stare trepidously down the table at Justin Finch-Fletchley.")
        self.assertEqual(self.player.location.name, "Duel Room")
        self.assertEqual(self.player.print_inventory(), "your wand")
        self.assertEqual(self.player.name, "You")

    def test_justin_attributes(self):
        justin = self.castle.players['justin']
        self.assertEqual(
            justin.description,
            "Justin Finch-Fletchley stares at you bullishly from the other end of the table.")
        self.assertEqual(justin.location.name, "Duel Room")
        self.assertEqual(justin.print_inventory(), "justin's wand")
        self.assertEqual(justin.name, "Justin Finch-Fletchley")


class TestBasicCommands(unittest.TestCase):

    def setUp(self):
        self.parser = duel_setup()

    def test_initial_inventory(self):
        try:
            response = self.parser.execute('inventory')
        except (StateError, LogicError, ParserError):
            self.fail("`inventory` should not raise an error")

        self.assertEqual(response, self.parser.player.print_inventory())

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
        response = self.parser.execute('expelliarmus wand')
        self.assertEqual(response, "You can only perform that action on other people!")

        # Yuck
        player = self.parser.castle.players.get('me')
        justin = self.parser.castle.players.get('justin')

        # gotta have a better way of checking this than comparing strings?
        self.assertEqual(player.print_inventory(), 'your wand')
        self.assertEqual(justin.print_inventory(), "justin's wand")

    @patch('tests.examples.duel.commands._get_expelliarmus_skill', return_value=20)
    def test_successful_expelliarmus(self, _):
        player = self.parser.castle.players.get('me')
        initial_skill = player.expelliarmus_skill

        response = self.parser.execute('expelliarmus justin')
        # this is a bit gross
        self.assertEqual(
            response,
            "A stream of red sparks shoots out the end of your wand!\
\n\nJustin's wand spins out of his hand and flies to you.\
\nYour casting skill for the expelliarmus spell has increased.")

        justin = self.parser.castle.players.get('justin')

        self.assertEqual(player.expelliarmus_skill, initial_skill+1)
        # I don't know rn what the ordering will be here
        self.assertEqual(player.print_inventory(), "your wand\njustin's wand")
        self.assertEqual(justin.print_inventory(), "")
