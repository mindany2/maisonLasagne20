from tree.Environnement import Environnement
from threading import Thread
from tree.utils.Logger import Logger
from tree.utils.List_radio import List_radio
import threading

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
        try:
            return self.list_modes.get(name_mode)
        except KeyError:
            raise(KeyError("Could not find the mode {} in the tree".format(name_mode)))

    def change_mode(self, name_mode):
        Logger.info("Change mode : {} => {}".format(self.list_modes.selected().name, name_mode))
        mode_select = self.get_mode(name_mode)
        self.global_environnement.change_mode(mode_select)
        self.list_modes.change_select(mode_select)
        self.do_current_scenars()

    def do_current_scenars(self):
        self.global_environnement.do_current_scenar()

    def add_mode(self, mode):
        self.list_modes.add(mode)

    def get_current_mode(self):
        return self.list_modes.selected()

    def get_env(self, path):
        path = path.split(".")
        if path[0] == self.global_environnement.name:
            # just removing the global env name
            path = path[1:]
        try:
            return self.global_environnement.get_env(path)
        except KeyError:
            raise(KeyError("The environnement research : {} is not present in the tree".format(path))) 
    

    def get_list_envs(self):
        return self.global_environnement.get_list_envs()

    def get_modes(self):
        return self.list_modes

    def press_inter(self, name_env, name_inter, state):
        Logger.info("press inter {}, state = {}, env = {}".format(name_inter, state, name_env))
        if name_env.split(".")[0] == "mode":
            self.change_mode(name_env.split(".")[1])
        else:
            self.get_env(name_env).press_inter(name_inter, state)

    def get_scenar(self, name_env, name_scenar, preset=None):
        return self.get_env(name_env).get_scenar(name_scenar, preset)

    def initialize(self):
        # function called after all the tree is created
        self.global_environnement.initialize()
        for mode in self.list_modes:
            mode.initialize()
        self.global_environnement.change_mode(self.get_current_mode())

    def __eq__(self, other):
        if isinstance(other, Tree):
            return self.list_modes == other.list_modes\
                    and self.global_environnement == other.global_environnement
        return False

    def __str__(self):
        string = "-"*10 + "Tree"+"-"*10 + "\n"
        string += "Threads:" + str(threading.active_count())+"\n"
        string += "".join(["|  {}\n".format(thread.name) for thread in threading.enumerate()])
        string += "-Modes\n"
        string += "".join(["|  {}\n".format(string) for string in str(self.list_modes).split("\n")])
        string += "-Environnements\n"
        string += "".join(["|  {}\n".format(string) for string in str(self.global_environnement).split("\n")])
        return string
