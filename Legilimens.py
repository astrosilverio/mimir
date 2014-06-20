from hogwartsexceptions import LegilimensError, RowlingError, MaraudersMapError
from Rowling import Rowling

class Legilimens(object):
	''' Takes user input. Processes it into list of things user wants to do.
	Gets response from Rowling. Gives response back to user. '''

	def __init__(self, username, castle):
		''' ALL INFO ABOUT DATA STORED IN MARAUDERSMAP 
		JUST LINK THIS WITH A MARAUDERSMAP OBJECT 
		'''
		self.castle = castle
		player = self.castle.add_player(username)
		self.player_id = player.id

	def process(self, user_input):
		''' Takes user_input, processes it into an attempted command.'''
		words = user_input.split()
		words = [word if (word in self.castle.canonicals) else self.castle.noncanonicals.get(word, None) for word in words]
		words = [word for word in words if word is not None]

		if not words:
			raise LegilimensError("I didn't understand any of that.")

		return words

	def execute(self, user_input):
		'''Gives processed user input to Rowling, gets response.'''
		try:
			legit_input = self.process(user_input)
			response = Rowling().handle_command(self.castle, self.player_id, legit_input)
		except (LegilimensError, MaraudersMapError, RowlingError) as e:
			response = e.message
		finally:
			return response

