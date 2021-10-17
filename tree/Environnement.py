from tree.utils.Dico import Dico
from tree.utils.List import List
from tree.utils.List_radio import List_radio
from tree.scenario.Scenario import MARKER
from tree.utils.calculs.Calculator import Calculator
from tree.utils.calculs.Variable import Variable
from tree.utils.Logger import Logger
import sys


class Environnement:
    """
    Define a group of light that works with a list of preset
    Also can define sub-environnements 
    """
    def __init__(self, name):
        self.name = name
        self.list_objects = List()
        self.list_sub_env = List()
        self.list_presets = List_radio()
        # hash table between mode and preset
        self.list_presets_chosen = Dico()
        self.calculator = Calculator()

    def get_list_presets(self):
        return self.list_presets

    def get_list_subs_env(self):
        return self.list_sub_env

    def get_list_objs(self):
        return self.list_objects

    def add_object(self, obj):
        self.list_objects.add(obj)

    def add_variable(self, var, recursive=True):
        self.calculator.add(var)
        # add it in all sub_env
        if recursive:
            for env in self.list_sub_env:
                env.add_variable(var)

    def add_env(self, env):
        self.list_sub_env.add(env)

    def add_preset(self, preset):
        self.list_presets.add(preset)

    def state(self):
        # it tells if the scenario is ON
        return self.get_preset_select().get_marker() == MARKER.ON

    def is_on(self):
        # return true if this environnement is ON or 
        # at least one of it's sub-environnement
        for env in self.list_sub_env:
            if env.is_on():
                return True
        return self.state()

    def get_preset_select(self):
        return self.list_presets.selected()

    def change_mode(self, mode):
        # do it in all the sub-envs
        for env in self.list_sub_env:
            env.change_mode(mode)

        try:
            new_preset = self.list_presets_chosen.get(mode.name)
        except KeyError:
            # the env haven't a preset selected for this mode, just keep the actual
            return
        if new_preset:
            old_preset = self.get_preset_select()
            self.calculator.reset()
            if new_preset is not old_preset:
                marker = old_preset.get_marker()
                # no keeping deco, just principal state
                if marker == MARKER.DECO:
                    marker = MARKER.OFF
                old_preset.reset()
                new_preset.initialize(marker)
                self.change_preset_select(new_preset)

    def do_current_scenar(self):
        self.get_preset_select().do_current_scenar()
        # do it in all the sub-envs
        for env in self.list_sub_env:
            env.do_current_scenar()

    def change_preset_select(self, preset):
        self.list_presets.change_select(preset)


    def add_mode(self, mode, preset):
        self.list_presets_chosen.add(mode, preset)

    def get_preset(self, name):
        try:
            return self.list_presets.get(name)
        except KeyError:
            raise(KeyError("The preset {} doesn't exist in the environnement {}".format(name, self.name)))

    def get_env(self, path):
        if path:
            # it is in a sub-environnement
            try:
                return self.list_sub_env.get(path[0]).get_env(path[1:])
            except KeyError:
                raise(KeyError("Could not found an env like {} in {}".format(".".join(path), self.name)))

        return self

    def get_object(self, name):
        try:
            return self.list_objects.get(name)
        except KeyError:
            raise(KeyError("The object {} is doesn't exist in the environnement {}".format(name, self.name)))

    def get_var(self, name):
        try:
            return self.calculator.get(name)
        except KeyError:
            raise(KeyError("The variable {} is doesn't exist in the environnement {}".format(name, self.name)))

    def get_list_envs(self):
        list_env = Dico()
        list_env.add(self.name, self)
        for env in self.list_sub_env:
            list_sub_env = env.get_list_envs()
            for name in list_sub_env.keys():
                list_env.add("{}.{}".format(self.name, name), list_sub_env.get(name))
        return list_env

    def get_scenar(self, name, preset=None):
        try:
            if preset:
                return self.get_preset(preset).get_scenar(name)
            else:
                return self.get_preset_select().get_scenar(name)
        except KeyError:
            raise(KeyError("The scenario {} is doesn't exist in the preset {} in the environnement {}".format(name, preset, self.name)))

    def get_calculator(self):
        return self.calculator

    def press_inter(self, name_inter, state):
        try:
            self.calculator.change_variable(name_inter, state)
        except KeyError:
            # the interrupt had not variable
            pass
        self.get_preset_select().press_inter(name_inter, state)
        # also press it also in all the sub-environnements
        for env in self.list_sub_env:
            env.press_inter(name_inter, state)

    def initialize(self):
        self.get_preset_select().initialize(MARKER.OFF)
        for env in self.list_sub_env:
            env.initialize()

    def __eq__(self, other):
        if isinstance(other, Environnement):
            return self.name == other.name\
                    and self.list_presets_chosen == other.list_presets_chosen\
                    and self.list_objects == other.list_objects\
                    and self.list_presets == other.list_presets\
                    and self.calculator == other.calculator\
                    and self.list_sub_env == other.list_sub_env
        return False

    def __str__(self):
        string = self.name + "\n"
        string += "-Link modes\n"
        string += "".join(["|  {} => {}\n".format(mode, self.list_presets_chosen.get(mode).name) for mode in self.list_presets_chosen.keys()])
        string += "".join("-Objects\n")
        string += "".join(["|  {}\n".format(string) for string in str(self.list_objects).split("\n")])
        string += "".join("-Current_preset\n")
        string += "".join(["|  {}\n".format(string) for string in str(self.get_preset_select()).split("\n")])
        string += "".join("-Variables\n")
        string += "".join(["|  {}\n".format(string) for string in str(self.calculator).split("\n")])
        """
        string += "".join("-Sub-environnements\n")
        string += "".join(["|  {}\n".format(string) for string in str(self.list_sub_env).split("\n")])
        """
        return string

    
