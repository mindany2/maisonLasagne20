from enum import Enum
from tree.Liste_boutons import Liste_boutons
from eclairage.Liste_lumieres import Liste_lumieres


class Environnement:
    """
    Definit une zone avec toutes ses
    lumières et boutons
    """
    def __init__(this, nom, liste_info):
        this.nom = nom
        this.liste_lumières = Liste_lumieres()
        this.liste_info = []
        liste_info.append(this.liste_info)
        this.liste_boutons = Liste_boutons(this.liste_info)

    def add_bouton(self, bouton):
        this.liste_boutons.add(bouton)

    def add_lumiere(self, lum):
        this.liste_lumières.add(lum)

    def show(this):
        print("----- Environnement "+this.nom +" -----")
        print("----- Lumières -----")
        this.liste_lumières.show()
        print("----- Boutons -----")
        this.liste_boutons.show()

