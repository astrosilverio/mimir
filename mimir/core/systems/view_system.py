from braga import System, Aspect

from hogwarts.core.components import View


class ViewSystem(System):

    def __init__(self, world):
        super(ViewSystem, self).__init__(world=world, aspect=Aspect(all_of=set([View])))
