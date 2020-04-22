from tree.utils.Liste import Liste
from tree.utils.Liste_radios import Liste_radios
from tree.utils.Dico import Dico
from tree.Tree import Tree
from In_out.Liste_interrupteur import Liste_interrupteur


class Environnement:
    """
    Definit une zone avec toutes ses
    lumières et boutons
    """
    def __init__(self, nom):
        self.nom = nom
        self.liste_lumières = Liste()
        self.liste_presets = Liste_radios()
        # table de hashage entre mode et preset
        self.liste_presets_choisis = Dico()

    def add_lumiere(self, lum):
        self.liste_lumières.add(lum)

    def etat(self):
        # retourne si l'environnement est allumer ou éteint
        return self.get_preset_select().get_marqueur()

    def get_preset_select(self):
        return self.liste_presets.selected()

    def change_mode(self):
        print(Tree.get_current_mode().nom)
        nv_preset = self.liste_presets_choisis.get(Tree.get_current_mode())
        # on met le premier sénario qui correspond au même mode que celui en cours
        for scenar in nv_preset.liste_scénario:
            if scenar.etat != self.etat():
                nv_preset.change_select(scenar)
                break
        # on change de preset
        self.liste_presets.change_select(nv_preset)
        self.get_preset_select().show()



    def change_scenario_select(self, scenar):
        self.get_preset_select().change_select(scenar)

    def add_preset(self, preset):
        self.liste_presets.add(preset)

    def change_preset_select(self, preset):
        self.liste_presets.change_select(preset)

    def add_mode(self, mode, nom_preset):
        if Tree().get_current_mode() == mode:
            self.change_preset_select(self.get_preset(nom_preset))
        self.liste_presets_choisis.add(mode, nom_preset)

    def get_preset(self, nom):
        return self.liste_presets.get(nom)

    def get_lumiere(self, nom):
        return self.liste_lumières.get(nom)

    def get_scenar(self, nom):
        return self.get_preset_select().get_scenar(nom)


    def show(self):
        print("----- Environnement "+self.nom +" -----")
        print("----- Lumières -----")
        self.liste_lumières.show()
        print("----- Presets -----")
        self.liste_presets.show()
        print("---- Presets sélectionné ----")
        self.liste_presets_choisis.show()
        

