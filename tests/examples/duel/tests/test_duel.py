import unittest

from engine.exceptions import StateError, LogicError, ParserError
from engine.Parser import Parser
from tests.examples.duel.duel import setup_castle, setup_player
from tests.examples.duel.commands import equip, expelliarmus, inventory, look, set_expelliarmus_skill, get_expelliarmus_skill, give_away_wand
from tests.examples.duel.components import make_room, make_wand


class TestExpelliarmusHelperCommands(unittest.TestCase):

    def setUp(self):
        room = make_room(name="duel room", description="test room")
        self.player = setup_player(name="You", description="You are a test", location=room, wand_description="Imaginary")
        self.castle = setup_castle(
            players={'me': self.player},
            commands={'set': set_expelliarmus_skill, 'check': get_expelliarmus_skill},
            canonicals=set(['set', 'check', 'expelliarmus', 'justin']),
            noncanonicals={})
        self.parser = Parser(self.player, self.castle)

    def test_set(self):
        try:
            response = self.parser.execute('set expelliarmus 10')
        except (StateError, LogicError, ParserError):
            self.fail("correct usage of `set` should not raise an error")

        self.assertEqual(response, '10\nYour chance of success is 15/20.')
        self.assertEqual(self.player.expelliarmus_skill, 10)

    def test_set_non_integer_skill(self):
        try:
            response = self.parser.execute('set expelliarmus justin')
        except (StateError, LogicError, ParserError):
            self.fail("incorrect usage of `set` should not raise an error")

        self.assertEqual(response, "You must use an integer skill level.")
        self.assertEqual(self.player.expelliarmus_skill, 0)

    def test_set_out_of_range_skill(self):
        response = self.parser.execute('set expelliarmus 100000')

        self.assertEqual(response, "Skill levels range from 0 to 15.")
        self.assertEqual(self.player.expelliarmus_skill, 0)

    def test_get(self):
        try:
            response = self.parser.execute('check expelliarmus skill')
        except (StateError, LogicError, ParserError):
            self.fail("correct usage of `get` should not raise an error")

        self.assertEqual(response, "0\nYour chance of success is 5/20.")


class TestEquipCommand(unittest.TestCase):

    def setUp(self):
        room = make_room(name="duel room", description="test room")
        self.player = setup_player(name="You", description="You are a test", location=room, wand_description="Imaginary")
        self.wand = self.player.wand
        self.other_wand = make_wand(name="elder wand", description="Yep, that Elder Wand")

        self.castle = setup_castle(
            players={'me': self.player},
            commands={'equip': equip},
            canonicals=set(['equip', 'elder', 'wand', 'your']),
            noncanonicals={'my': 'your'})
        self.parser = Parser(self.player, self.castle)

    def test_can_equip_wand_in_inventory(self):
        self.assertEqual(self.player.wand, self.wand)
        self.player.pick_up(self.other_wand)
        try:
            equip.execute(self.castle, self.player, 'elder', 'wand')
        except LogicError:
            self.fail("correct syntax for `equip` should not raise an error")
        self.assertEqual(self.player.wand, self.other_wand)
        self.assertIsNone(self.wand.bearer)
        self.assertEqual(self.player, self.wand.owner)
        self.assertEqual(self.player, self.other_wand.bearer)
        self.assertIsNone(self.other_wand.owner)

    def test_cannot_equip_wand_not_in_inventory(self):
        self.assertEqual(self.player.wand, self.wand)
        with self.assertRaises(LogicError) as e:
            equip.execute(self.castle, self.player, 'elder', 'wand')
        self.assertEqual(e.exception.message, "You are not carrying that.")
        self.assertEqual(self.player.wand, self.wand)

    def test_parser_integration_correct_syntax(self):
        self.assertEqual(self.player.wand, self.wand)
        self.player.pick_up(self.other_wand)
        try:
            self.parser.execute('equip elder wand')
        except (StateError, LogicError, ParserError):
            self.fail("correct syntax for `equip` should not raise an error")
        self.assertEqual(self.player.wand, self.other_wand)


