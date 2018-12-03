import random

class Player(object):
    def __init__(self, username="testuser"):
        self.username = username
        self.id = random.randint()

class Room(object):
    def __init__(self, description="This is a test room"):
        self.description = description

class Thing(object):
    def __init__(self, description="This is a test thing"):
        self.description = description