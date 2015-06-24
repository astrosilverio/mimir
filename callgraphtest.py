from Legilimens import Legilimens
from StateManager import StateManager
from Command import Command
from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.output import GraphvizOutput, GephiOutput

hogwarts = StateManager('init_state_not_usable_yet')
hogwarts.canonicals = ['look']
look = Command(rules=['can_look_in_room'])
hogwarts.commands = {'look': look}
username = "tony_stark"
processor = Legilimens(username, hogwarts)

test = processor.execute('look')
print test
