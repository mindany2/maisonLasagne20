from tree.Tree import Tree
from tree.utils.Dico import Dico

class Mode:
    """
    This is a mode of the tree, this allow to change all the preset in
    all the environnements in the tree (normal, evenning..)
    """
    def __init__(self, name, color, scenar_init):
        self.name = name
        self.state = False
        self.scenar_init = scenar_init

    def __str__(self):
        return self.name

    def change(self):
        self.state = not(self.state)
        if self.state and self.scenar_init:
            # do the scenar_init
            env, preset, name = self.scenar_init.split(".")
            scenar = Tree().get_scenar(env, name, preset = preset)
            if scenar:
                scenar.do()
