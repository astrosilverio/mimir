import unittest

from braga import Assemblage, World

from hogwarts.core.components import Name
from hogwarts.core.systems import name_system


class TestBasicNameSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.item_factory = Assemblage(components=[Name])
        self.item = self.world.make_entity(self.item_factory, name='item one')

    def test_entity_retrievable_from_name(self):
        entity = name_system.get_token_from_name('item one')
        self.assertEqual(entity, self.item)

    def test_unknown_name_raises(self):
        with self.assertRaises(ValueError) as e:
            self.assertIsNone(name_system.get_token_from_name('asdfdsa'))

        self.assertEqual(e.exception.message, "I don't know what you're talking about")

    def test_aliases_can_be_created(self):
        name_system.add_name('cool item', self.item)

        self.assertIn('cool item', self.item.names)

    def test_no_duplicate_name_entity_pairs_can_be_added(self):
        with self.assertRaises(ValueError) as e:
            self.name_system.add_name('item one', self.item)

        self.assertEqual(e.exception.message, 'Duplicate entity names')

    def test_names_in_tokens_property(self):
        self.assertIn('cool item', self.name_system.tokens)

    def test_retrieving_unspecific_name_without_context_raises(self):
        other_item = self.world.make_entity(self.item_factory, name='other item')
        self.name_system.add_name('item one', other_item)

        with self.assertRaises(ValueError) as e:
            self.name_system.get_token_from_name('item one')

        self.assertEqual(e.exception.message, "For now I can't handle confusion")
