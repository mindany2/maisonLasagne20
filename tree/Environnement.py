from tree.utils.Dico import Dico
from tree.utils.List import List
from tree.utils.List_radio import List_radio
from tree.scenario.Scenario import MARKER
from tree.utils.calculs.Calculator import Calculator
from tree.utils.calculs.Variable import Variable
from utils.Logger import Logger
import sys


class Environnement:
    """
    Define a group of light that works with a list of preset
    Also can define sub-environnements 
    """
    def __init__(self, name):
        self.name = name
        self.list_lights = Liste()
        self.list_sub_env = Liste()
        self.list_presets = Liste_radios()
        # hash table between mode and preset
        self.list_presets_chosen = Dico()
        self.calculator = Calculateur()

    def add_light(self, lum):
        if isinstance(lum, Variable):
            self.calculator.add(lum)
        else:
            self.list_lights.add(lum)

    def add_env(self, env):
        self.list_sub_env.add(env)

    def add_preset(self, preset):
        self.list_presets.add(preset)

    def state(self):
        # return the marker of the principal scenario
        # it tells if the scenario is ON/OFF/DECO
        return self.get_preset_select().get_marker()

    def est_on(self):
        # return true if this environnement is ON or 
        # at least one of it's sub-environnement
        for env in self.list_sub_env:
            if env.est_on():
                return True
        return self.state() == MARKER.ON

    def get_preset_select(self):
        return self.list_presets.selected()

    def change_mode(self, mode):
        nv_preset = self.list_presets_chosen.get(mode)
        if nv_preset != self.get_preset_select():
            if self.state() == MARKER.ON:
                # we need a ON scenario, search the first we find in the new preset
                for scenar in nv_preset.get_list_scenars():
                    if scenar.get_marker() == MARKER.ON:
                        nv_preset.change_select(scenar)
                        scenar.do()
            # just change the preset
            self.change_preset_select(nv_preset)
        # do it in all the sub-envs
        for env in self.list_sub_env:
            env.change_mode(mode)


    def change_preset_select(self, preset):
        self.list_presets.change_select(preset)

    def add_mode(self, mode, name_preset):
        self.list_presets_chosen.add(mode, self.get_preset(name_preset))

    def get_preset(self, name):
        return self.list_presets.get(name)

    def get_env(self, path):
        if len(path) > 1:
            # it is a sub-environnement
            return self.list_sub_env.get(path[0]).get_env(path[1:])
        elif path[0] == self.name:
            return self
        return None

    def get_light(self, name):
        lum = self.list_lights.get(name)
        if lum:
            return lum
        # it could be a variable
        return self.calculator.get(name)

    def get_names_envi(self):
        list_name = [self.name]
        for env in self.list_sub_env:
            names = env.get_names_envi()
            for name in names:
                list_name.append("{}.{}".format(self.name, name))
        return list_name

    def get_scenar(self, name, preset=None):
        if preset:
            return self.get_preset(preset).get_scenar(name)
        return self.get_preset_select().get_scenar(name)

    def press_inter(self, name_inter, state):
        self.get_preset_select().press_inter(name_inter, state)
    
