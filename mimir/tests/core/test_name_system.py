import unittest

from braga import Assemblage, World

from mimir.core.components import Name
from mimir.core.systems import NameSystem


class TestBasicNameSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.item_factory = Assemblage(components=[Name])
        self.item = self.world.make_entity(self.item_factory, name='item one')

        self.name_system = NameSystem(world=self.world)

    def test_entity_retrievable_from_name(self):
        entity = self.name_system.get_token_from_name('item one')
        self.assertEqual(entity, self.item)

    def test_unknown_name_raises(self):
        with self.assertRaises(ValueError) as e:
            self.assertIsNone(self.name_system.get_token_from_name('asdfdsa'))

        self.assertEqual(e.exception.message, "I don't know what you're talking about")

    def test_aliases_can_be_created(self):
        self.name_system.add_name('cool item', self.item)

        self.assertIn('cool item', self.name_system.names.keys())
        self.assertEqual(self.name_system.names['cool item'], [self.item])

    def test_no_duplicate_name_entity_pairs_can_be_added(self):
        with self.assertRaises(ValueError) as e:
            self.name_system.add_name('item one', self.item)

        self.assertEqual(e.exception.message, 'Duplicate entity names')

    def test_names_in_tokens_property(self):
        self.assertEqual(self.name_system.tokens, self.name_system.names.keys())

    def test_retrieving_unspecific_name_without_context_raises(self):
        other_item = self.world.make_entity(self.item_factory, name='other item')
        self.name_system.add_name('item one', other_item)

        with self.assertRaises(ValueError) as e:
            self.name_system.get_token_from_name('item one')

        self.assertEqual(e.exception.message, "For now I can't handle confusion")
