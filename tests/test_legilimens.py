import unittest
from mock import MagicMock, patch

from Legilimens import Legilimens
from hogwartsexceptions import LegilimensError, LogicError, Messages
from tests.fixtures import TestPlayer
from tests.fixtures import TestCommand


class TestLegilimens(unittest.TestCase):

    def setUp(self):
        marauders_map_mock = MagicMock()
        marauders_map_mock.canonicals = ['take', 'wand']
        marauders_map_mock.noncanonicals = {'get': 'take'}
        marauders_map_mock.commands = {'take': TestCommand()}
        marauders_map_mock.add_player = lambda x: TestPlayer()

        self.legilimens = Legilimens('zork', marauders_map_mock)

    def test_process_with_canonicals_and_fluff(self):
        processed = self.legilimens.process('take dratted wand')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_with_non_canonicals_and_fluff(self):
        processed = self.legilimens.process('get dratted wand')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_symbol_removal(self):
        processed = self.legilimens.process('*ta@ke* *this*, wand!?!')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_with_fluff(self):
        with self.assertRaises(LegilimensError):
            self.legilimens.process('dratted bloody thing')

    @patch('LogicHandler.handle_command')
    def test_execute_without_error(self, mock_handle_command):
        mock_handle_command.return_value = 'Congratulations you took your wand'
        response = self.legilimens.execute('take wand')
        self.assertEqual(response, mock_handle_command.return_value)

    @patch('LogicHandler.handle_command')
    def test_execute_with_logic_error(self, mock_handle_command):
        mock_handle_command.side_effect = LogicError('BOOM!')
        response = self.legilimens.execute('take wand')
        self.assertEqual(response, 'BOOM!')

    def test_execute_with_fluff(self):
        response = self.legilimens.execute('dratted bloody thing')
        self.assertEqual(response, Messages.GOBBLEDEGOOK)

    def test_execute_with_not_command(self):
        response = self.legilimens.execute('wand')
        self.assertEqual(response, Messages.UNKNOWN_VERB.format('wand'))
