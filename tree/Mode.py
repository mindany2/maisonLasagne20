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

    def initialize(self):
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
        if self.state and self.scenar_init:
            self.scenar_init.do(join = True)
        elif not(self.state) and self.scenar_end:
            print(self.scenar_end)
            self.scenar_end.do()

    def get_state(self):
        return self.state

    def __eq__(self, other):
        if isinstance(other, Mode):
            return self.name == other.name\
                    and self.state == other.state\
                    and self.scenar_init == other.scenar_init
        return False

    def __str__(self):
        string = self.name + "\n"
        if self.name_scenar_init:
            string += "|  Scenario_init : {}".format(str(self.name_scenar_init))
        return string

