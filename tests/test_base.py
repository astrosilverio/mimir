import unittest

from base import Player, Room, Thing


class TestFormatting(unittest.TestCase):

    def setUp(self):
        self.wand = Thing("wand", description="Pine with a dragon heartstring core.")
        self.book = Thing("arithmancy textbook", description="You want to read this? Really?!? Is your name Hermione Granger?", word_type="vowel")
        self.candy = Thing("chocolate frogs", description="Yummy!", word_type="plural")
        self.sword = Thing("Sword of Gryffindor", description="For all your basilisk venom-infused needs.", word_type="proper")

        self.hermione = Player('hermione')

        self.room = Room("Room of Requirement", description="There is a lot of stuff in here.", inventory=[self.hermione, self.book, self.candy, self.sword])

    def test_player_empty_inventory(self):
        self.assertFalse(self.wand in self.hermione)

    def test_player_with_inventory(self):
        self.hermione.inventory.add(self.wand)
        self.assertTrue(self.wand in self.hermione)

    def test_player_resting_description(self):
        expected = "Hermione is here."
        self.assertEqual(self.hermione.resting_description, expected)

        # add inventory, make sure resting_description stays the same
        self.hermione.inventory.add(self.wand)
        self.assertEqual(self.hermione.resting_description, expected)

    def test_room_inventory(self):
        self.assertTrue(self.hermione in self.room)
        self.assertTrue(self.book in self.room)
        self.assertFalse(self.wand in self.room)

    def test_nested_inventory_not_in_main_inventory(self):
        self.hermione.inventory.add(self.wand)
        self.assertFalse(self.wand in self.room)

    def test_room_description(self):
        description = str(self.room)

        self.assertTrue(description.startswith(self.room.description))
        self.assertTrue(self.hermione.resting_description in description)
        self.assertTrue(self.book.resting_description in description)
        self.assertTrue(self.candy.resting_description in description)
        self.assertTrue(self.sword.resting_description in description)

    def test_consonant_resting_description(self):
        expected = "A wand lies on the ground here."
        self.assertEqual(self.wand.resting_description, expected)

    def test_vowel_resting_description(self):
        expected = "An arithmancy textbook lies on the ground here."
        self.assertEqual(self.book.resting_description, expected)

    def test_plural_resting_description(self):
        expected = "Some chocolate frogs lie on the ground here."
        self.assertEqual(self.candy.resting_description, expected)

    def test_proper_resting_description(self):
        expected = "The Sword of Gryffindor lies on the ground here."
        self.assertEqual(self.sword.resting_description, expected)
