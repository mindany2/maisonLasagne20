from tree.eclairage.Lumiere import Lumiere
from utils.controle.Triac import ETAT

class Projecteur(Lumiere):
    """
    Un projecteur simple sur un dyrak
    """
    def __init__(self, nom, triak):
        Lumiere.__init__(self, nom)
        self.triak = triak

    def set(self, dimmeur):
        self.dimmeur = dimmeur
        if dimmeur == 0:
            self.triak.deconnect()
        else :
            self.triak.connect()
            self.triak.set(dimmeur)

    def show(self):
        print("nom = " + self.nom)

        
