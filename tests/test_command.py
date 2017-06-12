from __future__ import absolute_import
import unittest

from braga import Assemblage

from core.components import Name
from engine.exceptions import Messages, LogicError
from tests.fixtures import look, go, make_toy_world, PATH_ERROR, DIRECTION_ERROR


class TestCheckSyntax(unittest.TestCase):

    def setUp(self):
        self.world, self.name_system, self.player, self.room_one, _ = make_toy_world()
        self.north = self.name_system.get_token_from_name('north')
        self.south = self.name_system.get_token_from_name('south')
        self.there = self.world.make_entity(Assemblage(components=[Name]), name='there')

    def test_bad_syntax_too_many_args(self):
        with self.assertRaises(LogicError) as e:
            go.check_syntax(self.world, self.north, self.south)
        self.assertEqual(e.exception.message, Messages.TOO_MANY_ARGS)
        self.assertEqual(self.player.location, self.room_one)

    def test_bad_syntax_too_few_args(self):
        with self.assertRaises(LogicError) as e:
            go.check_syntax(self.world)
        self.assertEqual(e.exception.message, Messages.TOO_FEW_ARGS.format(go.name))

    def test_bad_syntax_wrong_args(self):
        with self.assertRaises(LogicError) as e:
            go.check_syntax(self.world, self.there)
        self.assertEqual(e.exception.message, DIRECTION_ERROR)

    def test_correct_syntax_with_args(self):
        response = go.check_syntax(self.world, self.north)
        self.assertEqual(response, None)


class TestCheckRules(unittest.TestCase):

    def setUp(self):
        self.world, self.name_system, self.player, _, __ = make_toy_world()

    def test_bad_rules_raises(self):
        with self.assertRaises(LogicError) as e:
            go.check_rules(self.world, self.player, self.name_system.get_token_from_name('east'))
        self.assertEqual(e.exception.message, PATH_ERROR)

    def test_good_rules_passes(self):
        response = go.check_rules(self.world, self.player, self.name_system.get_token_from_name('north'))
        self.assertEqual(response, None)


class TestExecuteCommand(unittest.TestCase):

    def setUp(self):
        self.world, self.name_system, self.player, _, __ = make_toy_world()
        self.there = self.world.make_entity(Assemblage(components=[Name]), name='there')

    def test_args_when_not_expected_raises(self):
        with self.assertRaises(LogicError) as e:
            look(self.world, self.player, self.there)
        self.assertEqual(e.exception.message, Messages.TOO_MANY_ARGS)

    def test_successful_command_returns_desired_response(self):
        response = look(self.world, self.player)
        self.assertEqual(response, "You are in room one.")

    def test_successful_changeful_command_changes_state(self):
        response = go(self.world, self.player, self.name_system.get_token_from_name('north'))
        self.assertEqual(response, "You are in room two.")

    def test_failed_changeful_command_does_not_change_state(self):
        with self.assertRaises(LogicError):
            go(self.world, self.player, self.name_system.get_token_from_name('west'))
        self.assertEqual(look(self.world, self.player), "You are in room one.")
