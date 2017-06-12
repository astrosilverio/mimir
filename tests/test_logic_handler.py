import unittest

from engine.exceptions import Messages
from engine.Parser import Parser
from tests.fixtures import make_toy_world, commands, PATH_ERROR


class TestFullIntegration(unittest.TestCase):

    def setUp(self):
        self.world, self.name_system, self.player, self.room_one, self.room_two = make_toy_world()
        self.parser = Parser(self.world, self.name_system, self.player, commands)

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
        self.assertEqual(response, PATH_ERROR)
        self.assertEqual(self.player.location, self.room_one)
