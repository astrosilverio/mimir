import unittest

from hogwartsexceptions import Messages, RowlingError
from tests.fixtures import Fixtures


class TestCheckSyntax(unittest.TestCase, Fixtures):

    def setUp(self):
        super(TestCheckSyntax, self).create_stuff()

    def test_bad_syntax_too_many_args(self):
        with self.assertRaises(RowlingError) as e:
            self.go.check_syntax(self.castle, 'that', 'way')
        self.assertEqual(e.exception.message, Messages.TOO_MANY_ARGS)

    def test_bad_syntax_too_few_args(self):
        with self.assertRaises(RowlingError) as e:
            self.go.check_syntax(self.castle)
        self.assertEqual(e.exception.message, Messages.TOO_FEW_ARGS.format(self.go.name))

    def test_bad_syntax_wrong_args(self):
        with self.assertRaises(RowlingError) as e:
            self.go.check_syntax(self.castle, 'there')
        self.assertEqual(e.exception.message, self.direction_error)

    def test_correct_syntax_with_args(self):
        response = self.go.check_syntax(self.castle, 'n')
        self.assertEqual(response, None)


class TestCheckRules(unittest.TestCase, Fixtures):

    def setUp(self):
        super(TestCheckRules, self).create_stuff()

    def test_bad_rules_raises(self):
        with self.assertRaises(RowlingError) as e:
            self.go.check_rules(self.castle, self.player, 'e')
        self.assertEqual(e.exception.message, self.path_error)

    def test_good_rules_passes(self):
        response = self.go.check_rules(self.castle, self.player, 'n')
        self.assertEqual(response, None)


class TestExecuteCommand(unittest.TestCase, Fixtures):

    def setUp(self):
        super(TestExecuteCommand, self).create_stuff()

    def test_args_when_not_expected_raises(self):
        with self.assertRaises(RowlingError) as e:
            self.look.execute(self.castle, self.player, 'there')
        self.assertEqual(e.exception.message, Messages.TOO_MANY_ARGS)

    def test_successful_command_returns_desired_response(self):
        response = self.look.execute(self.castle, self.player)
        self.assertEqual(response, "You are in room one.")

    def test_successful_changeful_command_changes_state(self):
        response = self.go.execute(self.castle, self.player, 'n')
        self.assertEqual(response, "You are in room two.")

    def test_failed_changeful_command_does_not_change_state(self):
        with self.assertRaises(RowlingError):
            self.go.execute(self.castle, self.player, 'w')
        self.assertEqual(self._look(self.castle, self.player), "You are in room one.")
