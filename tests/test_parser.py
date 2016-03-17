import unittest

from braga import World

from engine.Command import Command
from engine.Parser import Parser
from engine.exceptions import ParserError, Messages
from tests.fixtures import generic_thing_factory as gtf
from tests.fixtures import NameSystem


class TestParser(unittest.TestCase):

    def setUp(self):
        world = World()
        self.player = world.make_entity(gtf, name='you')
        self.wand = world.make_entity(gtf, name='wand')
        self.fluff = world.make_entity(gtf, name='fluff')
        world.add_system(NameSystem)

        self.command = Command(
            name='take',
            syntax=[lambda x, y: True],
            response=lambda x, y: 'Congratulations you took your wand')
        commands = {'take': self.command, 'get': self.command}

        self.parser = Parser(world, self.player, commands)

    def test_process_with_real_words_and_fluff(self):
        processed = self.parser.normalize('take dratted wand')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_symbol_removal(self):
        processed = self.parser.normalize('*ta@ke* *this*, wand!?!')
        self.assertEqual(processed, ['take', 'wand'])

    def test_process_with_fluff(self):
        with self.assertRaises(ParserError):
            self.parser.normalize('dratted bloody thing')

    def test_tokenization_of_known_words(self):
        tokens = self.parser.tokenize(['take', 'wand', 'you', 'fluff'])
        self.assertEqual(tokens, [self.command, self.wand, self.player, self.fluff])

    def test_tokenization_with_unknown_words(self):
        with self.assertRaises(ParserError):
            self.parser.tokenize(['take', 'broomstick', 'wand'])

    def test_execute_without_error(self):
        response = self.parser.execute('take wand')
        self.assertEqual(response, 'Congratulations you took your wand')

    # def test_execute_with_logic_error(self):
    #     response = self.parser.execute('take wand')
    #     self.assertEqual(response, 'BOOM!')

    def test_execute_with_fluff(self):
        response = self.parser.execute('dratted bloody thing')
        self.assertEqual(response, Messages.GOBBLEDEGOOK)

    def test_execute_with_not_command(self):
        response = self.parser.execute('wand')
        self.assertEqual(response, Messages.UNKNOWN_VERB.format('wand'))
