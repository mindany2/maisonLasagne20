from tree.Liste_boutons import Liste_boutons
from tree.Liste_boutons_radios import Liste_boutons_radios
from tree.eclairage.Liste_lumieres import Liste_lumieres


class Environnement:
    """
    Definit une zone avec toutes ses
    lumières et boutons
    """
    def __init__(self, nom, index):
        self.nom = nom
        self.liste_lumières = Liste_lumieres()
        self.liste_boutons = Liste_boutons()
        self.position = index

    def add_lumiere(self, lum):
        self.liste_lumières.add(lum)

    def add_bouton(self, bt):
        self.liste_boutons.add(bt)

    def get_bouton(self, nom):
        return self.liste_boutons.liste_boutons[nom]

    def change_select(self, bouton):
        if isinstance(self.liste_boutons, Liste_boutons_radios):
            self.liste_boutons.change_select(bouton)

    def show(self):
        print("----- Environnement "+self.nom +" -----")
        print("----- Lumières -----")
        self.liste_lumières.show()
        print("----- Boutons -----")
        self.liste_boutons.show()

