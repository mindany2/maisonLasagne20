from tree.eclairage.Lumiere import Lumiere
from tree.eclairage.Lampe import Lampe
from enum import Enum
from time import sleep
from threading import Lock

class ETAT(Enum):
    haut = 1
    bas = 2
    en_cours = 3

class Trappe(Lumiere):
    """
    modélise la trappe
    """
    def __init__(self,nom, relais_distrib_montée, relais_distrib_descente, relais_aimant, capteur_fermeture):
        """
        L'aimant est inversé
        """
        Lumiere.__init__(self, nom)
        self.distrib_montée = Lampe("distrib_montée",relais_distrib_montée)
        self.distrib_descente = Lampe("distrib_descente",relais_distrib_descente)
        self.aimant = Lampe("aimant",relais_aimant, invert=True)
        self.capteur_fermeture = capteur_fermeture
        etat = self.capteur_fermeture.capture() 
        if etat:
            self.etat = ETAT.haut
        else:
            self.etat = ETAT.bas
        print("la trappe est {}".format(self.etat))

    def set_aimant(self, etat):
        self.aimant.set(etat)

    def descendre(self):
        self.distrib_descente.set(True)
        sleep(0.5)
        self.distrib_descente.set(False)

    def monter(self):
        self.distrib_montée.set(True)
        sleep(0.5)
        self.distrib_montée.set(False)

    def change(self, etat):
        self.etat = etat



