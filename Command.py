class Command(object):
	''' Similar to my previous idea of having verbs except it doesn't suck'''
	def __init__(self, syntax=None, rules=None, state_changes=None, errors=None, query=None):
		self.syntax = syntax
		self.rules = rules
		self.state_changes = state_changes
		self.errors = errors
		self.query = query

		# what else do I need here?

    # maybe rewriting dunder methods would do fun things?
