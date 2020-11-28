from tree.Environnement import Environnement
from threading import Thread
from utils.Logger import Logger
from tree.utils.Liste_radios import Liste_radios

class Tree:
    environnement_global = Environnement("GENERAL")
    liste_modes = Liste_radios()

    @classmethod
    def get_mode(self, nom_mode):
        return self.liste_modes.get(nom_mode)

    @classmethod
    def change_mode(self, nom_mode):
        mode_select = self.liste_modes.get(nom_mode)
        self.liste_modes.change_select(mode_select)
        Logger.info("Changement de mode : " + self.get_current_mode().nom)
        # on met les environnements dans le même mode
        self.environnement_global.change_mode(mode_select)

    @classmethod
    def add_mode(self, mode):
        self.liste_modes.add(mode)

    @classmethod
    def repair(self):
        # permet de reset les leds si necessaires
        self.environnement_global.repair()

    @classmethod
    def get_current_mode(self):
        return self.liste_modes.selected()

    @classmethod
    def get_env(self, nom_env):
        path = nom_env.split(".")
        return self.environnement_global.get_env(path)

    @classmethod
    def get_noms_envi(self):
        return self.environnement_global.get_noms_envi()

    @classmethod
    def press_inter(self, nom_env, nom):
        Logger.info("press inter {}, env = {}".format(nom_env, nom))
        self.get_env(nom_env).press_inter(nom)

    @classmethod
    def get_scenar(self, nom_env, nom_scenar, preset=None):
        return self.get_env(nom_env).get_scenar(nom_scenar, preset)
