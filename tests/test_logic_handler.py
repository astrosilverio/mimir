import unittest
from mock import patch

from engine.Command import ChangefulCommand
from engine.exceptions import LogicError
from engine.LogicHandler import handle_command
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


class TestParserIntegration(unittest.TestCase):

    def test_good_simple_input_returns_sane_output(self):
        pass

    def test_bad_simple_input_returns_sane_output(self):
        pass

    def test_good_complex_input_returns_sane_output(self):
        pass

    def test_bad_complex_input_returns_sane_output(self):
        pass


class TestStateIntegration(unittest.TestCase):

    def test_hc_state_changing_command_changes_state(self):
        pass

    def test_hc_non_state_changing_command_does_not_change_state(self):
        pass
