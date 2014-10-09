import unittest
from mock import MagicMock

from Legilimens import Legilimens
from hogwartsexceptions import LegilimensError
from tests.fixtures import TestPlayer

class TestLegilimens(unittest.TestCase):

    def setUp(self):
        marauders_map_mock = MagicMock()
        marauders_map_mock.canonicals = ['take', 'wand']
        marauders_map_mock.noncanonicals = {'get': 'take'}
        marauders_map_mock.add_player = lambda x: TestPlayer()

        self.legilimens = Legilimens('zork', marauders_map_mock)

    def test_process_with_canonicals_and_fluff(self):
        processed = self.legilimens.process('take dratted wand')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_with_non_canonicals_and_fluff(self):
        processed = self.legilimens.process('get dratted wand')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_with_fluff(self):
        with self.assertRaises(LegilimensError):
            self.legilimens.process('dratted bloody thing')


    
