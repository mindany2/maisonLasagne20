from tree.Liste import Liste
from tree.Liste_radios import Liste_radios
from tree.Dico import Dico
from utils.In_out.Liste_interrupteur import Liste_interrupteur


class Environnement:
    """
    Definit une zone avec toutes ses
    lumières et boutons
    """
    def __init__(self, nom):
        self.nom = nom
        self.liste_lumières = Liste()
        self.liste_presets = Liste()
        self.liste_input = Liste_interrupteur()
        # table de hashage entre mode et preset
        self.liste_presets_choisis = Dico()
        self.liste_boutons = Liste_radios()
        self.have_html_boutons = False

    def add_lumiere(self, lum):
        self.liste_lumières.add(lum)

    def change_bouton_select(self, bt):
        self.liste_boutons.change_select(bt)

    def add_boutons(self, bt):
        self.liste_boutons.add(bt)
        self.liste_boutons.show()

    def add_preset(self, preset):
        self.liste_presets.add(preset)

    def add_input(self, inter):
        self.liste_input.add(inter)

    def add_mode(self, mode, nom_preset):
        self.liste_presets_choisis.add(mode, nom_preset)

    def get_preset(self, nom):
        return self.liste_presets.get(nom)

    def get_lumiere(self, nom):
        return self.liste_lumières.get(nom)

    def get_bouton(self, nom):
        return self.liste_boutons.get(nom)

    def show(self):
        print("----- Environnement "+self.nom +" -----")
        print("----- Lumières -----")
        self.liste_lumières.show()
        print("----- Presets -----")
        self.liste_presets.show()
        print("----- Input -------")
        self.liste_input.show()
        print("---- Presets sélectionné ----")
        self.liste_presets_choisis.show()
        print("---- boutons -----")
        self.liste_boutons.show()
        

