from engine.exceptions import StateError

from base import Player


class StateManager(object):
    """ This contains STATE ONLY.
        Perhaps should have an associated log?
    """

    def __init__(self, name, init_state):
        """ Make initial state from JSON.
            Need helper functions to build from JSON.
            Set up log.
            WRITE JSON SHIT
            SOON
            PLEASE
        """
        self.build_from_json(init_state)
        self.name = name

    def build_from_json(self, state):
        """ json.load or json.loads will probably do the trick here.
            Make a bunch of dictionaries out of json
            Namely:
                self.canonicals, self.noncanonicals, self.commands, self.errors, self.rooms, self.players, self.things
            Possibly:
                build self.directions, self.nouns, self.verbs, etc. through reverse indexing
        """
        pass

    def update_state(self, state_change):
        """ Changes state by state_change that are vetted in the LogicHandler.
            Need helper functions to manage state change.
        """
        pass

    def add_player(self, username):
        """ If there is no player with username, add username.
            Otherwise, make something up. Return a Player object.
        """
        return Player(username)

    def transaction(self):
        pass

    def rollback(self):
        pass

    def commit(self):
        pass
