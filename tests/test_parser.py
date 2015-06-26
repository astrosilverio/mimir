import unittest
from mock import MagicMock, patch

from engine.base import Player
from engine.Command import Command
from engine.Parser import Parser
from engine.exceptions import ParserError, LogicError, Messages


class TestParser(unittest.TestCase):

    def setUp(self):
        marauders_map_mock = MagicMock()
        marauders_map_mock.canonicals = ['take', 'wand']
        marauders_map_mock.noncanonicals = {'get': 'take'}
        marauders_map_mock.commands = {'take': Command()}
        marauders_map_mock.add_player = lambda x: Player(x)

        self.parser = Parser('zork', marauders_map_mock)

    def test_process_with_canonicals_and_fluff(self):
        processed = self.parser.process('take dratted wand')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_with_non_canonicals_and_fluff(self):
        processed = self.parser.process('get dratted wand')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_symbol_removal(self):
        processed = self.parser.process('*ta@ke* *this*, wand!?!')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_with_fluff(self):
        with self.assertRaises(ParserError):
            self.parser.process('dratted bloody thing')

    @patch('engine.LogicHandler.handle_command')
    def test_execute_without_error(self, mock_handle_command):
        mock_handle_command.return_value = 'Congratulations you took your wand'
        response = self.parser.execute('take wand')
        self.assertEqual(response, mock_handle_command.return_value)

    @patch('engine.LogicHandler.handle_command')
    def test_execute_with_logic_error(self, mock_handle_command):
        mock_handle_command.side_effect = LogicError('BOOM!')
        response = self.parser.execute('take wand')
        self.assertEqual(response, 'BOOM!')

    def test_execute_with_fluff(self):
        response = self.parser.execute('dratted bloody thing')
        self.assertEqual(response, Messages.GOBBLEDEGOOK)

    def test_execute_with_not_command(self):
        response = self.parser.execute('wand')
        self.assertEqual(response, Messages.UNKNOWN_VERB.format('wand'))
