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
