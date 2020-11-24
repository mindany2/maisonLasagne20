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
        self.couleurs = None
        self.scenar_reload = None
        self.liste_lumières = Liste()
        self.liste_presets = Liste_radios()
        # table de hashage entre mode et preset
        self.liste_presets_choisis = Dico()
        self.style = Liste_radios()
        self.rang = 0 # rang 0 le plus bas, 1 le plus haut, 2 ect...
        self.calculateur = Calculateur()

    def get_rang(self):
        if self.rang == 0:
            # pour trier du plus gd nb de bouton
            return 10-len(self.liste_presets.selected().liste_boutons_html)
        return self.rang

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
            

    def reset_preset(self):
        for preset in self.liste_presets:
            preset.reset()
        self.liste_presets = Liste_radios()
        self.liste_presets_choisis = Dico()
        self.style = Liste_radios()
        self.couleurs = None

    def reload_style(self):
        self.style.change_select(self.style.get(Tree.get_current_mode().nom))

    def reload_scenar(self):
        if self.scenar_reload:
            scenar = self.get_preset_select().get_scenar(self.scenar_reload)
            if scenar:
                scenar.do()

    def get_style(self):
        return self.style

    def add_lumiere(self, lum):
        if isinstance(lum, Variable):
            self.calculateur.add(lum)
        else:
            self.liste_lumières.add(lum)

    def etat(self):
        # retourne si l'état correspondant au marqueur du scénario en cours
        # pour savoir si l'environnement est dans un état allumer, eteint ou juste décoratif
        return self.get_preset_select().get_marqueur()

    def nb_boutons_html(self):
        return self.get_preset_select().get_nb_boutons_html()

    def get_pile_scenarios(self):
        return self.get_preset_select().get_pile()

    def get_preset_select(self):
        return self.liste_presets.selected()

    def change_mode(self):
        nv_preset = self.liste_presets_choisis.get(Tree.get_current_mode())
        # on met le premier sénario qui correspond au même mode que celui en cours
        if nv_preset != self.get_preset_select():
            etat = self.etat()
            if etat == MARQUEUR.DECO:
                etat = MARQUEUR.OFF
            for scenar in nv_preset.liste_scénario:
                if scenar.get_marqueur() == etat:
                    nv_preset.change_select(scenar)
                    print("oooooooooooookkkkkkkkkkkkk", self.nom, scenar.nom)
                    if self.etat() != MARQUEUR.OFF:
                        scenar.do()
                    # sinon pas besoin on est éteint
                    break
            # on change de preset
            self.change_preset_select(nv_preset)

    def change_scenario_select(self, scenar):
        self.get_preset_select().change_select(scenar)

    def add_preset(self, preset):
        self.liste_presets.add(preset)

    def change_preset_select(self, preset):
        # on met le style
        self.reload_style()
        self.liste_presets.change_select(preset)

    def add_mode(self, mode, nom_preset):
        if Tree().get_current_mode() == mode:
            self.change_preset_select(self.get_preset(nom_preset))
        self.liste_presets_choisis.add(mode, nom_preset)

    def get_preset(self, nom):
        return self.liste_presets.get(nom)

    def get_lumiere(self, nom):
        lum = self.liste_lumières.get(nom)
        if lum:
            return lum
        # ce peut être une variable
        return self.calculateur.get(nom)

    def get_scenar(self, nom, preset=None):
        if preset:
            return self.get_preset(preset).get_scenar(nom)
        return self.get_preset_select().get_scenar(nom)

    def press_inter(self, nom_inter, etat):
        # si on a qqc à faire dans cet environnement
        if self.get_preset_select().press_inter(nom_inter, etat):
            self.reload_scenar()
    
    def press_bouton_html(self, index):
        self.get_preset_select().press_bouton_html(index)
        self.reload_scenar()

    def show(self):
        print("----- Environnement "+self.nom +" -----")
        print("----- Lumières -----")
        self.liste_lumières.show()
        print("----- Presets -----")
        self.liste_presets.show()
        print("---- Presets sélectionné ----")
        self.liste_presets_choisis.show()
        

