from tree.Environnement import Environnement
from threading import Thread
from tree.utils.Logger import Logger
from tree.utils.List_radio import List_radio

class Tree:
    """
    This class allow to access all the environnements at any time
    It also manage modes
    """

    def __init__(self):
        self.global_environnement = Environnement("global")
        self.list_modes = List_radio()

    def get_global_env(self):
        return self.global_environnement

    def get_mode(self, name_mode):
        mode = self.list_modes.get(name_mode)
        if mode:
            return mode
        raise(NameError("Could not find the mode {} in the tree".format(name_mode)))

    def change_mode(self, name_mode):
        mode_select = self.get_mode(name_mode)
        self.list_modes.change_select(mode_select)
        self.global_environnement.change_mode(mode_select)

    def add_mode(self, mode):
        self.list_modes.add(mode)

    def get_current_mode(self):
        return self.list_modes.selected()

    def get_env(self, path):
        path = path.split(".")
        if path[0] == self.global_environnement.name:
            # just removing the global env name
            path = path[1:]
        env = self.global_environnement.get_env(path)
        if env:
            return env
        raise(NameError("The environnement research : {} is not present in the tree".format(path))) 

    def get_list_envs(self):
        return self.global_environnement.get_list_envs()

    def press_inter(self, name_env, name_inter, state):
        Logger.info("press inter {}, state = {}".format(name_inter, state))
        self.get_env(name_env).press_inter(name_inter, state)

    def get_scenar(self, name_env, name_scenar, preset=None):
        return self.get_env(name_env).get_scenar(name_scenar, preset)

    def initialize(self):
        # function called after all the tree is created
        for mode in self.list_modes:
            mode.initialize()
        self.global_environnement.initialize()

    def __str__(self):
        string = "-"*10 + "Tree"+"-"*10 + "\n"
        string += "-Modes\n"
        string += "".join(["|  {}\n".format(string) for string in str(self.list_modes).split("\n")])
        string += "-Environnements\n"
        string += "".join(["|  {}\n".format(string) for string in str(self.global_environnement).split("\n")])
        return string
