from tree.Tree import Tree
from tree.utils.Dico import Dico

class Mode:
    """
    This is a mode of the tree, this allow to change all the preset in
    all the environnements in the tree (normal, evenning..)
    """
    def __init__(self, name, scenar_init = None):
        self.name = name
        self.state = False
        self.name_scenar_init = scenar_init
        self.scenar_init = None

    def initialize(self):
        if self.name_scenar_init:
            self.scenar_init = self.name_scenar_init.get_scenarios()

    def change_state(self, state):
        self.state = state
        if self.state and self.scenar_init:
            # do the scenar_init
            self.scenar_init.do()

    def __str__(self):
        string = self.name + "\n"
        if self.name_scenar_init:
            string += "|  Scenario_init : {}".format(str(self.name_scenar_init))
        return string

