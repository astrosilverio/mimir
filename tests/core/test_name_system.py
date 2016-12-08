import unittest

from braga import Assemblage, World

from core.components import Name
from core.systems import NameSystem


class TestBasicNameSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.item_factory = Assemblage(components=[Name])
        self.item = self.world.make_entity(self.item_factory, name='item one')

        self.name_system = NameSystem(world=self.world)

    def test_entity_retrievable_from_name(self):
        entity = self.name_system.get_entity('item one')
        self.assertEqual(entity, self.item)

    def test_none_returned_for_unknown_name(self):
        self.assertIsNone(self.name_system.get_entity('asdfdsa'))

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


class TestContexts(unittest.TestCase):

    def setUp(self):
        self.world = World()
        self.item_factory = Assemblage(components=[Name])
        self.human = self.world.make_entity(self.item_factory, name='human')
        self.cat_one = self.world.make_entity(self.item_factory, name='cat')
        self.cat_two = self.world.make_entity(self.item_factory, name='cat')

        self.name_system = NameSystem(world=self.world)

    def test_adding_entity_to_context(self):
        self.name_system.add_entity_to_context(self.cat_one, self.human)

        self.assertIn('cat', self.name_system.contexts[self.human].keys())
        self.assertEqual(self.name_system.contexts[self.human].get('cat'), self.cat_one)

    def test_system_preferentially_chooses_name_from_context(self):
        self.name_system.add_entity_to_context(self.cat_one, self.human)

        chosen_cat = self.name_system.get_entity('cat', self.human)
        self.assertEqual(chosen_cat, self.cat_one)
