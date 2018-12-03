import unittest

from braga import World, Assemblage

from mimir.core.components import Container, Moveable
from mimir.core.systems import ContainerSystem


class TestContainerSystem(unittest.TestCase):

    def setUp(self):
        self.world = World()
        bucket_factory = Assemblage(components=[Container])
        self.bucket_one = self.world.make_entity(bucket_factory)
        self.bucket_two = self.world.make_entity(bucket_factory)

        self.thing_factory = Assemblage(components=[Moveable])
        self.thing = self.world.make_entity(self.thing_factory, location=self.bucket_one)

        self.container_system = ContainerSystem(world=self.world)

    def test_move_item_to_new_inventory(self):
        self.container_system.move(self.thing, self.bucket_two)

        self.assertEqual(self.thing.location, self.bucket_two)
        self.assertEqual(self.bucket_two.inventory, set([self.thing]))

    def test_cannot_move_immoveable_item(self):
        bookcase = self.world.make_entity()

        with self.assertRaises(ValueError) as e:
            self.container_system.move(bookcase, self.bucket_two)

        self.assertEqual(e.exception.message, "You cannot move this item")
        self.assertEqual(self.bucket_two.inventory, set([]))

    def test_cannot_move_item_to_non_container(self):
        new_thing = self.thing_factory.make()
        with self.assertRaises(ValueError) as e:
            self.container_system.move(self.thing, new_thing)

        self.assertEqual(e.exception.message, "Invalid destination")
        self.assertEqual(self.thing.location, self.bucket_one)
