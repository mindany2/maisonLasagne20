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

    def add_variable(self, var):
        self.calculator.add(var)

    def add_env(self, env):
        self.list_sub_env.add(env)

    def add_preset(self, preset):
        self.list_presets.add(preset)

    def state(self):
        # return the marker of the principal scenario
        # it tells if the scenario is ON/OFF/DECO
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
        except KeyError as e:
            # the env haven't a preset selected for this mode, just keep the actual
            return
        if new_preset:
            old_preset = self.get_preset_select()
            if new_preset is not old_preset:
                new_preset.initialize(old_preset.get_marker())
                old_preset.reset()
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
        preset = self.list_presets.get(name)
        if preset: return preset
        raise(NameError("The preset {} doesn't exist in the environnement {}".format(name, self.name)))

    def get_env(self, path):
        if path:
            # it is in a sub-environnement
            try:
                return self.list_sub_env.get(path[0]).get_env(path[1:])
            except KeyError as e:
                raise(KeyError("Could not found an env like {} in {}".format(path[0], self.name)))
        return self

    def get_object(self, name):
        obj = self.list_objects.get(name)
        if obj:
            return obj
        raise(NameError("The object {} is doesn't exist in the environnement {}".format(name, self.name)))

    def get_var(self, name):
        var = self.calculator.get(name)
        if var:
            return var
        raise(NameError("The variable {} is doesn't exist in the environnement {}".format(name, self.name)))

    def get_list_envs(self):
        list_env = Dico()
        list_env.add(self.name, self)
        for env in self.list_sub_env:
            list_sub_env = env.get_list_envs()
            for name in list_sub_env.keys():
                list_env.add("{}.{}".format(self.name, name), list_sub_env.get(name))
        return list_env

    def get_scenar(self, name, preset=None):
        if preset:
            scenar = self.get_preset(preset).get_scenar(name)
        else:
            scenar = self.get_preset_select().get_scenar(name)
        if scenar: return scenar
        raise(NameError("The scenario {} is doesn't exist in the preset {} in the environnement {}".format(name, preset, self.name)))

    def get_calculator(self):
        return self.calculator

    def press_inter(self, name_inter, state):
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
        string += "".join("-Presets\n")
        string += "".join(["|  {}\n".format(string) for string in str(self.list_presets).split("\n")])
        string += "".join("-Variables\n")
        string += "".join(["|  {}\n".format(string) for string in str(self.calculator).split("\n")])
        string += "".join("-Sub-environnements\n")
        string += "".join(["|  {}\n".format(string) for string in str(self.list_sub_env).split("\n")])
        return string

    