class TestExpelliarmusCommand(unittest.TestCase):

    def setUp(self):
        room = make_room(name="duel room", description="test room")
        self.player = setup_player(name="You", description="You are a test", location=room, wand_name='your wand', wand_description="Imaginary")
        self.justin = setup_player(name="Justin", description="Test opponent.", location=room, wand_name="justin's wand", wand_description="Not real")
        self.castle = setup_castle(
            players={'me': self.player, 'justin': self.justin},
            commands={'expelliarmus': expelliarmus},
            canonicals=set(['expelliarmus', 'justin', 'wand', 'me']),
            noncanonicals={})
        self.parser = Parser(self.player, self.castle)

    def test_bad_syntax(self):
        with self.assertRaises(LogicError) as e:
            expelliarmus.execute(self.castle, self.player, 'wand')
        self.assertEqual(e.exception.message, "You can only perform that action on other people!")

    def test_can_cast_expelliarmus_on_yourself(self):
        try:
            self.player.expelliarmus_skill = 100
            expelliarmus.execute(self.castle, self.player, 'me')
        except LogicError:
            self.fail("You can cast on yourself")

    def test_cannot_cast_on_wandless_player(self):
        wand = self.justin.wand
        self.justin.unequip(wand)
        with self.assertRaises(AttributeError):
            self.justin.wand
        self.player.expelliarmus_skill = 100
        with self.assertRaises(LogicError) as e:
            expelliarmus.execute(self.castle, self.player, 'justin')
        self.assertEqual(e.exception.message, "Nothing happens. Your opponent is not carrying their wand!")

    def test_wandless_player_cannot_cast_expelliarmus(self):
        wand = self.player.wand
        self.player.unequip(wand)
        with self.assertRaises(AttributeError):
            self.player.wand
        self.assertTrue(self.justin.wand)
        with self.assertRaises(LogicError) as e:
            expelliarmus.execute(self.castle, self.player, 'justin')
        self.assertEqual(e.exception.message, "Nothing happens.")

    def test_setup_of_wand(self):
        self.assertEqual(self.player.wand.owner, self.player)
        self.assertEqual(self.player.wand.bearer, self.player)


class TestGiveCommand(unittest.TestCase):

    def setUp(self):
        room = make_room(name="duel room", description="test room")
        self.player = setup_player(name="You", description="You are a test", location=room, wand_name="your wand", wand_description="Imaginary")
        self.justin = setup_player(name="Justin", description="Test opponent.", location=room, wand_name="justin's wand", wand_description="Not real")
        self.castle = setup_castle(
            players={'me': self.player, 'justin': self.justin},
            commands={'give': give_away_wand},
            canonicals=set(['give', 'justin', 'wand', 'your']),
            noncanonicals={'my': 'your'})
        self.parser = Parser(self.player, self.castle)

        self.wand = self.player.wand

        self.justin_wand = self.justin.wand
        self.justin.unequip(self.justin_wand)
        self.justin.put_down(self.justin_wand)
        self.player.pick_up(self.justin_wand)

    def test_setup(self):
        self.assertIn(self.wand, self.player.inventory)
        self.assertIn(self.justin_wand, self.player.inventory)

        self.assertNotIn(self.justin_wand, self.justin.equipment)

    def test_full_parser_integration(self):
        try:
            self.parser.execute('give my wand to justin')
        except Exception:
            self.fail("That is correct syntax")

        self.assertIn(self.justin_wand, self.player.inventory)
        self.assertIn(self.wand, self.justin.inventory)
        self.assertIn(self.wand, self.justin.equipment)

    def test_command_execute_with_correct_syntax(self):
        try:
            give_away_wand.execute(self.castle, self.player, 'your', 'wand', 'justin')
        except LogicError:
            self.fail("That is correct syntax")

        self.assertIn(self.justin_wand, self.player.inventory)
        self.assertIn(self.wand, self.justin.inventory)
        self.assertIn(self.wand, self.justin.equipment)
