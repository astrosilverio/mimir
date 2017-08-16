from __future__ import absolute_import
import unittest

from braga import World, Assemblage

from hogwarts.core.components import Name, Description
from hogwarts.engine.Command import Command
from hogwarts.engine.Parser import Parser
from hogwarts.engine.exceptions import ParserError, Messages
from hogwarts.tests.fixtures import NameSystem


class TestParser(unittest.TestCase):

    def setUp(self):
        world = World()
        self.player = world.make_entity(Assemblage(components=[Name, Description]), name='you')
        self.wand = world.make_entity(Assemblage(components=[Name, Description]), name='wand')
        self.fluff = world.make_entity(Assemblage(components=[Name, Description]), name='fluff')
        self.cotton_candy = world.make_entity(Assemblage(components=[Name, Description]), name='cotton candy')
        world.add_system(NameSystem)

        self.command = Command(
            name='take',
            syntax=[lambda x, y: True],
            response=lambda x, y: 'Congratulations you took your wand')
        commands = {'take': self.command, 'get': self.command}

        self.parser = Parser(world, world.systems[NameSystem], self.player, commands)

    def test_normalize_with_real_words_and_fluff(self):
        normalized = self.parser.normalize('take dratted wand')
        self.assertEqual(normalized, ['take', 'wand'])

    @unittest.skipIf(True, "I haven't figured out symbols yet")
    def test_normalize_symbol_removal(self):
        normalized = self.parser.normalize('*ta@ke* *this*, wand!?!')
        self.assertEqual(normalized, ['take', 'wand'])

    def test_normalize_with_fluff(self):
        with self.assertRaises(ParserError):
            self.parser.normalize('dratted bloody thing')

    def test_normalize_with_double_word_names(self):
        normalized = self.parser.normalize('take cotton candy')
        self.assertEqual(normalized, ['take', 'cotton candy'])

    def test_tokenization_of_known_words(self):
        tokens = self.parser.tokenize(['take', 'wand', 'you', 'fluff'])
        self.assertEqual(tokens, [self.command, self.wand, self.player, self.fluff])

    def test_tokenization_with_unknown_words(self):
        with self.assertRaises(ValueError):
            self.parser.tokenize(['take', 'broomstick', 'wand'])

    def test_tokenization_with_double_word_names(self):
        tokens = self.parser.tokenize(['take', 'cotton candy'])
        self.assertEqual(tokens, [self.command, self.cotton_candy])

    def test_execute_without_error(self):
        response = self.parser.execute('take wand')
        self.assertEqual(response, 'Congratulations you took your wand')

    def test_execute_with_fluff(self):
        response = self.parser.execute('dratted bloody thing')
        self.assertEqual(response, Messages.GOBBLEDEGOOK)

    def test_execute_with_not_command(self):
        response = self.parser.execute('wand')
        self.assertEqual(response, Messages.UNKNOWN_VERB.format('wand'))
