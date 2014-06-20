from hogwartsexceptions import MaraudersMapError
from AHistoryOfMagic import AHistoryOfMagic

class MaraudersMap(object):
	''' This contains STATE ONLY.
	Perhaps should have an associated log? '''

	def __init__(self, init_state):
		''' Make initial state from JSON.
		Need helper functions to build from JSON.
		Set up log.
		WRITE JSON SHIT
		SOON
		PLEASE'''
		self.logbook = AHistoryOfMagic(init_state)
		self.build_from_json(init_state)

	def build_from_json(self, state):
		''' json.load or json.loads will probably do the trick here.
		Make a bunch of dictionaries out of json
		Namely:
		  self.canonicals, self.noncanonicals, self.commands, self.errors, self.rooms, self.players, self.things
		  Possibly:
		    build self.directions, self.nouns, self.verbs, etc. through reverse indexing
		'''
		pass

	def update_state(self, state_change):
		''' Changes state by state_change that are vetted in the Rowling.
		Need helper functions to manage state change.
		'''
		pass

	def get_state(self):
		'''Returns a giant dict of states?
		...
		why?'''
		pass

	def add_player(self, username):
		'''If there is no player with username, add username. Otherwise, make something up. Return a Player object.'''
		class Player():
			def __init__(self, username):
				self.username = username
				self.id = "1234"
		return Player(username)

	def look(self, room):
		return room.description
