import unittest
from mock import patch

from engine.Command import ChangefulCommand
from engine.exceptions import LogicError, Messages
from engine.LogicHandler import handle_command
from engine.Parser import Parser
from tests.fixtures import CommandTestBase


class TestHandleCommand(unittest.TestCase, CommandTestBase):

    def setUp(self):
        super(TestHandleCommand, self).create_stuff()

    @patch.object(ChangefulCommand, 'execute')
    def test_hc_calls_correct_command(self, go_mock):
        handle_command(self.castle, self.player, ['go', 'west'])
        go_mock.assert_called_once_with(self.castle, self.player, 'west')

    def test_hc_returns_sane_output_if_command_passes(self):
        result = handle_command(self.castle, self.player, ['go', 'n'])
        self.assertEqual(result, "You are in room two.")

    def test_hc_returns_sane_output_if_command_fails(self):
        with self.assertRaises(LogicError) as e:
            handle_command(self.castle, self.player, ['go', 'e'])

        self.assertEqual(e.exception.message, "You can't go that way.")


class TestParserIntegration(unittest.TestCase, CommandTestBase):

    def setUp(self):
        super(TestParserIntegration, self).create_stuff()
        self.parser = Parser(self.player, self.castle)

    def test_good_simple_input_returns_sane_output(self):
        response = self.parser.execute("look")
        self.assertEqual(response, "You are in room one.")

    def test_bad_simple_input_returns_sane_output(self):
        response = self.parser.execute("look n")
        self.assertEqual(response, Messages.TOO_MANY_ARGS)

    def test_good_complex_input_returns_sane_output(self):
        response = self.parser.execute("go n")
        self.assertEqual(response, "You are in room two.")

    def test_bad_complex_input_returns_sane_output(self):
        response = self.parser.execute("go e")
        self.assertEqual(response, self.path_error)


class TestStateIntegration(unittest.TestCase, CommandTestBase):

    def setUp(self):
        super(TestStateIntegration, self).create_stuff()

    def test_hc_state_changing_command_success_changes_state(self):
        handle_command(self.castle, self.player, ['go', 'n'])
        self.assertEqual(self.player.location, self.room_two)

    def test_hc_state_changing_command_failure_does_not_change_state(self):
        with self.assertRaises(LogicError):
            handle_command(self.castle, self.player, ['go', 's'])
        self.assertEqual(self.player.location, self.room_one)

    def test_hc_non_state_changing_command_does_not_change_state(self):
        handle_command(self.castle, self.player, ['look'])
        self.assertEqual(self.player.location, self.room_one)


class TestFullIntegration(unittest.TestCase, CommandTestBase):

    def setUp(self):
        super(TestFullIntegration, self).create_stuff()
        self.parser = Parser(self.player, self.castle)

    def test_good_simple_input_returns_sane_output(self):
        response = self.parser.execute("look")
        self.assertEqual(response, "You are in room one.")
        self.assertEqual(self.player.location, self.room_one)

    def test_bad_simple_input_returns_sane_output(self):
        response = self.parser.execute("look n")
        self.assertEqual(response, Messages.TOO_MANY_ARGS)
        self.assertEqual(self.player.location, self.room_one)

    def test_good_complex_input_returns_sane_output(self):
        response = self.parser.execute("go n")
        self.assertEqual(response, "You are in room two.")
        self.assertEqual(self.player.location, self.room_two)

    def test_bad_complex_input_returns_sane_output(self):
        response = self.parser.execute("go e")
        self.assertEqual(response, self.path_error)
        self.assertEqual(self.player.location, self.room_one)