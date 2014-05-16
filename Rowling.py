from hogwartsexceptions import RowlingError

class Rowling(object):
	''' Recieves from Legilimens what the user wants to do, who user is, which castle they're in.
	Decides if user can do what they want.
	Makes MaraudersMap change state if necessary.
	Gives Legilimens a response.
	should not contain instancemethods'''

	# SHOULD MAYBE MOVE THIS TO JSON AND THEN IT'S ALL IN THE CASTLE
	# Below is sample commands and errors dicts

#	commands = {'go': {'syntax': ['direction'], 'rules': ['path_exists', 'player_can_move'], 'state_changes': 'move_player'},
#				'look': {'syntax': [], 'rules': ['can_look_in_room']}}
#	errors = {'path_exists': "You can't go that way.", 'player_can_move': "You can't move right now.",
#				'can_look_in_room': "You can't see a thing."}

	@classmethod
	def handle_command(cls, castle, player_id, command):
		'''Takes processed command from Legilimens.
		Performs checks.
		If command can be performed, passes it to MaraudersMap.
		Otherwise, set response to appropriate error.
		Passes response to Legilimens.'''
		verb = command[0]
		args = command[1:]
		validity = True
		checks = castle.commands[verb]['rules']
		for check in checks:
			validity = validity and cls.__getattribute__(check)(castle, player_id, command)
			if not validity:
				raise RowlingError(castle.errors[check])
		# Should not get here if any of the checks return False
		if cls.is_state_change(command):
			for change in castle.commands[verb]['state_changes']:
				castle.update_state(change, player_id, *args)
		if castle.commands[verb]['query'] and castle.commands[verb]['query'] != 'radio_silence':
			return castle.__getattribute__(castle.commands[verb]['query'])(player_id, *args)
		elif castle.commands[verb]['query'] == 'radio_silence':
			return ''
		else:
			room = cls.find_player_location(castle, player_id)
			return castle.look(room)

	@classmethod
	def is_state_change(cls, command):
		'''Checks to see if the verb in the command is in state_commands'''
		verb = command[0]
		return 'state_changes' in castle.commands[verb]

	@classmethod
	def find_player_location(cls, castle, player_id):
		'''Finds which room the player is in. If location is an attribute on player I won't need this. Maybe goes in MaraudersMap?'''
		pass

	@classmethod
	def path_exists(cls, castle, player_id, command):
		room = cls.find_player_location(castle, player_id)
		direction = command[1]
		return direction in room.paths

	@classmethod
	def player_can_move(cls, castle, player_id, command):
		player = castle.players[player_id]
		return not player.in_limbo

	@classmethod
	def can_look_in_room(cls, castle, player_id):
		room = cls.find_player_location(castle, player_id)
		return not room.dark
