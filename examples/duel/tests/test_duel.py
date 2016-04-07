import unittest

from braga import World
from braga.examples import duel

from engine.exceptions import StateError, LogicError, ParserError
from engine.Parser import Parser
from examples.duel.commands import equip, expelliarmus, set_expelliarmus_skill, get_expelliarmus_skill, give_away_wand


class TestExpelliarmusHelperCommands(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.world.add_system(duel.ContainerSystem)
        self.world.add_system(duel.EquipmentSystem)
        self.world.add_system(duel.NameSystem)

        room = self.world.make_entity(duel.room_factory, name="duel room", description="test room")
        self.player = self.world.make_entity(
            duel.player_factory,
            name="you",
            description="You are a test",
            location=room)
        self.wand = self.world.make_entity(
            duel.wand_factory,
            description="Surprisingly swishy.",
            location=self.player,
            name="your wand",
            owner=self.player)
        self.world.systems[duel.EquipmentSystem].equip(self.player, self.wand)
        self.world.refresh()

    def test_set(self):
        try:
            set_expelliarmus_skill(self.world, self.player, 10)
        except (StateError, LogicError, ParserError):
            self.fail("correct usage of `set` should not raise an error")
        self.assertEqual(self.player.skill, 10)

    def test_set_non_integer_skill(self):
        initial_skill = self.player.skill
        with self.assertRaises(LogicError):
            set_expelliarmus_skill(self.world, self.player, self.wand)
        self.assertEqual(self.player.skill, initial_skill)

    def test_set_out_of_range_skill(self):
        initial_skill = self.player.skill
        with self.assertRaises(LogicError):
            set_expelliarmus_skill(self.world, self.player, 1000000)
        self.assertEqual(self.player.skill, initial_skill)

    def test_get(self):
        try:
            get_expelliarmus_skill(self.world, self.player)
        except (StateError, LogicError, ParserError):
            self.fail("correct usage of `get` should not raise an error")


class TestEquipCommand(unittest.TestCase):

    def setUp(self):
        world = World()
        world.add_system(duel.ContainerSystem)
        world.add_system(duel.EquipmentSystem)
        world.add_system(duel.NameSystem)

        room = world.make_entity(duel.room_factory, name="duel room", description="test room")
        self.player = world.make_entity(
            duel.player_factory,
            name="you",
            description="You are a test",
            location=room)
        self.wand = world.make_entity(
            duel.wand_factory,
            description="Surprisingly swishy.",
            location=self.player,
            name="your wand",
            owner=self.player)
        self.other_wand = world.make_entity(
            duel.wand_factory,
            description="Yep, that Elder Wand",
            location=room,
            name="elder wand")

        world.systems[duel.EquipmentSystem].auto_update = True
        world.systems[duel.EquipmentSystem].equip(self.player, self.wand)
        world.refresh()

        self.parser = Parser(
            world,
            world.systems[duel.NameSystem],
            self.player,
            {'equip': equip}
        )

    def test_can_equip_wand_in_inventory(self):
        self.assertEqual(self.player.wand, self.wand)
        self.parser.world.systems[duel.ContainerSystem].move(self.other_wand, self.player, True)

        try:
            equip(self.parser.world, self.player, self.other_wand)
        except LogicError:
            self.fail("correct syntax for `equip` should not raise an error")

        self.assertEqual(self.player.wand, self.other_wand)
        # self.assertIsNone(self.wand.bearer)
        self.assertEqual(self.player, self.wand.owner)
        # self.assertEqual(self.player, self.other_wand.bearer)
        self.assertIsNone(self.other_wand.owner)

    def test_cannot_equip_wand_not_in_inventory(self):
        self.assertEqual(self.player.wand, self.wand)
        with self.assertRaises(LogicError) as e:
            equip(self.parser.world, self.player, self.other_wand)
        self.assertEqual(e.exception.message, "You are not carrying that.")
        self.assertEqual(self.player.wand, self.wand)

    def test_parser_integration_correct_syntax(self):
        self.assertEqual(self.player.wand, self.wand)
        self.parser.world.systems[duel.ContainerSystem].move(self.other_wand, self.player, True)
        try:
            self.parser.execute('equip elder wand')
        except (StateError, LogicError, ParserError):
            self.fail("correct syntax for `equip` should not raise an error")
        self.assertEqual(self.player.wand, self.other_wand)


class TestExpelliarmusCommand(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.world.add_system(duel.ContainerSystem)
        self.world.add_system(duel.EquipmentSystem)
        self.world.add_system(duel.NameSystem)

        room = self.world.make_entity(duel.room_factory, name="duel room", description="test room")
        self.player = self.world.make_entity(duel.player_factory, name="you", description="You are a test", location=room)
        self.opponent = self.world.make_entity(duel.player_factory, name="them", description="They are a test opponent", location=room)
        self.wand = self.world.make_entity(
            duel.wand_factory,
            description="Surprisingly swishy.",
            location=self.player,
            name="your wand",
            owner=self.player)
        self.other_wand = self.world.make_entity(
            duel.wand_factory,
            description="Yep, that Elder Wand",
            location=room,
            name="elder wand")

        self.world.systems[duel.ContainerSystem].auto_update = True
        self.world.systems[duel.EquipmentSystem].auto_update = True
        self.world.systems[duel.ContainerSystem].move(self.wand, self.player)
        self.world.systems[duel.EquipmentSystem].equip(self.player, self.wand)
        self.world.systems[duel.ContainerSystem].move(self.other_wand, self.opponent)
        self.world.refresh()

    def test_bad_syntax(self):
        with self.assertRaises(LogicError) as e:
            expelliarmus(self.world, self.player, self.wand)
        self.assertEqual(e.exception.message, "You can only perform that action on other people!")

    def test_cannot_cast_expelliarmus_on_yourself(self):
        try:
            self.player.skill = 100
            expelliarmus(self.world, self.player, self.player)
        except LogicError:
            self.fail("You can cast on yourself")

    def test_cannot_cast_on_wandless_player(self):
        with self.assertRaises(AttributeError):
            self.opponent.wand
        self.player.skill = 100
        with self.assertRaises(LogicError) as e:
            expelliarmus(self.world, self.player, self.opponent)
        self.assertEqual(e.exception.message, "Nothing happens. Your opponent is not carrying their wand!")

    def test_wandless_player_cannot_cast_expelliarmus(self):
        self.world.systems[duel.EquipmentSystem].unequip(self.player, self.wand)
        self.world.systems[duel.EquipmentSystem].equip(self.opponent, self.other_wand)
        self.world.refresh()

        with self.assertRaises(AttributeError):
            self.player.wand
        self.assertTrue(self.opponent.wand)
        with self.assertRaises(LogicError) as e:
            expelliarmus(self.world, self.player, self.opponent)
        self.assertEqual(e.exception.message, "Nothing happens.")

    def test_setup_of_wand(self):
        self.assertEqual(self.player.wand.owner, self.player)
        self.assertEqual(self.player.wand.bearer, self.player)


class TestGiveCommand(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.world.add_system(duel.ContainerSystem)
        self.world.add_system(duel.EquipmentSystem)
        self.world.add_system(duel.NameSystem)

        room = self.world.make_entity(duel.room_factory, name="duel room", description="test room")
        self.player = self.world.make_entity(duel.player_factory, name="you", description="You are a test", location=room)
        self.opponent = self.world.make_entity(duel.player_factory, name="them", description="They are a test opponent", location=room)
        self.wand = self.world.make_entity(
            duel.wand_factory,
            description="Surprisingly swishy.",
            location=self.player,
            name="your wand",
            owner=self.player)
        self.other_wand = self.world.make_entity(
            duel.wand_factory,
            description="Yep, that Elder Wand",
            location=room,
            name="elder wand")

        self.world.systems[duel.ContainerSystem].auto_update = True
        self.world.systems[duel.EquipmentSystem].auto_update = True
        self.world.systems[duel.ContainerSystem].move(self.wand, self.player)
        self.world.systems[duel.EquipmentSystem].equip(self.player, self.wand)
        self.world.systems[duel.ContainerSystem].move(self.other_wand, self.player)
        self.world.refresh()

    # def test_full_parser_integration(self):
    #     try:
    #         self.parser.execute('give my wand to justin')
    #     except Exception:
    #         self.fail("That is correct syntax")

    #     self.assertIn(self.justin_wand, self.player.inventory)
    #     self.assertIn(self.wand, self.justin.inventory)
    #     self.assertIn(self.wand, self.justin.equipment)

    def test_command_execute_with_correct_syntax(self):
        try:
            give_away_wand(self.world, self.player, self.wand, self.opponent)
        except LogicError:
            self.fail("That is correct syntax")

        self.assertIn(self.other_wand, self.player.inventory)
        self.assertEqual(self.wand.bearer, self.opponent)
        self.assertNotIn(self.wand, self.player.inventory)
        self.assertIsNone(self.other_wand.bearer)
        self.assertIn(self.wand, self.opponent.inventory)
