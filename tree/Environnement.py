from enum import Enum
from tree.Liste_boutons import Liste_boutons
from eclairage.Liste_lumieres import Liste_lumieres


class Environnement:
    """
    Definit une zone avec toutes ses
    lumières et boutons
    """
    def __init__(self, nom, liste_info):
        self.nom = nom
        self.liste_lumières = Liste_lumieres()
        self.liste_info = []
        liste_info.append(self.liste_info)
        self.liste_boutons = Liste_boutons(self.liste_info)

    def add_bouton(self, bouton):
        self.liste_boutons.add(bouton)

    def add_lumiere(self, lum):
        self.liste_lumières.add(lum)

    def show(self):
        print("----- Environnement "+self.nom +" -----")
        print("----- Lumières -----")
        self.liste_lumières.show()
        print("----- Boutons -----")
        self.liste_boutons.show()

