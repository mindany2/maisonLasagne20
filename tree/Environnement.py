from tree.utils.Liste import Liste
from tree.utils.Liste_radios import Liste_radios
from tree.utils.Dico import Dico
from tree.Tree import Tree
from tree.boutons.html.style.Style import Style
from tree.eclairage.Projecteur import Projecteur
from tree.eclairage.Enceintes import Enceintes
from tree.scenario.Scenario import MARQUEUR
from utils.Logger import Logger
from tree.utils.Calculateur import Calculateur
from tree.utils.Variable import Variable
from In_out.utils.Magic_Home_init import check_for_reset
import sys


class Environnement:
    """
    Definit une zone avec toutes ses
    lumières et boutons
    """
    def __init__(self, nom):
        self.nom = nom
        self.liste_lumières = Liste()
        self.liste_sous_envs = Liste()
        self.liste_presets = Liste_radios()
        # table de hashage entre mode et preset
        self.liste_presets_choisis = Dico()
        self.calculateur = Calculateur()

    def add_lumiere(self, lum):
        if isinstance(lum, Variable):
            self.calculateur.add(lum)
        else:
            self.liste_lumières.add(lum)

    def add_env(self, env):
        self.liste_sous_envs.add(env)

    def add_preset(self, preset):
        self.liste_presets.add(preset)

    def etat(self):
        # retourne si un marqueur du scénario en cours
        # pour savoir si l'environnement est dans un état allumer, eteint ou juste décoratif
        return self.get_preset_select().get_marqueur()

    def est_on(self):
        # retourne si vrai si cet environnement ou au moins un 
        # des sous_environnements est ON
        for env in self.liste_sous_envs:
            if env.est_on():
                return True
        return self.etat() == MARQUEUR.ON

    def get_preset_select(self):
        return self.liste_presets.selected()

    def change_mode(self, mode):
        nv_preset = self.liste_presets_choisis.get(mode)
        if nv_preset != self.get_preset_select():
            if self.etat() == MARQUEUR.ON:
                # on est ON, on cherche donc le premier scénario ON dans la nouvelle preset
                for scenar in nv_preset.liste_scénario:
                    if scenar.get_marqueur() == MARQUEUR.ON:
                        nv_preset.change_select(scenar)
                        scenar.do()
            # on change de preset
            self.change_preset_select(nv_preset)
        # on fait la même chose dans les sous_environnements
        for env in self.liste_sous_envs:
            env.change_mode(mode)


    def change_preset_select(self, preset):
        self.liste_presets.change_select(preset)

    def add_mode(self, mode, nom_preset):
        self.liste_presets_choisis.add(mode, self.get_preset(nom_preset))

    def get_preset(self, nom):
        return self.liste_presets.get(nom)

    def get_env(self, path):
        if len(path) > 1:
            # c'est dans un sous_env
            return self.liste_sous_envs.get(path[0]).get_env(path[1:])
        elif path[0] == self.nom:
            return self
        return None

    def get_lumiere(self, nom):
        lum = self.liste_lumières.get(nom)
        if lum:
            return lum
        # ce peut être une variable
        return self.calculateur.get(nom)

    def get_noms_envi(self):
        liste_nom = [self.nom]
        for env in self.liste_sous_envs:
            noms = env.get_noms_envi()
            for nom in noms:
                liste_nom.append("{}.{}".format(self.nom, nom))
        return liste_nom

    def get_scenar(self, nom, preset=None):
        if preset:
            return self.get_preset(preset).get_scenar(nom)
        return self.get_preset_select().get_scenar(nom)

    def press_inter(self, nom_inter, etat):
        self.get_preset_select().press_inter(nom_inter, etat)
    
    def reset_preset(self):
        for preset in self.liste_presets:
            preset.reset()
        self.liste_presets = Liste_radios()
        self.liste_presets_choisis = Dico()

    def repair(self):
        hs = list(self.liste_lumières)
        count = 0
        Logger.info("On reparre l'environnement " +self.nom)
        while hs != [] and count < 3:
            hs = []
            for lum in self.liste_lumières:
                Logger.info("On repare la lumières " + lum.nom)
                if lum.repair():
                    hs.append(lum)
            # on reset le wifi
            if hs != []:
                count += 1
                check_for_reset()
        if hs != []:
            Logger.error("--------------  Environnement : {} --------------".format(self.nom))
            for lum in hs:
                Logger.error(" ---------- LED {} est totalement HS ----------".format(lum.nom))
            
