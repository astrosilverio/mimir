class AHistoryOfMagic(object):
	''' Keeps track of all commands and their success.'''

	def __init__(self, init_state):
		self.init_state = init_state
		self.log = []
		self.command_id = 0

	def make_log_entry(self, player, user_input, interpreted_command, success, state_diff, response):
		''' Adds an entry to the log.
		player is the player_id of player giving input,
		user_input is raw input,
		interpreted command is the command + args that the parser thinks happened,
		success if True if command succeeds and False if it fails,
		state_diff is dict of state changes,
		response is the response returned to user.'''

		self.command_id += 1

		log_entry = {'command_id': self.command_id,
					'player_id'  : player,
					'user_input' : user_input,
					'command'    : interpreted_command,
					'success'    : success,
					'state_diff' : state_diff,
					'response'   : response}
		self.log.append(log_entry)
