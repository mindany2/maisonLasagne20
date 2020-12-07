from tree.Environnement import Environnement
from threading import Thread
from tree.utils.Logger import Logger
from tree.utils.List_radio import List_radio

class Tree:
    """
    This static class allow to access all the environnements at any time
    It also manage modes
    """

    @classmethod
    def __init__(self):
        self.global_environnement = Environnement("environnements", self)
        self.list_modes = List_radio()

    @classmethod
    def get_global_env(self):
        return self.global_environnement

    @classmethod
    def get_mode(self, name_mode):
        mode = self.list_modes.get(name_mode)
        if mode:
            return mode
        raise(NameError("Could not find the mode {} in the tree".format(name_mode)))

    @classmethod
    def change_mode(self, name_mode):
        mode_select = self.get_mode(name_mode)
        self.list_modes.change_select(mode_select)
        self.global_environnement.change_mode(mode_select)

    @classmethod
    def add_mode(self, mode):
        self.list_modes.add(mode)

    @classmethod
    def get_current_mode(self):
        return self.list_modes.selected()

    @classmethod
    def get_env(self, path):
        path = path.split(".")
        env = self.global_environnement.get_env(path)
        if env:
            return env
        raise(NameError("The environnement research : {} is not present in the tree".format(path))) 

    @classmethod
    def get_names_envi(self):
        return self.global_environnement.get_names_envi()

    @classmethod
    def press_inter(self, name_env, name):
        Logger.info("press inter {}, env = {}".format(name_env, name))
        self.get_env(name_env).press_inter(name)

    @classmethod
    def get_scenar(self, name_env, name_scenar, preset=None):
        return self.get_env(name_env).get_scenar(name_scenar, preset)

    @classmethod
    def __str__(self):
        string = "-"*10 + "Tree"+"-"*10 + "\n"
        string += "-Modes\n"
        string += "".join(["|  {}\n".format(string) for string in str(self.list_modes).split("\n")])
        string += "-Environnements\n"
        string += "".join(["|  {}\n".format(string) for string in str(self.global_environnement).split("\n")])
        return string
