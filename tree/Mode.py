from tree.utils.Dico import Dico

class Mode:
    """
    This is a mode of the tree, this allow to change all the preset in
    all the environnements in the tree (normal, evenning..)
    """
    def __init__(self, name, scenar_init = None, scenar_end = None):
        self.name = name
        self.state = False
        self.name_scenar_init = scenar_init
        self.name_scenar_end = scenar_end
        self.scenar_init = None
        self.scenar_end = None
        self.inters = []
        self.initialized = False

    def get_name(self):
        return self.name

    def initialize(self):
        self.initialized = True
        if self.name_scenar_init:
            self.scenar_init = self.name_scenar_init.get_scenarios()
            self.scenar_init.initialize()
        if self.name_scenar_end:
            self.scenar_end = self.name_scenar_end.get_scenarios()
            self.scenar_end.initialize()

    def add_inter(self, name):
        self.inters.append(name)

    def get_inters(self):
        return self.inters

    def change_state(self, state):
        self.state = state
        if self.initialize:
            if self.state and self.scenar_init:
                self.scenar_init.do(join = True)
            elif not(self.state) and self.scenar_end:
                self.scenar_end.do(join = True)

    def get_state(self):
        return self.state

    def __str__(self):
        string = self.name + "\n"
        if self.name_scenar_init:
            string += "|  Scenario_init : {}".format(str(self.name_scenar_init))
            string += "|  Scenario_end : {}".format(str(self.name_scenar_end))
        return string

